"""Batch5 official package/runtime/output-contract checks. All fixtures are synthetic format tests, never science results."""
from pathlib import Path
from copy import deepcopy
import json,sys,re,tempfile,hashlib
B=Path(__file__).resolve().parent;ROOT=B.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(B))
from build_batch import IDS,MODES,DEST,dump,sha
from paper_specs import SPECS
import jsonschema
from evaluation.contracts.task_package import validate_task_package
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract
RESULTS=[]
def check(name,ok,detail=None):
 RESULTS.append({'test':name,'passed':bool(ok),**({'detail':str(detail)[:2500]} if detail else {})})
 if not ok:raise AssertionError((name,detail))
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
 if isinstance(typ,list):typ=next(t for t in typ if t!='null')
 if typ=='object':
  v={k:sample(s.get('properties',{}).get(k,{})) for k in s.get('required',[])}
  rules=s.get('allOf',[]);base=deepcopy(s);base.pop('allOf',None)
  for _ in range(12):
   additions={}
   for rule in rules:
    if 'if' in rule:additions=merge(additions,rule.get('then' if jsonschema.Draft202012Validator(rule['if']).is_valid(v) else 'else',{}))
   if not additions:return v
   nv=sample(merge(base,additions))
   if nv==v:return v
   v=nv
  raise AssertionError('Synthetic sampler did not reach stable conditional branch')
 if typ=='array':
  contains=[a['contains'] for a in s.get('allOf',[]) if 'contains' in a]
  if 'contains' in s:contains.append(s['contains'])
  a=[sample(merge(s.get('items',{}),c)) for c in contains]
  while len(a)<s.get('minItems',0):a.append(sample(s.get('items',{})))
  return a
 if typ in ['integer','number']:return max(s.get('minimum',1),s.get('exclusiveMinimum',0)+1)
 if typ=='boolean':return False
 if typ=='null':return None
 return 'outputs/SYNTHETIC_NOT_A_CALCULATION.log' if 'pattern' in s else 'SYNTHETIC FORMAT ONLY; NOT SCIENTIFIC EVIDENCE'
def fixture(contract,value,report=True):
 with tempfile.TemporaryDirectory(prefix='rcb_batch5_SYNTHETIC_') as td:
  t=Path(td);(t/'report').mkdir();(t/'report/results.json').write_text(json.dumps(value))
  if report:(t/'report/report.md').write_text('Synthetic contract fixture only. No real scientific evidence or validated numerical prediction.\n')
  return validate_output_contract(t,json.dumps(contract).encode())

def load_repo():
 # Required actual constructor is always attempted; other batches can be mid-write.
 try:return TaskRepository(roots=[Path('tasks/upgrade_tasks')]),'full_upgrade_root',None
 except Exception as exc:
  outside=str(exc)
  if any('/'+pid+':' in outside for pid in IDS):raise
  # Isolate candidate discovery only; run the normal public constructor and its validation.
  class Batch5Repository(TaskRepository):
   def _candidate_directories(self):return [DEST/m/p for m in MODES for p in IDS]
  repo=Batch5Repository(roots=[Path('tasks/upgrade_tasks')])
  return repo,'batch5_candidate_filter_during_concurrent_other_batch_write',outside

INNER={
'paper_0cd74ae20ab933f3':('exchange_matrix','R_OCH3'),
'paper_2c439196c2f349c9':('model_comparison','mixed'),
'paper_3316e45a74258fb7':('vertical_matrix','TD_2C'),
'paper_3d1d9b7f6df049da':('tensor_derivatives','D5h'),
'paper_72822e4ddb5d9b11':('state_matrix','BP86'),
'paper_80441aced6051d86':('coupling_controls','CB8_partner_B_no_host'),
'paper_94b0a8ae694590ea':('interface_matrix','2C8Ph-TTA'),
'paper_988bc12ae3768679':('thermodynamic_and_robustness','proton_cycles'),
'paper_a21b91f97ce3c68f':('pair_matrix','13'),
'paper_b5c446c7067dd511':('representative_controls','An-mP'),
'paper_c23cfabbd34b087f':('frozen_scaffold','2M_TIPS'),
'paper_d8e5490cd9942f4f':('conformer_hydration_matrix','Tb'),
'paper_e0791c047a731974':('rubrene_energy_cycle','rubrene_T1_record'),
'paper_e31cc7bc7b21b610':('fragment_interventions','Egan2Ir2'),
'paper_eda19e7c8edd4b39':('surface_cycles','110_mixed')}

def main():
 repo,scope,discovery_issue=load_repo()
 for pid in IDS:
  ar=DEST/MODES[0]/pid;pr=DEST/MODES[1]/pid
  af={str(p.relative_to(ar/'agent_input')):p.read_bytes() for p in (ar/'agent_input').rglob('*') if p.is_file()};pf={str(p.relative_to(pr/'agent_input')):p.read_bytes() for p in (pr/'agent_input').rglob('*') if p.is_file()}
  check(pid+':public_file_set_parity',af.keys()==pf.keys())
  for rel in af:
   if rel!='task.md':check(pid+':public_parity:'+rel,af[rel]==pf[rel])
  for name in ['reference_key_points.json','reference_conclusions.json','scoring_rules.json','critical_failures.json','evidence_map.json']:
   check(pid+':science_parity:'+name,(ar/'evaluation'/name).read_bytes()==(pr/'evaluation'/name).read_bytes())
  a=af['task.md'].decode();p=pf['task.md'].decode()
  check(pid+':PR_route_only','# Author-provided scientific guidance' not in a and '# Author-provided scientific guidance' in p)
  stripped=re.sub(r'# Author-provided scientific guidance\n.*?(?=# Public inputs)', '',p,flags=re.S)
  stripped=stripped.replace('This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls.','This is an autonomous-research task. Formulate and test the explanation independently.')
  check(pid+':instruction_parity',a==stripped)
  for heading in ['# Scientific objective','# Public inputs and scientific boundaries','# Required scientific validation/investigation','# Deliverables']:check(pid+':heading:'+heading,heading in a)
  contract=json.loads(af['submission_schema.json']);sc=contract['result_schema'];jsonschema.Draft202012Validator.check_schema(sc)
  pos=sample(sc);r=fixture(contract,pos);check(pid+':synthetic_complete_format',r['valid'],r['errors'][:4])
  for conclusion in ['refuted','indistinguishable']:
   alt=deepcopy(pos);alt['conclusion']['assessment']=conclusion
   for h in alt['hypotheses']:h['assessment']=conclusion
   check(pid+':'+conclusion+'_format_allowed',fixture(contract,alt)['valid'])
  for panel in pos['results']:
   neg=deepcopy(pos);del neg['results'][panel];check(pid+':missing_panel_rejected:'+panel,not fixture(contract,neg)['valid'])
  panel,axis=INNER[pid];neg=deepcopy(pos);del neg['results'][panel][axis];check(pid+':missing_specific_scientific_axis:'+axis,not fixture(contract,neg)['valid'])
  for f,v in [('charge',19),('multiplicity',12),('object_id','unrelated_object')]:
   neg=deepcopy(pos);neg['calculation_records'][0][f]=v;check(pid+':wrong_'+f+'_rejected',not fixture(contract,neg)['valid'])
  neg=deepcopy(pos);neg['reference_definition']='OLD_OR_INCOMPATIBLE_ENERGY_ZERO';check(pid+':wrong_observable_reference_rejected',not fixture(contract,neg)['valid'])
  neg=deepcopy(pos)
  for r in neg['calculation_records']:r['outcome']='failed'
  check(pid+':all_failed_not_complete',not fixture(contract,neg)['valid'])
  neg=deepcopy(pos);neg['results']={};neg['conclusion']['assessment']='indistinguishable';check(pid+':missing_matrix_not_indistinguishable',not fixture(contract,neg)['valid'])
  check(pid+':old_scalar_rejected',not fixture(contract,{'status':'complete','energy_difference':1.23})['valid'])
  check(pid+':missing_report_rejected',not fixture(contract,pos,False)['valid'])
  for path in ['outputs/../evaluation/reference.json','/tmp/answer','evaluation/private.json','outputs//bad.log','outputs/a/../../bad']:
   neg=deepcopy(pos);neg['evidence_files']=[path];check(pid+':unsafe_path:'+path,not fixture(contract,neg)['valid'])
  alt=deepcopy(pos);alt['evidence_files']=['./outputs/SYNTHETIC_NOT_A_CALCULATION.log'];check(pid+':safe_dot_relative_path',fixture(contract,alt)['valid'])
  neg=deepcopy(pos);neg['evidence_files']=[];check(pid+':complete_needs_evidence',not fixture(contract,neg)['valid'])
  neg=deepcopy(pos);neg['calculation_records'][0]['outcome']='collapsed';check(pid+':collapse_without_destination_rejected',not fixture(contract,neg)['valid'])
  failure={k:deepcopy(v) for k,v in pos.items() if k in ['paper_id','reference_definition','resources','evidence_files','conclusion']};failure['status']='bounded_failure';failure['conclusion']['assessment']='incomplete';failure['failure_report']=sample(sc['properties']['failure_report']);r=fixture(contract,failure);check(pid+':early_failure_reportable',r['valid'],r['errors'])
  failure['evidence_files']=[];failure['conclusion']['evidence_records']=[];failure['failure_report']['evidence_files']=[]
  for key in failure['resources']:
   if key!='measurement_basis':failure['resources'][key]=0
  failure['resources']['measurement_basis']='SYNTHETIC input-gate test: zero engine starts, no created scientific outputs.'
  check(pid+':zero_start_no_fictional_evidence_failure_allowed',fixture(contract,failure)['valid'])
  failure['conclusion']['assessment']='supported';check(pid+':failure_cannot_claim_support',not fixture(contract,failure)['valid']);failure['conclusion']['assessment']='incomplete';del failure['failure_report'];check(pid+':failure_needs_diagnostics',not fixture(contract,failure)['valid'])
  if pid=='paper_72822e4ddb5d9b11':
   collapsed=deepcopy(pos)
   for meth in ['B3LYP','BP86']:collapsed['results']['state_matrix'][meth]['broken_symmetry']=sample(sc['properties']['results']['properties']['state_matrix']['properties'][meth]['properties']['broken_symmetry']['oneOf'][1])
   check(pid+':evidenced_BS_collapse_format',fixture(contract,collapsed)['valid'])
  if pid=='paper_d8e5490cd9942f4f':
   collapsed=deepcopy(pos)
   for met in ['La','Tb','Lu']:collapsed['results']['conformer_hydration_matrix'][met]['water1']=sample(sc['properties']['results']['properties']['conformer_hydration_matrix']['properties'][met]['properties']['water1']['oneOf'][1])
   check(pid+':evidenced_water_loss_format',fixture(contract,collapsed)['valid'])
  if pid=='paper_80441aced6051d86':
   absence=deepcopy(pos)
   cells=[d for pair in absence['results']['host_matrix'].values() for d in pair.values()]+[v for k,v in absence['results']['coupling_controls'].items() if k!='placement_attempt_records']
   for d in cells:d['dark_state_id']=None;d['bright_dark_split_eV']=None;d['dark_state_search_explanation']='SYNTHETIC format branch: no selected dark state in computed window; not an actual scientific result.'
   check(pid+':no_dark_state_in_window_allowed',fixture(contract,absence)['valid'])
   neg=deepcopy(absence);neg['results']['host_matrix']['CB7_G1']['full_host']['bright_dark_split_eV']=1
   check(pid+':absent_dark_state_cannot_have_numeric_split',not fixture(contract,neg)['valid'])
   neg=deepcopy(absence);del neg['results']['host_matrix']['CB7_G1']['full_host']['dark_state_search_explanation']
   check(pid+':dark_absence_needs_explanation',not fixture(contract,neg)['valid'])
   neg=deepcopy(absence);neg['results']['host_matrix']['CB8_G1_2']['full_host']['guest_centroid_distance_angstrom']=None
   check(pid+':dimer_still_requires_interguest_geometry',not fixture(contract,neg)['valid'])
   neg=deepcopy(absence);del neg['results']['coupling_controls']['CB8_partner_B_no_host']
   check(pid+':dark_absence_does_not_waive_partner_control',not fixture(contract,neg)['valid'])
   neg=deepcopy(pos);neg['results']['coupling_controls']['free_G1']['slip_angstrom']=0
   check(pid+':monomer_uses_null_not_fictional_partner',not fixture(contract,neg)['valid'])
  for mode in MODES:
   pkg=DEST/mode/pid;v=validate_task_package(pkg);check(pid+':'+mode+':official_package_validation',v.status=='passed',v.findings)
   rt=load_runtime_evaluation(paper_id=pid,task_type=mode,repository=repo)
   check(pid+':'+mode+':runtime_adapter',rt.adapter_id=='split-computational-evaluator.v3-flat')
   check(pid+':'+mode+':weight_100',sum(x['max_score'] for x in rt.ground_truth['scientific_conclusion_rubric'])==100)
   with tempfile.TemporaryDirectory(prefix='batch5_public_materialize_') as td:
    materialize_agent_files(paper_id=pid,task_type=mode,destination=td,repository=repo)
    files={str(p.relative_to(td)) for p in Path(td).rglob('*') if p.is_file()}
    check(pid+':'+mode+':public_exact',files==af.keys())
    check(pid+':'+mode+':no_private_materialized',not any('.snapshot' in f or f.startswith('evaluation/') or f.endswith('.pdf') for f in files))
   audit=json.loads((pkg/'evaluation/task_provenance/upgrade_audit.json').read_text());src=ROOT/audit['source']
   check(pid+':'+mode+':no_science_pass_claim',audit['status'] in ['blocked','implemented_pending_expanded_reference'] and audit['new_scientific_calculations_performed'] is False)
   for rel,entry in audit['source_payload_snapshots'].items():check(pid+':'+mode+':snapshot_and_unchanged_source:'+rel,sha(pkg/entry['snapshot'])==entry['sha256']==sha(src/rel))
   for d in audit['source_docs']:check(pid+':'+mode+':source_doc_hash:'+d['path'],sha(ROOT/d['path'])==d['sha256'])
  row=json.loads((B/'paper_status'/f'{pid}.json').read_text());row['checks']['full_batch_regression']='passed';row['package_hashes']={m:json.loads((DEST/m/pid/'package_manifest.json').read_text())['package_content_sha256'] for m in MODES};dump(B/'paper_status'/f'{pid}.json',row)
 return {'date':'2026-09-27','status':'passed','checks':len(RESULTS),'papers':len(IDS),'packages':len(IDS)*2,'repository_constructor':'TaskRepository(roots=[Path("tasks/upgrade_tasks")])','repository_test_scope':scope,'concurrent_outside_batch_issue':discovery_issue,'scientific_engine_starts':0,'LLM_judge_run':False,'boundary':'Official package/runtime/public-export plus synthetic format regressions only. No newly calibrated scientific reference or upgraded scientific PASS.','results':RESULTS}
if __name__=='__main__':
 try:out=main()
 except Exception as exc:
  out={'status':'failed','error':repr(exc),'results':RESULTS};dump(B/'validation_report.json',out);print(json.dumps(out,ensure_ascii=False)[-5000:]);raise
 dump(B/'validation_report.json',out);print(json.dumps({k:v for k,v in out.items() if k!='results'},ensure_ascii=False))
