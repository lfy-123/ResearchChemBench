"""Batch 6 development implementation. Writes only assigned upgrade packages.
No quantum jobs are launched. Existing upgraded packages are resumed, never recopied.
"""
from pathlib import Path
import sys,json,hashlib,shutil,re,copy
ROOT=Path(__file__).resolve().parents[4];sys.path.insert(0,str(ROOT))
from evaluation.contracts.task_package import package_payload_entries,package_content_hash,validate_task_package
BATCH=Path(__file__).resolve().parent;DEST=ROOT/'tasks/upgrade_tasks'
IDS=['paper_5ea491c741fbd8d4','paper_72f60526b64ce1b6','paper_c7217910ecbee1d9']
MODES=['autonomous_research','paper_reproduction']
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(p,required=None):return {'type':'object','properties':p,'required':list(p) if required is None else required,'additionalProperties':False}
def arr(s,n=1):return {'type':'array','items':s,'minItems':n}
def enum(*x):return {'enum':list(x)}
def const(x):return {'const':x}
S={'type':'string','minLength':1};N={'type':'number'};I={'type':'integer','minimum':0};B={'type':'boolean'}
P={'type':'string','pattern':r'^(?:\./)?(?:outputs|report)/(?!\.\.(?:/|$))(?!.*?/\.\.(?:/|$))[A-Za-z0-9_.-]+(?:/[A-Za-z0-9_.-]+)*$'}
PS=arr(P);REFS=arr(S);POS={'type':'number','minimum':0};SHA={'type':'string','pattern':'^[0-9a-f]{64}$'}
def vec(n=3):return {'type':'array','items':N,'minItems':n,'maxItems':n}
def cond(field,values,props=None,required=None):return {'if':{'properties':{field:enum(*values)},'required':[field]},'then':{'properties':props or {},'required':required or []}}
def common_schema(pid,results,job_schema,gates):
 gate=obj({'gate_id':enum(*gates),'status':enum('closed','open'),'evidence_files':PS,'finding':S})
 complete_gates={'type':'array','items':gate,'minItems':len(gates),'maxItems':len(gates),'allOf':[{'contains':obj({'gate_id':const(g),'status':const('closed'),'evidence_files':PS,'finding':S})} for g in gates]}
 methods=obj({'primary':S,'software_versions':S,'numerical_settings_file':P,'environment':S,'definitions':S})
 sensitivity=obj({'factor':S,'baseline_record_ids':REFS,'perturbed_record_ids':REFS,'observable':S,'unit':S,'baseline_value':N,'perturbed_value':N,'difference':N,'uncertainty_basis':S,'evidence_files':PS})
 hypothesis=obj({'id':S,'claim':S,'counterprediction':S,'comparison_ids':REFS,'outcome':enum('supported','refuted','indistinguishable'),'reason':S,'evidence_files':PS})
 result=obj({'paper_id':const(pid),'status':enum('complete','partial','bounded_failure'),'prerequisite_checks':arr(gate),'calculation_records':arr(job_schema,0),'methods':methods,'results':results,'hypotheses':arr(hypothesis,2),'sensitivity':arr(sensitivity),'conclusion':obj({'outcome':enum('supported','refuted','indistinguishable','incomplete'),'claim':S,'comparison_ids':arr(S,0),'limitations':S}),'artifact_index':arr(obj({'path':P,'sha256':SHA,'role':enum('input','log','geometry','mapping','density','table','diagnostic','script','restart')}),0),'resource_record':obj({'engine_launches':I,'failed_launches':I,'allocated_core_hours':POS,'engine_wall_hours_sum':POS,'elapsed_wall_hours':POS,'measurement_basis':S}),'failure_report':obj({'attempted_scope':S,'observed_failure':S,'missing_endpoints':arr(S),'release_conditions':arr(S),'diagnostic_files':PS})},['paper_id','status','prerequisite_checks','calculation_records','conclusion','artifact_index','resource_record'])
 result['$schema']='https://json-schema.org/draft/2020-12/schema'
 result['allOf']=[cond('status',['complete'],{'prerequisite_checks':complete_gates,'artifact_index':{'minItems':1},'resource_record':{'properties':{'engine_launches':{'minimum':1}}},'calculation_records':{'minItems':1,'contains':{'properties':{'status':const('converged')},'required':['status']}},'conclusion':{'properties':{'outcome':enum('supported','refuted','indistinguishable')}}},['methods','results','hypotheses','sensitivity']),cond('status',['partial','bounded_failure'],{'conclusion':{'properties':{'outcome':const('incomplete')}}},['failure_report'])]
 return {'required_files':['report/results.json','report/report.md'],'primary_result_file':'report/results.json','report_file':'report/report.md','result_schema':result}
def job_base(species,charges,mults):
 p={'record_id':S,'system_id':enum(*species),'method_id':S,'status':enum('converged','failed','not_run'),'charge':enum(*charges),'multiplicity':enum(*mults),'input_file':P,'log_file':P,'geometry_file':P,'atom_map_file':P,'evidence_files':PS,'validation':obj({'identity_check':S,'scf_convergence':S,'geometry_or_boundary_check':S,'state_check':S}),'electronic_Eh':N}
 return obj(p,[k for k in p if k not in ['electronic_Eh']])

def initialize(pid,mode):
 src=ROOT/'tasks'/f'final_verified_{mode}'/pid;dst=DEST/mode/pid
 if not dst.exists():shutil.copytree(src,dst)
 auditp=dst/'evaluation/task_provenance/upgrade_audit.json'
 old=json.loads(auditp.read_text()) if auditp.exists() else None
 if old:
  for rel,d in old['source_payload_snapshots'].items():
   assert sha(dst/d['snapshot'])==d['sha256'],f'Snapshot drift {dst}/{rel}'
  return src,dst,old['source_payload_snapshots']
 snapshots={}
 for f in src.rglob('*'):
  if not f.is_file():continue
  rel=f.relative_to(src).as_posix();snap=dst/'evaluation/legacy_final_snapshot'/(rel+'.snapshot')
  if snap.exists():assert snap.read_bytes()==f.read_bytes()
  else:snap.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,snap)
  snapshots[rel]={'sha256':sha(f),'snapshot':snap.relative_to(dst).as_posix()}
 return src,dst,snapshots

def build(pid,c):
 if pid==IDS[2]:
  from cluster_reference_update import update_spec
  c=update_spec(c)
 state=c.get('development_status','blocked')
 blocked=state=='blocked'
 state_label='BLOCKED' if blocked else 'EXPANDED REFERENCE PENDING'
 records=[]
 for mode in MODES:
  src,dst,snapshots=initialize(pid,mode)
  # Public data rebuilt narrowly from frozen identities; old answer coordinates remain private snapshots.
  public=dst/'agent_input/data/inputs';public.mkdir(parents=True,exist_ok=True)
  for name in c.get('remove_public',[]):
   f=public/name
   if f.exists():f.unlink()
  for name,data in c['public'].items():dump(public/name,data)
  dump(public/'development_gate.json',{'status':state,'implementation_status':'implemented_pending_expanded_reference','release_ready':False,'missing_prerequisites':c['blockers'],'unblocking_conditions':c['unblock'],'no_new_reference_calculations':True,'instructions':'Development package only. Diagnose missing prerequisites; do not treat an open gate or an old result as completed science.'})
  body='# Scientific objective\n\n'+c['objective']+'\n\n'
  if mode=='paper_reproduction':body+='# Author-provided scientific guidance\n\n'+c['author']+'\n\n'
  body+='# Public inputs and scientific boundaries\n\n'+c['boundaries']+'\n\nThis development package is '+state_label+'. Read `data/inputs/development_gate.json`. Expanded numerical references and acceptance intervals have not been calibrated. Do not launch the full matrix until its prerequisites are actually closed. An evidence-backed diagnosis is a valid incomplete submission, not a successful result. Use only supplied public identities and observations; the paper, SI, author endpoint coordinates, private snapshots and evaluator are not authorized research inputs.\n\n# Required scientific validation/investigation\n\n'+c['investigation']+'\n\nTest at least two distinguishable explanations with the required numerical comparisons. Support, refutation and evidence-sufficient indistinguishability are equally acceptable; missing core controls are incomplete. Quantify one decisive sensitivity using both baseline and perturbed results. Optional extensions are not scored requirements.\n\n# Deliverables\n\nSubmit `report/results.json` and readable `report/report.md`, following `submission_schema.json` and `submission_guide.md`. Include actual job inputs, raw outputs, mapped geometries, analysis tables/scripts and an artifact index with SHA-256 hashes. References must resolve to submitted files under `outputs/` or `report/`. Preserve failed attempts and distinguish constraints from free minima. Record actual engine launches, failures, engine wall time and allocated CPU core-hours; do not count analysis work units as launches. A `bounded_failure` or `partial` submission identifies missing endpoints and evidence without fabricating unavailable numbers. Scientific completion requires the entire core comparison and valid underlying evidence.\n'
  (dst/'agent_input/task.md').write_text(body)
  schema=common_schema(pid,c['schema'],c['job_schema'],c['gates'])
  if pid==IDS[2]:
   schema['result_schema']['allOf'].append(cond('status',['complete'],{'results':{'properties':{'series':{'properties':{'n2':{'properties':{'disposition':const('retained_pair')}}}}}}}))
  dump(dst/'agent_input/submission_schema.json',schema)
  (dst/'agent_input/submission_guide.md').write_text('# Submission guide\n\nDevelopment status: '+state_label+'; no calibrated expanded reference or publishable upgraded score.\n\n'+c['guide']+'\n\nThe top-level `status` is `complete`, `partial` or `bounded_failure`. Complete requires closed prerequisite records backed by actual evidence, methods, all results panels, at least two hypothesis records and a quantitative sensitivity record. This hypothetical complete contract does not certify that the current development package is scientifically validated. Failed/partial submissions require `failure_report` and an incomplete conclusion; zero engine launches is truthful when failure precedes computation. Never enter zero for an unknown scientific value.\n\nEach job ID and comparison reference must resolve uniquely. Every referenced artifact must exist, match its hash, and contain the named raw calculation; a schema-valid path or synthetic test fixture is not evidence. Hash the exact input, coordinate, log, wavefunction/density and analysis files used. Keep units, atom labels, charge/spin and geometry reference explicit. The report must explain numerical derivations and why the control can falsify the proposed explanation.\n\nOptional work must be labelled separately. No extra ligand family, Group B junction, SAPT decomposition, docking, graphene or bulk/application inference is required unless explicitly in the core task.\n')
  docs=[]
  for f in sorted((ROOT/'papers'/pid/'documents').glob('*')):
   docs.append({'path':f.relative_to(ROOT).as_posix(),'sha256':sha(f),'read_scope':c['source_scope'].get(f.name,'identity/background')})
  ev=[{'evidence_id':'paper_main','source':docs[0] if docs[0]['path'].endswith('main.pdf') else next(d for d in docs if d['path'].endswith('main.pdf')),'scope':c['source_summary']},{'evidence_id':'paper_si','source':next(d for d in docs if not d['path'].endswith('main.pdf')),'scope':c['si_summary']},{'evidence_id':'extension','source':{'path':'evaluation/reference_validation_plan.md','kind':'benchmark_design_not_reference_result'},'scope':'Expanded controls and definitions; not claimed to be author calculations.'},{'evidence_id':'readiness_review','source':{'path':'evaluation/task_provenance/source_review.json'},'scope':'Local/public prerequisite investigation and historical failure evidence; not a new PASS.'}]
  keypoints=[];rules=[];rubric=[]
  for k,title,weight,fields,expect in c['criteria']:
   expect+=' Read the actual cited inputs and raw outputs, check IDs and arithmetic, and award credit only for demonstrated endpoints. No numerical target/tolerance is inherited from the old scalar task.'
   kp='kp_'+k
   keypoints.append({'key_point_id':kp,'key_point_type':'result','statement':title,'expected':expect,'evidence_ids':['paper_main','paper_si','extension','readiness_review']})
   rules.append({'rule_id':'rule_'+k,'reference_id':kp,'type':'condition' if k=='identity' else 'semantic','expected':expect,'binding':{'artifact_paths':['report/results.json','report/report.md'],'fields':fields,'comparison':expect}})
   rubric.append({'id':k,'max_score':weight,'description':title,'rule_ids':['rule_'+k]})
  conclusion='A complete matched comparison supports, refutes or leaves indistinguishable the stated explanations within measured uncertainty. All required controls must have real, correctly identified results; missing calculations and open prerequisites cannot be called scientific indistinguishability. While the expanded references are uncalibrated, report development assessments only, never a publishable upgraded PASS.'
  rules.append({'rule_id':'rule_conclusion','reference_id':'conclusion_investigation','type':'semantic','expected':conclusion,'binding':{'artifact_paths':['report/results.json','report/report.md'],'fields':['$.conclusion','$.results','$.hypotheses','$.sensitivity','$.prerequisite_checks'],'comparison':conclusion}})
  rubric.append({'id':'conclusion','max_score':10,'description':'Evidence-supported bounded scientific judgement','rule_ids':['rule_conclusion']})
  assert sum(r['max_score'] for r in rubric)==100
  dump(dst/'evaluation/reference_key_points.json',{'paper_id':pid,'items':keypoints})
  dump(dst/'evaluation/reference_conclusions.json',{'paper_id':pid,'items':[{'conclusion_id':'conclusion_investigation','claim_role':'final','statement':c['objective'],'expected':conclusion,'supporting_key_point_ids':[x['key_point_id'] for x in keypoints],'evidence_ids':['paper_main','paper_si','extension','readiness_review']}]})
  dump(dst/'evaluation/scoring_rules.json',{'paper_id':pid,'scoring_policy':'dual_axis_100.scientific_results.v1','rules':rules,'scientific_rubric':rubric,'reference_stage':('blocked_pending_prerequisite_and_expanded_reference' if blocked else 'historical_n2_audited_expanded_reference_pending'),'release_ready':False,'numerical_reference_policy':{'expanded_targets':None,'expanded_tolerances':None,'calibration':'Freeze only after real pilot/full-matrix evidence and method/numerical uncertainty review.'},'scoring_notes':['No upgraded scientific PASS while release prerequisites/reference remain open.','Ordinary honest failure is not fabrication, but failure reporting cannot replace a missing scored endpoint.','A source-author ranking is not required; demonstrated refutation or uncertainty is acceptable.','Old scalar-only work, fabricated endpoints, wrong identities/states and incompatible energy/bias zeros invalidate dependent claims.']})
  dump(dst/'evaluation/critical_failures.json',{'paper_id':pid,'items':[{'failure_id':'cf_'+str(i+1),'condition':x,'severity':'scientifically serious','scientific_impact':'Invalidate the affected endpoint and all dependent completion claims; retain independent valid partial credit.'} for i,x in enumerate(c['failures']+['Claims full completion from only the old scalar or without required new comparisons.','Claims a failed, constrained or wrong-object calculation is a validated free endpoint; invents or substitutes raw evidence.','Treats the current development package, a historical PASS, or schema acceptance as proof of upgraded scientific validation.'])]})
  dump(dst/'evaluation/evidence_map.json',{'paper_id':pid,'evidence':ev})
  review=json.loads((BATCH/'source_review'/f'{pid}_review.json').read_text());dump(dst/'evaluation/task_provenance/source_review.json',review)
  if pid==IDS[1]:dump(dst/'evaluation/task_provenance/author_coordinate_blocks.json',json.loads((BATCH/'source_review/transport_source_coordinate_blocks.json').read_text()))
  plan='# Reference validation plan — '+state_label+'\n\n'+c['source_summary']+'\n\n'+c['si_summary']+'\n\n## Reusable evidence and limits\n\n'+c['reuse']+'\n\n## Explicit missing prerequisites\n\n'+'\n'.join('- '+x for x in c['blockers'])+'\n\n## Minimum pilot and release sequence\n\n'+'\n'.join(f'{i+1}. {x}' for i,x in enumerate(c['unblock']))+'\n\n## Full expanded reference\n\n'+c['full_reference']+'\n\n## Software and quantitative calibration\n\n'+c['software']+' Numerical uncertainty must be measured from converged raw calculations, model variation and geometry sensitivity. Paper numbers remain historical anchors only; there is no newly calibrated absolute tolerance, ranking or winner. Do not impose optional extensions as gates.\n\n## Actual work in this upgrade\n\nNo new quantum, periodic or transport engine was launched. Local source reading, graph/stoichiometry checks and schema tests are development work. Preserve inputs, failed/restarted jobs, actual engine launches, CPU allocation and engine times when a future pilot is authorized and budgeted. Current scope is a development package, not a released benchmark or validated scientific reference.\n'
  (dst/'evaluation/reference_validation_plan.md').write_text(plan)
  (dst/'evaluation/verified_computation_reference.md').write_text('# Historical reference boundary\n\nThe exact previous file is retained at `legacy_final_snapshot/evaluation/verified_computation_reference.md.snapshot`. It describes the old scalar scope only and is NOT an expanded reference.\n\n'+c['reuse']+'\n\nCurrent status: '+state+'; expanded reference not validated. See `reference_validation_plan.md` and `task_provenance/source_review.json`. No new scientific reference calculations.\n')
  (dst/'paper_route.md').write_text('# Private upgraded paper route\n\nStatus: '+state_label+', development package; A → proposed B.\n\n'+c['author']+'\n\n## Expanded scientific scope\n\n'+c['objective']+'\n\n'+c['investigation']+'\n\n## Historical boundary\n\n'+c['reuse']+'\n\nThe previous route is preserved verbatim in `evaluation/legacy_final_snapshot/paper_route.md.snapshot`; its old scope and PASS claims do not govern this task.\n')
  info=json.loads((src/'task_info.json').read_text());info.update(title='[DEVELOPMENT '+state_label+'] '+c['title'],category='bounded scientific hypothesis testing — development',difficulty='hard',difficulty_reasons=['Requires real discriminating controls and correct physical reference definitions beyond the old scalar endpoint.','Expanded reference calculations, remaining prerequisites and uncertainty calibration are not complete.'],data=[{'path':'data/inputs','description':'Mapped identities, explicit control matrix, provenance and blocking prerequisites; no hidden reference endpoints.'}],required_deliverables=[{'path':'report/results.json','description':'Structured scientific matrix, raw evidence index and honest completion/failure record.'},{'path':'report/report.md','description':'Readable evidence-based comparison with limitations.'}]);dump(dst/'task_info.json',info)
  source_docs=[{'path':str(f.relative_to(ROOT)),'sha256':sha(f)} for f in [ROOT/'docs/evalution/update/upgrade_implementation_guide_20260927.md',ROOT/'docs/evalution/update/upgrade_guidance_review_20260927.md',ROOT/'docs/evalution/update/upgrade_guidance_review_manifest_20260927.json',ROOT/'docs/evalution/update'/f'{pid}.md']]
  dump(dst/'evaluation/task_provenance/upgrade_audit.json',{'date':'2026-09-27','paper_id':pid,'batch':6,'source_path':src.relative_to(ROOT).as_posix(),'source_package_manifest_sha256':sha(src/'package_manifest.json'),'source_payload_snapshots':snapshots,'source_documents':docs,'source_guidance_documents':source_docs,'old_class':'A','new_class':'B','new_class_status':'proposed_implemented_not_validated','status':state,'implementation_status':'implemented_pending_expanded_reference','release_ready':False,'new_scientific_calculations_performed':False,'new_scientific_engine_launches':0,'remaining_reference_gaps':c['blockers'],'unblocking_conditions':c['unblock'],'mode_parity':'Same objective, public objects, controls, schema, completion requirements and all five scientific evaluators; only PR author guidance differs.'})
  if pid==IDS[2]:
   from cluster_reference_update import update_metadata
   update_metadata(dst)
  entries=package_payload_entries(dst);manifest={'paper_id':pid,'task_type':mode,'package_format':1,'agent_input_root':'agent_input','entries':[e.model_dump(mode='json') for e in entries],'package_content_sha256':package_content_hash(entries)};dump(dst/'package_manifest.json',manifest)
  v=validate_task_package(dst);assert v.status=='passed',(dst,v.findings)
  records.append({'mode':mode,'path':dst.relative_to(ROOT).as_posix(),'package_content_sha256':manifest['package_content_sha256'],'package_validation':v.status})
 rec={'paper_id':pid,'old_class':'A','new_class':'B','status':state,'implementation_status':'implemented_pending_expanded_reference','release_ready':False,'packages':records,'reference_gaps':c['blockers'],'release_conditions':c['unblock'],'source_review':'source_review/'+pid+'_review.json','new_scientific_calculations_performed':False}
 dump(BATCH/(pid+'_status.json'),rec)
 done={p:json.loads((BATCH/(p+'_status.json')).read_text()) for p in IDS if (BATCH/(p+'_status.json')).exists()}
 (BATCH/'STATUS.md').write_text('# 第6批开发状态\n\n2026-09-27。三篇均来自正常 final；新增科学引擎计算为 0。\n\n| 论文 | 开发状态 | 发布状态 |\n| --- | --- | --- |\n'+'\n'.join('| '+p+' | '+('AR/PR开发包已落地，官方包校验通过' if p in done else '进行中')+' | '+(done[p]['status']+'；扩展参考未验证' if p in done else '核查中')+' |' for p in IDS)+'\n\n逐篇详细记录见 `paper_*_status.json`。最终格式回归结果见 `validation_report.json`；格式有效不表示科学通过。\n')
 print(pid,'saved',len(records),'packages',flush=True)
 return rec
