"""Offline tests for the authorized eight-paper staging repair.

Actual archived computations test compatibility only. Marked synthetic examples
test public schemas and the real submission checker; they are not new scientific
evidence or an AR replay. No QM/HPC/model requests or global code edits.
"""
from pathlib import Path
from copy import deepcopy as cp
import json,sys,tempfile,tarfile,hashlib,math,re

ROOT=Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from rcb_audit_20260929 import IDS,group
import jsonschema
from chemistry_toolbox.src.output_contract import validate_output_contract
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from evaluation.scoring.rules import check_rule
from jsonpath_ng import parse
from scripts.rebuild_final_manifests import rebuild

BASE=ROOT/'tasks/verified_tasks'
BACKUP=ROOT/'.git/maintenance_backups/20260929_eight_papers_repair'
passed=0;failures=[];rows=[]
def check(ok,label,detail=None):
 global passed
 if ok:passed+=1
 else:failures.append({'test':label,'detail':detail})
def load(p):return json.loads(p.read_text())
def branch_fields(value,key='required'):
 if isinstance(value,dict):
  if key in value:yield value[key]
  for v in value.values():yield from branch_fields(v,key)
 elif isinstance(value,list):
  for v in value:yield from branch_fields(v,key)
def synthetic_note():return 'SYNTHETIC submission-format case; not a scientific computation or historical AR record.'
def adapted(i,mode,raw):
 d=cp(raw)
 if i=='c49993ae88ffa0e3' and mode=='autonomous_research':d['states']=[dict(v,state_id=k) for k,v in d['states'].items()]
 return d
def positive(i,mode,d):
 x=cp(d)
 if mode=='autonomous_research' and i=='1255ed42fa7e12ff':
  x['hypotheses']=[{'statement':synthetic_note(),'test':synthetic_note(),'outcome':synthetic_note()}]
 if mode=='autonomous_research' and i=='3c89b494a1645491':
  x['hypotheses']=[{'label':'synthetic_format','prediction':synthetic_note(),'test':synthetic_note(),'outcome':synthetic_note()}]
 return x
def early_failure(i,mode,real):
 d=cp(real)
 d.pop('limitations',None);d.pop('uncertainty',None)
 if i=='589f72ac15eb7acd':
  d.update(status='bounded_failure',method={},systems={c:{s:{'outcome':'not_selected'} for s in ['HS','LS']} for c in ['C1','C2','C3']},
      partial_gaps_kj_mol={c:None for c in ['C1','C2','C3']},unresolved_states=['C1_HS','C1_LS','C2_HS','C2_LS','C3_HS','C3_LS'],available_comparison='No values computed: '+synthetic_note())
  for f in ['gaps_kj_mol','ordering_assessment']:d.pop(f,None)
 elif i=='3c3d73b8715d5fcd':
  d.update(completion_status='bounded_failure',method={},candidates=[],failure_account=synthetic_note());d.pop('observables',None)
 elif i=='c49993ae88ffa0e3':
  d.update(status='bounded_failure',method=synthetic_note(),partial_results=[],coverage=synthetic_note())
  for f in ['states','candidates','water_effect','sensitivity']:d.pop(f,None)
  if mode=='paper_reproduction':d.update(attempted_states=['pt_dry'],failure_diagnostics=[synthetic_note()])
  else:d.update(attempt_diagnostics=[{'hypothesis_id':'synthetic','diagnostic':synthetic_note()}])
 elif i=='c56ec62e92dbdfbc':
  d.update(status='bounded_failure',method={},candidates=[{'candidate_id':'failed_early','pathway_family':'attempt','validation':{'status':'failed','disposition':'failed before saddle','failure_reason':synthetic_note()}}],unresolved_blockers=[synthetic_note()])
  for f in ['selected_R_pathway_id','selected_S_pathway_id','barrier_R_kcal_mol','barrier_S_kcal_mol','delta_delta_G_dagger_kcal_mol','favored_configuration','selectivity_determining_event','step_comparison']:d.pop(f,None)
 elif i=='1e3a1d290a02e5f0':
  d['results']=[{'molecule_id':r['molecule_id'],'identity':r['identity'],'method':{},'status':'bounded_failure','failure_reason':synthetic_note(),'attempted_methods':synthetic_note()} for r in d['results']]
 elif i=='9e7293af88532cd4':
  d={'status':'bounded_failure','failure':{'failed_object':'water','attempted_method':synthetic_note(),'evidence':synthetic_note()}}
 elif i=='1255ed42fa7e12ff':
  d['results']=[{'compound':r['compound'],'identity':r['identity'],'status':'bounded_failure','barrier_kcal_mol':None,'rate_s_inv':None,'units':r['units'],'search_record':synthetic_note(),'failure_reason':synthetic_note()} for r in d['results']]
 elif i=='3c89b494a1645491':
  d.update(completion_status='bounded_failure',provenance={'software':synthetic_note(),'method':synthetic_note()},validation={},classification='unresolved',conclusion='unresolved')
  for r in d['contacts']:
   r.update(status='unavailable',notes=synthetic_note())
   for k in ['rho','laplacian','elf','H','V','G','V_over_G','DI']:r[k]=None
 return d

for mode in ['autonomous_research','paper_reproduction']:
 for i in IDS:rebuild(BASE/mode/('paper_'+i))
repository=TaskRepository(roots=[BASE])
with tarfile.open(BACKUP/'before_repair.tar.gz') as tar:
 for mode in ['autonomous_research','paper_reproduction']:
  for i in IDS:
   p=BASE/mode/('paper_'+i);label=mode+'/'+i
   schema_bytes=(p/'agent_input/submission_schema.json').read_bytes();schema=json.loads(schema_bytes)['result_schema']
   try:jsonschema.Draft202012Validator.check_schema(schema);check(True,label+' schema well formed')
   except Exception as ex:check(False,label+' schema well formed',str(ex));continue
   v=jsonschema.Draft202012Validator(schema)
   check(all(not {'limitations','uncertainty'} & set(x) for x in branch_fields(schema)),label+' no required generic disclaimers')
   raw=load(group(i)/'report/results.json');actual=adapted(i,mode,raw);valid=positive(i,mode,actual)
   raw_expected=not(mode=='autonomous_research' and i in ['1255ed42fa7e12ff','3c89b494a1645491'])
   cases=[('actual historical data'+(' with lossless state mapping' if i=='c49993ae88ffa0e3' and mode=='autonomous_research' else ''),actual,raw_expected),
       ('positive format fixture (synthetic AR wrapper where missing)',valid,True)]
   no=cp(valid);no.pop('limitations',None);no.pop('uncertainty',None);cases.append(('without generic disclaimers',no,True))
   blank=cp(valid)
   for k in ['limitations','uncertainty']:
    if k in blank:blank[k]=[] if isinstance(blank[k],list) else ''
   cases.append(('empty optional disclaimers',blank,True))
   extra=cp(no);extra['attempts']=[{'status':'failed','diagnostic':synthetic_note()}];cases.append(('success plus unsuccessful extra attempt',extra,True))
   early=early_failure(i,mode,valid);cases.append(('early failure without invented successful evidence',early,True))
   cases.append(('empty result is not success',{},False))
   if i=='589f72ac15eb7acd':
    for key in ['charge','multiplicity','energy_hartree','geometry_file','frequency_validation','convergence']:
     x=cp(valid);x['systems']['C1']['HS'].pop(key,None);cases.append(('selected state missing '+key,x,False))
    for key,value in [('charge',1),('multiplicity',1),('energy_hartree',None),('geometry_file',''),('frequency_validation',{})]:
     x=cp(valid);x['systems']['C1']['HS'][key]=value;cases.append(('invalid selected state '+key,x,False))
    x=cp(valid);x['unresolved_states']=[];cases.append(('complete result tolerates empty unresolved states',x,True))
    x=cp(early);x['unresolved_states']=[];cases.append(('failure needs actual unresolved state',x,False))
   if i=='3c3d73b8715d5fcd':
    for f in ['observables','candidates']:
     x=cp(valid);x.pop(f);cases.append(('complete missing '+f,x,False))
    x=cp(valid);x['candidates']=[];cases.append(('complete no validated candidates',x,False))
    x=cp(early);x['completion_status']='partial';cases.append(('truthful partial branch',x,True))
    x=cp(early);x['failure_account']='';cases.append(('failure has no explanation',x,False))
   if i=='c49993ae88ffa0e3':
    for f in ['candidates','states','coverage','conclusion','reference_convention']:
     x=cp(valid);x.pop(f,None);cases.append(('success missing '+f,x,False))
    if mode=='paper_reproduction':
     x=cp(valid);x['candidates']=[r for r in x['candidates'] if r['state_id']!='et_hydrated'];cases.append(('missing hydrated ET candidate class',x,False))
    else:
     x=cp(valid);x['states'][1]['state_id']=x['states'][0]['state_id'];cases.append(('different state rows with duplicate identity flagged semantically (schema not identity validator)',x,True))
   if i=='c56ec62e92dbdfbc':
    # Data-dependent ID joins are scientific review duties, not JSON Schema assertions.
    for configuration in ['R','S']:
     selected=[r for r in actual['candidates'] if r['candidate_id']==actual['selected_'+configuration+'_pathway_id']]
     check(len(selected)==1 and re.match(r'^'+configuration+r'(?:\s|$)',selected[0]['product_configuration']) and selected[0]['validation'].get('status','validated')=='validated',label+' archived selected '+configuration+' candidate resolves uniquely')
    x=cp(valid);x['unresolved_blockers']=[];cases.append(('successful result plus empty blockers',x,True))
    x=cp(valid)
    for f in ['selected_R_pathway_id','selected_S_pathway_id','barrier_R_kcal_mol','barrier_S_kcal_mol','delta_delta_G_dagger_kcal_mol']:x.pop(f,None)
    x['unresolved_blockers']=[synthetic_note()];cases.append(('success cannot borrow failure branch',x,False))
    x=cp(valid);x['candidates'][0]['validation'].pop('ts_geometry_file');cases.append(('selected legacy validated candidate missing TS',x,False))
    x=cp(valid);x['candidates'].append(early['candidates'][0]);cases.append(('success with explicit failed candidate alongside main results',x,True))
    x=cp(early);x['candidates'][0]['validation'].pop('failure_reason');cases.append(('failed candidate without diagnostic',x,False))
    x=cp(early);x['barrier_R_kcal_mol']=10;cases.append(('failure cannot claim complete-only barrier',x,False))
    x=cp(early);x['partial_results']=[{'candidate_id':'synthetic','barrier_kcal_mol':10,'evidence':synthetic_note()}];cases.append(('explicit partial data in failure',x,True))
   if i in ['1e3a1d290a02e5f0','1255ed42fa7e12ff']:
    key='molecule_id' if i=='1e3a1d290a02e5f0' else 'compound'
    x=cp(valid);x['results'][0]={key:x['results'][0][key]};cases.append(('identity alone cannot bypass row constraints',x,False))
    for name,mutate in [('reordered',lambda a:a.reverse()),('missing row',lambda a:a.pop()),('duplicate row',lambda a:a.__setitem__(1,cp(a[0]))),('unknown identity',lambda a:a[0].__setitem__(key,'unknown'))]:
     x=cp(valid);mutate(x['results']);cases.append(('canonical primary rows '+name,x,False))
    field='lambda_h_eV' if i=='1e3a1d290a02e5f0' else 'barrier_kcal_mol'
    x=cp(valid);x['results'][0][field]=None;cases.append(('validated result with null primary property',x,False))
    x=cp(valid);x['results'][0]=early['results'][0];cases.append(('one failed object preserves other valid primary objects',x,True))
   if i=='9e7293af88532cd4':
    x=cp(valid);x['endpoints'].reverse();cases.append(('endpoint order independent with stable identity',x,True))
    x=cp(valid);x['endpoints'][0]=cp(x['endpoints'][1]);cases.append(('duplicate endpoint rejected',x,False))
    x=cp(valid);x['thermochemistry'].pop('all_solutes_1M_kcal_mol');cases.append(('missing required thermochemical convention',x,False))
   if i=='1255ed42fa7e12ff':
    for key,val in [('rate_s_inv',0),('rate_s_inv',-1),('ts_id',None),('evidence',[])]:
     x=cp(valid);x['results'][0][key]=val;cases.append(('invalid validated '+key+' '+str(val),x,False))
    x=cp(valid);x['results'][0]['units']['rate']='ps^-1';cases.append(('wrong rate units',x,False))
   if i=='3c89b494a1645491':
    x=cp(valid);x['contacts'].reverse();cases.append(('contact order independent',x,True))
    for kind in ['duplicate','null','missing','empty notes']:
     x=cp(valid)
     if kind=='duplicate':x['contacts'][1]=cp(x['contacts'][0])
     if kind=='null':x['contacts'][0]['DI']=None
     if kind=='missing':x['contacts'].pop()
     if kind=='empty notes':x['contacts'][0]['notes']=''
     cases.append(('contacts '+kind,x,kind=='empty notes'))
    x=cp(early);x['completion_status']='complete';cases.append(('complete cannot contain unavailable contacts',x,False))
    x=cp(early);x['contacts'][0]['notes']='';cases.append(('unavailable requires specific note',x,False))
   with tempfile.TemporaryDirectory(prefix='rcb-eight-regression-') as tmp:
    w=Path(tmp);(w/'report').mkdir()
    for title,d,expected in cases:
     errors=list(v.iter_errors(d));check((not errors)==expected,label+' schema '+title,[{'path':e.json_path,'error':e.message[:250]} for e in errors[:2]])
     (w/'report/results.json').write_text(json.dumps(d))
     observed=validate_output_contract(w,schema_bytes,max_errors=3)
     check(observed['valid']==expected,label+' runner '+title,observed['errors'])
   report=rebuild(p);pkg=validate_task_package(p);check(pkg.status=='passed',label+' package manifest',str(pkg.findings)[:1200])
   runtime=load_runtime_evaluation(paper_id=p.name,task_type=mode,repository=repository)
   check(runtime.policy_id=='dual_axis_100.scientific_results.v1',label+' actual runtime policy')
   rt=runtime.ground_truth['rule_table'];check(all(r['diagnostic'] is None for r in rt),label+' rules resolve to live IDs')
   kps=load(p/'evaluation/reference_key_points.json')['items'];cons=load(p/'evaluation/reference_conclusions.json')['items']
   allkp={k['key_point_id'] for k in kps}
   check(all(set(c['supporting_key_point_ids'])<=allkp for c in cons),label+' conclusions resolve to live KPs')
   check(not any(c.get('claim_role')=='limitation' for c in cons),label+' no limitation conclusion')
   check(all(r['association']!='standalone' for r in rt),label+' scientific and process rules linked to live conclusions')
   check(all('$.limitations' not in r['rule'].get('binding',{}).get('fields',[]) and '$.uncertainty' not in r['rule'].get('binding',{}).get('fields',[]) for r in rt),label+' no disclaimer scoring bindings')
   nr=load(p/'evaluation/scoring_rules.json')['rules'];old=json.loads(tar.extractfile(str((p/'evaluation/scoring_rules.json').relative_to(ROOT))).read())['rules']
   for r in old:
    if r.get('type')=='numeric':
     n=next((x for x in nr if x['rule_id']==r['rule_id']),None)
     check(n is not None and (n.get('target'),n.get('tolerance'))==(r.get('target'),r.get('tolerance')),label+' unchanged numerical target/tolerance '+r['rule_id'])
   numeric=[]
   for entry in rt:
    rule=entry['rule']
    if rule['type']!='numeric':continue
    result=check_rule(entry,{'report/results.json':actual});numeric.append(result)
    if result['assessment']=='pass':
     bad=cp(actual);selector=rule['binding']['fields'][0];parse(selector).update(bad,rule['target']+rule['tolerance']+1)
     check(check_rule(entry,{'report/results.json':bad})['assessment']=='fail',label+' wrong numeric value rejected '+rule['rule_id'])
    elif result['assessment']=='fail':check(False,label+' actual numeric value outside unchanged range '+rule['rule_id'],result)
    if i=='1255ed42fa7e12ff' and rule['rule_id'].startswith('r4_'):
     value=parse(rule['binding']['fields'][0]).find(actual)[0].value
     check(abs(math.log10(value)-math.log10(rule['target']))<=rule['tolerance'],label+' actual log-rate '+rule['rule_id'])
   if i=='1255ed42fa7e12ff':
    for r in actual['results']:
     k=1.380649e-23*298.15/6.62607015e-34*math.exp(-r['barrier_kcal_mol']*4184/(8.31446261815324*298.15))
     check(abs(k-r['rate_s_inv'])/k<1e-8,label+' actual barrier/rate consistency '+r['compound'])
   task=(p/'agent_input/task.md').read_text();heads=re.findall(r'^# (.+)$',task,re.M)
   expected=['Scientific objective']+(['Author-provided scientific guidance'] if mode=='paper_reproduction' else [])+['Public inputs and scientific boundaries','Required scientific validation/investigation','Deliverables']
   check(heads==expected,label+' instruction heading order',heads)
   check(not any(x.is_symlink() for x in p.rglob('*')),label+' no package symlink')
   for f in (p/'agent_input/data').rglob('*'):
    if f.is_file():
     oldbytes=tar.extractfile(str(f.relative_to(ROOT))).read()
     check(f.read_bytes()==oldbytes,label+' unchanged scientific input '+str(f.relative_to(p)))
   if i=='3c3d73b8715d5fcd':
    private=p/'evaluation/author_results/invalid_mixed_coordinate_fragment.xyz'
    oldbytes=tar.extractfile(str((p/'agent_input/data/inputs/README_coordinates.xyz').relative_to(ROOT))).read()
    check(not(p/'agent_input/data/inputs/README_coordinates.xyz').exists() and private.read_bytes()==oldbytes,label+' invalid Rh fragment preserved privately')
   for dest in ['final_verified_'+mode,'hold_verified_'+mode]:check(not(ROOT/'tasks'/dest/p.name).exists(),label+' no migration '+dest)
   rows.append({'paper_id':p.name,'mode':mode,'contract_cases':len(cases),'actual_historical_contract_valid':raw_expected,'historical_adaptation':'lossless state object-to-array mapping' if i=='c49993ae88ffa0e3' and mode=='autonomous_research' else 'none','synthetic_AR_wrapper_used_for_format_only':not raw_expected,'key_points':len(kps),'conclusions':len(cons),'policy':runtime.policy_id,'numeric_screen':numeric})

meta=load(BACKUP/'baseline.json')
for rel,digest in meta['source_files'].items():check((ROOT/rel).is_file() and hashlib.sha256((ROOT/rel).read_bytes()).hexdigest()==digest,'source unchanged '+rel)
out={'passed':passed,'failed':len(failures),'failures':failures,'packages':rows,'scope':'Offline schema, actual runner, runtime policy/bindings and archived numerical checks; synthetic negative cases are not scientific validation. No new QM/HPC, LLM judge, AR blind replay, deployment isolation or migration.'}
path=BASE/'maintenance_tools/repair_checks_20260929.json';path.write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'passed':passed,'failed':len(failures),'failures':failures,'packages':len(rows),'report':str(path)},ensure_ascii=False,indent=2))
raise SystemExit(bool(failures))
