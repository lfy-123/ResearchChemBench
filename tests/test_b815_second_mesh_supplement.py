"""Current private supplement integrity; no new quantum or blind-agent run."""
import hashlib
import json
from pathlib import Path

import pytest
from jsonschema import Draft202012Validator

from evaluation.contracts import validate_task_package

ROOT = Path(__file__).resolve().parents[1]
PAPER = 'paper_b815e2622b0d6085'
MODES = ('autonomous_research', 'paper_reproduction')


def package(mode):
    return ROOT / 'tasks' / ('hold_verified_' + mode) / PAPER


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


@pytest.mark.parametrize('mode', MODES)
def test_real_author_route_record_matches_current_schema_and_bound_targets(mode):
    p = package(mode)
    record = read(p / 'evaluation/verification_supplement.json')
    value = record['author_route_results']
    Draft202012Validator(read(p / 'agent_input/submission_schema.json')['result_schema']).validate(value)
    rules = read(p / 'evaluation/scoring_rules.json')['rules']
    for rule in (r for r in rules if r['type'] == 'numeric'):
        field = next(f for f in rule['binding']['fields'] if f.endswith('.framework_interband.gap_eV'))
        actual = value
        for key in field[2:].split('.'):
            actual = actual[key]
        assert abs(actual - rule['target']) <= rule['tolerance']
    for obj in value['objects'].values():
        assert obj['optical_allowedness']['status'] == 'not_established'
        scalar = obj['scalar_relativistic']
        assert scalar['fundamental']['gap_eV'] < scalar['framework_interband']['gap_eV']
        assert scalar['framework_interband']['assignment_status'] == 'supported'
    assert value['record_type'] == 'real_author_route_results_not_an_autonomous_agent_run'


@pytest.mark.parametrize('mode', MODES)
def test_supplement_binds_independent_projected_output_without_contract_drift(mode):
    p = package(mode)
    supplement = p / 'evaluation/verification_supplement.json'
    record = read(supplement)
    history = read(p / 'evaluation/boundary_repair_evidence.json')
    assert history['current_verification']['sha256'] == sha(supplement)
    assert record['second_mesh_identity_gap_closed']
    assert record['agent_visible'] is False
    assert record['required_additional_quantum_calculations'] == []
    for path, digest in record['unchanged_contract_sha256'].items():
        assert sha(ROOT / path) == digest, path
    for label, obj in record['objects'].items():
        evidence = ROOT / obj['evidence']['path']
        assert sha(evidence) == obj['evidence']['sha256']
        extracted = read(evidence)
        for mesh in ('primary', 'check'):
            raw = obj['raw_output_sha256'][mesh]
            for filename in ('INCAR', 'POSCAR', 'POTCAR', 'KPOINTS', 'PROCAR', 'EIGENVAL'):
                assert sha(ROOT / raw['directory'] / filename) == raw['files'][filename]
            states = obj['independent_projection_assignment'][mesh]
            assert states['selected_band_is_lowest_Pb_p_leading_at_every_sampled_k_spin']
            assert states['all_lower_candidates_C_p_leading']
            assert extracted[mesh]['candidate_edge']['leading_group'] == 'framework:Pb:p'
        for branch in ('fundamental', 'framework'):
            for quantity in ('edge_gap_eV', 'minimum_same_k_gap_eV'):
                primary = extracted['primary'][branch][quantity]
                check = extracted['check'][branch][quantity]
                recorded = obj['mesh_comparison']['changes'][branch][quantity]
                assert recorded['signed_change_eV'] == pytest.approx(check - primary, abs=1e-12)
                assert recorded['absolute_change_eV'] == pytest.approx(abs(check - primary), abs=1e-12)
        # Preserve the historical missing-projection finding for the OLD run;
        # it must not be fabricated into a success or substituted for the new.
        old = history['release_reconciliation']['objects'][label]
        assert not old['raw_validation']['stability_3x3']['projection_present']
        assert obj['raw_validation']['check']['XML_has_projected_array']
        assert obj['raw_validation']['check']['complete_wave_bytes'] > 0


def test_both_modes_share_evidence_and_preserve_sampled_domain_limits():
    ar, pr = (package(mode) / 'evaluation/verification_supplement.json' for mode in MODES)
    assert ar.read_bytes() == pr.read_bytes()
    r = read(ar)
    iodine = read(ROOT / r['objects']['I']['evidence']['path'])
    assert iodine['check']['candidate_edge']['normalized_framework_weight'] < 0.5
    assert iodine['check']['candidate_edge']['leading_group'] == 'framework:Pb:p'
    primary = {k: v['all_four_observables_and_per_spin']['primary']['framework']['edge_gap_eV'] for k, v in r['objects'].items()}
    check = {k: v['all_four_observables_and_per_spin']['check']['framework']['edge_gap_eV'] for k, v in r['objects'].items()}
    assert primary['I'] < min(primary['Cl'], primary['Br'])
    assert check['I'] < min(check['Cl'], check['Br'])
    assert (primary['Cl'] - primary['Br']) * (check['Cl'] - check['Br']) < 0
    assert 'fine ordering reverses' in r['author_route_results']['structural_comparison']['evidence']
    for mode in MODES:
        p = package(mode)
        assert validate_task_package(p).status == 'passed'
        entries = read(p / 'package_manifest.json')['entries']
        private = next(x for x in entries if x['path'] == 'evaluation/verification_supplement.json')
        assert private['visibility'] == 'evaluator'
        assert not (ROOT / 'tasks' / ('final_verified_' + mode) / PAPER).exists()
