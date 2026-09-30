"""Public format regressions with synthetic fixtures, not chemical validation.

Fixtures name explicit unavailable stages. They are independent of untracked
verification archives and exercise the same validator exposed to the agent.
"""
from copy import deepcopy
import json
from pathlib import Path

import pytest

from chemistry_toolbox.src.output_contract import validate_output_contract
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository
from evaluation.scoring.adapters import load_runtime_evaluation

ROOT = Path(__file__).resolve().parents[1]
PAPERS = ("paper_0de37d01e35c27df", "paper_5d94285cfbd51973",
          "paper_9aa6d5655edfeb52", "paper_c23cfabbd34b087f",
          "paper_e31cc7bc7b21b610", "paper_fda8b9b53f8276db")
MODES = ("autonomous_research", "paper_reproduction")


def package(paper, mode):
    return ROOT / "tasks" / f"final_verified_{mode}" / paper


def fixture(paper, mode):
    method = {"software": "fixture", "method": "fixture", "basis_or_pseudopotential": "fixture",
              "environment": "gas", "convergence": "fixture", "rationale": "format-only test"}
    if paper == PAPERS[0]:
        return {"status": "complete", "states": [
            {"state": name, "charge": charge, "multiplicity": mult, "sulfur_distance_angstrom": distance,
             "provenance": {"file": name + ".xyz", "atom_indices": [16, 17]},
             "validation": {"converged": True, "stationary_point_evidence": "fixture.log", "imaginary_frequency_count": 0}}
            for name, charge, mult, distance in (("neutral", 0, 1, 4.1), ("radical_cation", 1, 2, 4.0))],
            "distance_change": {"value_angstrom": -0.1, "definition": "cation minus neutral"},
            "validation": ["fixture.log"], "coverage": "two objects", "conclusion": "format-only fixture"}
    if paper == PAPERS[1]:
        return {"system": {"name": "AZ9", "charge": 0, "multiplicity": 1},
            "method": {"software": "fixture", "electronic_structure_method": "fixture", "basis_or_representation": "fixture",
                       "phase": "gas", "justification": "format-only test"},
            "conformer_search": {"generated_count": 1, "deduplicated_count": 1, "advanced_count": 1,
                "frequency_validated_count": 1, "energy_span_kcal_mol": 0.0, "deduplication": "fixture",
                "candidates": [{"candidate_id": "a", "relative_energy_kcal_mol": 0.0, "advanced": True, "validation_evidence": "fixture.log"}],
                "coverage_rationale": "fixture"},
            "selected_structure": {"xyz": "synthetic coordinates", "selection_basis": "fixture"},
            "stationarity": {"imaginary_frequency_count": 0, "lowest_frequency_cm_1": 30.0, "evidence": "fixture.log"},
            "properties": {"homo_ev": -6.0, "lumo_ev": -2.0, "gap_ev": 4.0, "dipole_debye": 3.0,
                "ip_ev": 6.0, "ea_ev": 2.0, "hardness_ev": 2.0, "softness_ev_inverse": 0.25,
                "chemical_potential_ev": -4.0, "electronegativity_ev": 4.0, "electrophilicity_ev": 4.0},
            "sensitivity": {"test": "fixture", "delta_homo_ev": 0.01, "delta_lumo_ev": 0.01,
                "delta_gap_ev": 0.0, "delta_dipole_debye": 0.01, "interpretation": "fixture"}, "conclusion": "fixture"}
    if paper == PAPERS[2]:
        state = {"state_label": "S1", "multiplicity": 1, "energy": {"value": 4.0, "unit": "eV"},
                 "wavelength": {"value": 310.0, "unit": "nm"}, "oscillator_strength": 0.2,
                 "contributions": ["fixture"], "selection_basis": "fixture"}
        return {"status": "complete", "structure": {"system_id": "2a", "formula": "C18H20B10", "charge": 0, "multiplicity": 1},
            "method": {"software": "fixture", "ground_state": "fixture", "excited_state": "fixture", "geometry_protocol": "fixture"},
            "orbital_properties": {"homo": -6.0, "lumo": -2.0, "gap": {"value": 4.0, "unit": "eV"}},
            "excitations": [deepcopy(state)], "selected_excitation": state,
            "validation": {"geometry_converged": True, "electronic_state_check": "fixture",
                           "sensitivity_check": "fixture", "evidence": ["fixture.log"]},
            "interpretation": {"conclusion": "fixture", "author_hypothesis_assessment": "format-only fixture"}}
    if paper == PAPERS[3]:
        return {"status": "complete", "system": {"name": "1M-TIPS", "charge": 0, "multiplicity": 1},
            "method": {"software": "fixture", "ground_state_method": "fixture", "basis": "fixture", "solvent_model": "CHCl3", "excited_state_method": "fixture"},
            "validation": {"geometry_converged": True, "stationary_point_test": "fixture", "imaginary_frequency_count": 0,
                           "excited_state_converged": True, "state_selection_evidence": "fixture.log"},
            "investigation": {"states_examined": 2, "selection_rule": "fixture", "attempted_calculations": ["fixture.log"]},
            "result": {"wavelength_nm": 730.0, "oscillator_strength": 1.2, "state_identity": "S1",
                       "dominant_transition": "fixture", "transition_character": "fixture", "conclusion": "fixture"}}
    if paper == PAPERS[4]:
        return {"status": "complete", "method": {"software": "fixture", "electronic_structure": "fixture", "charge": 0,
                                                  "multiplicity": 1, "convergence_settings": "fixture"},
            "isomers": {name: {"name": name, "input_file": name + ".xyz", "status": "success",
                "normal_termination": True, "optimization_completed": True, "energy_hartree": energy,
                "imaginary_frequency_count": 0, "imaginary_frequencies": [], "frequency_count": 168,
                "validation_status": "fixture", "evidence": ["fixture.log"]}
                for name, energy in (("cis_alpha", -2204.5), ("cis_beta", -2204.498))},
            "relative_energy": {"definition": "beta minus alpha", "value": 1.255, "unit": "kcal/mol"},
            "lower_energy_identity": "cis_alpha", "conclusion": "fixture"}
    conformer = {"assignment": "cis", "atom_indices": [1, 2, 3, 4], "signed_dihedral_deg": 30.0, "evidence": "fixture.xyz"}
    selected = {"candidate_id": "a", "outcome": "fixture", "protocol": method, "optimized_structure_file": "fixture.xyz",
                "coordinates_units": "angstrom", "atom_mapping_file": "mapping.json", "conformer": conformer}
    return {"status": "completed", "system": {"name": "ligand 1", "formula": "C15H13N3", "charge": 0, "multiplicity": 1},
        "input_provenance": {"database": "CCDC", "record_id": "2433822", "record_doi": "fixture", "retrieval_date": "2026-09-24",
                             "component_selection": "fixture", "source_file": "source.cif"},
        "protocol": method, "protocols_or_candidates": [{"candidate_id": "a", "description": "fixture", "outcome": "fixture", "validation_context": "fixture"}],
        "selected_result": deepcopy(selected), "optimization": selected,
        "frequency_validation": {"performed": True, "outcome": "fixture", "imaginary_mode_count": 0,
                                 "frequencies_units": "cm-1", "frequency_file": "fixture.log", "diagnostics": "fixture"},
        "bond_comparison": {"performed": True, "bond_table_file": "bonds.csv", "bond_count": 6,
            "bonds": [{"bond_id": pair, "crystal_endpoints": pair.split('-'), "optimized_endpoints": pair.split('-'),
                       "crystal_length": 1.4, "optimized_length": 1.405, "units": "angstrom"}
                      for pair in ("C1-C2", "C2-C3", "N1-C1", "N2-C2", "N3-C3", "C1-C10")],
            "rmse": 0.005, "rmse_units": "angstrom", "r2_reported": None, "metrics_method": "fixture"},
        "conclusion": "fixture", "completion": {"criterion_met": True, "coverage": "fixture"}, "artifacts": ["fixture.log"]}


def incomplete(paper, mode, *, early=False):
    d = fixture(paper, mode)
    d['status'] = 'bounded_failure' if early else 'partial'
    d['failure'] = {'reason': 'Synthetic failed calculation', 'missing_observables': ['unavailable calculated endpoint'], 'evidence': []}
    if paper == PAPERS[0]:
        for state in d['states'] if early else d['states'][1:]:
            state['sulfur_distance_angstrom'] = None
            state['provenance']['file'] = None
            state['validation'].update(converged=False, imaginary_frequency_count=None)
        d['distance_change']['value_angstrom'] = None
    elif paper == PAPERS[1]:
        for k in ('delta_homo_ev', 'delta_lumo_ev', 'delta_gap_ev', 'delta_dipole_debye'):
            d['sensitivity'][k] = None
        if early:
            for k in ('generated_count', 'deduplicated_count', 'advanced_count', 'frequency_validated_count'):
                d['conformer_search'][k] = 0
            d['conformer_search'].update(candidates=[], energy_span_kcal_mol=None)
            d['selected_structure'] = None
            d['stationarity'].update(imaginary_frequency_count=None, lowest_frequency_cm_1=None)
            d['properties'] = dict.fromkeys(d['properties'])
    elif paper == PAPERS[2]:
        d['excitations'] = []
        d['selected_excitation'] = None
        if early:
            d['orbital_properties'].update(homo=None, lumo=None, gap={'value': None, 'unit': 'eV'})
            d['validation'].update(geometry_converged=False, evidence=[])
    elif paper == PAPERS[3]:
        d['result'].update(wavelength_nm=None, oscillator_strength=None, state_identity='unresolved')
        d['validation']['excited_state_converged'] = False
        d['investigation']['states_examined'] = 0
        if early:
            d['validation'].update(geometry_converged=False, imaginary_frequency_count=None)
    elif paper == PAPERS[4]:
        for name in ('cis_alpha', 'cis_beta') if early else ('cis_beta',):
            d['isomers'][name].update(energy_hartree=None, imaginary_frequency_count=None,
                imaginary_frequencies=None, frequency_count=None, normal_termination=False,
                optimization_completed=False, status='failed', evidence=[])
        d['relative_energy']['value'] = None
        d['lower_energy_identity'] = 'unresolved'
    else:
        selected = 'selected_result' if mode == 'autonomous_research' else 'optimization'
        d['frequency_validation'].update(performed=False, imaginary_mode_count=None, frequency_file=None)
        d['completion']['criterion_met'] = False
        if early:
            d[selected] = None
            d['bond_comparison'].update(performed=False, bond_table_file=None, bonds=[], bond_count=0, rmse=None)
    return d


def validate(tmp_path, paper, mode, data):
    (tmp_path / 'report').mkdir(exist_ok=True)
    path = tmp_path / 'report/results.json'
    original = json.dumps(data).encode()
    path.write_bytes(original)
    outcome = validate_output_contract(tmp_path, (package(paper, mode) / 'agent_input/submission_schema.json').read_bytes())
    assert path.read_bytes() == original
    return outcome


@pytest.mark.parametrize('mode', MODES)
@pytest.mark.parametrize('paper', PAPERS)
def test_success_partial_and_early_failure_are_distinct(tmp_path, paper, mode):
    result = validate_task_package(package(paper, mode))
    assert result.status == 'passed', result.findings
    load_runtime_evaluation(paper_id=paper, task_type=mode,
                            repository=TaskRepository.from_final(ROOT / 'tasks', approved_tasks=[(mode, paper)]))
    success = fixture(paper, mode)
    assert validate(tmp_path, paper, mode, success)['valid']
    for early in (False, True):
        data = incomplete(paper, mode, early=early)
        out = validate(tmp_path, paper, mode, data)
        assert out['valid'], out['errors']
        without_diagnostics = deepcopy(data)
        del without_diagnostics['failure']
        assert not validate(tmp_path, paper, mode, without_diagnostics)['valid']
        claimed_complete = deepcopy(data)
        claimed_complete['status'] = 'complete'
        if paper == PAPERS[5]:
            claimed_complete['completion']['criterion_met'] = True
        assert not validate(tmp_path, paper, mode, claimed_complete)['valid']


@pytest.mark.parametrize('mode', MODES)
@pytest.mark.parametrize('paper', PAPERS)
def test_failure_does_not_remove_identity_types_or_diagnostics(tmp_path, paper, mode):
    data = incomplete(paper, mode, early=True)
    for field, value in [('reason', ''), ('missing_observables', []), ('evidence', 'not an array')]:
        bad = deepcopy(data)
        bad['failure'][field] = value
        assert not validate(tmp_path, paper, mode, bad)['valid']
    identity = data['states'][0] if paper == PAPERS[0] else data['structure'] if paper == PAPERS[2] else data['method'] if paper == PAPERS[4] else data['system']
    identity['charge'] = None
    assert not validate(tmp_path, paper, mode, data)['valid']


@pytest.mark.parametrize('mode', MODES)
@pytest.mark.parametrize('paper', PAPERS)
def test_available_results_stay_typed_and_unknown_status_cannot_bypass_complete(tmp_path, paper, mode):
    data = incomplete(paper, mode)
    if paper == PAPERS[0]:
        data['states'][0]['sulfur_distance_angstrom'] = 'unknown'
    elif paper == PAPERS[1]:
        data['properties']['homo_ev'] = 'unknown'
    elif paper == PAPERS[2]:
        data['orbital_properties']['gap']['value'] = 'unknown'
    elif paper == PAPERS[3]:
        data['result']['wavelength_nm'] = 'unknown'
    elif paper == PAPERS[4]:
        data['isomers']['cis_alpha']['energy_hartree'] = 'unknown'
    else:
        data['bond_comparison']['rmse'] = 'unknown'
    assert not validate(tmp_path, paper, mode, data)['valid']
    data = incomplete(paper, mode, early=True)
    data['status'] = 'completed_with_missing_values'
    assert not validate(tmp_path, paper, mode, data)['valid']


@pytest.mark.parametrize('mode', MODES)
def test_shared_isomer_definition_validates_both_failure_orders(tmp_path, mode):
    paper = PAPERS[4]
    data = incomplete(paper, mode)
    data['isomers']['cis_alpha'], data['isomers']['cis_beta'] = data['isomers']['cis_beta'], data['isomers']['cis_alpha']
    assert validate(tmp_path, paper, mode, data)['valid']
    data['status'] = 'complete'
    assert not validate(tmp_path, paper, mode, data)['valid']


@pytest.mark.parametrize('mode', MODES)
def test_incomplete_six_bond_record_cannot_claim_completion(tmp_path, mode):
    paper = PAPERS[5]
    data = incomplete(paper, mode)
    data['completion']['criterion_met'] = True
    assert not validate(tmp_path, paper, mode, data)['valid']
