"""Offline regression. Every generated fixture is SYNTHETIC, NOT SCIENTIFIC DATA.
Only this batch's six packages are asserted; concurrent batches may also exist.
"""
from pathlib import Path
import sys,json,copy,tempfile,re,hashlib,collections
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
import jsonschema
from evaluation.contracts.task_package import validate_task_package,EVALUATION_FILES
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract
BATCH=Path(__file__).resolve().parent;DEST=ROOT/'tasks/upgrade_tasks'
IDS=['paper_5ea491c741fbd8d4','paper_72f60526b64ce1b6','paper_c7217910ecbee1d9'];MODES=['autonomous_research','paper_reproduction']
R=[]
def check(name,ok,detail=None):
 R.append({'test':name,'passed':bool(ok),**({'detail':detail} if detail else {})})
 if not ok:raise AssertionError((name,detail))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def merge(a,b):
 a=copy.deepcopy(a)
 for k,v in b.items():
  if k=='required':a[k]=list(dict.fromkeys(a.get(k,[])+v))
  elif isinstance(v,dict) and isinstance(a.get(k),dict):a[k]=merge(a[k],v)
  else:a[k]=copy.deepcopy(v)
 return a

def sample(s):
 s=copy.deepcopy(s)
 if 'const' in s:return s['const']
 if 'enum' in s:return s['enum'][0]
 if 'oneOf' in s:s=merge(s,s.pop('oneOf')[0])
 typ=s.get('type','object' if 'properties' in s else 'string')
 if isinstance(typ,list):typ=next(x for x in typ if x!='null')
 if typ=='object':
  d={k:sample(s['properties'][k]) for k in s.get('required',[])}
  extra={}
  for c in s.get('allOf',[]):
   if 'if' in c and jsonschema.Draft202012Validator(c['if']).is_valid(d):extra=merge(extra,c.get('then',{}))
  if extra:
   s.pop('allOf',None);return sample(merge(s,extra))
  return d
 if typ=='array':
  cs=[x['contains'] for x in s.get('allOf',[]) if 'contains' in x]
  if 'contains' in s:cs.append(s['contains'])
  d=[sample(merge(s.get('items',{}),c)) for c in cs]
  while len(d)<s.get('minItems',0):d.append(sample(s.get('items',{})))
  return d
 if typ=='boolean':return True
 if typ=='null':return None
 if typ in ['number','integer']:return min(s.get('maximum',1),max(s.get('minimum',0),1))
 if s.get('pattern')=='^[0-9a-f]{64}$':return '0'*64
 if s.get('pattern'):return 'outputs/SYNTHETIC_NOT_SCIENTIFIC_DATA.txt'
 return 'SYNTHETIC CONTRACT TEST ONLY; NOT SCIENTIFIC EVIDENCE'

def validate_fixture(c,d,report=True):
 with tempfile.TemporaryDirectory(prefix='rcb_batch6_SYNTHETIC_ONLY_') as td:
  t=Path(td);(t/'report').mkdir();(t/'report/results.json').write_text(json.dumps(d))
  if report:(t/'report/report.md').write_text('SYNTHETIC FORMAT TEST ONLY; no scientific calculation or reference value.\n')
  return validate_output_contract(t,json.dumps(c).encode())

def positive(c):
 d=sample(c['result_schema']);d['status']='complete';return d

def failure(c):
 d=positive(c);d['status']='bounded_failure'
 for k in ['methods','results','hypotheses','sensitivity']:d.pop(k,None)
 for g in d['prerequisite_checks']:g['status']='open'
 d['calculation_records']=[];d['artifact_index']=[]
 d['conclusion']['outcome']='incomplete';d['conclusion']['comparison_ids']=[]
 d['resource_record']={k:0 for k in ['engine_launches','failed_launches','allocated_core_hours','engine_wall_hours_sum','elapsed_wall_hours']};d['resource_record']['measurement_basis']='SYNTHETIC PRECOMPUTATION FAILURE FORMAT TEST'
 d['failure_report']={'attempted_scope':'SYNTHETIC prerequisite audit','observed_failure':'SYNTHETIC missing prerequisite','missing_endpoints':['entire expanded matrix'],'release_conditions':['Supply verified prerequisite and execute pilot'],'diagnostic_files':['outputs/SYNTHETIC_DIAGNOSTIC.txt']}
 return d

def reject(c,d,name):
 r=validate_fixture(c,d);check(name,not r['valid'])

def main():
 # Scope discovery before validating; other authors may be writing peers.
 repository_note={'requested_roots':['tasks/upgrade_tasks'],'scoped_official_discovery':'assigned six packages; ordinary validators preserved'}
 repo=TaskRepository.__new__(TaskRepository)
 repo.roots=(DEST,)
 repo._approved_final_directories=tuple(DEST/m/pid for pid in IDS for m in MODES)
 repo._index=repo._build_index()
 check('exact_batch6_runtime_scope',all(repo.get(paper_id=pid,task_type=m) for pid in IDS for m in MODES))
 for pid in IDS:
  a=DEST/MODES[0]/pid;p=DEST/MODES[1]/pid
  aa={f.relative_to(a/'agent_input').as_posix():f.read_bytes() for f in (a/'agent_input').rglob('*') if f.is_file()}
  pp={f.relative_to(p/'agent_input').as_posix():f.read_bytes() for f in (p/'agent_input').rglob('*') if f.is_file()}
  check(pid+':public_file_set_parity',set(aa)==set(pp))
  for rel in aa:
   if rel!='task.md':check(pid+':public_bytes_parity:'+rel,aa[rel]==pp[rel])
  at=aa['task.md'].decode();pt=pp['task.md'].decode()
  stripped=re.sub(r'# Author-provided scientific guidance\n\n.*?(?=# Public inputs and scientific boundaries)', '',pt,flags=re.S)
  check(pid+':task_science_parity',stripped==at)
  check(pid+':only_PR_author_guidance','# Author-provided scientific guidance' not in at and '# Author-provided scientific guidance' in pt)
  for name in EVALUATION_FILES:check(pid+':evaluator_parity:'+name,(a/'evaluation'/name).read_bytes()==(p/'evaluation'/name).read_bytes())
  c=json.loads(aa['submission_schema.json']);s=c['result_schema'];jsonschema.Draft202012Validator.check_schema(s)
  check(pid+':draft202012_schema_valid',True)
  d=positive(c);rr=validate_fixture(c,d);check(pid+':synthetic_complete_contract',rr['valid'],rr['errors'][:4])
  for outcome in ['refuted','indistinguishable']:
   t=copy.deepcopy(d);t['conclusion']['outcome']=outcome
   for h in t['hypotheses']:h['outcome']=outcome
   check(pid+':synthetic_'+outcome+'_contract',validate_fixture(c,t)['valid'])
  f=failure(c);rr=validate_fixture(c,f);check(pid+':early_honest_failure_contract',rr['valid'],rr['errors'][:4])
  f['status']='partial';check(pid+':honest_partial_contract',validate_fixture(c,f)['valid'])
  f.pop('failure_report');reject(c,f,pid+':failure_without_diagnostics_rejected')
  for name in d['results']:
   t=copy.deepcopy(d);t['results'].pop(name);reject(c,t,pid+':missing_panel:'+name)
  for field,value in [('charge',12),('multiplicity',8)]:
   t=copy.deepcopy(d);t['calculation_records'][0][field]=value;reject(c,t,pid+':wrong_'+field)
  t=copy.deepcopy(d)
  for g in t['prerequisite_checks']:g['status']='open'
  reject(c,t,pid+':open_gate_cannot_complete')
  t=copy.deepcopy(d)
  for j in t['calculation_records']:j['status']='failed'
  reject(c,t,pid+':all_jobs_failed_cannot_complete')
  for gate in range(len(d['prerequisite_checks'])):
   t=copy.deepcopy(d);t['prerequisite_checks'].pop(gate);reject(c,t,pid+':missing_gate:'+str(gate))
  for path in ['outputs/../secret','evaluation/reference.json','/tmp/answer','outputs//bad','outputs/a/../../bad','outputs/../evaluation/reference_key_points.json']:
   t=copy.deepcopy(d);t['calculation_records'][0]['log_file']=path;reject(c,t,pid+':unsafe_path:'+path)
  t=copy.deepcopy(d);t['artifact_index']=[];reject(c,t,pid+':complete_without_artifact_index')
  t=copy.deepcopy(d);t['resource_record']['engine_launches']=0;reject(c,t,pid+':complete_without_engine_launch')
  check(pid+':missing_report_rejected',not validate_fixture(c,d,False)['valid'])
  for old in [{'status':'complete','gap_eV':3.6191},{'status':'complete','dipole_magnitude_debye':2.67},{'status':'complete','aea':{'value':3.93}}]:reject(c,old,pid+':old_scalar_rejected:'+next(k for k in old if k!='status'))
  if pid==IDS[0]:
   t=copy.deepcopy(d);t['results']['crystal']['deposit']='CCDC 2512981';reject(c,t,pid+':wrong_crystal_deposit')
   t=copy.deepcopy(d);t['results']['neighbors'][0].pop('E_A_ghost_Eh');reject(c,t,pid+':missing_CP_fragment')
   t=copy.deepcopy(d);t['results']['cutoff_control']['expanded_offset_A']=0.5;reject(c,t,pid+':no_cutoff_perturbation')
  elif pid==IDS[1]:
   for name in ['AD_reversed','AD_left_gap_plus_0p2A','ApiD_base','AsigmaD_base']:
    t=copy.deepcopy(d);t['results']['devices'].pop(name);reject(c,t,pid+':missing_required_device:'+name)
   for bias in [-.5,0.,.5]:
    t=copy.deepcopy(d);rows=t['results']['devices']['AD_base']['bias_points'];t['results']['devices']['AD_base']['bias_points']=[x for x in rows if x['bias_V']!=bias];reject(c,t,pid+':missing_bias:'+str(bias))
   t=copy.deepcopy(d);rows=t['results']['devices']['AD_base']['bias_points'];rows[2]=copy.deepcopy(rows[0]);reject(c,t,pid+':duplicate_bias_cannot_cover_sign')
   t=copy.deepcopy(d);t['results']['devices']['AD_base']['rectification']['definition']='abs(I(-0.5V))/abs(I(+0.5V))';reject(c,t,pid+':wrong_rectification_reference')
   t=copy.deepcopy(d);t['results']['isolated']['AD']['formula']='C10H6N2S2';reject(c,t,pid+':wrong_isolated_stoichiometry')
   t=copy.deepcopy(d);t['results']['devices']['AD_base']['bias_points'][0]['self_consistent']=False;reject(c,t,pid+':nonselfconsistent_current')
  else:
   for n in ['n0','n1','n2']:
    t=copy.deepcopy(d);t['results']['series'].pop(n);reject(c,t,pid+':missing_ligand_member:'+n)
   t=copy.deepcopy(d);t['results']['series']['n1'].pop('fixed_core');reject(c,t,pid+':missing_frozen_core_control')
   t=copy.deepcopy(d);t['results']['series']['n2']['neutral']['multiplicity']=1;reject(c,t,pid+':wrong_electron_parity')
   t=copy.deepcopy(d);t['results']['series']['n2']['neutral']['core_retained']=False;reject(c,t,pid+':reconstruction_claimed_intact')
   t=copy.deepcopy(d);t['results']['series']['n1']['fixed_core']['geometry_reference']='each_own_relaxed_core';reject(c,t,pid+':wrong_common_core_reference')
   t=copy.deepcopy(d);t['results']['series']['n2']['neutral']['imaginary_internal_modes_cm1']=[-50.];reject(c,t,pid+':imaginary_minimum_rejected')
   t=copy.deepcopy(d);ex=s['properties']['results']['properties']['series']['properties']['n2']['oneOf'][1];t['results']['series']['n2']=sample(ex)
   cp=t['results']['comparisons']['n2_minus_n1'];cp['outcome']='blocked_by_evidenced_exclusion'
   for key in ['delta_AEA_eV','delta_VEA_eV','delta_fixed_core_attachment_eV','uncertainty_eV']:cp[key]=None
   reject(c,t,pid+':missing_original_intact_endpoint_cannot_complete')
   t['status']='partial';t['conclusion']['outcome']='incomplete';t['failure_report']=failure(c)['failure_report']
   check(pid+':evidenced_exclusion_partial_format',validate_fixture(c,t)['valid'])
   t['results']['series']['n2']['excluded_AEA']=7.731;reject(c,t,pid+':excluded_aggregate_AEA_rejected')
   t=copy.deepcopy(d);t['results']['candidates'][0]['status']='collapsed'
   check(pid+':candidate_collapse_with_retained_endpoints_format',validate_fixture(c,t)['valid'])
  for mode in MODES:
   q=DEST/mode/pid;v=validate_task_package(q);check(pid+':'+mode+':official_package',v.status=='passed',v.findings)
   runtime=load_runtime_evaluation(paper_id=pid,task_type=mode,repository=repo)
   check(pid+':'+mode+':runtime_loaded',runtime.adapter_id=='split-computational-evaluator.v3-flat')
   check(pid+':'+mode+':weight100',sum(x['max_score'] for x in runtime.ground_truth['scientific_conclusion_rubric'])==100)
   for jf in q.rglob('*.json'):
    if 'legacy_final_snapshot' in str(jf):continue
    json.load(open(jf))
   check(pid+':'+mode+':all_JSON_valid',True)
   audit=json.load(open(q/'evaluation/task_provenance/upgrade_audit.json'));src=ROOT/audit['source_path']
   check(pid+':'+mode+':blocked_state',audit['status']==('implemented_pending_expanded_reference' if pid==IDS[2] else 'blocked') and not audit['release_ready'] and not audit['new_scientific_calculations_performed'])
   snapshot_files=audit['source_payload_snapshots']
   check(pid+':'+mode+':all_source_files_snapshotted',set(snapshot_files)=={f.relative_to(src).as_posix() for f in src.rglob('*') if f.is_file()})
   for rel,r in snapshot_files.items():
    check(pid+':'+mode+':source_snapshot:'+rel,sha(src/rel)==r['sha256']==sha(q/r['snapshot']))
   for record in audit['source_documents']+audit['source_guidance_documents']:check(pid+':'+mode+':source_unchanged:'+record['path'],sha(ROOT/record['path'])==record['sha256'])
   with tempfile.TemporaryDirectory(prefix='rcb_batch6_PUBLIC_export_') as td:
    paths=materialize_agent_files(paper_id=pid,task_type=mode,destination=td,repository=repo)
    files=[x.relative_to(td).as_posix() for x in Path(td).rglob('*') if x.is_file()]
    check(pid+':'+mode+':public_export_only_agent',set(files)==set(aa))
    check(pid+':'+mode+':no_private_export',all('evaluation' not in x and 'snapshot' not in x and 'paper_route' not in x for x in files))
   pub='\n'.join(x.read_text() for x in (q/'agent_input').rglob('*') if x.is_file())
   check(pid+':'+mode+':no_old_numeric_target',not any(n in pub for n in ['3.6191','2.497077','2.67 Debye','3.93 eV','7.731']))
  check(pid+':no_author_optimized_xyz_public',not list((a/'agent_input').rglob('*.xyz')))
 # Local chemical identity checks, not quantum results.
 from rdkit import Chem
 from rdkit.Chem import rdMolDescriptors
 for pid,filename,key in [(IDS[0],'system.json',None),(IDS[1],'systems.json','systems')]:
  data=json.load(open(DEST/MODES[0]/pid/'agent_input/data/inputs'/filename));rows=data[key] if key else [data]
  for row in rows:
   m=Chem.MolFromSmiles(row['mapped_smiles']);check(pid+':graph_formula:'+row.get('id','1a'),rdMolDescriptors.CalcMolFormula(m)==row.get('formula_isolated',row.get('formula')))
   check(pid+':unique_atom_maps:'+row.get('id','1a'),len({a['map'] for a in row['atoms']})==len(row['atoms']))
   if pid==IDS[1]:check(pid+':source_H_removal:'+row['id'],row['removed_thiol_H_maps_in_junction']==[21,22])
 p=json.load(open(DEST/MODES[0]/IDS[2]/'agent_input/data/inputs/system_specification.json'))
 for lig in p['ligands']:
  check('cluster:'+lig['id']+':composition',collections.Counter(a['element'] for a in lig['atoms'])=={'B':1,'C':18,'F':15})
  check('cluster:'+lig['id']+':bond_count',len(lig['bonds'])==36)
 for s in p['systems']:check('cluster:'+s['id']+':identity_atom_count',len(s['atom_maps'])==s['atom_count']==13+34*s['ligand_count'])
 return {'date':'2026-09-27','status':'passed','batch':6,'papers':3,'packages':6,'checks':len(R),'new_scientific_engine_launches':0,'LLM_scientific_judge_run':False,'release_ready_papers':0,'blocked_papers':IDS[:2],'historical_n2_recovered_expanded_reference_pending':[IDS[2]],'boundary':'Official package/runtime/materialization, source hashes, local graphs and SYNTHETIC output-contract regression only; not a scientific reference or calibrated pass.','repository':repository_note,'results':R}
if __name__=='__main__':
 try:report=main()
 except Exception as exc:report={'date':'2026-09-27','status':'failed','error':repr(exc),'results':R}
 (BATCH/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k!='results'},ensure_ascii=False,indent=2))
 if report['status']!='passed':sys.exit(1)
