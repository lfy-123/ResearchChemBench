"""Batch 5 development packages. Never touches final or another paper's directory."""
from pathlib import Path
from copy import deepcopy
import json,hashlib,shutil,sys,re
B=Path(__file__).resolve().parent
ROOT=B.parents[3]; sys.path.insert(0,str(ROOT)); sys.path.insert(0,str(B))
from evaluation.contracts.task_package import package_payload_entries,package_content_hash,validate_task_package
DEST=ROOT/'tasks/upgrade_tasks'; MODES=['autonomous_research','paper_reproduction']
ASSIGN=json.loads((B/'assignment.json').read_text()); IDS=ASSIGN['batch']['papers']; RECORDS={r['paper_id']:r for r in ASSIGN['records']}
def write(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t,encoding='utf-8')
def dump(p,x):write(p,json.dumps(x,indent=2,ensure_ascii=False,allow_nan=False)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def S(desc=''):return {'type':'string','minLength':1,**({'description':desc} if desc else {})}
def N(desc='',minimum=None):return {'type':'number',**({'minimum':minimum} if minimum is not None else {}),**({'description':desc} if desc else {})}
def I(minimum=0):return {'type':'integer','minimum':minimum}
def C(v):return {'const':v}
def E(v):return {'enum':v}
def A(s,n=1):return {'type':'array','items':deepcopy(s),'minItems':n}
def O(**fields):return {'type':'object','properties':deepcopy(fields),'required':list(fields),'additionalProperties':False}
def K(keys,s):return O(**{k:deepcopy(s) for k in keys})
PATH={'type':'string','pattern':r'^(?!.*(?:^|/)\.\.(?:/|$))(?!.*//)(?:\./)?(outputs|data|code)/[A-Za-z0-9_./+@=,: -]+$'}
EV=A(PATH); REF=A(S()); VEC=A(N(),3); VEC['maxItems']=3; TENSOR=A(VEC,3);TENSOR['maxItems']=3
PAIR=O(left_record=S(),right_record=S(),left_value=N(),right_value=N(),difference_right_minus_left=N(),unit=S(),uncertainty=N(minimum=0),uncertainty_basis=S(),evidence_files=EV)
STATE=O(state_id=S(),multiplicity=E([1,3]),root_index=I(1),energy_eV=N(),oscillator_strength=N(minimum=0),hole_fragment_weights=A(N(minimum=0)),electron_fragment_weights=A(N(minimum=0)),state_match_metric=N(),state_match_definition=S(),transition_density_file=PATH,evidence_files=EV)
SOC=O(singlet_state_id=S(),triplet_state_id=S(),components_cm1=VEC,norm_cm1=N(minimum=0),operator_and_relativistic_definition=S(),evidence_files=EV)
def panel(schema,title,rule):return {'schema':schema,'title':title,'rule':rule}
def schema(spec):
 objs=spec['objects']; ids=list(objs)
 rec=O(record_id=S(),object_id=E(ids),formula=S(),charge={'type':'integer'},multiplicity=I(1),state=S(),method_id=S(),geometry_regime=E(['relaxed','frozen_control','displaced','single_point','reference','data_fit']),outcome=E(['converged','collapsed','failed']),input_file=PATH,raw_output_files=EV,validation=O(convergence=S(),state_identity=S(),stationarity_or_model_validity=S(),evidence_files=EV))
 rec['properties'].update({'electronic_energy':N(),'energy_unit':E(['hartree','eV']),'geometry_file':PATH,'s2':N(minimum=0),'collapse_destination':S(),'attempt_id':S()})
 rec['allOf']=[]
 for oid,obj in objs.items():
  props={'charge':E(obj.get('charges',[obj.get('charge',0)])),'multiplicity':E(obj.get('multiplicities',[1,3]))}
  if obj.get('formula'):props['formula']=C(obj['formula'])
  rec['allOf'].append({'if':{'properties':{'object_id':C(oid)},'required':['object_id']},'then':{'properties':props}})
 rec['allOf'].append({'if':{'properties':{'outcome':C('collapsed')}},'then':{'required':['collapse_destination','geometry_file']}})
 methods=O(primary=O(software_version=S(),electronic_or_physical_model=S(),basis_ecp_or_parameters=S(),relativity=S(),environment=S(),numerical_settings=S()),sensitivity_protocol=S())
 hyp=O(proposition=S(),falsifying_observation=S(),actual_test_records=REF,assessment=E(['supported','refuted','indistinguishable']),quantitative_basis=S())
 sens=O(changed_factor=S(),baseline_records=REF,alternative_records=REF,quantity=S(),baseline_value=N(),alternative_value=N(),change=N(),unit=S(),uncertainty_basis=S(),evidence_files=EV)
 props={'paper_id':C(spec['id']),'status':E(['complete','bounded_failure']),'reference_definition':C(spec['reference_definition']),'methods':methods,'calculation_records':A(rec),'results':O(**{k:v['schema'] for k,v in spec['panels'].items()}),'hypotheses':A(hyp,2),'sensitivity':A(sens),'conclusion':O(assessment=E(['supported','refuted','indistinguishable','incomplete']),statement=S(),supported_scope=S(),limitations=S(),evidence_records=REF),'evidence_files':EV,'resources':O(scientific_engine_starts=I(),successful_starts=I(),failed_starts=I(),restarts=I(),allocated_cores=I(),wall_job_hours=N(minimum=0),cpu_core_hours=N(minimum=0),parallel_elapsed_hours=N(minimum=0),measurement_basis=S()),'failure_report':O(attempted_scope=S(),observed_failure=S(),missing_endpoints=A(S()),release_conditions=A(S()),evidence_files=A(PATH,0))}
 props['control_equivalence']=A(O(reference_comparison_id=S(),alternative_control_definition=S(),held_factors=A(S()),changed_factor=S(),coverage_justification=S(),evidence_files=EV),0)
 required=['paper_id','status','reference_definition','conclusion','evidence_files','resources']
 sc={'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','properties':props,'required':required,'additionalProperties':False,'allOf':[{'if':{'properties':{'status':C('complete')}},'then':{'required':['methods','calculation_records','results','hypotheses','sensitivity'],'properties':{'calculation_records':{'contains':{'properties':{'outcome':C('converged')},'required':['outcome']},'minContains':1},'conclusion':{'properties':{'assessment':E(['supported','refuted','indistinguishable'])}}}},'else':{'required':['failure_report'],'properties':{'conclusion':{'properties':{'assessment':C('incomplete')}}}}}]}
 # An input gate may fail before any engine starts or creates an artifact.
 # The complete branch still requires real evidence and record references.
 props['evidence_files']['minItems']=0
 props['conclusion']['properties']['evidence_records']['minItems']=0
 complete_props=sc['allOf'][0]['then']['properties']
 complete_props['evidence_files']={'minItems':1}
 complete_props['conclusion']['properties']['evidence_records']={'minItems':1}
 return {'contract_version':'batch5-expanded-20260927','primary_result_file':'report/results.json','report_file':'report/report.md','required_files':['report/results.json','report/report.md'],'result_schema':sc,'validation_boundary':'Format only. Raw outputs, controls, arithmetic and state identity must pass the scientific evaluator. A bounded failure is accepted for reporting, never as scientific completion.'}

def build(spec):
 pid=spec['id']; assert pid in IDS
 source_docs=json.loads((B/'source_review'/(pid+'.sources.json')).read_text())
 for p in sorted((B/'source_review').glob(pid+'.publisher_si.*')):
  if p.suffix in ['.pdf','.docx']:source_docs.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'sections':spec.get('extra_source_sections','Relevant methods, experimental observations and identity blocks; see source review.')})
 if pid=='paper_d8e5490cd9942f4f':
  for p in sorted((B/'source_review').glob('cologne_*')):
   if p.suffix in ['.gbs','.txt']:source_docs.append({'path':str(p.relative_to(ROOT)),'sha256':sha(p),'role':'Official originating-library molecular ECP/basis coefficients; parsed identity only.'})
 guide=ROOT/'docs/evalution/update'/f'{pid}.md'; source_docs.append({'path':str(guide.relative_to(ROOT)),'sha256':sha(guide),'role':'First-version specification, not scientific evidence'})
 contract=schema(spec)
 status=spec.get('status','implemented_pending_expanded_reference');blocked=spec.get('blockers',[])
 complete=['Identity, charge/spin, atom mapping, the stated observable definition and genuine raw evidence.']+[v['title'] for v in spec['panels'].values()]+['An actually computed sensitivity and an evidence-supported conclusion.']
 for mode in MODES:
  source=ROOT/'tasks'/('final_verified_'+mode)/pid; dest=DEST/mode/pid
  if not dest.exists():shutil.copytree(source,dest)
  old_audit=dest/'evaluation/task_provenance/upgrade_audit.json'
  if old_audit.exists():
   prior=json.loads(old_audit.read_text())
   if prior.get('batch')!=5:raise RuntimeError('Refusing to overwrite external progress '+str(dest))
   snapshots=prior['source_payload_snapshots']
  else:
   snapshots={}
   for p in sorted(source.rglob('*')):
    if not p.is_file():continue
    rel=p.relative_to(source);dst=dest/'evaluation/legacy_final_snapshot'/(str(rel)+'.snapshot');dst.parent.mkdir(parents=True,exist_ok=True)
    if dst.exists() and sha(dst)!=sha(p):raise RuntimeError('Snapshot drift '+str(dst))
    if not dst.exists():shutil.copyfile(p,dst)
    snapshots[str(rel)]={'sha256':sha(p),'snapshot':str(dst.relative_to(dest))}
  # Only files copied for this paper: retire obsolete public/evaluator files into the immutable snapshots.
  keep=set(spec.get('keep_files',[]))
  for p in (dest/'agent_input/data').rglob('*'):
   if p.is_file() and str(p.relative_to(dest/'agent_input/data/inputs')) not in keep:p.unlink()
  for p in (dest/'evaluation').iterdir():
   if p.is_file() and p.name not in ['reference_validation_plan.md']:p.unlink()
  for p in (dest/'evaluation/task_provenance').rglob('*'):
   if p.is_file() and p.name!='upgrade_audit.json':p.unlink()
  inp=dest/'agent_input/data/inputs';inp.mkdir(parents=True,exist_ok=True)
  for name in keep:
   target=inp/name
   if not target.exists():shutil.copyfile(source/'agent_input/data/inputs'/name,target)
  prep=B/'prepared_inputs'/pid
  if prep.exists():
   for p in prep.rglob('*'):
    if p.is_file():shutil.copyfile(p,inp/p.relative_to(prep))
  scope={'paper_id':pid,'development_status':status,'objects':spec['objects'],'identity_files':sorted(p.name for p in inp.iterdir() if p.is_file()),'control_definitions':spec['controls'],'observable_definition':spec['reference_definition'],'experimental_conditions':spec.get('conditions',{}),'required_comparisons':[{'id':k,'description':v['title']} for k,v in spec['panels'].items()],'optional_not_scored':spec['optional'],'input_blockers':blocked,'source_note':spec.get('public_source_note','The supplied identity graphs/starting models and explicitly labelled observations are public inputs. Source-specific method guidance is provided only in the reproduction task; predicted outcomes and author optimized added geometries are withheld.'),'public_private_boundary':'Identity/connectivity and declared measured observations are public. Author optimized new candidate geometries, computed rankings, reference outputs and legacy PASS archives are private.'}
  if spec.get('observations'):scope['identity_files'].append('experimental_observations.json')
  dump(inp/'study_scope.json',scope)
  if spec.get('observations'):dump(inp/'experimental_observations.json',spec['observations'])
  task='# Scientific objective\n\n'+spec['objective']+'\n\n'
  if mode=='paper_reproduction':task+='# Author-provided scientific guidance\n\n'+spec['author']+'\n\nThe matched controls and robustness checks below are benchmark-authored extensions. Reproducing an author assertion or old numerical endpoint alone does not complete this investigation.\n\n'
  task+='# Public inputs and scientific boundaries\n\n'+spec['boundary']+'\n\nUse `data/inputs/study_scope.json` and the identity/data files it lists. The observable convention is: **'+spec['reference_definition']+'**.\n\n'
  task+=('This is an autonomous-research task. Formulate and test the explanation independently.' if mode=='autonomous_research' else 'This is a paper-reproduction task. Use the authorized author guidance to reproduce the baseline and test it with the same expanded controls.')
  task+=' Do not access private evaluators, historical verification archives, the target article/SI or its answer data. General software and scientific documentation is permitted. The supplied identities and declared experimental observations are authorized inputs.\n\n'
  if blocked:task+='**Development input gate: blocked.** '+ ' '.join(blocked)+' A current bounded-failure submission can document this gate, but cannot earn scientific completion. The full contract below remains the release requirement; it has not been weakened to make the blocked input pass.\n\n'
  task+='# Required scientific validation/investigation\n\n'
  for i,(key,p) in enumerate(spec['panels'].items(),1):task+=f'{i}. **{p["title"]}** {spec["investigations"][key]}\n\n'
  task+='The named control definitions provide a reproducible reference design. A scientifically equivalent intervention is allowed if its mapping, held factors, observable and coverage are documented in control_equivalence and genuinely test the same comparison; this does not waive any core scientific axis. Test at least two distinguishable explanations with actual interventions. The evidence may support, refute, or leave explanations indistinguishable after the required comparisons. Missing a core comparison, an unattempted candidate or one failed calculation is not evidence of indistinguishability. Record independent starts and any supported collapse; do not fabricate separate minima.\n\n'
  task+='Keep free minima, frozen interventions, displaced structures and failures distinct. Validate each claimed minimum on the relevant electronic surface with convergence and curvature evidence; a Hessian at another method does not validate it. Track the same physical states with orbital/density evidence instead of matching root numbers blindly. Quantify one decisive numerical, method or conformational sensitivity. Preserve the raw input, complete output, structures and analysis code for every comparison.\n\n'
  task+='Outside the mandatory first-version scope: '+spec['optional']+'\n\n# Completion and allowed outcomes\n\n'
  task+='`complete` requires the full comparison matrix and real evidence, not an affirmative author conclusion. `bounded_failure` accepts truthful missing-input or computation diagnostics without fabricated numbers, but is not a scientific pass. This development package has not completed expanded reference calibration.\n\n# Deliverables\n\n'
  task+='Submit `report/results.json` following `submission_schema.json` and a readable `report/report.md`. Include methods, calculation records, all required `results` panels, evidence-assessed hypotheses, quantitative sensitivity, resources and the final bounded conclusion. Raw artifacts use workspace-relative `outputs/`, `data/` or `code/` paths. Do not merely refer to unavailable external files.\n\n'+ '\n'.join('- `'+k+'`: '+p['title'] for k,p in spec['panels'].items())+'\n'
  write(dest/'agent_input/task.md',task);dump(dest/'agent_input/submission_schema.json',contract)
  sg='# Submission guide\n\n'+spec['objective']+'\n\n`report/results.json` and `report/report.md` are both mandatory. The schema uses named objects/comparisons to prevent old scalar submissions from satisfying the expanded contract. All numbers must come from real calculations or the declared measurements.\n\n'
  sg+='Every `record_id` is unique and resolves from panel references to a real input/output. Preserve formula, charge, multiplicity, atom mapping, method and geometry regime. A failed record need not invent an energy. `collapsed` requires a destination and actual geometry; duplicate attempts are not independent minima. `resources` separates actual engine starts, summed job hours, CPU core-hours and parallel elapsed time; no work-package count is an engine count.\n\n'
  sg+='Energies and units are explicit. Electronic E excludes ZPE and thermal terms. Any G correction is G minus E; never add ZPE twice. Frozen structures have no borrowed equilibrium thermal correction. Difference conventions and state matching are validated from raw data. Positive `uncertainty` values require an empirical/convergence/method basis; zero must also be justified. No new numerical reference tolerance has been frozen in this development version.\n\n'
  for k,p in spec['panels'].items():sg+='## `'+k+'`\n\n'+spec['investigations'][k]+'\n\nAudit: '+p['rule']+'\n\n'
  sg+='## Scientific failures\n\n'+spec['pitfalls']+'\n\nA `bounded_failure` identifies the missing endpoints, observed problem, attempted scope and concrete release conditions. It may omit uncomputed panels. An input failure before any engine start may report zero resource counters, empty evidence arrays and no calculation records; never invent an output file to fill the contract. Preserve any actual diagnostics that do exist. Contract acceptance only confirms reporting format. Every core comparison remains necessary for scientific completion. Evidence-backed negative/indistinguishable conclusions receive the same standards as support. Optional extensions are not critical failures. Safe workspace-relative paths may have a leading `./`; parent traversal is forbidden.\n'
  write(dest/'agent_input/submission_guide.md',sg)
  ev=[{'evidence_id':'source_documents','source':source_docs,'context':spec['source_note'],'scope':'Source identities, methods and observations; author conclusions remain hypotheses for the expanded comparison.'},{'evidence_id':'extension','source':{'path':'evaluation/reference_validation_plan.md'},'scope':'Benchmark-authored controls; new numerical references and error calibration pending.'},{'evidence_id':'legacy','source':{'path':'evaluation/legacy_final_snapshot'},'scope':'Historical payload only. Old outputs/PASS certify no expanded endpoint.'}]
  items=[];rules=[];rubric=[]
  defs=[('identity','Correct objects, states, definitions and raw evidence.',spec['boundary']+' '+spec['reference_definition']+' '+spec['pitfalls'],['$.calculation_records','$.reference_definition'],10)]
  weights=[25,25,15] if len(spec['panels'])==3 else [20,20,15,10]
  for (k,p),w in zip(spec['panels'].items(),weights):defs.append((k,p['title'],p['rule'],['$.results.'+k,'$.calculation_records'],w))
  defs.append(('discrimination','Falsification and robustness based on actual controls.','Check distinct hypotheses against actual paired results and inspect quantitative changes under the sensitivity intervention. Uncomputed endpoints cannot be relabelled indistinguishable. '+spec['pitfalls'],['$.hypotheses','$.sensitivity','$.results'],15))
  for k,title,expected,fields,w in defs:
   items.append({'key_point_id':'kp_'+k,'statement':title,'expected':expected,'evidence_ids':['source_documents','extension']})
   rules.append({'rule_id':'rule_'+k,'reference_id':'kp_'+k,'type':'semantic','expected':expected,'binding':{'artifact_paths':['report/results.json','report/report.md'],'fields':fields,'comparison':expected},'evidence_policy':'Inspect real raw logs, models and analysis. Recompute all differences and verify named comparison coverage. Schema validity is not scientific validity.'})
   rubric.append({'id':k,'max_score':w,'description':title,'rule_ids':['rule_'+k]})
  final='Accept supported, refuted or evidence-sufficient indistinguishable conclusions from the complete required matrix. '+spec['objective']+' '+spec['pitfalls']+' No scientific completion from legacy scalars, missing controls or failed jobs. Reference calibration is pending; no fabricated numeric threshold applies.'
  conclusions={'paper_id':pid,'items':[{'conclusion_id':'con_expanded','claim_role':'final','statement':spec['objective'],'expected':final,'supporting_key_point_ids':[i['key_point_id'] for i in items],'evidence_ids':['source_documents','extension']}]}
  rules.append({'rule_id':'rule_conclusion','reference_id':'con_expanded','type':'semantic','expected':final,'binding':{'artifact_paths':['report/results.json','report/report.md'],'fields':['$.conclusion','$.results','$.sensitivity'],'comparison':final}});rubric.append({'id':'conclusion','max_score':10,'description':'Evidence-supported conclusion within the validated scope.','rule_ids':['rule_conclusion']})
  assert sum(x['max_score'] for x in rubric)==100
  evaluator={'reference_key_points.json':{'paper_id':pid,'items':items},'reference_conclusions.json':conclusions,'scoring_rules.json':{'paper_id':pid,'rules':rules,'scientific_rubric':rubric,'reference_stage':status,'completion_gate':{'requirements':complete,'missing_core_endpoint':'Scientific completion is false regardless of presentation/format credit.','blocked_input':blocked},'scoring_notes':['Development evaluator. Numerical tolerances require the expanded reference and independent run.','Score demonstrated coverage and correct calculation, never author agreement. Accept evidence-backed equivalent controls that preserve the same scientific factors and endpoint coverage; a changed method does not waive validation.','Do not promote bounded_failure to a scientific pass. Evidence-backed candidate collapse may satisfy the searched-candidate requirement, but failed numerical convergence alone cannot.']},'critical_failures.json':{'paper_id':pid,'items':[{'failure_id':'cf_identity_state_reference','condition':spec['pitfalls'],'severity':'scientifically serious'},{'failure_id':'cf_missing_expanded_matrix','condition':'Only old scalar endpoints, missing a named mandatory comparison, or unsupported uncertainty used as completed discrimination.','severity':'scientifically serious'},{'failure_id':'cf_fabrication','condition':'Failed or absent jobs, fabricated values, copied author answers or incompatible raw artifacts presented as scientific completion. Honest reported failure is not fabrication, but does not pass.','severity':'scientifically serious'},{'failure_id':'cf_overclaim','condition':'Local molecular descriptors or static thermodynamics used as proof of experimental yield, device performance, kinetics or bulk mechanisms outside the validated scope.','severity':'scientifically serious'}]},'evidence_map.json':{'paper_id':pid,'evidence':ev}}
  for n,x in evaluator.items():dump(dest/'evaluation'/n,x)
  old_reference='The former final package and all original evaluator/reference files are preserved byte-for-byte under `legacy_final_snapshot/`. They are historical records, not current scoring or upgraded verification. '+spec.get('legacy_reuse','Old identity and like-defined baseline outputs may be audited; none covers the added comparison matrix.')
  plan='# Expanded reference validation plan\n\nStatus: **'+status+'**. New scientific engine calculations in this upgrade: **0**.\n\n## Sources actually reviewed\n\n'+spec['source_note']+'\n\n'+'\n'.join('- `'+d['path']+'` — '+str(d.get('pages') or d.get('sections') or d.get('role')) for d in source_docs)+'\n\n## Historical reference boundary\n\n'+old_reference+'\n\n## Missing inputs / reference gaps\n\n'+'\n'.join('- '+x for x in blocked+spec['reference_gaps'])+'\n\n## Callable route and pilot\n\n'+spec['software']+' Interface availability does not establish this model or reference. See chemistry_toolbox/README.md, config/native_software_guides.yaml and config/mcp_profiles.yaml. No new paid service or long scientific run was started.\n\n'+spec['pilot']+'\n\n## Minimum complete reference\n\n'+'\n'.join(str(i+1)+'. '+spec['investigations'][k] for i,k in enumerate(spec['panels']))+'\n\nKeep initial/failed/final artifacts, independently recompute every reported difference, repeat the decisive sensitivity, and test support, refutation and justified ambiguity with the same rubric. Establish tolerances separately for source baseline, new controls, method differences and digitization/numerical errors. Until then, scoring is developmental, not calibrated.\n\n## Resource and release gate\n\nRecord actual scientific engine starts, failed/restarted jobs, allocated cores, summed job hours, CPU core-hours and parallel elapsed time. No estimated budget is an observed measurement. Finish an independent public-input run before considering release. Blocked inputs require the explicit conditions above; a source drawing, installation or old PASS does not remove them.\n'
  write(dest/'evaluation/reference_validation_plan.md',plan)
  audit={'batch':5,'date':'2026-09-27','paper_id':pid,'mode':mode,'source':str(source.relative_to(ROOT)),'source_package_content_sha256':json.loads((source/'package_manifest.json').read_text())['package_content_sha256'],'source_payload_snapshots':snapshots,'source_docs':source_docs,'old_class':RECORDS[pid]['current_class'],'new_class':RECORDS[pid]['target'],'status':status,'new_scientific_calculations_performed':False,'new_scientific_engine_starts':0,'short_checks':'Connectivity/formula/stoichiometry checks and synthetic format regressions only.','input_blockers':blocked,'new_reference_gaps':spec['reference_gaps'],'source_read_claim':'Relevant full-text pages/sections were read; list is not a claim that every page was scientifically revalidated.'}
  dump(old_audit,audit)
  info=json.loads((source/'task_info.json').read_text());info.update(title=('Autonomous investigation: ' if mode=='autonomous_research' else 'Paper reproduction and hypothesis testing: ')+spec['title'],category=('bounded candidate discovery' if RECORDS[pid]['target']=='C' else 'bounded scientific hypothesis testing'),difficulty='hard',difficulty_reasons=[spec['objective'],'Requires matched controls, state/model validation and uncertainty from real scientific evidence.'],data=[{'path':'data/inputs','description':'Expanded identities, explicit control definitions and authorized observations.'}],required_deliverables=[{'path':'report/results.json','description':'Auditable expanded matrix, raw evidence, hypotheses and robustness.'},{'path':'report/report.md','description':'Readable scientific reasoning linked to real artifacts.'}]);dump(dest/'task_info.json',info)
  if (dest/'paper_route.md').exists():write(dest/'paper_route.md','# Author route and expanded benchmark scope\n\n'+spec['author']+'\n\n## Expanded development scope\n\n'+spec['objective']+'\n\nStatus: '+status+'. Source numerical outputs and former reference remain private in evaluation/legacy_final_snapshot.\n')
  entries=package_payload_entries(dest);dump(dest/'package_manifest.json',{'paper_id':pid,'task_type':mode,'package_format':1,'agent_input_root':'agent_input','package_content_sha256':package_content_hash(entries),'entries':[x.model_dump(mode='json') for x in entries]})
  v=validate_task_package(dest)
  if v.status!='passed':raise RuntimeError((pid,mode,v.findings))
  print(pid,mode,status,'package validated',flush=True)
 # Save after each individual paper.
 row={'paper_id':pid,'status':status,'old_class':RECORDS[pid]['current_class'],'new_class':RECORDS[pid]['target'],'packages':{m:str((DEST/m/pid).relative_to(ROOT)) for m in MODES},'new_reference_gaps':spec['reference_gaps'],'blockers':blocked,'checks':{'validate_task_package':'passed','full_batch_regression':'pending'},'new_scientific_calculations_performed':False}
 path=B/'paper_status'/f'{pid}.json';dump(path,row)
 rows=[json.loads(p.read_text()) for p in sorted((B/'paper_status').glob('*.json'))]
 dump(B/'manifest.json',{'batch':5,'date':'2026-09-27','papers':rows,'scientific_engine_starts':0,'scope':'Development implementation; no expanded scientific PASS.'})
 present={r['paper_id']:r for r in rows};write(B/'STATUS.md','# 第5批状态\n\n逐篇保存。新增科学引擎计算：0。包检查不代表科学验证通过。\n\n'+'\n'.join('- '+x+'：'+(present[x]['status'] if x in present else '进行中：待实装') for x in IDS)+'\n')
 review='# '+pid+'\n\n## 科学升级\n\n'+RECORDS[pid]['first_version_spec']['matrix']+'\n\n'+spec['objective']+'\n\n## 实际核读与依据\n\n'+spec['source_note']+'\n\n## 评估与可行性\n\n权重为对象/定义10、新比较65、真实假设检验及稳健性15、结论10。各比较绑定具体JSON字段及原始产物。'+spec['software']+'\n\n状态：'+status+'。新增科学计算0；开发包完成不等于扩展参考通过。\n\n## 限制及解除条件\n\n'+'\n'.join('- '+x for x in blocked+spec['reference_gaps'])+'\n'
 write(B/'paper_reviews'/f'{pid}.md',review)

if __name__=='__main__':
 from paper_specs import SPECS
 selected=sys.argv[1:] or IDS
 for pid in selected:build(SPECS[pid])
