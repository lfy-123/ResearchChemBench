"""Static/software regressions for the approved 18-paper staged repairs.

These are not quantum validations or demonstrations of an LLM judge's behavior.
"""
import copy
import csv
import json
import math
import re
import shutil
import subprocess
from pathlib import Path

import jsonschema
import pytest

from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository, materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'tasks/verified_tasks'
PAPERS = (
    'paper_d2d08c91f34da1cb', 'paper_6f9a36fff6964313',
    'paper_746e066c163800d8', 'paper_5ea491c741fbd8d4',
    'paper_a0f6b899582cb9f7', 'paper_ef26687d63a37e29',
    'paper_e31cc7bc7b21b610', 'paper_80cc1ffb2cf73fc5',
    'paper_a3892396b1843698', 'paper_46f6118697c6397c',
    'paper_d8e5490cd9942f4f', 'paper_c23cfabbd34b087f',
    'paper_d7967e22bb965daa', 'paper_5d94285cfbd51973',
    'paper_b33676a2051f5e91', 'paper_46a9ca0dab36dd9e',
    'paper_44f9727c4e9a4b6f',
)
PR_ONLY = {'paper_d7967e22bb965daa', 'paper_44f9727c4e9a4b6f'}
# Keep the approved batch explicit: an empty staging directory must not turn
# the package regressions into an empty parametrization after migration.
PACKAGES = sorted(
    ROOT/'tasks'/('final_verified_'+mode)/paper_id
    for mode in ('autonomous_research', 'paper_reproduction')
    for paper_id in PAPERS
    if mode == 'paper_reproduction' or paper_id not in PR_ONLY
)


def task_mode(p):
    return p.parent.name.removeprefix('final_verified_').removeprefix('hold_verified_')


@pytest.fixture(scope='session')
def release_repository(tmp_path_factory):
    # The production repository discovers standard mode directories, not
    # final_verified_* aliases. Test a standard-layout release copy explicitly;
    # this does not change the production task root or publish the benchmark.
    release_root = tmp_path_factory.mktemp('approved_task_release')
    for p in PACKAGES:
        shutil.copytree(p, release_root/task_mode(p)/p.name)
    return TaskRepository(roots=[release_root])


def package(prefix,mode='paper_reproduction'):
    matches=[p for p in PACKAGES if task_mode(p)==mode and p.name.startswith('paper_'+prefix)]
    if not matches and prefix.startswith('a396'):
        matches=list((ROOT/'tasks'/('hold_verified_'+mode)).glob('paper_'+prefix+'*'))
    assert len(matches)==1, (prefix,mode,matches)
    return matches[0]


def obj(path):return json.loads(path.read_text())


def schema(prefix,mode):
    d=obj(package(prefix,mode)/'agent_input/submission_schema.json')
    return d.get('result_schema',d)


def valid(s,data):return jsonschema.validators.validator_for(s)(s).is_valid(data)


@pytest.mark.parametrize('p',PACKAGES,ids=lambda p:p.parent.name+'/'+p.name)
def test_package_schema_targets_and_visibility(p,tmp_path,release_repository):
    assert validate_task_package(p).status=='passed'
    d=obj(p/'agent_input/submission_schema.json');s=d.get('result_schema',d)
    jsonschema.validators.validator_for(s).check_schema(s)
    for f in p.rglob('*.json'):obj(f)
    original = 'tasks/verified_tasks/'+task_mode(p)+'/'+p.name
    before=json.loads(subprocess.check_output(['git','show','ed724c76:'+original+'/evaluation/scoring_rules.json'],cwd=ROOT))
    after=obj(p/'evaluation/scoring_rules.json')
    # The approved 2026-09-18 revision removes generic disclaimer rules.
    # Preserve the original numeric contracts, not the empty dictionaries
    # formerly contributed by those deleted semantic rules.
    def numbers(data):return {z['rule_id']:{k:z[k] for k in ('target','tolerance','weight','unit') if k in z} for z in data['rules'] if any(k in z for k in ('target','tolerance','weight','unit'))}
    assert numbers(before)==numbers(after)
    repo=release_repository; runtime=load_runtime_evaluation(paper_id=p.name,task_type=task_mode(p),repository=repo)
    assert runtime.ground_truth['expected_result']['scoring_rules']==after['rules']
    copied=materialize_agent_files(paper_id=p.name,task_type=task_mode(p),destination=tmp_path,repository=repo)
    assert set(copied)=={str(x.relative_to(p/'agent_input')) for x in (p/'agent_input').rglob('*') if x.is_file()}
    assert not any(any(w in x for w in ['author_results','task_provenance','verified_computation_reference']) for x in copied)
    assert not any(x.is_symlink() for x in p.rglob('*'))


def test_finalized_batch_is_complete_without_staging_duplicates(release_repository):
    assert len(PAPERS)==17 and len(PACKAGES)==32
    assert len(release_repository.list(task_type='autonomous_research'))==15
    assert len(release_repository.list(task_type='paper_reproduction'))==17
    for p in PACKAGES:
        assert p.is_dir()
        assert not (BASE/task_mode(p)/p.name).exists()
        assert (p/'evaluation/verified_computation_reference.md').is_file()
        # Under the later approved limitation revision, public chemical data
        # and identity metadata stay frozen for this batch. Task/schema and
        # semantic grading text are covered by the revision contract tests;
        # numeric targets remain checked separately above.
        science=list((p/'agent_input/data').rglob('*')) + [p/'task_info.json', p/'paper_route.md']
        for f in science:
            if not f.is_file():
                continue
            original='tasks/verified_tasks/'+task_mode(p)+'/'+p.name+'/'+f.relative_to(p).as_posix()
            assert f.read_bytes()==subprocess.check_output(['git','show','8feb10f5:'+original],cwd=ROOT), f


def test_final_archive_current_inputs_and_main_results():
    for p in PACKAGES:
        archive=(p/'evaluation/verified_computation_reference.md').read_text()
        assert '2026-09-17 最终包审查通过' in archive
        assert '当前目录/审批状态：已退回 verified_tasks' not in archive
        assert '[canonical 源任务](..)' not in archive
        audit=(p/'evaluation/task_provenance/maintenance_audit.md').read_text()
        assert audit.startswith('# 当前目录与审批状态（2026-09-17）')
        assert p.relative_to(ROOT).as_posix() in audit.split('---',1)[0]
        assert '属于此前维护阶段的历史状态' in audit
    for mode in ('autonomous_research','paper_reproduction'):
        archive=(package('46a9',mode)/'evaluation/verified_computation_reference.md').read_text()
        assert '当前以第 20 态 Mulliken-like' in archive
        assert '以第 22 态 LMCT/MLCT 数值对照 evaluator' not in archive
        archive=(package('80cc',mode)/'evaluation/verified_computation_reference.md').read_text()
        assert 'prominence=0.02' in archive and '20093' in archive
        archive=(package('ef266',mode)/'evaluation/verified_computation_reference.md').read_text()
        assert '当前公开输入有 SI-derived 坐标' not in archive


def test_final_markdown_links_resolve():
    checked=0
    files=[f for p in PACKAGES for f in p.rglob('*.md')]
    files += [BASE/'MAINTENANCE_REPORT.md', BASE/'POST_REPAIR_REAUDIT_20260916.md']
    for f in files:
        # Exclude SMILES and illustrative code from Markdown link parsing.
        content=re.sub(r'```.*?```|`[^`\n]*`','',f.read_text(),flags=re.S)
        for target in re.findall(r'\]\(([^\s)]+)\)',content):
            if target.startswith(('https://','http://','mailto:','#')):
                continue
            target=target.split('#')[0]
            if target:
                assert (f.parent/target).exists(), (f,target)
                checked+=1
    assert checked>900


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_helicene_truthful_failure_and_complete(mode):
    s=schema('746',mode)
    d={'status':'bounded_failure','method':{'software':'fixture','model':'fixture','charge':0,'multiplicity':1},'candidate':{'id':'fixture','geometry_source':'fixture','converged':False},'validation':{'minimum_test':'not computed','imaginary_modes':None,'independent_check':'not computed','search_coverage':'attempted','stopping_reason':'fixture failure'},'failure_diagnostics':'No Hessian was computed','limitations':'synthetic software fixture'}
    assert valid(s,d)
    d['status']='complete';d.update(torsions=[{'label':str(i),'atom_indices':[1,2,3,4],'value_deg':0.,'convention':'signed'} for i in range(5)],mean_torsion_deg=0.,mean_definition='mean(abs(phi))',uncertainty_deg=0.,interpretation='fixture');d['candidate']['converged']=True
    assert not valid(s,d)
    d['validation']['imaginary_modes']=0;assert valid(s,d)
    d['validation']['imaginary_modes']=None;d['validation']['equivalent_minimum_evidence']='fixture equivalent Hessian artifact';assert valid(s,d)
    p=package('746',mode)
    assert not (p/'agent_input/data/inputs/experimental_torsion_boundary.json').exists()
    assert (p/'evaluation/author_results/experimental_torsion_boundary.json').is_file()
    assert '27.0' not in (p/'agent_input/task.md').read_text()


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_isoxazole_candidate_unknown_not_zero(mode):
    s=schema('5ea',mode)['properties']['candidates']['items']
    d={'candidate_id':'failed','identity':'fixture','disposition':'failed','optimization_status':'failed','stationary_point_test':{'method':'not run','imaginary_frequency_count':None,'minimum_assessment':'unknown'},'relative_energy_kcal_mol':None,'diagnostics':'Hessian unavailable'}
    assert valid(s,d)
    d['diagnostics']='';assert not valid(s,d)
    d['stationary_point_test']['imaginary_frequency_count']=0;assert valid(s,d)


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_seven_a_empty_failure_not_complete(mode):
    s=schema('a396',mode)
    model={'name':'fixture','method':'fixture','coordinates':'','converged':False,'stationary':False,'identity_validation':'unavailable','stationarity_evidence':'not computed','rationale':'fixture'}
    d={'status':'bounded_failure','models':[model,dict(model,name='second')],'mapping':{'label_to_atom':{},'mapping_basis':'unavailable'},'observables':[],'metrics':[],'conclusion':'unavailable','limitations':'fixture','failure_reason':'optimization not run'}
    assert valid(s,d)
    d['status']='complete';assert not valid(s,d)
    evidence=obj(package('a396',mode)/'evaluation/task_provenance/identity_evidence_check_20260916.json')
    assert evidence['matching_records']==0
    rows=list(csv.DictReader((package('a396',mode)/'agent_input/data/inputs/experimental_geometry.csv').open()))
    assert len(rows)==len({r['selector'] for r in rows})==47
    assert {k:sum(r['kind']==k for r in rows) for k in ['bond','angle','torsion']}=={'bond':13,'angle':23,'torsion':11}
    assert not any('calculated' in k.lower() for k in rows[0])


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_seven_a_owner_authorized_hold_preserves_package(mode,release_repository):
    p=package('a396',mode)
    assert p.parent.name=='hold_verified_'+mode
    assert not (BASE/mode/p.name).exists()
    assert validate_task_package(p).status=='passed'
    for f in p.rglob('*.json'):obj(f)
    original='tasks/verified_tasks/'+mode+'/'+p.name+'/evaluation/scoring_rules.json'
    baseline=json.loads(subprocess.check_output(['git','show','db98ad0c:'+original],cwd=ROOT))
    assert obj(p/'evaluation/scoring_rules.json')==baseline
    assert not any(x.is_symlink() for x in p.rglob('*'))
    assert '已移入对应 hold_verified 目录' in (p/'evaluation/verified_computation_reference.md').read_text()
    with pytest.raises(FileNotFoundError):
        TaskRepository(roots=[BASE]).get(paper_id=p.name,task_type=mode)
    with pytest.raises(FileNotFoundError):
        release_repository.get(paper_id=p.name,task_type=mode)


def test_insertion_channels_have_no_public_ts_and_truthful_unknown():
    p=package('d796');inp=p/'agent_input/data/inputs';d=obj(inp/'reaction_channels.json')
    assert len(d['channels'])==4
    assert [x['hydride_transfer_to'] for x in d['channels']]==['terminal_alkyne_C','substituted_alkyne_C']*2
    for letter in 'ABCD':
        assert not (inp/f'TS3{letter}_quartet.xyz').exists()
        assert (p/f'evaluation/author_results/TS3{letter}_quartet.xyz').exists()
    s=schema('d796','paper_reproduction')['properties']['candidates']['items']
    rec={'label':'TS3A-quartet','status':'failed','input_provenance':{'file':'INT2A_quartet.xyz','atom_count':68,'charge':0,'multiplicity':4},'frequency_validation':{'imaginary_frequency_count':None,'imaginary_frequencies':[],'assignment_evidence':'not computed','validated':False},'barrier':{'status':'unavailable'},'notes':'Hessian not computed'}
    assert valid(s,rec)
    rec['frequency_validation']['validated']=True;assert not valid(s,rec)
    rec['frequency_validation']['imaginary_frequency_count']=1;assert valid(s,rec)


def test_numeric_condition_is_carried_to_judge_not_a_fake_predicate(release_repository):
    repo=release_repository
    p=package('b336','autonomous_research');run=load_runtime_evaluation(paper_id=p.name,task_type=task_mode(p),repository=repo)
    rule=next(x for x in run.ground_truth['expected_result']['scoring_rules'] if x['rule_id']=='ar_r4')
    assert 'ONLY' in rule['binding']['comparison'] and 'mapped product connectivity' in rule['binding']['comparison']
    assert 'not a numerical failure' in rule['binding']['comparison']
    for mode in ['autonomous_research','paper_reproduction']:
        p=package('e31',mode);rules=obj(p/'evaluation/scoring_rules.json')['rules'];texts=json.dumps(rules)
        assert 'positive E(beta)-E(alpha)' in texts
        # This checks the mathematical counterexample, not actual judge behavior.
        assert abs(-.02-1.44)<1.5 and not (-.02>0)


def test_primary_protocols_not_auto_injected_into_ar():
    for prefix,protocol in [('6f9a','M06-2X-D3/def2-TZVP'),('5ea','B3LYP/6-311+G(d,p)'),('a396','B3LYP and CAM-B3LYP'),('46a9','30 sextet TD states')]:
        assert protocol in (package(prefix)/'agent_input/task.md').read_text()
        assert protocol not in (package(prefix,'autonomous_research')/'agent_input/task.md').read_text()


def test_z1_data_are_experiment_not_fc_and_all_sticks_audited():
    p=package('80cc');meta=obj(p/'agent_input/data/inputs/experimental_spectrum_metadata.json')
    assert 'not original detector data' in meta['data_kind']
    assert meta['point_count']>750
    for mode in ['autonomous_research','paper_reproduction']:
        inputs=package('80cc',mode)/'agent_input/data/inputs'
        with (inputs/'experimental_spectrum.csv').open() as stream:
            rows=list(csv.DictReader(stream))
        assert len(rows)==obj(inputs/'experimental_spectrum_metadata.json')['point_count']==825
    assert len(obj(p/'evaluation/task_provenance/experimental_comparison_20260916.json')['matches'])==11
    public=(p/'agent_input/task.md').read_text()
    assert '517.809' not in public and '512 cm' not in public


def test_cat1_fixed_state_selection_and_partition_are_explicit():
    for mode in ['autonomous_research','paper_reproduction']:
        p=package('46a9',mode);definition=obj(p/'agent_input/data/inputs/catalyst_system.json')
        assert 'highest oscillator strength' in definition['measurement_protocol']['representative_state']
        assert definition['measurement_protocol']['fragments']==['all four Cl','Fe','complete TEA+']
        assert definition['environment']['solvent']=='acetonitrile'
        assert 'state20' not in (p/'agent_input/task.md').read_text()


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_phosphonium_contact_selector_contract(mode,release_repository):
    p=package('ef266',mode)
    task=(p/'agent_input/task.md').read_text()
    assert 'input atom-map ID 49' in task and 'phosphorus is ID 46' in task
    assert 'not the other carboxylate oxygen O50 or the acyl oxygen O51' in task
    assert 'do not average contacts or minimize over different oxygens' in task
    assert 'smallest input atom-map ID' in task
    assert 'same H atoms selected by these distance rules' in task
    for answer in ['2.651','2.312','2.363','0.447','0.455']:
        assert answer not in task
    s=schema('ef266',mode)
    # AR still reports primary pairs in species[].distances; no new mandatory
    # PR-style scalar output is silently imposed on it.
    assert ('contact_summary' in s['required'])==(mode=='paper_reproduction')
    assert set(s['properties']['contact_summary']['properties'])=={'PO','PA'}
    for spec in s['properties']['contact_summary']['properties'].values():
        assert set(spec['required'])=={'O_P_A','O_alphaH_A','O_betaH_A'}
        assert all('O49' in x['description'] for x in spec['properties'].values())
    rules=obj(p/'evaluation/scoring_rules.json')['rules']
    ids=['r_ar_geometry','r_ar_provenance'] if mode=='autonomous_research' else ['r_pr_mapping','r_pr_po_OP','r_pr_po_OalphaH','r_pr_po_ObetaH','r_pr_pa_OP','r_pr_pa_OalphaH','r_pr_pa_ObetaH']
    for rule in rules:
        if rule['rule_id'] in ids:
            assert 'same O49' in rule['binding']['comparison']
            assert 'No averaging or minimization across different oxygens' in rule['binding']['comparison']
    charge=next(x for x in rules if x['rule_id']==('r_ar_charges' if mode=='autonomous_research' else 'r_pr_H_charge'))
    assert 'no hidden source-selected H is required' in charge['binding']['comparison']
    # The judge receives these definitions; this is not a claim that JSON
    # Schema itself measures distances or that a live LLM judge was tested.
    repo=release_repository
    runtime=load_runtime_evaluation(paper_id=p.name,task_type=mode,repository=repo)
    assert runtime.ground_truth['expected_result']['scoring_rules']==rules


@pytest.mark.parametrize('mode',['autonomous_research','paper_reproduction'])
def test_phosphonium_existing_results_and_failure_schema(mode):
    path=ROOT/'docs/verification/group_1/paper_ef26687d63a37e29/report/results.json'
    if not path.is_file():
        pytest.skip('Local historical verification artifacts are not installed')
    d=obj(path);s=schema('ef266',mode)
    assert valid(s,d)
    failed=copy.deepcopy(d)
    failed['status']='bounded_failure'
    failed['species']=[{'name':x['name'],'status':'failed','failure_reason':'Synthetic fixture: geometry or wavefunction unavailable','missing_observables':['contacts','charges']} for x in d['species']]
    failed['contact_summary']={k:{field:None for field in v} for k,v in d['contact_summary'].items()}
    failed['charge_summary']={k:{'P_e':None} for k in d['charge_summary']}
    assert valid(s,failed)
    if mode=='autonomous_research':
        d.pop('contact_summary');assert valid(s,d)


@pytest.mark.parametrize('species',['PO','PA'])
def test_phosphonium_selector_matches_existing_coordinates(species):
    base=ROOT/'docs/verification/group_1/paper_ef26687d63a37e29/report'
    geometry=base/f'structures/{species}_optimized.xyz'
    if not geometry.is_file() or not (base/'results.json').is_file():
        pytest.skip('Local historical verification artifacts are not installed')
    result=obj(base/'results.json')
    record=next(x for x in result['species'] if x['name'].endswith('-'+species))
    coords=[tuple(map(float,line.split()[1:4])) for line in geometry.read_text().splitlines()[2:] if line.strip()]
    # These sets were independently checked against the public mapped graph,
    # not selected by proximity to any target contact or charge.
    alpha=[5,6,12,13,19,20,26,27,33,34,36,37]
    beta=[8,9,10,15,16,17,22,23,24,29,30,31,39,40,41,43,44,45]
    def nearest(o,hs):
        return min((math.dist(coords[o-1],coords[h-1]),h) for h in hs)
    primary={'O_P_A':(math.dist(coords[48],coords[45]),46),'O_alphaH_A':nearest(49,alpha),'O_betaH_A':nearest(49,beta)}
    for field,(value,other) in primary.items():
        observed=next(x for x in record['distances'] if x['label']==field)
        assert observed['atom_indices']==[49,other]
        assert value==pytest.approx(observed['value_angstrom'],abs=1e-10)
        assert value==pytest.approx(result['contact_summary'][species][field],abs=1e-10)
        if field!='O_P_A':
            charge=next(x['value_e'] for x in record['charges'] if x['atom_index']==other)
            assert charge==result['charge_summary'][species]['nearest_contact_H_e'][field]
    if species=='PA':
        # A global O/H minimum changes the observable even if it accidentally
        # remains within a numerical tolerance. It is not the primary rule.
        assert nearest(50,beta)[0]<primary['O_betaH_A'][0]
        assert math.dist(coords[49],coords[45])>primary['O_P_A'][0]+1


def test_cat1_ar_primary_vs_auxiliary_state_is_unambiguous():
    p=package('46a9','autonomous_research')
    task=(p/'agent_input/task.md').read_text()
    assert 'or another justified criterion' not in task
    assert 'Do not assume any author mechanism or target state' not in task
    assert 'excluding solvent and reaction substrates' not in task
    assert 'must not replace that primary state' in task
    assert 'state_selection' in task and 'ifct_records' in task
    s=schema('46a9','autonomous_research')['properties']
    assert 'highest-oscillator-strength' in s['state_selection']['description']
    assert 'same highest-f physical state' in s['ifct']['description']
    coverage=next(x for x in obj(p/'evaluation/scoring_rules.json')['rules'] if x['rule_id']=='ar_r_coverage')
    assert 'primary highest-f state' in coverage['expected']
    assert 'auxiliary/sensitivity' in coverage['expected']
