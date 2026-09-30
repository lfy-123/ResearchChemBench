import pytest

from chemistry_toolbox.src.electronic_state import resolve_state, preflight_inputs, ElectronicStateError, inherit_state
from chemistry_toolbox.src.backends.common import _parse_xyz
from chemistry_toolbox.src.catalog import action_specs, backend_specs


def structure(symbols=("H", "H"), **extra):
    return {"atoms": [{"element": s, "position_angstrom": [i, 0, 0]} for i, s in enumerate(symbols)], **extra}


def test_missing_and_conflicting_electronic_state_are_explicit():
    with pytest.raises(ElectronicStateError, match="No declared charge"):
        resolve_state(structure(), {}, policy="strict")
    with pytest.raises(ElectronicStateError, match="inconsistent"):
        resolve_state(structure(("H",)), {"charge": 0, "multiplicity": 1}, policy="strict")
    resolved, view = resolve_state(structure(charge=0, multiplicity=1), {"charge": -1, "multiplicity": 2}, policy="strict")
    assert resolved["charge"] == -1
    assert view["sources"]["charge"] == "method_spec.charge"
    assert len(view["warnings"]) == 2
    with pytest.raises(ElectronicStateError, match="Conflicting"):
        resolve_state(structure(), {"charge": 0, "multiplicity": 1, "spin": 1}, policy="strict")


@pytest.mark.parametrize("bad", [0.5, True, "1.0", "singlet"])
def test_integer_fields_do_not_silently_round(bad):
    with pytest.raises(ElectronicStateError):
        resolve_state(structure(), {"charge": bad, "multiplicity": 1}, policy="strict")


def test_xyz_comment_is_not_guessed_and_legacy_is_visible(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    p=tmp_path / "input.xyz"
    p.write_text("1\nAn anion; charge -1, multiplicity 1\nH 0 0 0\n")
    value=_parse_xyz(p)
    with pytest.raises(ElectronicStateError): resolve_state(value, {}, policy="strict")
    _, old=resolve_state(value, {}, policy="legacy")
    assert old["sources"]["charge"] == "legacy_default"
    p.write_text("1\ncharge=-1 multiplicity=1\nH 0 0 0\n")
    _, parsed=resolve_state(_parse_xyz(p), {}, policy="strict")
    assert parsed["charge"] == -1 and parsed["validation"] == "checked"


@pytest.mark.parametrize("backend", ["orca", "xtb", "pyscf", "psi4", "gaussian"])
def test_multiple_backends_share_preflight(backend):
    result, view=preflight_inputs(backend_specs()[backend], action_specs()["calculate_energy"],
                                  {"structure":structure()}, {"charge":0,"multiplicity":1}, policy="strict")
    assert result["structure"]["charge"] == 0
    assert view["electronic_state"]["structure"]["validation"] == "checked"


def test_periodic_ecp_and_nonquantum_coverage_is_not_overstated():
    for mol, method in [(structure(("H",), pbc=[True,True,True]), {}), (structure(("H",)), {"ecp":"explicit"})]:
        _, view=resolve_state(mol, {**method,"charge":0,"multiplicity":1}, policy="strict")
        assert view["validation"] == "not_checked"
    _, view=preflight_inputs(backend_specs()["rdkit"], action_specs()["calculate_energy"], {}, {}, policy="strict")
    assert view["electronic_state"]["validation"] == "not_applicable"


def test_state_survives_geometry_output_without_native_metadata():
    output=inherit_state(structure(("H",), charge=0, multiplicity=1, electronic_state_sources={"charge":"legacy_default","multiplicity":"legacy_default"}),
                         structure(("H",), charge=-1,multiplicity=1), {})
    _, view=resolve_state(output, {}, policy="strict")
    assert view["charge"] == -1 and view["sources"]["charge"] == "structured_input"


def test_public_preflight_does_not_submit_or_probe(tmp_path, monkeypatch):
    import json
    from chemistry_toolbox.mcp.discovery_tools import validate_action
    from chemistry_toolbox.mcp.discovery_models import ProgressiveActionRequest
    from chemistry_toolbox.mcp.execution_store import execution_store
    monkeypatch.setenv("RESEARCHCHEM_MCP_WORKSPACE", str(tmp_path))
    monkeypatch.setenv("RESEARCHCHEMBENCH_RECOVERY_ENABLED", "1")
    monkeypatch.setenv("RESEARCHCHEMBENCH_ELECTRONIC_STATE_POLICY", "strict")
    (tmp_path/"_toolbox_catalog.json").write_text(json.dumps({"catalog_hash":"fixture"}))
    def forbidden(*args, **kwargs):raise AssertionError("Preflight must not launch/probe a backend")
    monkeypatch.setattr("chemistry_toolbox.src.service.invoke_worker", forbidden)
    monkeypatch.setattr("chemistry_toolbox.src.service.probe_all_backends", forbidden)
    value=validate_action(ProgressiveActionRequest(action_id="calculate_energy",backend_id="orca",inputs={"structure":structure()},
                         method_spec={"method":"HF","basis":"STO-3G","charge":0,"multiplicity":1}))
    assert value["validation_only"] and value["status"]=="success"
    assert value["effective_inputs"]["electronic_state"]["structure"]["charge"]==0
    assert not execution_store().list_jobs()
