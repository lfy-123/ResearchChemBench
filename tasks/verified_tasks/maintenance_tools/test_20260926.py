"""Scoped offline regression; synthetic submissions are never verification evidence.

Reads current tasks and historical results. Writes only disposable temporary test
workspaces. No QM/HPC/network/model calls, task edits or migration.
"""
from pathlib import Path
import sys, json, re, copy, tempfile, math
import subprocess
sys.path.insert(0,str(Path(__file__).resolve().parents[3]))
import jsonschema
from jsonpath_ng import parse
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository, materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from evaluation.scoring.rules import check_rule
from chemistry_toolbox.src.output_contract import validate_output_contract
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds, rdMolDescriptors
import networkx as nx

ROOT=Path('tasks/verified_tasks');BASE=Path.cwd();passed=0;failures=[];rows=[]
def check(ok,label,detail=None):
 global passed
 if ok:passed+=1
 else:failures.append({'test':label,'detail':detail})

def drop_caveats(x):
 if isinstance(x,dict):
  for k in list(x):
   if k in ['limitations','stopping_rule','stopping_criterion','stopping_basis','unresolved_alternatives']:del x[k]
   else:drop_caveats(x[k])
 elif isinstance(x,list):
  for v in x:drop_caveats(v)

def add_empty_caveats(x, schema):
 # Only optional compatibility fields, never manufacture scientific results.
 if isinstance(x,dict):
  for name,prop in schema.get('properties',{}).items():
   if name in ['limitations','stopping_rule','stopping_criterion','stopping_basis','unresolved_alternatives']:
    x[name]=[] if prop.get('type')=='array' else ''
   elif name in x:add_empty_caveats(x[name],prop)
 elif isinstance(x,list):
  for v in x:add_empty_caveats(v,schema.get('items',{}))
 for key in ['oneOf','anyOf','allOf']:
  for branch in schema.get(key,[]):add_empty_caveats(x,branch)

def ts_input_check(p,d):
 system=json.loads((p/'agent_input/data/inputs/system.json').read_text())
 template=Chem.AddHs(Chem.MolFromSmiles(system['smiles']))
 starter=molecule(p/'agent_input/data/inputs/radical_starter.xyz')
 check(rdMolDescriptors.CalcMolFormula(template)==system['formula'] and template.GetNumAtoms()==53,str(p)+' starter formula')
 check(set(graph(template).edges)==set(graph(starter).edges),str(p)+' XYZ matches explicit SMILES connectivity')
 check([a.GetSymbol() for a in template.GetAtoms()]==[a.GetSymbol() for a in starter.GetAtoms()],str(p)+' starter atom order')
 check([(a.GetIdx()+1,a.GetNumRadicalElectrons()) for a in template.GetAtoms() if a.GetNumRadicalElectrons()]==[(10,1)],str(p)+' radical identity')
 check({tuple(sorted(b['atoms_1based'])):b['order'] for b in system['bonds']}=={tuple(sorted([b.GetBeginAtomIdx()+1,b.GetEndAtomIdx()+1])):b.GetBondTypeAsDouble() for b in template.GetBonds()},str(p)+' public bond map')
 conf=starter.GetConformer()
 check(min((conf.GetAtomPosition(i)-conf.GetAtomPosition(j)).Length() for i in range(53) for j in range(i))>0.6,str(p)+' no coincident starter atoms')
 for private in (p/'evaluation/author_results').glob('*.xyz'):
  old=subprocess.check_output(['git','show','940d3d04:'+str(p/'agent_input/data/inputs'/private.name)])
  check(private.read_bytes()==old,str(p)+' author geometry preserved '+private.name)
 check({f.name for f in (p/'agent_input/data/inputs').iterdir()}=={'radical_starter.xyz','system.json'},str(p)+' no public author endpoint')
 # Test the chemical mapping underlying the authored semantic rule. This is
 # not the LLM judge and it is not an independent scientific computation.
 def identify(st):
  pair=[st['atom_mapping'][i-1]-1 for i in st['forming_bond_1based']]
  aryl=next(i for i in pair if i!=9)
  for ring in Chem.GetSymmSSSR(template):
   if aryl in ring:
    outside={a.GetIdx() for i in ring for a in template.GetAtomWithIdx(i).GetNeighbors() if a.GetIdx() not in ring}
    return 'arenesulfonyl' if any(template.GetAtomWithIdx(i).GetSymbol()=='S' for i in outside) else 'benzyl'
  raise AssertionError('Forming bond does not reach an aryl ring')
 ref='intermediate_B' if p.parent.name=='paper_reproduction' else 'state_reference'
 names=[n for n in d['states'] if n!=ref]
 check({identify(d['states'][n]) for n in names}=={'benzyl','arenesulfonyl'},str(p)+' channels identified by connectivity')
 reference=d['states'][ref]['energy']
 # State energy field in the historical result is a scalar in Hartree.
 barriers={identify(d['states'][n]):(d['states'][n]['energy']-reference)*627.509474 for n in names}
 check(abs(barriers['benzyl']-13.08)<=1.5 and abs(barriers['arenesulfonyl']-19.25)<=1.5,str(p)+' mapped barrier arithmetic',barriers)
 if p.parent.name=='autonomous_research':
  swapped=copy.deepcopy(d)
  swapped['states'][names[0]],swapped['states'][names[1]]=swapped['states'][names[1]],swapped['states'][names[0]]
  altered={identify(swapped['states'][n]):(swapped['states'][n]['energy']-reference)*627.509474 for n in names}
  check(altered==barriers,str(p)+' arbitrary AR labels preserve chemical scoring identity')

def graph(m):
 g=nx.Graph();g.add_nodes_from((a.GetIdx(),{'e':a.GetSymbol()}) for a in m.GetAtoms());g.add_edges_from((b.GetBeginAtomIdx(),b.GetEndAtomIdx()) for b in m.GetBonds());return g

def molecule(path):
 m=Chem.MolFromXYZBlock(path.read_text());rdDetermineBonds.DetermineConnectivity(m);return m

def real(p):
 ref=p/'evaluation/verified_computation_reference.md'
 f=(ref.parent/re.search(r'\[历史结构化结果\]\(([^)]+)\)',ref.read_text()).group(1)).resolve()
 d=json.loads(f.read_text());adapt=[]
 if '8fef' in p.name:
  pub=molecule(p/'agent_input/data/inputs/radical_starter.xyz')
  old=molecule(p/'evaluation/author_results'/('intermediate_B.xyz' if p.parent.name=='paper_reproduction' else 'state_reference.xyz'))
  matcher=nx.algorithms.isomorphism.GraphMatcher(graph(old),graph(pub),node_match=lambda a,b:a['e']==b['e']);assert matcher.is_isomorphic()
  mapping=[matcher.mapping[i]+1 for i in range(53)]
  group=BASE/'docs/verification/group_2'/p.name
  for st in d['states'].values():
   path=group/st['optimized_geometry'];assert path.is_file()
   st['geometry_file']=str(path);st['atom_mapping']=mapping
   if st['mode_check']:st['forming_bond_1based']=st['mode_check']['forming_C_C_pair_1based']
  adapt.append('lossless geometry/mode fields and element-graph atom mapping; no result change')
 if 'd83e' in p.name and p.parent.name=='autonomous_research':
  d['investigation']={'plan':'SYNTHETIC schema-test wrapper only; not an AR verification claim.', 'models_or_conformers':['SYNTHETIC format field'], 'coverage':'SYNTHETIC schema-test wrapper around existing real scientific results.'}
  adapt.append('synthetic investigation wrapper; historical AR trajectory was not recorded')
 return d,adapt

def failure_case(p,d):
 x=copy.deepcopy(d);pid=p.name;why='SYNTHETIC early calculation failure for format test; no computed result.'
 if 'd83e' in pid:return {'status':'bounded_failure','failure_stage':'before optimization','diagnostics':why,'partial_results':{},'investigation_scope':'no successful calculations','conclusion':'unresolved'}
 if '2877' in pid:
  for row in x['complexes']:row.update(status='bounded_failure',validation=why,observables={'failure_reason':why})
  x['comparison']='unresolved'
 elif '0e83' in pid:
  x['status']='bounded_failure';x['comparison']=x['conclusion']='unresolved'
  for row in x['systems']:
   row.clear()
  x['systems']=[{'system_id':n,'minimum':{'optimized':False,'evidence':why},'ts_search':{'candidates_attempted':0,'candidates_validated':0,'coverage':'none','evidence':why},'barrier':None,'outcome_status':'bounded_failure','failure_reason':why} for n in ['1','V-prime']]
 elif '8fef' in pid:
  x['status']='bounded_failure';x['conclusion']='unresolved'
  x['states']={n:{'identity':n,'validation_status':'failed','validation_evidence':why,'failure_reason':why} for n in x['states']}
  x['comparison']={'reference_state':next(iter(x['states'])),'failure_reason':why}
 elif '9132' in pid:
  x['status']='bounded_failure';x['conclusion']='unresolved'
  for key in ['stationary_point','barrier','connection_evidence']:x.pop(key,None)
  x['investigation']={'attempts':[],'completion_basis':why};x['failure_report']={'reason':why,'attempted_search':'No converged calculation','available_diagnostics':why}
 elif '9ec3' in pid:
  x['status']='bounded_failure';x['conclusion']='unresolved'
  for row in x['structures']:row['stationary_point']={'status':'failed'};row['free_energy']={'status':'unavailable','source_or_diagnostic':why}
  x['comparison']={'definition':'G_coplanar - G_perpendicular','status':'bounded_failure','failure_reason':why}
 elif '7282' in pid:
  x['status']='bounded_failure';x['failure_reason']=why;x['conclusion']={'claim':'unresolved','validation_summary':why}
  x.pop('gap_kcal_mol',None);x.pop('lower_state',None)
  x['states']={n:{'multiplicity':v['multiplicity'],'method':v['method'],'failure_reason':why} for n,v in x['states'].items()}
 elif '1a47' in pid:
  x['status']='bounded_failure';x['candidates']=[];x['coverage']={'conformer_generation':'failed before construction','deduplication':'no candidates'};x['conclusion']={'claim':'unresolved'}
  x['barrier_comparison']={'availability':'not_available','reason':why};x['failure_report']={'failed_channels':['ortho_4_hydroxybenzofuran','para_6_hydroxybenzofuran'],'attempted_candidate_ids':[],'reason':why}
 elif '2a71' in pid:
  x['status']='bounded_failure';x['scan_states']=[];x['conclusion']='unresolved';x['failure_summary']=why;x.pop('barrier_result',None);x.pop('sensitivity',None)
 drop_caveats(x);return x

def mutations(p,d):
 pid=p.name;out=[]
 def add(label,fn):
  x=copy.deepcopy(d);fn(x);out.append((label,x))
 if '2877' in pid:
  add('duplicate metal',lambda x:x['complexes'].__setitem__(1,copy.deepcopy(x['complexes'][0])))
  add('completed with failure observables',lambda x:x['complexes'][0].__setitem__('observables',{'failure_reason':'SYNTHETIC'}))
 elif '0e83' in pid:
  add('duplicate system',lambda x:x['systems'].__setitem__(1,copy.deepcopy(x['systems'][0])))
  add('complete without barrier',lambda x:x['systems'][0].pop('barrier'))
 elif '9ec3' in pid:
  add('duplicate conformer',lambda x:x['structures'].__setitem__(1,copy.deepcopy(x['structures'][0])))
  add('complete with failed comparison',lambda x:x.__setitem__('comparison',{'definition':'delta','status':'bounded_failure','failure_reason':'SYNTHETIC'}))
 elif '8fef' in pid:
  add('complete without barrier',lambda x:x.__setitem__('comparison',{'reference_state':'radical','failure_reason':'SYNTHETIC'}))
  add('complete without energy',lambda x:next(iter(x['states'].values())).pop('energy'))
 elif '9132' in pid:
  add('success with failure-only fields',lambda x:[x.pop(k) for k in ['stationary_point','barrier','connection_evidence']])
  add('success with null barrier',lambda x:x['barrier'].__setitem__('value_kcal_mol',None))
 elif '7282' in pid:
  add('completed without gap',lambda x:x.pop('gap_kcal_mol'))
  add('completed without energies',lambda x:[v.pop('energy_hartree') for v in x['states'].values()])
 elif '1a47' in pid:
  add('completed with one channel',lambda x:x.__setitem__('candidates',x['candidates'][:1]))
  add('completed without frequency evidence',lambda x:x['candidates'][0].pop('frequency_evidence'))
 elif '2a71' in pid:
  add('completed with one scan point',lambda x:x.__setitem__('scan_states',x['scan_states'][:1]))
  add('completed with repeated scan point',lambda x:x.__setitem__('scan_states',[x['scan_states'][0]]*6))
  add('completed without barrier',lambda x:x['barrier_result'].pop('barrier_kcal_mol'))
 elif 'd83e' in pid:
  add('success without BDE',lambda x:x.pop('bde_2g'))
  add('wrong cation charge',lambda x:x['system'].__setitem__('charge',0))
 return out

repo=TaskRepository(roots=[ROOT])
for p in sorted(ROOT.glob('*/*')):
 if not (p/'task_info.json').is_file():continue
 label=f'{p.parent.name}/{p.name}'
 result=validate_task_package(p);check(result.status=='passed',label+' package',str(result.findings))
 contract=(p/'agent_input/submission_schema.json').read_bytes();s=json.loads(contract)['result_schema'];v=jsonschema.Draft202012Validator(s);v.check_schema(s)
 check(not any(k in json.loads(contract) for k in ['properties','required']),label+' no conflicting legacy top-level result schema')
 d,adapt=real(p);drop_caveats(d)
 tests=[('real science, mapped contract' if not any('synthetic' in a for a in adapt) else 'real science plus SYNTHETIC AR wrapper',d,True),('SYNTHETIC early failure',failure_case(p,d),True)]
 x=copy.deepcopy(d);add_empty_caveats(x,s);tests.append(('empty optional ordinary caveats',x,True))
 tests.extend((name,x,False) for name,x in mutations(p,d))
 x=copy.deepcopy(d);x['attempts']=[{'status':'bounded_failure','reason':'SYNTHETIC extra attempt'}];tests.append(('extra failed attempt with successful main results',x,True))
 for array in ['systems','structures','complexes','candidates']:
  if array in d:
   x=copy.deepcopy(d);x[array].reverse();tests.append(('reversed result order',x,True));break
 with tempfile.TemporaryDirectory(prefix='rcb-contract-20260926-') as tmp:
  tmp=Path(tmp);(tmp/'report').mkdir()
  for name,x,expected in tests:
   errs=list(v.iter_errors(x));check((not errs)==expected,label+' schema '+name,[e.message[:250] for e in errs])
   (tmp/'report/results.json').write_text(json.dumps(x,ensure_ascii=False))
   (tmp/'report/README.md').write_text('SYNTHETIC FORMAT TEST WORKSPACE ONLY; not a calculation record.\n')
   rr=validate_output_contract(tmp,contract);check(rr['valid']==expected,label+' runner '+name,rr['errors'][:2])
  dest=tmp/'public';files=materialize_agent_files(paper_id=p.name,task_type=p.parent.name,destination=dest,repository=repo)
  expected={str(f.relative_to(p/'agent_input')) for f in (p/'agent_input').rglob('*') if f.is_file()}
  check(set(files)==expected,label+' export exactly agent_input',files)
  check(not any('evaluation' in f or 'author_results' in f or 'verified_computation' in f or 'paper_route' in f for f in files),label+' private files not exported')
 runtime=load_runtime_evaluation(paper_id=p.name,task_type=p.parent.name,repository=repo)
 check(runtime.policy_id=='dual_axis_100.scientific_results.v1',label+' scientific policy',runtime.policy_id)
 table=runtime.ground_truth['rule_table'];check(all(x['conclusion_ids'] and not x['diagnostic'] for x in table),label+' rule associations')
 baseline=json.loads(subprocess.check_output(['git','show','940d3d04:'+str(p/'evaluation/scoring_rules.json')]))
 numeric_before={r['rule_id']:(r.get('target'),r.get('tolerance'),r.get('unit')) for r in baseline['rules'] if r.get('type')=='numeric'}
 numeric_after={x['rule_id']:(x['rule'].get('target'),x['rule'].get('tolerance'),x['rule'].get('unit')) for x in table if x['rule'].get('type')=='numeric'}
 # The Hirshfeld unit label is normalized; its numerical definition is unchanged.
 if 'r_spin' in numeric_before:numeric_before['r_spin']=(*numeric_before['r_spin'][:2],'dimensionless')
 check(numeric_before==numeric_after,label+' existing numeric targets and tolerances preserved')
 for x in table:
  for field in x['rule'].get('binding',{}).get('fields',[]):
   try:parse(field)
   except Exception as e:failures.append({'test':label+' invalid selector','detail':str(e)})
 checks=[check_rule(x,{'report/results.json':d}) for x in table if x['rule'].get('type')=='numeric']
 check(all(x['assessment'] in ['pass','requires_semantic_review'] for x in checks),label+' numeric diagnostic',checks)
 rows.append({'task':label,'contract_cases':len(tests),'adaptations':adapt,'numeric':checks})
 if '8fef' in p.name:ts_input_check(p,d)
 # Public files parsed and no symlink bypass.
 for f in (p/'agent_input').rglob('*'):
  check(not f.is_symlink(),label+' no symlink '+f.name)
  if f.suffix=='.xyz':
   lines=f.read_text().splitlines();n=int(lines[0]);coords=[l.split() for l in lines[2:] if l.strip()]
   check(len(coords)==n and all(len(a)==4 and all(math.isfinite(float(b)) for b in a[1:]) for a in coords),label+' valid XYZ '+f.name)
  if f.suffix=='.json':json.loads(f.read_text())
 # Local links in historical reference and maintenance record must resolve.
 for f in [p/'evaluation/verified_computation_reference.md',p/'evaluation/task_provenance/maintenance_audit.md']:
  for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)',f.read_text()):
   if not target.startswith(('http:','https:','#')):check((f.parent/target.split('#')[0]).exists(),label+' link '+target)
print(json.dumps({'passed_checks':passed,'failed_checks':failures,'task_count':len(rows),'rows':rows},ensure_ascii=False,indent=2))
sys.exit(bool(failures))
