"""Regression checks for approved contracts, not new chemistry verification."""
from copy import deepcopy
import json
from pathlib import Path
import re

import pytest
from jsonpath_ng import parse
from jsonschema import Draft202012Validator

from evaluation.contracts import validate_task_package
from evaluation.scoring.adapters import _runtime_contract
from evaluation.scoring.rules import associate_rules

ROOT = Path(__file__).resolve().parents[1]
MODES = ('autonomous_research', 'paper_reproduction')


def package(mode, pid):
    return ROOT / 'tasks' / ('final_verified_' + mode) / ('paper_' + pid)


def read(p):
    return json.loads(p.read_text())


def references(p):
    return {name: read(p / 'evaluation' / name) for name in (
        'reference_key_points.json', 'reference_conclusions.json', 'scoring_rules.json',
        'critical_failures.json', 'evidence_map.json')}


PACKAGES = sorted(p for mode in MODES for p in (ROOT / 'tasks' / ('final_verified_' + mode)).glob('paper_*') if p.is_dir())


@pytest.mark.parametrize('p', PACKAGES, ids=lambda p: p.parent.name + '/' + p.name)
def test_all_final_manifests_contracts_and_runtime_still_load(p):
    report = validate_task_package(p)
    assert report.status == 'passed', report.findings
    mode = p.parent.name.removeprefix('final_verified_')
    runtime = _runtime_contract(task_type=mode, reference=references(p), submission=read(p / 'agent_input/submission_schema.json'))
    assert sum(x['max_score'] for x in runtime['scientific_conclusion_rubric']) == 100
    assert runtime['dual_axis_scoring_policy']['policy_id'] == 'dual_axis_100.scientific_results.v1'


def test_photocyclization_public_branch_does_not_name_the_winner():
    p = package('paper_reproduction', '0dc85595cab7bc0a')
    for file in (p / 'agent_input').rglob('*'):
        if file.is_file():
            assert 'dibenzo[a,o]picene' not in file.read_text().lower()
    task = (p / 'agent_input/task.md').read_text()
    assert 'thermochemical' in task and 'candidate comparisons' in task


@pytest.mark.parametrize('mode', MODES)
def test_hydration_keeps_all_observations_but_not_assignments_or_onset(mode):
    p = package(mode, '6e09640463562644')
    values = read(p / 'agent_input/data/inputs/experimental_band_assignments.json')
    original = read(ROOT / 'tasks' / mode / p.name / 'agent_input/data/inputs/experimental_band_assignments.json')
    assert values['units'] == original['units']
    assert set(values['bands']) == set(original['bands'])
    for key, item in values['bands'].items():
        assert item['values'] == original['bands'][key]['values']
        assert 'assignment' not in item
    task = (p / 'agent_input/task.md').read_text()
    assert not re.search(r'n\s*=\s*3', task)
    assert 'neutral band labels' in task
    if mode == 'paper_reproduction':
        assert 'contact Ba–OH' in task and 'solvent-shared' in task


@pytest.mark.parametrize('mode', MODES)
def test_model_and_primary_method_remain_fixed_but_no_conflicting_text(mode):
    t = (package(mode, '1b285cf9f763f2cf') / 'agent_input/task.md').read_text()
    assert 'finite-.' not in t and 'undoped UC-1 environment' not in t
    assert 'Zn8FeAl15O32' in t and 'neutral-cell electronic compensation' in t
    t = (package(mode, '94e7481ded3b6a75') / 'agent_input/task.md').read_text()
    assert 'while reporting.' not in t and 'or a preselected computational protocol' not in t
    assert 'B3LYP/6-31G(d)' in t and '298.15 K and 1 atm' in t


@pytest.mark.parametrize('mode', MODES)
def test_barrier_convention_is_public_without_answer(mode):
    p = package(mode, '221aafe4bd916a11')
    t = (p / 'agent_input/task.md').read_text()
    assert 'G(TS) - G(2a) - G(CO2)' in t and '298.15 K, 1 atm' in t
    assert '21.8' not in t and '19.871' not in t
    ref = (p / 'evaluation/verified_computation_reference.md').read_text()
    assert '"geometry_or_source": "SI-recovered TS optimization followed by successful standalone frequency' in ref
    assert 'historical low-basis verification branch is not the SI high-basis' in ref
    assert (-2324.733530 + 2136.233723 + 188.531475) * 627.5094740631 == pytest.approx(19.871970024681406, abs=1e-6)


@pytest.mark.parametrize('mode', MODES)
def test_lifetime_and_vertical_gap_definitions_without_numerical_answers(mode):
    t = (package(mode, '98b6f8a0352f72c2') / 'agent_input/task.md').read_text()
    assert '1.4999 / (f * wavenumber_cm_inverse**2)' in t
    assert '2.688686' not in t and '29559.6' not in t
    tau = 1e9 * 1.4999 / (.638447321 * 29559.6**2)
    assert tau == pytest.approx(2.688686276, abs=1e-8)
    t = (package(mode, '3316e45a74258fb7') / 'agent_input/task.md').read_text()
    assert 'same S0 geometry' in t and 'not the difference between separately relaxed' in t


@pytest.mark.parametrize('mode', MODES)
def test_dye_named_records_validate_in_either_order_and_reject_duplicate_identity(mode):
    p = package(mode, '988bc12ae3768679')
    schema = read(p / 'agent_input/submission_schema.json')['result_schema']
    validator = Draft202012Validator(schema)
    historical = read(ROOT / 'docs/verification/group_3/paper_988bc12ae3768679/report/results.json')
    validator.validate(historical)
    swapped = deepcopy(historical)
    swapped['structures'].reverse()
    validator.validate(swapped)
    bad = deepcopy(historical)
    bad['structures'][1]['name'] = bad['structures'][0]['name']
    assert list(validator.iter_errors(bad))
    bad['structures'][1]['name'] = 'unknown'
    assert list(validator.iter_errors(bad))
    assert not re.search(r'\$\.structures\[[01]\]', json.dumps(references(p)))
    for rule in read(p / 'evaluation/scoring_rules.json')['rules']:
        if rule['reference_id'].endswith(('result_acid', 'result_base')):
            name = '2a-acid' if rule['reference_id'].endswith('result_acid') else '2a-base'
            assert 'name="' + name + '"' in rule['expected']
            assert rule['binding']['fields'] == ['$.structures[*]']
            # Binding exposes whole named records; semantic acceptance selects identity.
            # This verifies selector/order invariance, not a real LLM verdict.
            def bound(doc):
                return {m.value['name']: m.value for m in parse(rule['binding']['fields'][0]).find(doc)}
            assert bound(historical)[name] == bound(swapped)[name]


@pytest.mark.parametrize('mode', MODES)
@pytest.mark.parametrize('pid', ['d2d08c91f34da1cb', 'f9d09d28c7d9adaa'])
def test_all_existing_result_points_have_score_association_and_no_duplicate_final(mode, pid):
    p = package(mode, pid)
    ref = references(p)
    result_ids = {k['key_point_id'] for k in ref['reference_key_points.json']['items'] if k['key_point_type'] == 'result'}
    table = associate_rules(ref)
    for key in result_ids:
        assert any(row['rule']['reference_id'] == key and row['conclusion_ids'] for row in table)
    if pid.startswith('f9'):
        final = ref['reference_conclusions.json']['items'][0]['conclusion_id']
        assert sum(r['reference_id'] == final for r in ref['scoring_rules.json']['rules']) == 1


def test_stale_reference_id_headers_are_explicitly_historical():
    for p in PACKAGES:
        text = (p / 'evaluation/verified_computation_reference.md').read_text()
        for label, fn, key in [('Conclusion', 'reference_conclusions.json', 'conclusion_id'), ('Scoring-rule', 'scoring_rules.json', 'rule_id')]:
            m = re.search(r'^- ' + label + r' IDs: `([^`]+)`', text, re.M)
            if m:
                doc = read(p / 'evaluation' / fn)
                actual = {v[key] for v in doc.get('items', doc.get('rules', []))}
                if set(m.group(1).split(', ')) - actual:
                    assert '## Historical evaluator alignment (archived snapshot)' in text
