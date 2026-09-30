"""Batch 2 development authoring. Never runs electronic-structure jobs.

All mutations are restricted to the assigned upgrade packages and this directory.
Existing destinations are never copied over; edits require our provenance marker.
"""
from pathlib import Path
from copy import deepcopy
import hashlib, json, shutil, sys
ROOT=Path(__file__).resolve().parents[4]
B=Path(__file__).resolve().parent
sys.path.insert(0,str(ROOT))
from evaluation.contracts.task_package import package_payload_entries,package_content_hash
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
A=json.loads((B/'assignment.json').read_text()); IDS=A['batch']['papers']
RECORDS={r['paper_id']:r for r in A['records']}
MODES=['autonomous_research','paper_reproduction']
OPTIONAL_EN=dict(zip(IDS,[
'Full concentration-dependent kinetics, films, TTA efficiency and nonadiabatic propagation are outside this version.',
'Complete C–Cl dissociation, substrate yields and the full catalytic cycle are outside this version.',
'The other 42 members, dynamic response at 4556 nm and material-design extrapolation are optional future extensions.',
'Other natural products, synthetic routes and pharmacology are outside this version.',
'Explicit solvent is optional only when justified by continuum residuals; cellular and antimicrobial extrapolation is outside scope.',
'Bulk carrier separation and hydrogen-production rates are outside the finite-oligomer task.',
'Dissociation networks and emission lifetimes are future extensions; four covalent triflates must remain part of compound 2.',
'Molecular targets, docking, cross-strain generalization and drug discovery are outside scope.',
'Film quantum yields and complete nonradiative dynamics are outside scope.',
'A comprehensive solvent library and kinetic lifetimes are outside scope.',
'Different protonation states, charges and antifungal pharmacology must not be mixed into the same ensemble.',
'Optoelectronic device response and complete solid-state packing are outside this version.'
]))
FIVE=['reference_key_points.json','reference_conclusions.json','scoring_rules.json','critical_failures.json','evidence_map.json']
def dump(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def S(description='Nonempty scientific explanation'):return {'type':'string','minLength':1,'description':description}
def N(description=''):return {'type':'number',**({'description':description} if description else {})}
def I(minimum=0):return {'type':'integer','minimum':minimum}
def E(*values):return {'type':'string','enum':list(values)}
def C(v):return {'const':v}
def O(**props):return {'type':'object','additionalProperties':False,'required':list(props),'properties':props}
def L(item,minn=1):return {'type':'array','minItems':minn,'items':item}
def V(n=3):return {'type':'array','minItems':n,'maxItems':n,'items':N()}
P={'type':'string','pattern':r'^(?!.*(?:^|/)\.\.(?:/|$))(?!.*//)(?:\./)*(?:outputs|analysis|structures)/[A-Za-z0-9_.\-/]+$'}
EV=L(P)
def row(**props):return O(**props,calculation_ids=L(S()),evidence_files=EV)
def table(keys,schema):return O(**{k:deepcopy(schema) for k in keys})
def collapse(schema):
 good=deepcopy(schema);good['properties']['outcome']=C('resolved');good['required'].append('outcome')
 other=O(outcome=C('collapsed_to_other_basin'),destination_id=S(),initial_geometry=P,final_geometry=P,trajectory_evidence=EV,physical_interpretation=S())
 return {'oneOf':[good,other]}
def molecule(id,smiles,q=0,m=1,source='Benchmark identity transcribed from cited structural definition',keep_maps=False):
 params=Chem.SmilesParserParams();params.removeHs=False
 mol=Chem.MolFromSmiles(smiles,params)
 if mol is None:raise ValueError((id,smiles))
 if not keep_maps:
  for a in mol.GetAtoms():a.SetAtomMapNum(a.GetIdx()+1)
 if Chem.GetFormalCharge(mol)!=q:raise ValueError(('charge',id,Chem.GetFormalCharge(mol),q))
 rad=sum(a.GetNumRadicalElectrons() for a in mol.GetAtoms())
 if rad!=m-1:raise ValueError(('radicals',id,rad,m))
 return {'id':id,'mapped_smiles':Chem.MolToSmiles(mol),'formula':rdMolDescriptors.CalcMolFormula(mol),'charge':q,'multiplicity':m,'source':source,'atom_mapping':'Integer atom maps identify graph atoms; retain maps across generated coordinates. Add explicit hydrogens deterministically and record their parent map. No reference geometry is supplied.'}
def source_input(pid,name):return ROOT/'tasks/final_verified_paper_reproduction'/pid/'agent_input/data/inputs'/name
def contract(spec):
 species=spec['species'];states={x['id']:(x['charge'],x['multiplicity']) for x in species}
 rec=O(calculation_id=S(),system=E(*states),record_type=E('electronic_structure','analysis'),kind=E('completed','failed'),method=S(),environment=S(),input_file=P,output_file=P,convergence=S())
 rec['properties'].update(charge={'type':'integer'},multiplicity=I(1),basis=S(),geometry_role=E('relaxed_minimum','constrained_control','single_point','excited_state'),geometry_file=P,electronic_energy_hartree=N(),imaginary_frequencies_cm1=L(N(),0),state_identity=S(),failure_reason=S(),analysis_type=S(),source_evidence_files=EV)
 rec['allOf']=[{'if':{'properties':{'system':C(k)}},'then':{'properties':{'charge':C(q),'multiplicity':C(m)}}} for k,(q,m) in states.items()]
 rec['allOf'] += [{'if':{'properties':{'record_type':C('electronic_structure')}},'then':{'required':['charge','multiplicity','basis','geometry_role']}},{'if':{'properties':{'kind':C('completed'),'record_type':C('electronic_structure')}},'then':{'required':['geometry_file','electronic_energy_hartree','state_identity']}},{'if':{'properties':{'record_type':C('analysis')}},'then':{'required':['analysis_type','source_evidence_files']}},{'if':{'properties':{'kind':C('failed')}},'then':{'required':['failure_reason']}}]
 methods=O(primary=S(),software_versions=S(),solvent_and_state_convention=S(),energy_zero_and_units=S(),state_matching=S(),conformer_coverage=S(),uncertainty_protocol=S())
 result=O(**{p['id']:p['schema'] for p in spec['panels']})
 schema=O(paper_id=C(spec['id']),status=E('complete','bounded_failure','blocked'),methods=methods,resources=O(engine_calls=I(),wall_seconds={'type':'number','minimum':0},cpu_core_hours={'type':['number','null'],'minimum':0},max_memory_MB={'type':['number','null'],'minimum':0},accounting_basis=S(),attempt_log=P),calculation_records=L(rec,0),evidence_files=EV,conclusion=O(verdict=E('supported','refuted','indistinguishable','not_established'),claim=S(),scope_limit=S(),evidence_files=EV))
 schema['$schema']='https://json-schema.org/draft/2020-12/schema'
 schema['properties'].update(results=result,hypotheses=L(O(id=S(),prediction=S(),falsifier=S(),discriminating_panel=E(*[p['id'] for p in spec['panels']])) ,2),sensitivity=L(row(setting=S(),baseline_value=N(),perturbed_value=N(),unit=S(),conclusion_changed={'type':'boolean'},uncertainty_basis=S())),failure_report=O(attempted_scope=S(),observed_failure=S(),missing_endpoints=L(S()),recovery_condition=S(),evidence_files=EV))
 schema['allOf']=[
  {'if':{'properties':{'status':C('complete')}},'then':{'required':['results','hypotheses','sensitivity'],'properties':{'conclusion':{'properties':{'verdict':E('supported','refuted','indistinguishable')}},'calculation_records':{'contains':{'properties':{'kind':C('completed'),'record_type':C('electronic_structure')},'required':['kind','record_type']}}}}},
  {'if':{'properties':{'status':E('bounded_failure','blocked')}},'then':{'required':['failure_report'],'properties':{'conclusion':{'properties':{'verdict':C('not_established')}}}}},
  {'if':{'properties':{'calculation_records':{'maxItems':0}}},'then':{'properties':{'resources':{'properties':{'engine_calls':C(0)}}}}}
 ]
 return {'required_files':['report/results.json','report/report.md'],'primary_result_file':'report/results.json','report_file':'report/report.md','result_schema':schema}

def build(spec):
 pid=spec['id'];assert pid in IDS
 status=spec.get('status','implemented_pending_expanded_reference')
 sources=json.loads((B/'source_reviews'/pid/'sources.json').read_text())
 baseobjective=spec['objective']
 boundary=spec['boundary']+' All required comparisons are core; the optional extension listed below is not a completion condition. A documented failure is a valid submission but is not scientific completion. Evidence-supported collapse of an initialized basin, or inability to distinguish explanations after completing the core matrix, is scientifically admissible. An unattempted core comparison cannot be replaced by an uncertainty statement.'
 public={'paper_id':pid,'scope':baseobjective,'species':spec['species'],'controls':spec['controls'],'source_notes':spec['public_sources'],'molecular_boundary':boundary,'optional_not_required':OPTIONAL_EN[pid]}
 c=contract(spec)
 expected={'identity': 'Verify every supplied molecular graph, atom correspondence, charge/spin and environment against actual inputs and outputs; minimum claims require frequency evidence; constrained geometries are not minima.'}
 expected.update({p['id']:p['criteria'] for p in spec['panels']})
 expected['robustness']='Recompute the declared sensitivity comparison from raw evidence. Freeze fitting/selection choices before holdout evaluation where required. Propagate method, state matching, sampling and numerical uncertainty without fitting a tolerance to the answer.'
 kp=[];rules=[];rubric=[]
 weights=[10]+[p['weight'] for p in spec['panels']]+[15]
 assert sum(weights)==90,(pid,weights)
 for (key,statement),weight in zip(expected.items(),weights):
  kp.append({'key_point_id':'kp_'+key,'key_point_type':'result' if key!='identity' else 'process','statement':statement,'expected':statement,'evidence_ids':['paper_main','paper_si','benchmark_extension']})
  fields=['$.calculation_records','$.methods','$.evidence_files'] if key=='identity' else (['$.sensitivity','$.hypotheses'] if key=='robustness' else ['$.results.'+key,'$.calculation_records','$.evidence_files'])
  rules.append({'rule_id':'r_'+key,'reference_id':'kp_'+key,'type':'condition' if key=='identity' else 'semantic','expected':statement,'binding':{'artifact_paths':['report/results.json','report/report.md'],'fields':fields,'comparison':statement+' Inspect the referenced native input/output, final mapped structures and analysis code. Recompute reported differences and transformations. A JSON value or literature quotation alone earns no calculated-result credit.'},'evidence_policy':'All artifact references must resolve inside the submission; successful job termination, correct object and actual requested property must be independently checked.'})
  rubric.append({'id':key,'max_score':weight,'description':statement,'rule_ids':['r_'+key]})
 conclusion='Determine whether the proposed explanation survives the expanded comparisons: '+spec['conclusion']+' Support, refutation and evidence-sufficient indistinguishability are scored equally for scientific reasoning. No expected winner or old scalar agreement is a completion criterion.'
 rules.append({'rule_id':'r_conclusion','reference_id':'conclusion_investigation','type':'semantic','expected':conclusion,'binding':{'artifact_paths':['report/results.json','report/report.md'],'fields':['$.conclusion','$.results','$.sensitivity'],'comparison':conclusion}})
 rubric.append({'id':'conclusion','max_score':10,'description':conclusion,'rule_ids':['r_conclusion']})
 critical=['Only the legacy scalar or original narrow systems are submitted; the expanded core comparisons are missing.','Wrong molecular graph, atom mapping, charge, spin, stoichiometry, solvent, electronic state, or incompatible energy reference is used.','Failed or unconverged calculations, fabricated artifacts, literature/reference numbers, or archived PASS are represented as new successful calculations.','Core controls or holdout tests are absent but an uncertainty statement is used to claim completion.','Raw evidence files are missing, point outside the submitted workspace, or contradict the reported numerical results.']+spec['critical']
 evidence=[]
 for label,stem in [('paper_main','main.pdf'),('paper_si','supplementary_001.pdf')]:
  src=next(s for s in sources if s['path'].endswith('/'+stem))
  evidence.append({'evidence_id':label,'source':{'path':src['path'],'sha256':src['sha256'],'pdf_pages_1_based':spec['pages'][label]},'scope':spec['source_review'][label],'context':'Source evidence was inspected during development. Calculated author outcomes and reference coordinates are private; public input includes only the permitted identity/observational subset.'})
 evidence.append({'evidence_id':'benchmark_extension','source':{'path':'docs/evalution/update/'+pid+'.md','sha256':sha(ROOT/'docs/evalution/update'/f'{pid}.md')},'scope':'First-version core specification plus source-grounded corrections described in upgrade_audit.json; added controls are benchmark interventions, not author experiments.'})
 evaluations={'reference_key_points.json':{'paper_id':pid,'items':kp},'reference_conclusions.json':{'paper_id':pid,'items':[{'conclusion_id':'conclusion_investigation','claim_role':'final','statement':conclusion,'expected':conclusion,'supporting_key_point_ids':[k['key_point_id'] for k in kp],'evidence_ids':['paper_main','paper_si','benchmark_extension']}]},'scoring_rules.json':{'paper_id':pid,'scoring_policy':'dual_axis_100.scientific_results.v1','rules':rules,'scientific_rubric':rubric,'reference_stage':'development_pending_expanded_reference_calculations','scoring_notes':['Transport/schema validation does not validate scientific conclusions. Expanded references have not been calculated.','No new numerical reference tolerance is asserted. Compare internal differences with computed numerical, sampling and method uncertainty; calibrate external tolerances only after the reference-validation plan.','Legacy scalar targets and narrow tolerances are historical evidence only and are not reused as expanded acceptance bands.','Optional extensions have zero required weight. Honest failure is accepted for audit, not counted as complete or awarded absent-result points.']},'critical_failures.json':{'paper_id':pid,'items':[{'failure_id':f'cf_{i+1}','condition':t,'severity':'scientifically serious'} for i,t in enumerate(critical)]},'evidence_map.json':{'paper_id':pid,'evidence':evidence}}
 outputs=[]
 for mode in MODES:
  source=ROOT/'tasks'/('final_verified_'+mode)/pid;dest=ROOT/'tasks/upgrade_tasks'/mode/pid
  auditpath=dest/'evaluation/task_provenance/upgrade_audit.json'
  if not dest.exists():
   shutil.copytree(source,dest)
   snapshots={}
   for f in sorted(source.rglob('*')):
    if f.is_file():
     rel=f.relative_to(source);snap=Path('evaluation/legacy_final_snapshot')/(str(rel)+'.snapshot')
     (dest/snap).parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(f,dest/snap)
     snapshots[str(rel)]={'snapshot':str(snap),'sha256':sha(f)}
   dump(auditpath,{'authoring_owner':'batch2_20260927','source_payload_snapshots':snapshots,'initialization_only':True})
   # All previous payload bytes are archived before replacing obsolete public/evaluation content.
   shutil.rmtree(dest/'agent_input');(dest/'agent_input/data/inputs').mkdir(parents=True)
   for f in (dest/'evaluation').iterdir():
    if f.name not in ['legacy_final_snapshot','task_provenance']:
     shutil.rmtree(f) if f.is_dir() else f.unlink()
  prior=json.loads(auditpath.read_text())
  if prior.get('authoring_owner')!='batch2_20260927':raise RuntimeError('Existing progress owned elsewhere: '+str(dest))
  dump(dest/'agent_input/data/inputs/research_matrix.json',public)
  for name,value in spec.get('data',{}).items():
   target=dest/'agent_input/data/inputs'/name
   if isinstance(value,Path):shutil.copyfile(value,target)
   elif isinstance(value,str):target.write_text(value)
   else:dump(target,value)
  dump(dest/'agent_input/submission_schema.json',c)
  task='# Scientific objective\n\n'+baseobjective+'\n'
  if mode=='paper_reproduction':task+='\n# Author-provided scientific guidance\n\n'+spec['author']+' The added comparisons below are benchmark extensions; do not represent them as calculations or controls performed by the authors. Reproduce a defensible source baseline, then test its interpretation.\n'
  task+='\n# Public inputs and scientific boundaries\n\nRead `data/inputs/research_matrix.json` and its listed companion data. The mapped graphs, explicit control definitions and observations define the authorized objects in both task modes. '+boundary+'\n\n'+spec.get('availability','This is a development task with an expanded scientific contract; no supplied coordinate is a validated expanded reference.')+'\n'
  task+='\n# Required scientific validation/investigation\n\n'
  for i,p in enumerate(spec['panels'],1):task+=f'{i}. **{p["title"]}.** {p["criteria"]}\n\n'
  task+='Validate identity and convergence before interpreting results. Report at least two falsifiable competing explanations and an explicit numerical sensitivity comparison. Retain native inputs, full outputs, mapped final geometries and executable analysis with all intermediate tables. Report what would overturn your interpretation. Do not equate a constrained point, an SCF energy or a process return code with a local minimum.\n\nOptional, not required: '+OPTIONAL_EN[pid]+'\n\n# Deliverables\n\nSubmit `report/results.json` conforming to `submission_schema.json` and a readable `report/report.md`. See `submission_guide.md` for units, coverage and raw-evidence requirements. A bounded failure or blocked submission must identify attempted work, missing endpoints, raw diagnostics and a concrete recovery condition.\n'
  (dest/'agent_input/task.md').write_text(task)
  guide='# Submission guide\n\nThe contract requires both report/results.json and report/report.md. `status=complete` requires every named panel and every member of its matrix; it does not guarantee scientific validity. `bounded_failure` or `blocked` requires a failure_report and verdict not_established.\n\n'
  guide+='Each numerical row binds to calculation_ids and evidence_files. These IDs must resolve to calculation_records. Evidence paths must be relative below outputs/, structures/ or analysis/; a harmless ./ segment is permitted, while .. traversal is prohibited. Supply actual files, not only names. Electronic-structure records require basis, q/M and geometry role; completed engine records additionally require geometry, electronic energy and state identity. Analysis records instead require analysis_type and source_evidence_files and do not invent an electronic energy. A pre-engine failure may submit zero calculation_records and engine_calls=0 with an actual attempt/diagnostic log and failure_report; it cannot claim scientific completion. Record method/version, solvent, units and energy zero. Preserve absolute energies before taking differences; report constrained single points separately from free energies of minima.\n\n'
  for p in spec['panels']:guide+=f'## results.{p["id"]}\n\n{p["criteria"]}\n\n'+p.get('units','Field names encode units; dimensionless quantities must be identified. No benchmark target values are provided.')+'\n\n'
  guide+='## Evidence and interpretation\n\nSubmit calculation input/output, final geometries with atom correspondence, frequency results when claiming minima, state/tensor/orbital data when relevant, and analysis code/tables sufficient to recompute the panels. Report per-attempt provenance and failures. The resources object records actual engine-call count, elapsed time and available CPU/memory accounting; null CPU or memory means unmeasured, never zero-cost evidence. Sensitivity requires numerical baseline and perturbation under a stated unit and uncertainty model. Do not invent a precision or tolerance from the old task. `indistinguishable` is a conclusion after the required comparisons, not an alternative to doing them. Optional extensions are not required.\n'
  (dest/'agent_input/submission_guide.md').write_text(guide)
  for name,v in evaluations.items():dump(dest/'evaluation'/name,v)
  old=json.loads((source/'task_info.json').read_text());old.update(title=spec['title'],difficulty='hard',difficulty_reasons=[p['title'] for p in spec['panels']],data=[{'path':'data/inputs/'+f.name,'description':'Expanded public identity, control or observational input; '+spec['title']} for f in sorted((dest/'agent_input/data/inputs').iterdir())],required_deliverables=[{'path':'report/results.json','description':'Structured expanded research matrix and evidence bindings'},{'path':'report/report.md','description':'Readable scientific investigation, competing explanations and limits'}])
  dump(dest/'task_info.json',old)
  (dest/'paper_route.md').write_text('# Development route\n\n'+spec['title']+'\n\nSource: '+str(source.relative_to(ROOT))+'\n\nClass: '+RECORDS[pid]['current_class']+' → '+RECORDS[pid]['target']+'; status: '+status+'.\n\nThe public task and submission contract define the core. Native Gaussian/ORCA, conformer tools and analysis are usable only after checking the installed capability and guide. No expanded reference PASS is claimed.\n')
  plan='# Expanded reference validation plan\n\nStatus: '+status+'. No new quantum-chemical reference calculation was performed during package development.\n\n## Inspected primary evidence\n\n'
  for k in ['paper_main','paper_si']:plan+=f'- {k}, PDF pages {spec["pages"][k]}: {spec["source_review"][k]}\n'
  plan+='\n## Reusable legacy evidence\n\n'+spec['legacy']+' The private legacy_final_snapshot is a byte-for-byte provenance archive, not new completion evidence.\n\n## New reference gaps\n\n'+spec['gaps']+'\n\n## Minimum pilot\n\n'+spec['pilot']+'\n\n## Full expanded validation\n\nExecute the complete public matrix, inspect identities and raw outputs, reproduce all new differences and sensitivity analyses, and independently review the claimed discrimination. Calibrate property-specific method/sampling errors before any numerical acceptance bands. Do not reuse narrow legacy tolerances. Document failed, collapsed and unresolved candidates rather than inventing minima.\n\n## Available route and resource boundary\n\n'+spec['software']+' Consult chemistry_toolbox/README.md, config/native_software_manual_profiles.yaml, native_software_docs/gaussian/QUICKSTART.md, orca/EXCITED_STATES.md, crest/CONFORMER_SEARCH.md and goodvibes/QUICKSTART.md as applicable. Listed capabilities are not proof that this expanded system has run. Use inspect_software and validate_native_job before submission. This authoring run did not submit long jobs, HPC work or paid services.\n'
  (dest/'evaluation/reference_validation_plan.md').write_text(plan)
  audit={'authoring_owner':'batch2_20260927','paper_id':pid,'task_type':mode,'date':'2026-09-27','source':str(source.relative_to(ROOT)),'source_manifest_sha256':sha(source/'package_manifest.json'),'source_package_content_sha256':json.loads((source/'package_manifest.json').read_text())['package_content_sha256'],'source_payload_snapshots':prior['source_payload_snapshots'],'source_docs':sources+[{'path':'docs/evalution/update/'+pid+'.md','sha256':sha(ROOT/'docs/evalution/update'/f'{pid}.md')}],'historical_evidence_review':{'path':str((B/'source_reviews/history_reports.json').relative_to(ROOT)),'sha256':sha(B/'source_reviews/history_reports.json'),'scope':'Legacy report read when present; never reused as expanded completion.'},'old_class':RECORDS[pid]['current_class'],'new_class':RECORDS[pid]['target'],'status':status,'new_scientific_calculations_performed':False,'short_checks_performed':['RDKit graph parsing/formula/charge/radical checks where mapped SMILES provided','Primary PDF text/selected figures inspected','Package/schema/runtime/export regression reported separately'],'source_corrections':spec.get('corrections',[]),'new_reference_gaps':spec['gaps'],'blockers':spec.get('blockers',[]),'optional_not_required':OPTIONAL_EN[pid]}
  dump(auditpath,audit)
  entries=package_payload_entries(dest);manifest={'paper_id':pid,'task_type':mode,'package_format':1,'agent_input_root':'agent_input','package_content_sha256':package_content_hash(entries),'entries':[e.model_dump(mode='json') for e in entries]};dump(dest/'package_manifest.json',manifest)
  outputs.append({'path':str(dest.relative_to(ROOT)),'task_type':mode,'package_content_sha256':manifest['package_content_sha256']})
 summary={'paper_id':pid,'title':spec['title'],'status':status,'packages':outputs,'new_reference_gaps':spec['gaps'],'blockers':spec.get('blockers',[]),'source_review':spec['source_review'],'source_corrections':spec.get('corrections',[]),'check_summary':'Package-specific checks pending final batch regression; no scientific validation claimed.'}
 dump(B/'paper_status'/f'{pid}.json',summary)
 update_status()
 print(pid,status,flush=True)
def update_status():
 rows=[]
 for pid in IDS:
  f=B/'paper_status'/f'{pid}.json';r=json.loads(f.read_text()) if f.exists() else {}
  rows.append('| '+pid+' | '+r.get('status','进行中：源文与输入核对')+' | '+('2 包已保存；待批次检查' if r else '尚未写入开发包')+' |')
 (B/'STATUS.md').write_text('# 第 2 批实施状态\n\n仅本批 12 篇；不启动长量化计算。开发完成不等于新版科学验证通过。\n\n| 论文 | 状态 | 进度 |\n|---|---|---|\n'+'\n'.join(rows)+'\n')
