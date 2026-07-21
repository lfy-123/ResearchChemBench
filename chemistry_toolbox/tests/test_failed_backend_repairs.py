from __future__ import annotations

import sys
from types import SimpleNamespace

import httpx
import numpy as np
import pytest

from researchchem_toolbox.backends import data, dynamics, electronic, periodic


class _PsiVector:
    def __init__(self, *blocks):
        self.blocks = blocks

    def to_array(self):
        return tuple(np.asarray(block) for block in self.blocks)


class _PsiDimension:
    def __init__(self, *values):
        self.values = values

    def to_tuple(self):
        return self.values


def test_psi4_multi_irrep_orbitals_are_flattened_with_matching_occupations():
    blocks = electronic._psi4_irrep_blocks(_PsiVector([-1.0, 0.2], [], [-0.5]))
    assert blocks == [[-1.0, 0.2], [], [-0.5]]
    assert electronic._psi4_irrep_occupations(
        _PsiDimension(1, 0, 1), [2, 0, 1], 2.0
    ) == [2.0, 0.0, 2.0]
    assert electronic._psi4_restricted_occupations(
        _PsiDimension(2, 0, 1), _PsiDimension(1, 0, 1), [3, 0, 1]
    ) == [2.0, 1.0, 0.0, 2.0]


def _cp2k_request() -> dict:
    return {
        "inputs": {
            "structure": {
                "atoms": [{"element": "Si", "position_angstrom": [0.0, 0.0, 0.0]}],
                "cell_angstrom": [[5.43, 0.0, 0.0], [0.0, 5.43, 0.0], [0.0, 0.0, 5.43]],
                "pbc": [True, True, True],
            }
        },
        "method_spec": {
            "method": "PBE",
            "basis_set": "DZVP-MOLOPT-SR-GTH",
            "potential": "GTH-PBE",
            "cutoff_ry": 100.0,
            "k_points": [1, 1, 1],
            "scf_algorithm": "ot",
        },
        "action_settings": {"scf_convergence": 1.0e-6, "max_scf_cycles": 100},
    }


def test_cp2k_current_force_and_stress_print_formats_are_generated_and_parsed(tmp_path):
    force_input = periodic._cp2k_input("calculate_periodic_forces", _cp2k_request())
    assert "&FORCES ON" in force_input
    stress_input = periodic._cp2k_input("calculate_periodic_stress", _cp2k_request())
    assert "STRESS_TENSOR ANALYTICAL" in stress_input
    assert "&STRESS_TENSOR ON" in stress_input

    force_output = """
 ENERGY| Total FORCE_EVAL ( QS ) energy [hartree]             -3.701430592573918
 FORCES| Atomic forces [hartree/bohr]
 FORCES|   Atom     x               y               z               |f|
 FORCES|      1 -2.08241778E-06 -2.08289641E-06 -2.08293559E-06   3.60742872E-06
 FORCES| Sum    -2.08241778E-06 -2.08289641E-06 -2.08293559E-06
"""
    force = periodic._parse_cp2k(
        "calculate_periodic_forces", force_output, tmp_path, _cp2k_request()
    )
    assert force["forces"] == [[-2.08241778e-06, -2.08289641e-06, -2.08293559e-06]]

    stress_output = """
 ENERGY| Total FORCE_EVAL ( QS ) energy [hartree]             -3.701430592615132
 STRESS| Analytical stress tensor [bar]
 STRESS|                        x                   y                   z
 STRESS|      x        6.08184838865E+03  -4.15401392519E+03  -4.15378539843E+03
 STRESS|      y       -4.15401392519E+03   6.07947827181E+03  -4.15350217683E+03
 STRESS|      z       -4.15378539843E+03  -4.15350217683E+03   6.07756249544E+03
"""
    stress = periodic._parse_cp2k(
        "calculate_periodic_stress", stress_output, tmp_path, _cp2k_request()
    )
    assert stress["unit"] == "GPa"
    assert stress["source_unit"] == "bar"
    assert stress["stress"][0][0] == pytest.approx(0.608184838865)


def _gromacs_settings(ensemble: str) -> dict:
    settings = {
        "ensemble": ensemble,
        "temperature_kelvin": 300.0,
        "timestep_fs": 1.0,
        "steps": 10,
        "report_interval": 2,
        "generate_velocities": True,
        "random_seed": 13,
    }
    if ensemble in {"NVT", "NPT"}:
        settings["temperature_coupling_groups"] = ["System"]
    if ensemble == "NPT":
        settings["pressure_bar"] = 1.0
    return settings


def test_gromacs_mdp_keeps_ensemble_coupling_fields_separate():
    nve = dynamics._gromacs_dynamics_mdp({"cutoff_scheme": "Verlet"}, _gromacs_settings("NVE"))
    assert nve["tcoupl"] == "no"
    assert nve["pcoupl"] == "no"
    assert "ref-t" not in nve and "tau-t" not in nve and "tc-grps" not in nve
    assert "ref-p" not in nve and "tau-p" not in nve and "compressibility" not in nve
    assert nve["gen-vel"] == "yes" and nve["gen-seed"] == 13

    nvt = dynamics._gromacs_dynamics_mdp({"cutoff_scheme": "Verlet"}, _gromacs_settings("NVT"))
    assert nvt["tc-grps"] == "System"
    assert nvt["ref-t"] == "300.0"
    assert "ref-p" not in nvt

    npt = dynamics._gromacs_dynamics_mdp({"cutoff_scheme": "Verlet"}, _gromacs_settings("NPT"))
    assert npt["pcoupl"] == "C-rescale"
    assert npt["ref-p"] == 1.0


def _pubchem_compound():
    return SimpleNamespace(
        cid=962,
        canonical_smiles="O",
        isomeric_smiles="O",
        inchi="InChI=1S/H2O/h1H2",
        inchikey="XLYOFNOQVPJJNP-UHFFFAOYSA-N",
        molecular_formula="H2O",
        molecular_weight=18.015,
        iupac_name="oxidane",
    )


def test_pubchem_retries_transient_503_and_records_attempt_count(monkeypatch):
    calls = 0

    class BusyError(Exception):
        code = 503

    def get_compounds(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise BusyError("server busy")
        return [_pubchem_compound()]

    monkeypatch.setattr(data.time, "sleep", lambda _delay: None)
    monkeypatch.setitem(sys.modules, "pubchempy", SimpleNamespace(get_compounds=get_compounds))
    result = data.execute(
        "resolve_chemical_identity",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "water", "namespace": "name"}},
            "method_spec": {},
            "action_settings": {
                "require_unique": True,
                "max_records": 1,
                "max_retries": 1,
                "retry_backoff_seconds": 0,
            },
        },
    )
    assert result["status"] == "success"
    assert result["provenance"]["remote_attempts"] == 2


def test_pubchem_http_client_preserves_retry_after_for_full_records(monkeypatch):
    calls = 0

    class BusyError(Exception):
        response = SimpleNamespace(status_code=503, headers={"Retry-After": "0"})

    class Response:
        status_code = 200
        headers = {}
        content = b"{}"

        def raise_for_status(self):
            return None

        def json(self):
            return {"PC_Compounds": [{"id": {"id": {"cid": 962}}}]}

    def post(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            class BusyResponse:
                content = b"{}"

                def raise_for_status(self):
                    raise BusyError("busy")

            return BusyResponse()
        return Response()

    monkeypatch.setattr(data.time, "sleep", lambda _delay: None)
    monkeypatch.setattr(data.httpx, "post", post)
    pcp = SimpleNamespace(Compound=lambda record: SimpleNamespace(record=record))
    compounds, attempts = data._pubchem_get_compounds(
        pcp,
        "water",
        "name",
        {
            "max_retries": 1,
            "retry_backoff_seconds": 0,
            "minimum_request_interval_seconds": 0,
            "timeout_seconds": 10,
        },
    )
    assert attempts == 2
    assert compounds[0].record["id"]["id"]["cid"] == 962


def test_pubchem_http_not_found_remains_an_empty_result(monkeypatch):
    class Response:
        status_code = 404
        headers = {}
        content = b"{}"

        def raise_for_status(self):
            raise AssertionError("404 should be treated as an empty PubChem result")

        def json(self):
            return {"Fault": {"Code": "PUGREST.NotFound"}}

    monkeypatch.setattr(data.httpx, "post", lambda *_args, **_kwargs: Response())
    pcp = SimpleNamespace(Compound=lambda record: SimpleNamespace(record=record))
    compounds, attempts = data._pubchem_get_compounds(
        pcp,
        "not-a-real-compound-name",
        "name",
        {"max_retries": 0, "minimum_request_interval_seconds": 0, "timeout_seconds": 10},
    )
    assert compounds == []
    assert attempts == 1


def test_pubchem_exhausted_503_is_structured_and_retryable(monkeypatch):
    class BusyError(Exception):
        code = 503

    monkeypatch.setattr(data.time, "sleep", lambda _delay: None)
    monkeypatch.setitem(
        sys.modules,
        "pubchempy",
        SimpleNamespace(get_compounds=lambda *_args, **_kwargs: (_ for _ in ()).throw(BusyError("busy"))),
    )
    result = data.execute(
        "resolve_chemical_identity",
        "pubchem",
        {
            "inputs": {"query": {"identifier": "water", "namespace": "name"}},
            "method_spec": {},
            "action_settings": {
                "require_unique": True,
                "max_records": 1,
                "max_retries": 1,
                "retry_backoff_seconds": 0,
            },
        },
    )
    assert result["status"] == "failed"
    assert result["retryable"] is True
    assert result["error"]["code"] == "remote_service_unavailable"


def test_catalysis_hub_retries_a_transient_timeout(monkeypatch):
    calls = 0

    class Response:
        status_code = 200
        headers = {}

        def raise_for_status(self):
            return None

        def json(self):
            return {
                "data": {
                    "reactions": {
                        "totalCount": 1,
                        "edges": [{"node": {"id": "reaction-1"}}],
                    }
                }
            }

    def post(*_args, **_kwargs):
        nonlocal calls
        calls += 1
        if calls == 1:
            raise httpx.ReadTimeout("temporary timeout")
        return Response()

    monkeypatch.setattr(data.time, "sleep", lambda _delay: None)
    monkeypatch.setattr(data.httpx, "post", post)
    result = data.execute(
        "search_catalysis_records",
        "catalysis_hub",
        {
            "inputs": {"query": {"reactants": "CO"}},
            "method_spec": {},
            "action_settings": {
                "max_records": 1,
                "timeout_seconds": 10,
                "max_retries": 1,
                "retry_backoff_seconds": 0,
            },
        },
    )
    assert result["status"] == "success"
    assert result["provenance"]["remote_attempts"] == 2
