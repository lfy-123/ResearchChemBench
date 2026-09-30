"""Batch4 package and public contract regression; fixtures are never scientific evidence."""
from pathlib import Path
from copy import deepcopy
import hashlib,json,re,sys,tempfile,traceback
ROOT=Path(__file__).resolve().parents[4]; B=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
import jsonschema
from evaluation.contracts.task_package import validate_task_package,package_payload_entries,package_content_hash
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract
DEST=ROOT/'tasks/upgrade_tasks'; IDS=json.loads((B/'assignment.json').read_text())['batch']['papers'];MODES=['autonomous_research','paper_reproduction'];RESULTS=[];PACKAGE_HASHES={}
def check(n,ok,detail=None):
 RESULTS.append({'test':n,'passed':bool(ok),**({'detail':detail} if detail else {})})
 if not ok:raise AssertionError((n,detail))
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
 if typ=='object':
  value={k:sample(s.get('properties',{}).get(k,{})) for k in s.get('required',[])}
  additions={}
  for c in s.get('allOf',[]):
   if 'if' in c and jsonschema.Draft202012Validator(c['if']).is_valid(value):additions=merge(additions,c.get('then',{}))
  if additions:
   s.pop('allOf',None);return sample(merge(s,additions))
  return value
 if typ=='array':
  contains=[x['contains'] for x in s.get('allOf',[]) if 'contains' in x]
  if 'contains' in s:contains.append(s['contains'])
  rows=[sample(merge(s.get('items',{}),c)) for c in contains]
  while len(rows)<s.get('minItems',0):rows.append(sample(s.get('items',{})))
  return rows
 if typ in ['number','integer']:
  if 'exclusiveMaximum' in s:return s['exclusiveMaximum']-1
  return max(s.get('minimum',1),s.get('exclusiveMinimum',0)+1)
 if typ=='boolean':return False
 if 'pattern' in s:return 'outputs/SYNTHETIC_NOT_SCIENTIFIC.log'
 return 'SYNTHETIC FORMAT FIXTURE ONLY'
def fixture(contract,doc,report=True):
 with tempfile.TemporaryDirectory(prefix='rcb_batch4_synthetic_format_only_') as td:
  t=Path(td);(t/'report').mkdir();(t/'report/results.json').write_text(json.dumps(doc))
  if report:(t/'report/report.md').write_text('SYNTHETIC FORMAT TEST ONLY; NO SCIENTIFIC RESULT OR PASS.\n')
  return validate_output_contract(t,json.dumps(contract).encode())
def paths(value,path=()):
 if isinstance(value,dict):
  if 'outcome' in value and 'candidate_ids' in value:yield path,value
  for k,v in value.items():yield from paths(v,path+(k,))
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from paths(v,path+(i,))
def at(x,path):
 for p in path:x=x[p]
 return x
def comparisons(value,path=()):
 if isinstance(value,dict):
  if 'comparison_outcome' in value:yield path,value
  for k,v in value.items():yield from comparisons(v,path+(k,))
 elif isinstance(value,list):
  for i,v in enumerate(value):yield from comparisons(v,path+(i,))
def main():
 selected=IDS[(int(sys.argv[2])-1)*4:int(sys.argv[2])*4] if len(sys.argv)>2 and sys.argv[1]=='--shard' else IDS
 repo=TaskRepository(roots=[Path('tasks/upgrade_tasks')]);repository_mode='full_roots'
 check('32_assigned_packages_load',all(repo.get(paper_id=p,task_type=m) for p in IDS for m in MODES))
 for pid in selected:
  ar=DEST/MODES[0]/pid;pr=DEST/MODES[1]/pid
  af={str(p.relative_to(ar/'agent_input')):p.read_bytes() for p in (ar/'agent_input').rglob('*') if p.is_file()}
  pf={str(p.relative_to(pr/'agent_input')):p.read_bytes() for p in (pr/'agent_input').rglob('*') if p.is_file()}
  check(pid+':public_file_set_parity',af.keys()==pf.keys())
  for f in af:
   if f!='task.md':check(pid+':public_parity:'+f,af[f]==pf[f])
  for n in ['reference_key_points.json','reference_conclusions.json','scoring_rules.json','critical_failures.json','evidence_map.json']:
   check(pid+':scientific_evaluator_parity:'+n,(ar/'evaluation'/n).read_bytes()==(pr/'evaluation'/n).read_bytes())
  a=af['task.md'].decode();p=pf['task.md'].decode()
  check(pid+':author_guidance_only_PR','# Author-provided scientific guidance' not in a and '# Author-provided scientific guidance' in p)
  check(pid+':same_scientific_task',a==re.sub(r'# Author-provided scientific guidance\n\n.*?(?=# Public inputs)', '',p,flags=re.S))
  check(pid+':scientific_English',not re.search(r'[\u4e00-\u9fff]',a+p))
  contract=json.loads(af['submission_schema.json']);schema=contract['result_schema'];jsonschema.Draft202012Validator.check_schema(schema)
  positive=sample(schema);r=fixture(contract,positive);check(pid+':synthetic_complete_format_accepted',r['valid'],r['errors'][:3])
  for assess in ['refuted','not_distinguishable']:
   alternative=deepcopy(positive);alternative['conclusion']['assessment']=assess
   for h in alternative['hypotheses']:h['assessment']=assess
   check(pid+':'+assess+'_format_accepted',fixture(contract,alternative)['valid'])
  negative=deepcopy(positive);negative['results']={};check(pid+':empty_new_matrix_rejected',not fixture(contract,negative)['valid'])
  for panel,v in positive['results'].items():
   negative=deepcopy(positive);del negative['results'][panel];check(pid+':missing_panel_rejected:'+panel,not fixture(contract,negative)['valid'])
   # At least one paper-specific named row/mandatory field from every panel.
   negative=deepcopy(positive)
   if isinstance(v,dict):del negative['results'][panel][next(iter(v))]
   elif isinstance(v,list):negative['results'][panel]=v[:-1]
   check(pid+':missing_scientific_cell_rejected:'+panel,not fixture(contract,negative)['valid'])
  for path,_ in paths(positive):
   negative=deepcopy(positive);del at(negative,path)['endpoint_reverse_file']
   check(pid+':path_without_reverse_connection_rejected:'+'.'.join(map(str,path)),not fixture(contract,negative)['valid'])
   collapse=deepcopy(positive);cell=at(collapse,path);cell['outcome']='evidenced_collapse'
   for f in ['saddle_record_id','imaginary_frequency_cm1','mode_file','electronic_barrier_kcal_mol','gibbs_barrier_kcal_mol','preorganization_G_kcal_mol']:cell.pop(f,None)
   cell['non_saddle_evidence']={'sampled_coordinate_file':'outputs/SYNTHETIC_profile.json','endpoint_mapping_file':'outputs/SYNTHETIC_endpoints.json','stationarity_assessment':'SYNTHETIC ONLY','scope_of_exclusion':'SYNTHETIC ONLY'}
   check(pid+':collapse_format_accepted:'+'.'.join(map(str,path)),fixture(contract,collapse)['valid'])
   cell.pop('non_saddle_evidence');check(pid+':unevidenced_collapse_rejected:'+'.'.join(map(str,path)),not fixture(contract,collapse)['valid'])
  for path,_ in comparisons(positive):
   collapse=deepcopy(positive);cell=at(collapse,path);cell['comparison_outcome']='same_basin_after_evidenced_collapse'
   for k in ['left_value','right_value','right_minus_left','unit']:cell.pop(k,None)
   cell['collapse_identity']={'independent_search_records':['SYNTHETIC A','SYNTHETIC B'],'retained_basin_record_ids':['SYNTHETIC ONLY'],'mapped_structure_comparison_file':'outputs/SYNTHETIC_map.json','complete_search_profiles_file':'outputs/SYNTHETIC_profile.json','convergence_and_stationarity_file':'outputs/SYNTHETIC_stationarity.log','no_missing_core_control':True}
   check(pid+':same_basin_comparison_format_accepted:'+'.'.join(map(str,path)),fixture(contract,collapse)['valid'])
   cell.pop('collapse_identity');check(pid+':unevidenced_same_basin_rejected:'+'.'.join(map(str,path)),not fixture(contract,collapse)['valid'])
  if pid=='paper_0dc85595cab7bc0a':
   excluded=deepcopy(positive);cell=excluded['results']['candidate_layers']['first_closure'][0]
   cell['outcome']='excluded_with_evidence'
   for k in ['relative_G_kcal_mol','same_composition_reference']:cell.pop(k,None)
   cell['exclusion_or_collapse']={'reason':'SYNTHETIC FORMAT ONLY','search_and_geometry_trace_file':'outputs/SYNTHETIC_trace.log','mapped_outcome_file':'outputs/SYNTHETIC_map.json','surviving_candidate_id':'SYNTHETIC ONLY'}
   check(pid+':evidenced_exclusion_without_fake_energy_accepted',fixture(contract,excluded)['valid'])
   cell.pop('exclusion_or_collapse');check(pid+':unevidenced_candidate_exclusion_rejected',not fixture(contract,excluded)['valid'])
  for f,v in [('charge',17),('multiplicity',9)]:
   negative=deepcopy(positive);negative['calculation_records'][0][f]=v;check(pid+':out_of_contract_'+f+'_rejected',not fixture(contract,negative)['valid'])
  negative=deepcopy(positive)
  for r in negative['calculation_records']:r['kind']='failed';r['failure_reason']='SYNTHETIC ONLY'
  check(pid+':complete_all_failed_rejected',not fixture(contract,negative)['valid'])
  negative=deepcopy(positive);negative['calculation_records'][0]['energies'].pop('electronic_Eh');check(pid+':missing_raw_energy_rejected',not fixture(contract,negative)['valid'])
  for p in ['outputs/../evaluation/hidden.json','outputs/sub/../../hidden','/tmp/answer.json','evaluation/reference.json','outputs//../secret','./outputs/../hidden','outputs/./../hidden','outputs//name','outputs/name\n']:
   negative=deepcopy(positive);negative['evidence_files']=[p];check(pid+':unsafe_evidence_path_rejected:'+p,not fixture(contract,negative)['valid'])
  for p in ['./outputs/SYNTHETIC.log','outputs/./SYNTHETIC.log','./data/./SYNTHETIC.json','code/SYNTHETIC.py']:
   ordinary=deepcopy(positive);ordinary['evidence_files']=[p];check(pid+':ordinary_relative_evidence_path_accepted:'+p,fixture(contract,ordinary)['valid'])
  check(pid+':old_scalar_only_rejected',not fixture(contract,{'status':'complete','energy':1.23})['valid'])
  check(pid+':missing_readable_report_rejected',not fixture(contract,positive,False)['valid'])
  failure=deepcopy(positive);failure['status']='bounded_failure';failure['conclusion']['assessment']='incomplete'
  for f in ['results','hypotheses','sensitivity']:failure.pop(f,None)
  failure['methods'].pop('sensitivity',None);failure['calculation_records']=[{'record_id':'SYNTHETIC','job_id':'SYNTHETIC','system_id':'SYNTHETIC','charge':0,'multiplicity':1,'method_key':'primary','kind':'failed','log_file':'outputs/SYNTHETIC_FAILURE.log','input_file':'outputs/SYNTHETIC_INPUT.txt','failure_reason':'SYNTHETIC ONLY'}]
  failure['failure_report']={'attempted_scope':'SYNTHETIC','cause':'SYNTHETIC','missing_endpoints':['SYNTHETIC'],'diagnostic_files':['outputs/SYNTHETIC_FAILURE.log']}
  r=fixture(contract,failure);check(pid+':honest_failure_format_accepted',r['valid'],r['errors'][:3])
  pre_engine=deepcopy(failure);pre_engine['calculation_records']=[];pre_engine['methods']={};pre_engine['failure_report']['stage']='pre_engine'
  for k in ['scientific_engine_starts','successful_jobs','failed_jobs','restart_count','allocated_cores','summed_job_wall_hours','cpu_core_hours']:pre_engine['resource_usage'][k]=0
  pre_engine['failure_report']['cause']='SYNTHETIC INPUT GATE; no actual scientific execution'
  r=fixture(contract,pre_engine);check(pid+':zero_launch_diagnostic_failure_accepted',r['valid'],r['errors'][:3])
  for k in ['stage','diagnostic_files','cause','missing_endpoints']:
   negative=deepcopy(pre_engine);del negative['failure_report'][k]
   check(pid+':zero_launch_missing_'+k+'_rejected',not fixture(contract,negative)['valid'])
  for k in ['scientific_engine_starts','successful_jobs','failed_jobs','restart_count','allocated_cores','summed_job_wall_hours','cpu_core_hours']:
   negative=deepcopy(pre_engine);negative['resource_usage'][k]=1
   check(pid+':zero_launch_false_'+k+'_rejected',not fixture(contract,negative)['valid'])
  negative=deepcopy(positive);negative['calculation_records']=[]
  check(pid+':complete_without_real_records_rejected',not fixture(contract,negative)['valid'])
  negative=deepcopy(pre_engine);negative['results']=positive['results']
  check(pid+':zero_launch_claimed_matrix_rejected',not fixture(contract,negative)['valid'])
  negative=deepcopy(pre_engine);negative['methods']=positive['methods']
  check(pid+':zero_launch_claimed_actual_methods_rejected',not fixture(contract,negative)['valid'])
  failure['conclusion']['assessment']='supported';check(pid+':bounded_failure_not_supported_rejected',not fixture(contract,failure)['valid'])
  failure['conclusion']['assessment']='incomplete';failure.pop('failure_report');check(pid+':failure_without_diagnostics_rejected',not fixture(contract,failure)['valid'])
  if pid=='paper_d3b4575397179146':
   for state,wrong in [('triplet_O2',1),('singlet_O2',3),('superoxide',1)]:
    negative=deepcopy(positive);negative['results']['oxygen_states'][state]['multiplicity']=wrong
    check(pid+':wrong_named_oxygen_state_rejected:'+state,not fixture(contract,negative)['valid'])
  if pid=='paper_0e835b370ddd37b6':
   negative=deepcopy(positive);negative['results']['matched_coordinate_decomposition']['4']['points'][0]['coordinate_value']=9
   check(pid+':missing_matched_HH_point_rejected',not fixture(contract,negative)['valid'])
  for mode in MODES:
   package=DEST/mode/pid;v=validate_task_package(package);check(pid+':'+mode+':official_validate',v.status=='passed',v.findings)
   for f in package.rglob('*.json'):
    json.loads(f.read_text());check(pid+':'+mode+':json:'+str(f.relative_to(package)),True)
   man=json.loads((package/'package_manifest.json').read_text());check(pid+':'+mode+':official_hash',man['package_content_sha256']==package_content_hash(package_payload_entries(package)))
   PACKAGE_HASHES[mode+'/'+pid]={'package_content_sha256':man['package_content_sha256'],'package_manifest_sha256':hashlib.sha256((package/'package_manifest.json').read_bytes()).hexdigest()}
   runtime=load_runtime_evaluation(paper_id=pid,task_type=mode,repository=repo);check(pid+':'+mode+':runtime_adapter',runtime.adapter_id=='split-computational-evaluator.v3-flat')
   check(pid+':'+mode+':weights_100',sum(r['max_score'] for r in runtime.ground_truth['scientific_conclusion_rubric'])==100)
   with tempfile.TemporaryDirectory(prefix='rcb_batch4_public_export_') as td:
    materialize_agent_files(paper_id=pid,task_type=mode,destination=td,repository=repo)
    actual={str(p.relative_to(td)) for p in Path(td).rglob('*') if p.is_file()}
    check(pid+':'+mode+':export_exact_agent_input',actual==af.keys())
    check(pid+':'+mode+':no_private_export',not any('evaluation' in f or '.snapshot' in f or f.endswith('.pdf') for f in actual))
   audit=json.loads((package/'evaluation/task_provenance/upgrade_audit.json').read_text());source=ROOT/audit['source']
   for original,r in audit['source_payload_snapshots'].items():
    check(pid+':'+mode+':snapshot:'+original,hashlib.sha256((package/r['snapshot']).read_bytes()).hexdigest()==r['sha256']==hashlib.sha256((source/original).read_bytes()).hexdigest())
   check(pid+':'+mode+':new_science_not_fabricated',audit['new_scientific_calculations_performed'] is False and audit['scientific_engine_starts']==0)
   check(pid+':'+mode+':honest_development_status',audit['status']==('blocked' if pid=='paper_60f4c45810428116' else 'implemented_pending_expanded_reference'))
   check(pid+':'+mode+':source_pages_recorded',all(x['pdf_pages_1_based'] for x in audit['source_pdf_review']))
   for f in package.rglob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
     if not link.startswith(('http:','https:','#')):check(pid+':local_link:'+str(f.relative_to(package)),(f.parent/link.split('#')[0]).exists())
  (B/('validation_progress_'+selected[0]+'.json')).write_text(json.dumps({'last_completed':pid,'results':RESULTS},ensure_ascii=False,indent=2)+'\n')
  print(pid,'checks passed',flush=True)
 # Paper-specific chemical input checks. Graph tests are not quantum calculations.
 import chemistry_inputs_check
 chem=chemistry_inputs_check.run()
 for c in chem:check(c['test'],c['passed'],c.get('detail'))
 return {'date':'2026-09-27','batch':4,'status':'passed','paper_ids':selected,'paper_count':len(selected),'package_count':2*len(selected),'checks':len(RESULTS),'repository_mode':repository_mode,'scientific_calculations_run':0,'LLM_judge_run':False,'boundary':'Official package/runtime/public export and synthetic format regression plus graph consistency. No scientific reference or calibrated judge validation. Nominal in-range wrong states/references require raw-evidence scientific adjudication; schema acceptance never confers scientific PASS.','package_hashes':PACKAGE_HASHES,'results':RESULTS}
if __name__=='__main__':
 try:report=main()
 except Exception as exc:report={'status':'failed','batch':4,'error':repr(exc),'traceback':traceback.format_exc(),'results':RESULTS}
 output=B/('validation_shard_'+sys.argv[2]+'.json') if len(sys.argv)>2 and sys.argv[1]=='--shard' else B/'validation_report.json'
 output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({k:v for k,v in report.items() if k not in ['results','traceback']},ensure_ascii=False))
 if report['status']!='passed':sys.exit(1)
