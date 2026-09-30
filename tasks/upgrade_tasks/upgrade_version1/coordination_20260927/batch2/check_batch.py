"""Batch 2 package regressions. All temporary fixtures are explicitly NON-SCIENTIFIC.

This uses the official development TaskRepository and public output_contract.
It never starts a chemistry engine, judge, HPC job or paid service.
"""
from pathlib import Path
from copy import deepcopy
from datetime import datetime, timezone
import hashlib, json, re, sys, tempfile
B=Path(__file__).resolve().parent
ROOT=B.parents[3]
sys.path.insert(0,str(ROOT))
import jsonschema
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from evaluation.contracts.task_package import validate_task_package
from evaluation.repository import TaskRepository, materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract
DEST=ROOT/'tasks/upgrade_tasks'
IDS=json.loads((B/'assignment.json').read_text())['batch']['papers']
MODES=['autonomous_research','paper_reproduction']
FIVE=['reference_key_points.json','reference_conclusions.json','scoring_rules.json','critical_failures.json','evidence_map.json']
RESULTS=[]
SYN='SYNTHETIC FORMAT FIXTURE; NOT SCIENTIFIC EVIDENCE'
TMP=B/'test_tmp';TMP.mkdir(exist_ok=True)
def check(name,ok,detail=None):
    RESULTS.append({'test':name,'passed':bool(ok),**({'detail':detail} if detail else {})})
    if not ok:raise AssertionError((name,detail))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def read(p):return json.loads(p.read_text())
def merge(a,b):
    a=deepcopy(a)
    for k,v in b.items():
        if k=='required':a[k]=list(dict.fromkeys(a.get(k,[])+v))
        elif isinstance(v,dict) and isinstance(a.get(k),dict):a[k]=merge(a[k],v)
        else:a[k]=deepcopy(v)
    return a

def sample(schema):
    s=deepcopy(schema)
    if 'oneOf' in s:s=merge(s,s.pop('oneOf')[0])
    if 'const' in s:return s['const']
    if 'enum' in s:return s['enum'][0]
    typ=s.get('type','object' if 'properties' in s else 'string')
    if isinstance(typ,list):typ=next(x for x in typ if x!='null')
    if typ=='object':
        val={k:sample(s.get('properties',{}).get(k,{})) for k in s.get('required',[])}
        additions={}
        for rule in s.get('allOf',[]):
            if 'if' in rule and jsonschema.Draft202012Validator(rule['if']).is_valid(val):additions=merge(additions,rule.get('then',{}))
        if additions:
            s.pop('allOf',None)
            return sample(merge(s,additions))
        return val
    if typ=='array':
        contains=[x['contains'] for x in s.get('allOf',[]) if 'contains' in x]
        if 'contains' in s:contains.append(s['contains'])
        rows=[sample(merge(s.get('items',{}),c)) for c in contains]
        n=max(s.get('minItems',0),len(rows))
        if s.get('uniqueItems') and 'enum' in s.get('items',{}):return s['items']['enum'][:n]
        while len(rows)<n:rows.append(sample(s.get('items',{})))
        if s.get('uniqueItems'):
            for i,v in enumerate(rows):
                if isinstance(v,str):rows[i]=v+str(i)
                elif isinstance(v,(int,float)):rows[i]=v+i
        return rows
    if typ in ('number','integer'):return max(s.get('minimum',1),s.get('exclusiveMinimum',0)+1)
    if typ=='boolean':return False
    if typ=='null':return None
    return 'outputs/SYNTHETIC_NOT_A_CALCULATION.log' if 'pattern' in s else SYN

def fixture(contract,doc,report=True):
    with tempfile.TemporaryDirectory(prefix='format_only_',dir=TMP) as td:
        t=Path(td);(t/'report').mkdir()
        (t/'report/results.json').write_text(json.dumps(doc))
        if report:(t/'report/report.md').write_text(SYN+'\n')
        # Only transport-format files are needed by the official format validator.
        # It does not check nested evidence or execute scientific evaluator rules.
        return validate_output_contract(t,json.dumps(contract).encode())

def accept(pid,name,c,d):
    r=fixture(c,d);check(pid+':'+name,r['valid'],r['errors'][:2])
def reject(pid,name,c,d):
    r=fixture(c,d);check(pid+':'+name,not r['valid'])
def mol(x):
    p=Chem.SmilesParserParams();p.removeHs=False
    return Chem.MolFromSmiles(x['mapped_smiles'],p)
def bymap(m):return {a.GetAtomMapNum():a for a in m.GetAtoms()}
def unmapped(m):
    m=Chem.Mol(m)
    for a in m.GetAtoms():a.SetAtomMapNum(0)
    return Chem.MolToSmiles(m)
def mapping_ok(a,b,pairs,bond_orders=True):
    aa,bb=bymap(a),bymap(b);mp=dict(pairs)
    if len(mp)!=len(pairs) or len(set(mp.values()))!=len(mp):return False
    if not all(i in aa and j in bb and aa[i].GetAtomicNum()==bb[j].GetAtomicNum() for i,j in pairs):return False
    for bo in a.GetBonds():
        i,j=bo.GetBeginAtom().GetAtomMapNum(),bo.GetEndAtom().GetAtomMapNum()
        if i in mp and j in mp:
            other=b.GetBondBetweenAtoms(bb[mp[i]].GetIdx(),bb[mp[j]].GetIdx())
            if other is None:return False
            if bond_orders and bo.GetBondType()!=other.GetBondType():return False
    return True
def quadruples_ok(m,qs):
    by=bymap(m)
    return all(len(q)==4 and len(set(q))==4 and all(x in by for x in q) and all(m.GetBondBetweenAtoms(by[a].GetIdx(),by[b].GetIdx()) is not None for a,b in zip(q,q[1:])) for q in qs)

def graph_checks(pid,public):
    species={s['id']:s for s in public['species']};ms={k:mol(s) for k,s in species.items()};co=public['controls']
    for k,s in species.items():
        m=ms[k];check(pid+':graph:'+k,m is not None)
        check(pid+':formula:'+k,rdMolDescriptors.CalcMolFormula(m)==s['formula'])
        check(pid+':charge:'+k,Chem.GetFormalCharge(m)==s['charge'])
        maps=[a.GetAtomMapNum() for a in m.GetAtoms()]
        check(pid+':unique_atom_maps:'+k,all(maps) and len(set(maps))==len(maps))
        check(pid+':electron_multiplicity_parity:'+k,(sum(a.GetAtomicNum() for a in Chem.AddHs(m).GetAtoms())-s['charge'])%2==(s['multiplicity']-1)%2)
    if pid==IDS[0]:
        for p in co['mapping']:check(pid+':unchanged_two_arm_map:'+p['from'],mapping_ok(ms[p['from']],ms[p['to']],p['atom_map_pairs']) and len(p['atom_map_pairs'])>45)
        for k,qs in co['torsion_quadruples'].items():check(pid+':four_bonded_torsions:'+k,len(qs)==4 and quadruples_ok(ms[k],qs))
        check(pid+':sigma_pi_different_composition',species['An_sigma_Ph']['formula']!=species['An_pi_Ph']['formula'])
    elif pid==IDS[1]:
        check(pid+':experimental_plot_supplied',(DEST/MODES[0]/pid/'agent_input/data/inputs/quenching_figure3.png').is_file())
    elif pid==IDS[2]:
        rim=co['matched_inner_rim']
        for k in ['5','7']:check(pid+':mapped_inner_rim:'+k,quadruples_ok(ms[k],rim[k+'_quadruples']) and len(rim[k+'_quadruples'])==5)
    elif pid==IDS[3]:
        for k in ['R','S']:
            m=ms['candidate_'+k];Chem.AssignStereochemistry(m,cleanIt=True,force=True)
            check(pid+':CIP17:'+k,bymap(m)[17].GetProp('_CIPCode')==k)
        path=DEST/MODES[0]/pid/'agent_input/data/inputs/experimental_ecd.csv'
        check(pid+':experimental_ECD_nonempty',len(path.read_text().splitlines())>80)
    elif pid==IDS[4]:
        for k in ['7a_ZHK','7a_EHK','7a_AE','7a_AK']:
            pairs=co['explicit_tautomer_atom_pairs_from_ZHK'][k]
            check(pid+':tautomer_full_heavy_map:'+k,mapping_ok(ms['7a_ZHK'],ms[k],pairs,False) and len(pairs)==ms['7a_ZHK'].GetNumAtoms())
            check(pid+':tautomer_same_formula:'+k,species[k]['formula']==species['7a_ZHK']['formula'])
        check(pid+':distinct_E_Z',unmapped(ms['7a_ZHK'])!=unmapped(ms['7a_EHK']))
    elif pid==IDS[5]:
        check(pid+':regio_equal_formula',species['CN1_n2']['formula']==species['CN1_n2_regio']['formula'])
        check(pid+':regio_nonisomorphic',unmapped(ms['CN1_n2'])!=unmapped(ms['CN1_n2_regio']))
        p=co['explicit_regio_map'];check(pid+':ring_mapping',mapping_ok(ms[p['from']],ms[p['to']],p['atom_map_pairs']))
        for k,qs in co['matched_torsion_quadruples'].items():check(pid+':regio_torsion_graph:'+k,quadruples_ok(ms[k],qs))
    elif pid==IDS[6]:
        check(pid+':full_triflate_68atoms',Chem.AddHs(ms['2']).GetNumAtoms()==68 and species['2']['formula']=='C18H14B2F12N6O12S4')
        for k,pairs in co['common_core_atom_pairs_from_2'].items():check(pid+':common_B2N6_core:'+k,mapping_ok(ms['2'],ms[k],pairs))
    elif pid==IDS[7]:check(pid+':ten_source_AZ_objects',len(species)==10 and set(species)=={'AZ'+str(i) for i in range(1,11)})
    elif pid==IDS[8]:
        check(pid+':full_neutral_Cbz',species['DBC_Cbz']['formula']=='C38H24N2')
        for k,qs in co['common_torsion_quadruples'].items():check(pid+':DBC_torsion_graph:'+k,quadruples_ok(ms[k],qs))
    elif pid==IDS[9]:check(pid+':dyes_not_positional_isomers',species['dye3']['formula']!=species['dye4']['formula'])
    elif pid==IDS[10]:check(pid+':two_neutral_sulfonamides',all(x['charge']==0 and x['multiplicity']==1 for x in species.values()))
    elif pid==IDS[11]:
        check(pid+':full_mono_formula',species['mono_R']['formula']=='C40H22Cl4N2O4')
        check(pid+':full_di_formula',species['di_R']['formula']=='C80H42Cl4N4O8' and Chem.AddHs(ms['di_R']).GetNumAtoms()==138)
        for k in ['mono_R','mono_S','di_R','di_S']:
            m=ms[k];Chem.AssignStereochemistry(m,cleanIt=True,force=True)
            labels=[a.GetProp('_CIPCode') for a in m.GetAtoms() if a.HasProp('_CIPCode')]
            check(pid+':explicit_sidechain_CIP:'+k,len(labels)==(2 if k.startswith('mono') else 4) and set(labels)=={k[-1]})


def scientific_format_tests(pid,c,pos):
    # Explicit paper-specific matrix omissions and incorrect references.
    data=deepcopy(pos)
    for panel,val in pos['results'].items():
        if isinstance(val,dict) and val:
            data=deepcopy(pos);key=next(iter(val));del data['results'][panel][key]
            reject(pid,'missing_matrix_member:'+panel+'/'+key,c,data)
    data=deepcopy(pos)
    if pid==IDS[0]:data['results']['difference_of_effects']['Ph']['observable']='absolute_total_reaction_energy'
    elif pid==IDS[1]:data['results']['excited_ET']['1a']['reference']='arbitrary_electrode_fit'
    elif pid==IDS[2]:data['results']['static_series']['5']['frequency_au']=0.01
    elif pid==IDS[3]:data['results']['configuration_discrimination']['supported_configurations']=[]
    elif pid==IDS[4]:del data['results']['species_crosscheck']['7a_AE']
    elif pid==IDS[5]:del data['results']['regiochemical_control']['CN1_n2_regio']
    elif pid==IDS[6]:del data['results']['common_core']['3']
    elif pid==IDS[7]:data['results']['out_of_fold']['AZ1']['training_ids'][0]='AZ1'
    elif pid==IDS[8]:del data['results']['relaxation_cycles']['DBC_Cbz']
    elif pid==IDS[9]:del data['results']['micro_solvation']['dye4']
    elif pid==IDS[10]:del data['results']['interventions']['SNaft']
    else:del data['results']['spectral_series']['mono_R']
    reject(pid,'paper_specific_wrong_or_missing_axis',c,data)
    if pid==IDS[1]:
        d=deepcopy(pos);r=d['results']['quenching_challenge'];r['lifetime_evidence_kind']='qualitative_only';r['lifetime_change_fraction']=None;r.pop('lifetime_change_upper_bound_fraction',None)
        accept(pid,'source_supported_qualitative_lifetime',c,d)
        r['lifetime_change_fraction']=0.00001;reject(pid,'invented_quantitative_qualitative_lifetime',c,d)
        d=deepcopy(pos);d['results']['quenching_challenge'].pop('lifetime_change_upper_bound_fraction');reject(pid,'quantitative_lifetime_without_bound',c,d)
    if pid==IDS[2]:
        d=deepcopy(pos);d['results']['static_series']['1']['beta_au']=[1.0];reject(pid,'single_component_not_HRS_tensor',c,d)
    if pid==IDS[7]:
        d=deepcopy(pos);d['results']['out_of_fold']['AZ1']['heldout_id']='AZ2';reject(pid,'duplicated_heldout_member',c,d)
        d=deepcopy(pos);d['results']['null_and_resolution']['n_permutations']=0;reject(pid,'missing_label_permutation',c,d)
    if pid==IDS[4]:
        d=deepcopy(pos);d['results']['species_crosscheck']['7a_AE']['IR']['carbonyl_mode']={'present':False,'frequency_cm_inverse':None,'absence_reason':SYN}
        accept(pid,'absent_carbonyl_not_invented_peak',c,d)
        d['results']['species_crosscheck']['7a_AE']['IR']['carbonyl_mode']['frequency_cm_inverse']=1700;reject(pid,'absent_mode_with_fabricated_frequency',c,d)
    def first_collapse(s,path=()):
        if isinstance(s,dict):
            if 'oneOf' in s and any(x.get('properties',{}).get('outcome',{}).get('const')=='collapsed_to_other_basin' for x in s['oneOf']):return path,s['oneOf'][1]
            for k,v in s.get('properties',{}).items():
                found=first_collapse(v,path+(k,))
                if found:return found
        return None
    collapse=first_collapse(c['result_schema']['properties']['results'],('results',))
    if collapse:
        path,cs=collapse;d=deepcopy(pos);v=d
        for k in path[:-1]:v=v[k]
        v[path[-1]]=sample(cs);accept(pid,'evidenced_collapse_branch',c,d)
        v[path[-1]].pop('trajectory_evidence');reject(pid,'collapse_without_trajectory',c,d)

def main():
    # Exact requested runtime constructor, no fallback/private discovery bypass.
    repo=TaskRepository(roots=[Path('tasks/upgrade_tasks')])
    check('development_repository_all_batch2_pairs_found',all(repo.get(paper_id=p,task_type=m) for p in IDS for m in MODES))
    for pid in IDS:
        ar=DEST/MODES[0]/pid;pr=DEST/MODES[1]/pid
        pub={str(p.relative_to(ar/'agent_input')):p.read_bytes() for p in (ar/'agent_input').rglob('*') if p.is_file()}
        check(pid+':mode_public_file_set',set(pub)=={str(p.relative_to(pr/'agent_input')) for p in (pr/'agent_input').rglob('*') if p.is_file()})
        for name,content in pub.items():
            if name!='task.md':check(pid+':mode_public_parity:'+name,content==(pr/'agent_input'/name).read_bytes())
        for name in FIVE:check(pid+':mode_evaluator_parity:'+name,(ar/'evaluation'/name).read_bytes()==(pr/'evaluation'/name).read_bytes())
        a=(ar/'agent_input/task.md').read_text();p=(pr/'agent_input/task.md').read_text()
        check(pid+':author_route_only_PR','# Author-provided scientific guidance' not in a and '# Author-provided scientific guidance' in p)
        stripped=re.sub(r'\n# Author-provided scientific guidance\n\n.*?(?=\n# Public inputs)','',p,flags=re.S)
        check(pid+':science_instructions_equal',a==stripped)
        check(pid+':scientific_English',not re.search('[\u4e00-\u9fff]',a+p))
        for heading in ['Scientific objective','Public inputs and scientific boundaries','Required scientific validation/investigation','Deliverables']:check(pid+':original_heading:'+heading,'# '+heading in a)
        contract=read(ar/'agent_input/submission_schema.json');schema=contract['result_schema']
        jsonschema.Draft202012Validator.check_schema(schema);check(pid+':valid_Draft202012_schema',True)
        positive=sample(schema);accept(pid,'synthetic_complete_format',contract,positive)
        for verdict in ['supported','refuted','indistinguishable']:
            d=deepcopy(positive);d['conclusion']['verdict']=verdict;accept(pid,'symmetric_verdict:'+verdict,contract,d)
        reject(pid,'old_scalar_only',contract,{'status':'complete','value':1.23})
        for panel in positive['results']:
            d=deepcopy(positive);del d['results'][panel];reject(pid,'missing_core_panel:'+panel,contract,d)
        for key,val in [('charge',17),('multiplicity',9),('system','unknown_molecule')]:
            d=deepcopy(positive);d['calculation_records'][0][key]=val;reject(pid,'incorrect_'+key,contract,d)
        for path in ['outputs/../private','analysis/../../private','structures/a/../private','./outputs/../private','../outputs/private','/tmp/output','evaluation/answer','outputs//private']:
            d=deepcopy(positive);d['evidence_files']=[path];reject(pid,'invalid_evidence_path:'+path,contract,d)
        for path in ['outputs/./SAFE_SYNTHETIC.log','./outputs/SAFE_SYNTHETIC.log']:
            d=deepcopy(positive);d['evidence_files']=[path];accept(pid,'benign_dot_segment:'+path,contract,d)
        d=deepcopy(positive);d['conclusion']['verdict']='not_established';reject(pid,'incomplete_claim_not_complete',contract,d)
        d=deepcopy(positive);d['calculation_records']=[];reject(pid,'no_calculations_not_complete',contract,d)
        d=deepcopy(positive)
        for r in d['calculation_records']:r['kind']='failed';r['failure_reason']=SYN
        reject(pid,'all_failed_not_complete',contract,d)
        check(pid+':readable_report_required',not fixture(contract,positive,False)['valid'])
        d=deepcopy(positive);d['calculation_records'].append({'calculation_id':'SYNTHETIC_ANALYSIS','system':positive['calculation_records'][0]['system'],'record_type':'analysis','kind':'completed','method':SYN,'environment':SYN,'input_file':'analysis/SYNTHETIC.py','output_file':'analysis/SYNTHETIC.csv','convergence':SYN,'analysis_type':SYN,'source_evidence_files':['outputs/SYNTHETIC.log']})
        accept(pid,'analysis_without_fake_geometry_or_Hartree',contract,d)
        d['calculation_records']=d['calculation_records'][1:];reject(pid,'analysis_only_not_expanded_completion',contract,d)
        fail=deepcopy(positive);fail['status']='bounded_failure';fail['conclusion']['verdict']='not_established';fail['resources']['engine_calls']=0;fail['calculation_records']=[]
        for k in ['results','hypotheses','sensitivity']:fail.pop(k,None)
        fail['failure_report']=sample(schema['properties']['failure_report'])
        accept(pid,'zero_launch_bounded_failure',contract,fail)
        fail['status']='blocked';accept(pid,'zero_launch_blocked',contract,fail)
        bad=deepcopy(fail);bad.pop('failure_report');reject(pid,'failure_requires_diagnostics',contract,bad)
        bad=deepcopy(fail);bad['conclusion']['verdict']='supported';reject(pid,'failure_cannot_claim_support',contract,bad)
        bad=deepcopy(fail);bad['resources']['engine_calls']=5;reject(pid,'empty_records_cannot_claim_engine_work',contract,bad)
        scientific_format_tests(pid,contract,positive)
        graph_checks(pid,read(ar/'agent_input/data/inputs/research_matrix.json'))
        for mode in MODES:
            package=DEST/mode/pid;prefix=pid+':'+mode+':'
            for f in package.rglob('*.json'):read(f)
            check(prefix+'JSON_payload_parse',True)
            v=validate_task_package(package);check(prefix+'official_package_validation',v.status=='passed',v.findings)
            runtime=load_runtime_evaluation(paper_id=pid,task_type=mode,repository=repo)
            check(prefix+'runtime_flat_adapter',runtime.adapter_id=='split-computational-evaluator.v3-flat')
            check(prefix+'scientific_weights_100',sum(r['max_score'] for r in runtime.ground_truth['scientific_conclusion_rubric'])==100)
            with tempfile.TemporaryDirectory(prefix='public_export_',dir=TMP) as td:
                materialize_agent_files(paper_id=pid,task_type=mode,destination=td,repository=repo)
                actual={str(p.relative_to(td)) for p in Path(td).rglob('*') if p.is_file()}
                check(prefix+'export_only_agent_input',actual==set(pub))
                check(prefix+'no_evaluator_snapshot_or_PDF_export',not any('evaluation' in p or '.snapshot' in p or p.endswith(('.pdf','.xyz','.cif')) for p in actual))
            audit=read(package/'evaluation/task_provenance/upgrade_audit.json');source=ROOT/audit['source']
            for rel,record in audit['source_payload_snapshots'].items():
                check(prefix+'snapshot:'+rel,sha(package/record['snapshot'])==record['sha256'])
                check(prefix+'source_final_unchanged:'+rel,sha(source/rel)==record['sha256'])
            check(prefix+'source_manifest',sha(source/'package_manifest.json')==audit['source_manifest_sha256'])
            for source_doc in audit['source_docs']:
                check(prefix+'source_document:'+source_doc['path'],sha(ROOT/source_doc['path'])==source_doc['sha256'])
            history=audit['historical_evidence_review'];check(prefix+'history_read_hash',sha(ROOT/history['path'])==history['sha256'])
            check(prefix+'pending_expanded_references',audit['status']=='implemented_pending_expanded_reference' and audit['new_scientific_calculations_performed'] is False)
            check(prefix+'reference_plan_present',(package/'evaluation/reference_validation_plan.md').stat().st_size>1200)
            score=read(package/'evaluation/scoring_rules.json')
            check(prefix+'rules_bind_new_results_and_raw_evidence',all(r.get('binding',{}).get('fields') and r['binding'].get('artifact_paths')==['report/results.json','report/report.md'] for r in score['rules']))
            status=read(B/'paper_status'/f'{pid}.json');declared=next(x for x in status['packages'] if x['task_type']==mode)
            check(prefix+'status_hash_current',declared['package_content_sha256']==read(package/'package_manifest.json')['package_content_sha256'])
        print(pid,'package/contract/source/graph checks passed',flush=True)
    check('temporary_synthetic_fixtures_removed',not any(TMP.iterdir()))
    return {'date':'2026-09-27','finished_utc':datetime.now(timezone.utc).isoformat(),'status':'passed','paper_count':len(IDS),'package_count':len(IDS)*2,'checks':len(RESULTS),'scientific_calculations_run':0,'LLM_judge_run':False,'runtime_constructor':"TaskRepository(roots=[Path('tasks/upgrade_tasks')])",'boundary':'Official package/runtime/export tests, source hashes, chemical graph identities, and synthetic public-output-format regression only. No expanded quantum reference or scientific-score calibration is claimed. Nested artifact content/evidence sufficiency is adjudicated by the scientific evaluator, not the public format validator.','results':RESULTS}

if __name__=='__main__':
    try:r=main()
    except Exception as e:
        r={'status':'failed','error':repr(e),'checks':len(RESULTS),'results':RESULTS}
        (B/'validation_report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({k:v for k,v in r.items() if k!='results'},ensure_ascii=False));raise
    (B/'validation_report.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k!='results'},ensure_ascii=False))
