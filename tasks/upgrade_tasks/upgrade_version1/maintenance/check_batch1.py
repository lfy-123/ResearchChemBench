"""Offline package/contract regression. Synthetic fixtures are NOT scientific results."""
from pathlib import Path
from copy import deepcopy
import hashlib, json, re, sys, tempfile
ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT))
import jsonschema
from evaluation.contracts.task_package import validate_task_package
from evaluation.repository import TaskRepository, materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract
DEST=ROOT/'tasks/upgrade_tasks'
IDS=['paper_d83e607f125440cc','paper_2f302589e5e9e420','paper_628af8d0bf0a1bfe','paper_9ec32e81e2826041','paper_2f0a4f80a37fbccd','paper_0dcba54d6a1436bd']
MODES=['autonomous_research','paper_reproduction']
RESULTS=[]
def check(name,ok,detail=None):
    RESULTS.append({'test':name,'passed':bool(ok),**({'detail':detail} if detail else {})})
    if not ok: raise AssertionError((name,detail))
def merge(a,b):
    a=deepcopy(a)
    for k,v in b.items():
        if k=='required': a[k]=list(dict.fromkeys(a.get(k,[])+v))
        elif isinstance(v,dict) and isinstance(a.get(k),dict): a[k]=merge(a[k],v)
        else: a[k]=deepcopy(v)
    return a
def sample(schema,defs):
    s=deepcopy(schema)
    if '$ref' in s: s=merge(defs[s.pop('$ref').split('/')[-1]],s)
    if 'oneOf' in s: s=merge(s,s.pop('oneOf')[0])
    if 'const' in s: return s['const']
    if 'enum' in s: return s['enum'][0]
    typ=s.get('type','object' if 'properties' in s else 'string')
    if isinstance(typ,list):typ=next(x for x in typ if x!='null')
    if typ=='object':
        value={k:sample(s.get('properties',{}).get(k,{}),defs) for k in s.get('required',[])}
        additions={}
        for condition in s.get('allOf',[]):
            if 'if' in condition and jsonschema.Draft202012Validator(condition['if']).is_valid(value): additions=merge(additions,condition.get('then',{}))
        if additions:
            s.pop('allOf',None)
            return sample(merge(s,additions),defs)
        return value
    if typ=='array':
        contains=[x['contains'] for x in s.get('allOf',[]) if 'contains' in x]
        if 'contains' in s:contains.append(s['contains'])
        rows=[sample(merge(s.get('items',{}),c),defs) for c in contains]
        while len(rows)<s.get('minItems',0):rows.append(sample(s.get('items',{}),defs))
        if s.get('uniqueItems'):
            for i in range(len(rows)):
                if isinstance(rows[i],(int,float)):rows[i]+=i
                elif isinstance(rows[i],str):rows[i]+=str(i)
        return rows
    if typ in ['number','integer']:return max(s.get('minimum',1),s.get('exclusiveMinimum',0)+1)
    if typ=='boolean':return False
    if typ=='null':return None
    if 'pattern' in s:return 'outputs/SYNTHETIC_NOT_A_CALCULATION.log'
    return 'SYNTHETIC FORMAT FIXTURE; NOT SCIENTIFIC EVIDENCE'

def validate_fixture(contract,doc,report=True):
    with tempfile.TemporaryDirectory(prefix='rcb_batch1_format_only_') as td:
        t=Path(td);(t/'report').mkdir()
        (t/'report/results.json').write_text(json.dumps(doc))
        if report:(t/'report/report.md').write_text('Synthetic schema regression fixture only; no scientific calculation or result.\n')
        return validate_output_contract(t,json.dumps(contract).encode())

def main():
    # Later batches share DEST. Validate only the original twelve packages,
    # including while another batch is being authored; do not make unrelated
    # drafts a prerequisite for this batch's regression checks.
    repo=TaskRepository.__new__(TaskRepository)
    repo.roots=(DEST,)
    repo._approved_final_directories=tuple(DEST/mode/pid for mode in MODES for pid in IDS)
    repo._index=repo._build_index()
    check('exact_12_package_scope',len(repo.list())==12)
    for pid in IDS:
        ar=DEST/MODES[0]/pid;pr=DEST/MODES[1]/pid
        expected_pub={str(p.relative_to(ar/'agent_input')):p.read_bytes() for p in (ar/'agent_input').rglob('*') if p.is_file()}
        for rel,data in expected_pub.items():
            if rel!='task.md':check(pid+':mode_public_parity:'+rel,data==(pr/'agent_input'/rel).read_bytes())
        for name in ['reference_key_points.json','reference_conclusions.json','scoring_rules.json','critical_failures.json','evidence_map.json']:
            check(pid+':mode_scientific_parity:'+name,(ar/'evaluation'/name).read_bytes()==(pr/'evaluation'/name).read_bytes())
        a=(ar/'agent_input/task.md').read_text();p=(pr/'agent_input/task.md').read_text()
        check(pid+':author_route_only_PR','# Author-provided scientific guidance' not in a and '# Author-provided scientific guidance' in p)
        stripped=re.sub(r'\n\n# Author-provided scientific guidance\n\n.*?(?=\n\n# Public inputs)', '',p,flags=re.S)
        stripped=stripped.replace('This is a paper-reproduction task. The author guidance above is authorized route information; reproduce that baseline and test its interpretation using the expanded controls.','This is an autonomous-research task. Use the authorized public objects to formulate and test explanations independently.')
        check(pid+':mode_scientific_instruction_parity',a==stripped)
        contract=json.loads((ar/'agent_input/submission_schema.json').read_text())
        schema=contract['result_schema'];jsonschema.Draft202012Validator.check_schema(schema)
        positive=sample(schema,schema.get('$defs',{}))
        result=validate_fixture(contract,positive)
        check(pid+':synthetic_complete_format_accepted',result['valid'],result['errors'][:3])
        if 'd83e' in pid:
            ordering=deepcopy(positive)
            ordering['results']['prediction_test']['comparison']={'kind':'ordering','reference_member':'OMe','predicted_relation':'higher','observed_relation':'unresolved','member_value_kJ_mol':1.0,'reference_value_kJ_mol':1.1,'uncertainty_basis':'SYNTHETIC FORMAT TEST ONLY'}
            check(pid+':ordering_prediction_format_accepted',validate_fixture(contract,ordering)['valid'])
        if '9ec32' in pid:
            collapse=deepcopy(positive)
            for setting in collapse['results']['conformers'].values():
                setting['comparison']={'outcome':'one_retained_basin','collapse_evidence':['outputs/SYNTHETIC_COLLAPSE.log']}
                for family in setting['families'].values():family['outcome']='collapsed_to_other_family'
            check(pid+':evidenced_basin_collapse_format_accepted',validate_fixture(contract,collapse)['valid'])
        negative=deepcopy(positive);negative['results']={}
        check(pid+':empty_new_results_rejected',not validate_fixture(contract,negative)['valid'])
        for panel in list(positive['results']):
            negative=deepcopy(positive);del negative['results'][panel]
            check(pid+':missing_panel_rejected:'+panel,not validate_fixture(contract,negative)['valid'])
        for field,value in [('charge',17),('multiplicity',9)]:
            negative=deepcopy(positive);negative['calculation_records'][0][field]=value
            check(pid+':wrong_'+field+'_rejected',not validate_fixture(contract,negative)['valid'])
        negative=deepcopy(positive);negative['calculation_records'][0]['kind']='failed'
        check(pid+':complete_all_failed_rejected',not validate_fixture(contract,negative)['valid'])
        for path in ['outputs/../evaluation/hidden.json','outputs/sub/../../hidden','/tmp/answer.json','evaluation/reference.json','outputs//../secret']:
            negative=deepcopy(positive);negative['evidence_files']=[path]
            check(pid+':unsafe_evidence_path_rejected:'+path,not validate_fixture(contract,negative)['valid'])
        check(pid+':missing_readable_report_rejected',not validate_fixture(contract,positive,False)['valid'])
        check(pid+':old_scalar_only_rejected',not validate_fixture(contract,{'status':'complete','result':1.23,'conclusion':'Old scalar only'})['valid'])
        failure=deepcopy(positive)
        failure['status']='bounded_failure'
        for key in ['results','hypotheses','sensitivity']:failure.pop(key,None)
        failure['methods'].pop('sensitivity',None)
        failure['calculation_records'][0]['kind']='failed'
        failure['calculation_records'][0].pop('energies',None);failure['calculation_records'][0].pop('geometry_file',None)
        failure['failure_report']={'attempted_scope':'SYNTHETIC early engine failure','observed_failure':'No electronic result','missing_endpoints':['all expanded endpoints'],'evidence_files':['outputs/SYNTHETIC_failure.log']}
        result=validate_fixture(contract,failure)
        check(pid+':honest_early_failure_format_accepted',result['valid'],result['errors'][:3])
        failure.pop('failure_report')
        check(pid+':failure_without_diagnostics_rejected',not validate_fixture(contract,failure)['valid'])
        if 'd83e' in pid:
            negative=deepcopy(positive);del negative['results']['series']['Cl']
        elif '2f302' in pid:
            negative=deepcopy(positive);del negative['results']['conformers']['EPI2']
        elif '628af' in pid:
            negative=deepcopy(positive);negative['results']['probe_results'][0]['probes'][-1]=deepcopy(negative['results']['probe_results'][0]['probes'][0])
        elif '9ec32' in pid:
            negative=deepcopy(positive);del negative['results']['conformers']['D3_off']
        elif '2f0a4' in pid:
            negative=deepcopy(positive)
            for c in negative['results']['candidates']:c['initial_binding']='eta2'
        else:
            negative=deepcopy(positive)
            for c in negative['results']['geometries']['structures']:c['system']='AQCZCS'
        check(pid+':missing_scientific_axis_rejected',not validate_fixture(contract,negative)['valid'])
        for mode in MODES:
            package=DEST/mode/pid
            v=validate_task_package(package)
            check(pid+':'+mode+':package_manifest_contract',v.status=='passed',v.findings)
            runtime=load_runtime_evaluation(paper_id=pid,task_type=mode,repository=repo)
            check(pid+':'+mode+':runtime_flat_rubric',runtime.adapter_id=='split-computational-evaluator.v3-flat')
            check(pid+':'+mode+':scientific_weights_100',sum(r['max_score'] for r in runtime.ground_truth['scientific_conclusion_rubric'])==100)
            with tempfile.TemporaryDirectory(prefix='rcb_batch1_public_export_') as td:
                files=materialize_agent_files(paper_id=pid,task_type=mode,destination=td,repository=repo)
                actual={str(p.relative_to(td)) for p in Path(td).rglob('*') if p.is_file()}
                expected={str(p.relative_to(package/'agent_input')) for p in (package/'agent_input').rglob('*') if p.is_file()}
                check(pid+':'+mode+':export_only_agent_input',actual==expected)
                check(pid+':'+mode+':no_private_export',not any('evaluation' in f or '.snapshot' in f or f.endswith('.pdf') for f in actual))
            audit=json.loads((package/'evaluation/task_provenance/upgrade_audit.json').read_text())
            for original,record in audit['source_payload_snapshots'].items():
                check(pid+':'+mode+':snapshot_hash:'+original,hashlib.sha256((package/record['snapshot']).read_bytes()).hexdigest()==record['sha256'])
            check(pid+':'+mode+':pending_reference_not_claimed_verified',audit['status']=='implemented_pending_expanded_reference' and audit['new_scientific_calculations_performed'] is False)
            for document in package.rglob('*.md'):
                for target in re.findall(r'\]\(([^)]+)\)',document.read_text()):
                    if not target.startswith(('http:','https:','#')):
                        check(pid+':local_link:'+str(document.relative_to(package))+':'+target,(document.parent/target.split('#')[0]).exists())
    ir=DEST/'autonomous_research/paper_2f0a4f80a37fbccd/agent_input/data/inputs'
    check('Ir_no_Xray_answer_exposed',not (ir/'experimental_xray_ir_boundary.json').exists())
    irdata=json.loads((ir/'complex_specification.json').read_text())
    check('Ir_connectivity_not_fixed',irdata['fixed_metal_nitrate_connectivity'] is False)
    known_targets=['198.5','0.401','139.4','23.6','19.2','2.173','2.174','60.02','3.1097','2.4526','2.2223','1.9036']
    for pid in IDS:
        folder=DEST/'autonomous_research'/pid/'agent_input'
        exposed='\n'.join(p.read_text() for p in folder.rglob('*') if p.is_file() and p.suffix in ['.md','.json'])
        check(pid+':no_known_numeric_answer_leakage',not any(v in exposed for v in known_targets))
        if '0dcba' in pid:
            check(pid+':no_AQ_specific_state_answer_in_AR','AQCZCS S1' not in (folder/'task.md').read_text())
    manifest=json.loads((DEST/'batch1_implementation_manifest.json').read_text())
    for record in manifest['packages']:
        actual=json.loads((ROOT/record['path']/'package_manifest.json').read_text())
        check(record['paper_id']+':'+record['mode']+':batch_hash_current',record['package_content_sha256']==actual['package_content_sha256'])
    return {'date':'2026-09-27','status':'passed','checks':len(RESULTS),'scientific_calculations_run':0,'LLM_judge_run':False,
        'boundary':'Package/runtime/export and synthetic-format tests only. These are not scientific reference validation or calibrated scoring tests.','results':RESULTS}

if __name__=='__main__':
    try:
        report=main()
    except Exception as exc:
        report={'status':'failed','error':repr(exc),'results':RESULTS}
        print(json.dumps(report,ensure_ascii=False,indent=2));raise
    (DEST/'batch1_validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False))
