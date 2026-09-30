"""Opt-in runtime behavior; synthetic fixtures do not validate a scientific task."""
from __future__ import annotations

import json

import pytest

from evaluation.repository import TaskRepository
from evaluation.scoring.adapters import load_runtime_evaluation
from evaluation.scoring.dual_axis import (
    DUAL_AXIS_POLICY_ID, RESULTS_POLICY_ID, OPEN_RESEARCH_POLICY_ID,
    dual_axis_policy, process_rubric,
)
from evaluation.scoring.judging import ScoringBudget
from evaluation.scoring.policies import validate_judge_verdict
from evaluation.scoring.service import _aggregate, _system_prompt
from test_task_package_v19 import package, refresh_manifest


def runtime(root, mode, policy):
    p = package(root, task_type=mode)
    path = p / 'evaluation/scoring_rules.json'
    rules = json.loads(path.read_text())
    if policy is not None:
        rules['scoring_policy'] = policy
    # This fixture evaluates a computed inference, with no prescribed winner.
    rules['rules'][1]['expected'] = 'An inference supported by valid computed evidence.'
    path.write_text(json.dumps(rules))
    refresh_manifest(p)
    return load_runtime_evaluation(paper_id='paper_fixture', task_type=mode,
                                   repository=TaskRepository([root]))


def verdict(truth, *, evidence='supported', science=100, process=80):
    def item(criterion, fraction):
        return {'id':criterion['id'], 'score':criterion['max_score']*fraction/100,
                'rationale':'Synthetic evidence fixture, not a chemistry finding.',
                'citations':[{'ref':'task/contract'}]}
    return {'scientific_conclusions':[
                {**item(c,science),'evidence_status':evidence}
                for c in truth['scientific_conclusion_rubric']],
            'process_criteria':[item(c,process) for c in truth['scoring_rubric']],
            'submission_validity':'valid', 'rationale':'Synthetic test of runtime scoring.'}


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_package_opt_in_reaches_runtime_and_selects_unambiguous_prompt(tmp_path, mode):
    loaded = runtime(tmp_path, mode, OPEN_RESEARCH_POLICY_ID)
    truth = loaded.ground_truth
    assert loaded.policy_id == OPEN_RESEARCH_POLICY_ID
    assert truth['dual_axis_scoring_policy']['author_agreement_required'] is False
    prompt = _system_prompt(truth, ScoringBudget())
    assert 'supports the hidden paper conclusion' not in prompt
    assert 'scientific_results.v1' not in prompt
    assert 'demonstrated non-identifiability' in prompt
    assert 'self-written timestamps do not prove prior commitment' in prompt
    rubric = truth['scoring_rubric']
    assert sum(c['max_score'] for c in rubric) == 100
    assert 'protocol' in rubric[0]['description'] if mode=='paper_reproduction' else 'no prescribed hypothesis list or count' in rubric[0]['description']


def test_supported_alternative_can_score_but_unsupported_claim_cannot(tmp_path):
    truth = runtime(tmp_path, 'autonomous_research', OPEN_RESEARCH_POLICY_ID).ground_truth
    v = verdict(truth)
    v['scientific_conclusions'][0]['rationale'] = 'Registered evidence supports a conclusion different from the author.'
    validate_judge_verdict(v, truth, citation_check=lambda c: None)
    score = _aggregate(v, truth, tmp_path, {})
    assert score['scientific_conclusion_score'] == 100
    assert score['research_process_score'] == 80
    assert score['score'] == 80
    for status in ('unsupported','contradicted'):
        bad = verdict(truth,evidence=status)
        with pytest.raises(ValueError, match='cannot receive positive'):
            validate_judge_verdict(bad,truth,citation_check=lambda c:None)
        with pytest.raises(ValueError, match='cannot receive positive'):
            _aggregate(bad,truth,tmp_path,{})
    partial = verdict(truth,evidence='partially_supported',science=30)
    validate_judge_verdict(partial,truth,citation_check=lambda c:None)
    assert _aggregate(partial,truth,tmp_path,{})['score'] == 24
    empty = verdict(truth,evidence='unsupported',science=0,process=100)
    assert _aggregate(empty,truth,tmp_path,{})['score'] == 0


@pytest.mark.parametrize('policy',[None,DUAL_AXIS_POLICY_ID,RESULTS_POLICY_ID])
def test_existing_packages_keep_their_runtime_contract(tmp_path, policy):
    truth = runtime(tmp_path,'autonomous_research',policy).ground_truth
    expected = RESULTS_POLICY_ID if policy==RESULTS_POLICY_ID else DUAL_AXIS_POLICY_ID
    assert truth['dual_axis_scoring_policy']['policy_id']==expected
    prompt = _system_prompt(truth,ScoringBudget())
    assert OPEN_RESEARCH_POLICY_ID not in prompt
    assert 'supports the hidden paper conclusion' in prompt
    assert ('Authored policy: scientific_results.v1' in prompt)==(policy==RESULTS_POLICY_ID)


def test_policy_copies_cannot_mutate_shared_state_or_mix_versions():
    p = dual_axis_policy(open_research=True)
    p['formula']='changed'
    assert dual_axis_policy(open_research=True)['formula']=='scientific_conclusion_score * research_process_score / 100'
    for reproduction in (False,True):
        old=process_rubric(reproduction=reproduction)
        new=process_rubric(reproduction=reproduction,open_research=True)
        assert [(x['id'],x['max_score']) for x in old]==[(x['id'],x['max_score']) for x in new]
    with pytest.raises(ValueError,match='only one'):
        dual_axis_policy(scientific_results=True,open_research=True)
    with pytest.raises(ValueError,match='only one'):
        process_rubric(reproduction=False,scientific_results=True,open_research=True)
