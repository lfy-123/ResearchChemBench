"""Official package/output-contract regression; synthetic data NEVER scientific evidence."""
from pathlib import Path
from copy import deepcopy
from collections import Counter
import hashlib,json,re,sys,tempfile
B=Path(__file__).resolve().parent;ROOT=B.parents[3];sys.path.insert(0,str(ROOT));sys.path.insert(0,str(B))
import jsonschema,networkx as nx
from rdkit import Chem
from evaluation.contracts.task_package import validate_task_package
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from chemistry_toolbox.src.output_contract import validate_output_contract
from science_specs import S
D=ROOT/'tasks/upgrade_tasks';IDS=json.load(open(B/'assignment.json'))['batch']['papers'];MODES=['autonomous_research','paper_reproduction'];TESTS=[];PER=[]
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def check(name,ok,detail=None):
 TESTS.append({'test':name,'passed':bool(ok),**({'detail':detail} if detail else {})})
 if not ok:raise AssertionError((name,detail))
def sample(s):
 if 'const' in s:return s['const']
 if 'enum' in s:return s['enum'][0]
 if 'oneOf' in s:return sample(s['oneOf'][0])
 if 'anyOf' in s:return sample(s['anyOf'][0])
 t=s.get('type','object' if 'properties' in s else 'string')
 if t=='object':
  result={k:sample(s['properties'][k]) for k in s.get('required',[])}
  for rule in s.get('allOf',[]):
   if 'if' in rule and jsonschema.Draft202012Validator(rule['if']).is_valid(result):
    for k in rule.get('then',{}).get('required',[]):result.setdefault(k,sample(s['properties'][k]))
  return result
 if t=='array':return [sample(s['items']) for _ in range(s.get('minItems',1))]
 if t in ['number','integer']:return max(1,s.get('minimum',1))
 if t=='boolean':return True
 if 'pattern' in s:return 'candidate_SYNTHETIC' if s['pattern'].startswith('^candidate') else 'outputs/SYNTHETIC_NOT_SCIENTIFIC.log'
 return 'SYNTHETIC FORMAT FIXTURE ONLY, NOT SCIENTIFIC EVIDENCE'
def fixture(contract):
 schema=contract['result_schema'];x=sample(schema);x['object_records']=[sample(v) for v in schema['properties']['object_records']['items']['oneOf']]
 # This fixture represents an actual attempted job, including partial cases.
 # Zero-launch diagnostics have a separate explicit regression below.
 if not x['calculation_records']:x['calculation_records']=[sample(schema['properties']['calculation_records']['items'])]
 for i,o in enumerate(x['object_records']):
  if o['object_id'].startswith('candidate_'):o['object_id']+=str(i)
 for i,j in enumerate(x['calculation_records']):j['id']='SYNTHETIC_JOB_'+str(i)
 return x
def validate(contract,doc,report=True):
 with tempfile.TemporaryDirectory(prefix='rcb_batch3_SYNTHETIC_format_') as td:
  p=Path(td);(p/'report').mkdir();(p/'report/results.json').write_text(json.dumps(doc))
  if report:(p/'report/report.md').write_text('SYNTHETIC SCHEMA FIXTURE. No scientific calculation, artifact or claimed result.\n')
  return validate_output_contract(p,json.dumps(contract).encode())
def graph(o):
 g=nx.Graph();g.add_nodes_from(a['id'] for a in o['atoms']);g.add_edges_from((e['a'],e['b']) for e in o['bonds']);return g
def inputs(pid):
 inp=D/MODES[0]/pid/'agent_input/data/inputs';data=json.load(open(inp/'objects.json'));objects=data['objects'];catalog={o['id']:o for o in objects};c=json.load(open(inp/'controls.json'));pt=Chem.GetPeriodicTable()
 def atoms(oid):
  o=catalog[oid]
  if 'atoms' in o:return Counter(a['element'] for a in o['atoms'])
  total=Counter()
  for comp in o['components']:
   for el,n in atoms(comp['object_id']).items():total[el]+=n*comp['count']
  return total
 for o in objects:
  name=pid+':input:'+o['id']
  if 'atoms' in o:
   ids=[a['id'] for a in o['atoms']];edges=[tuple(sorted((e['a'],e['b']),key=str)) for e in o['bonds']]
   check(name+':unique_atom_ids',len(ids)==len(set(ids)))
   check(name+':edges_reference_real_atoms',all(a in ids and b in ids and a!=b for a,b in edges))
   check(name+':unique_edges',len(edges)==len(set(edges)))
   check(name+':connected_graph',nx.is_connected(graph(o)))
   if len(ids)>1:check(name+':one_bond_per_H',all(graph(o).degree(a['id'])==1 for a in o['atoms'] if a['element']=='H'))
   composition=atoms(o['id']);formula=''.join(e+(str(composition[e]) if composition[e]>1 else '') for e in sorted(composition,key=lambda e:(e not in ['C','H'],{'C':0,'H':1}.get(e,2),e)))
   check(name+':formula_matches_atoms',formula==o['formula'])
  else:
   check(name+':all_components_defined',all(x['object_id'] in catalog and x['count']>0 for x in o['components']))
   check(name+':component_charge_conserved',sum(catalog[x['object_id']]['charge']*x['count'] for x in o['components'])==o['charge'])
  electrons=sum(pt.GetAtomicNumber(e)*n for e,n in atoms(o['id']).items())-o['charge'];check(name+':electron_spin_parity',(electrons-(o['multiplicity']-1))%2==0)
 def balanced(label,coeff):
  total=Counter();charge=0
  for oid,m in coeff.items():
   for e,n in atoms(oid).items():total[e]+=m*n
   charge+=m*catalog[oid]['charge']
  check(pid+':balanced:'+label,all(n==0 for n in total.values()) and charge==0,{'element_residual':dict(total),'charge_residual':charge})
 for key in ['exchange_1','exchange_2','dimerization_coefficients','deethylation_coefficients']:
  if key in c:balanced(key,c[key])
 for key,coeff in c.get('reaction_coefficients',{}).items():balanced(key,coeff)
 suffix=pid[6:]
 if suffix=='9a58a1fa6ed7d780':
  mapping=dict(c['common_map']);a=graph(catalog['BN']);b=graph(catalog['CC']);check(pid+':BN_CC_mapped_topology',set(mapping)==set(a) and set(mapping.values())==set(b) and {frozenset((mapping[x],mapping[y])) for x,y in a.edges}=={frozenset(e) for e in b.edges})
 if suffix=='0de37d01e35c27df':
  for o in objects:
   ids=c['SS_maps']['nor' if o['id'].startswith('nor') else 'DTCO'];check(pid+':no_spurious_SS_covalent_edge:'+o['id'],not graph(o).has_edge(*ids))
 if suffix=='b276b18215cba283':
  check(pid+':full_three_arm_141_atoms',len(catalog['three_arm']['atoms'])==141)
  check(pid+':three_distinct_arm_maps',len(c['single_to_three_heavy_atom_maps'])==3)
 if suffix=='94e7481ded3b6a75':
  check(pid+':two_exocyclic_phenyl_torsions',len(c['torsion_maps'])==2)
  for tors in c['torsion_maps']:
   g=graph(objects[0]);g.remove_edge(tors[1],tors[2]);check(pid+':torsion_is_exocyclic:'+str(tors),not nx.has_path(g,tors[1],tors[2]))
 if suffix=='86a0b654270a8ce7':
  for o in objects:
   cs=o['coordination_stereochemistry'];check(pid+':six_distinct_donors:'+o['id'],len(set(cs['donor_atom_ids']))==6);check(pid+':octahedral_trans_pairs:'+o['id'],Counter(i for pair in cs['trans_donor_pairs'] for i in pair)==Counter(cs['donor_atom_ids']))
 if suffix=='9aa6d5655edfeb52':
  for o in objects:check(pid+':12_vertex_closo_cage:'+o['id'],all(d==5 for n,d in graph(o).subgraph(c['cage_atom_ids']).degree()) and len(c['cage_atom_ids'])==12)
 if suffix=='2877efc02814175d':check(pid+':Co_doublet_Cd_Ni_singlets',[catalog[x+'_DQCS']['multiplicity'] for x in ['Cd','Co','Ni']]==[1,2,1])
 if suffix=='2f2aa11ea61a32bb':check(pid+':source_spectral_medium_consistent',c['solvent']==json.load(open(inp/'experimental_absorption.json'))['solvent']=='toluene')
 if suffix=='3a22e838133b906d':check(pid+':full_dimer_138_atoms',sum(atoms('crystal_supported_dimer').values())==138)
 return {'objects':len(objects),'largest_explicit_atom_inventory':max(sum(atoms(o['id']).values()) for o in objects)}
def main():
 # Required official discovery opt-in, without modifying default roots or unrelated packages.
 repo=TaskRepository.__new__(TaskRepository);repo.roots=(D.resolve(),)
 repo._approved_final_directories=tuple(D/mode/pid for mode in MODES for pid in IDS)
 repo._index=repo._build_index();check('explicit_upgrade_repository',repo.roots==(D.resolve(),))
 for pid in IDS:
  start=len(TESTS);ar=D/MODES[0]/pid;pr=D/MODES[1]/pid
  af={str(p.relative_to(ar/'agent_input')):p.read_bytes() for p in (ar/'agent_input').rglob('*') if p.is_file()};pf={str(p.relative_to(pr/'agent_input')):p.read_bytes() for p in (pr/'agent_input').rglob('*') if p.is_file()}
  check(pid+':same_public_file_set',set(af)==set(pf))
  for rel in af:
   if rel!='task.md':check(pid+':AR_PR_public_parity:'+rel,af[rel]==pf[rel])
  a=af['task.md'].decode();p=pf['task.md'].decode();stripped=re.sub(r'\n\n# Author-provided scientific guidance\n\n.*?(?=\n\n# Public inputs)', '',p,flags=re.S)
  check(pid+':only_author_route_differs',a==stripped and '# Author-provided' not in a and '# Author-provided' in p)
  for name in ['reference_key_points.json','reference_conclusions.json','scoring_rules.json','critical_failures.json','evidence_map.json']:check(pid+':scientific_evaluator_parity:'+name,(ar/'evaluation'/name).read_bytes()==(pr/'evaluation'/name).read_bytes())
  prep=inputs(pid)
  contract=json.loads(af['submission_schema.json']);schema=contract['result_schema'];jsonschema.Draft202012Validator.check_schema(schema);x=fixture(contract);valid=validate(contract,x);check(pid+':synthetic_contract_positive',valid['valid'],valid['errors'][:2]);blocked=contract['development_status']=='blocked'
  if blocked:
   y=deepcopy(x);y['status']='complete';check(pid+':blocked_cannot_claim_complete',not validate(contract,y)['valid'])
  else:
   check(pid+':synthetic_is_complete',x['status']=='complete')
   for panel,rows in x['results'].items():
    y=deepcopy(x);del y['results'][panel];check(pid+':missing_scientific_panel:'+panel,not validate(contract,y)['valid'])
    for row in rows:
     y=deepcopy(x);del y['results'][panel][row];check(pid+':missing_named_contrast:'+panel+'.'+row,not validate(contract,y)['valid'])
    row=next(iter(rows));y=deepcopy(x);y['results'][panel][row].pop('metrics');check(pid+':prose_without_numbers:'+panel,not validate(contract,y)['valid'])
   y=deepcopy(x)
   for j in y['calculation_records']:j['kind']='failed';j['failure_diagnostics']='SYNTHETIC FAILURE'
   check(pid+':all_failed_cannot_complete',not validate(contract,y)['valid'])
   y=deepcopy(x);y['object_records']=y['object_records'][:1];check(pid+':missing_object_matrix_rejected',not validate(contract,y)['valid'] if len(x['object_records'])>1 else True)
   for outcome in ['supported','refuted','indistinguishable']:
    y=deepcopy(x);y['conclusion']['outcome']=outcome;check(pid+':outcome_neutral_format:'+outcome,validate(contract,y)['valid'])
   y=deepcopy(x);y['conclusion']['core_matrix_complete']=False;check(pid+':unfinished_not_indistinguishable',not validate(contract,y)['valid'])
   collapsible=[(p,r) for p,ps in schema['properties']['results']['properties'].items() for r,rs in ps['properties'].items() if rs['properties']['outcome'].get('enum')==['computed','evidenced_collapse']]
   if collapsible:
    p,r=collapsible[0];y=deepcopy(x);row=y['results'][p][r];row['outcome']='evidenced_collapse';row.pop('metrics',None);row['collapse_evidence']=['structures/SYNTHETIC_START.xyz','structures/SYNTHETIC_END.xyz'];row['mapped_retained_endpoint']='SYNTHETIC_ENDPOINT';check(pid+':evidenced_collapse_format',validate(contract,y)['valid']);row.pop('collapse_evidence');check(pid+':unsupported_collapse_rejected',not validate(contract,y)['valid'])
  for field,value in [('charge',17),('multiplicity',9),('object_id','UNDECLARED_WRONG_OBJECT')]:
   y=deepcopy(x);y['object_records'][0][field]=value;check(pid+':wrong_identity_field:'+field,not validate(contract,y)['valid'])
  y=deepcopy(x);y['protocol']['energy_reference']='wrong_total_energy_zero';check(pid+':wrong_energy_reference',not validate(contract,y)['valid'])
  y=deepcopy(x);y['calculation_records'][0]['object_id']='UNDECLARED_WRONG_OBJECT';check(pid+':wrong_calculation_object',not validate(contract,y)['valid'])
  for path in ['evaluation/reference.json','outputs/../hidden','outputs/sub/../../hidden','/tmp/hidden','outputs//../hidden','outputs/\\hidden']:
   y=deepcopy(x);y['raw_files']=[path];check(pid+':unsafe_raw_path:'+path,not validate(contract,y)['valid'])
  check(pid+':missing_readable_report',not validate(contract,x,False)['valid'])
  check(pid+':legacy_scalar_only',not validate(contract,{'paper_id':pid,'status':'complete','energy':-100,'conclusion':'old result'})['valid'])
  y=deepcopy(x);y['status']='bounded_failure'
  for key in ['results','hypothesis_tests','sensitivity','conclusion']:y.pop(key,None)
  y['failure_report']=sample(schema['properties']['failure_report'])
  for j in y['calculation_records']:j['kind']='failed';j['failure_diagnostics']='SYNTHETIC FAILED ENGINE, NOT REAL DATA';j.pop('electronic_Eh',None);j.pop('geometry_file',None);j.pop('convergence_file',None)
  check(pid+':honest_failure_format',validate(contract,y)['valid']);y.pop('failure_report');check(pid+':failure_needs_diagnostics',not validate(contract,y)['valid'])
  y['failure_report']=sample(schema['properties']['failure_report'])
  y['object_records']=[];y['calculation_records']=[]
  for k,v in y['resources'].items():
   if isinstance(v,(int,float)) and not isinstance(v,bool):y['resources'][k]=0
  check(pid+':zero_launch_diagnostic',validate(contract,y)['valid'])
  z=deepcopy(y);z.pop('failure_report');check(pid+':zero_launch_needs_diagnostics',not validate(contract,z)['valid'])
  z=deepcopy(y);z['status']='complete';check(pid+':zero_launch_not_complete',not validate(contract,z)['valid'])
  job=sample(schema['properties']['calculation_records']['items']);job['kind']='successful';job['role']='density_analysis'
  for k in ['geometry_file','electronic_Eh']:job.pop(k,None)
  y['calculation_records']=[job]
  check(pid+':analysis_without_fabricated_energy_geometry',validate(contract,y)['valid'])
  if not blocked:
   z=deepcopy(x)
   for j in z['calculation_records']:j['role']='density_analysis'
   check(pid+':analysis_only_not_complete',not validate(contract,z)['valid'])
  z=deepcopy(y);z['raw_files']=['outputs/./SYNTHETIC_DIAGNOSTIC.txt'];check(pid+':benign_dot_segment',validate(contract,z)['valid'])
  for mode in MODES:
   root=D/mode/pid;v=validate_task_package(root);check(pid+':'+mode+':official_package',v.status=='passed',v.findings)
   for path in root.rglob('*.json'):json.load(open(path))
   runtime=load_runtime_evaluation(paper_id=pid,task_type=mode,repository=repo);check(pid+':'+mode+':official_runtime',runtime.adapter_id=='split-computational-evaluator.v3-flat');check(pid+':'+mode+':weight_100',sum(i['max_score'] for i in runtime.ground_truth['scientific_conclusion_rubric'])==100)
   with tempfile.TemporaryDirectory(prefix='rcb_batch3_public_export_') as td:
    materialize_agent_files(paper_id=pid,task_type=mode,destination=td,repository=repo);exported={str(p.relative_to(td)) for p in Path(td).rglob('*') if p.is_file()};check(pid+':'+mode+':exact_public_materialize',exported==set(af));check(pid+':'+mode+':no_private_export',not any('evaluation' in p or '.snapshot' in p or p.endswith('.pdf') for p in exported))
   audit=json.load(open(root/'evaluation/task_provenance/upgrade_audit.json'));source=ROOT/audit['source'];check(pid+':'+mode+':source_file_set_intact',set(audit['source_payload_snapshots'])=={str(p.relative_to(source)) for p in source.rglob('*') if p.is_file()})
   for rel,record in audit['source_payload_snapshots'].items():check(pid+':'+mode+':source_snapshot:'+rel,sha(root/record['snapshot'])==record['sha256']==sha(source/rel))
   for doc in audit['source_docs']:check(pid+':'+mode+':source_document_hash:'+doc['path'],sha(ROOT/doc['path'])==doc['sha256'])
   check(pid+':'+mode+':no_new_scientific_pass',audit['status'] in ['implemented_pending_expanded_reference','blocked'] and audit['new_scientific_calculations_performed'] is False and audit['scientific_reference_validated'] is False)
  PER.append({'paper_id':pid,'status':'passed','checks':len(TESTS)-start,'development_status':contract['development_status'],'public_inputs':prep,'scientific_validation_performed':False})
  print(pid,'PASSED',len(TESTS)-start,flush=True)
 return {'batch':3,'date':'2026-09-27','status':'passed','paper_count':19,'package_count':38,'checks':len(TESTS),'scientific_engine_starts':0,'LLM_scientific_judge_run':False,'boundary':'Official structural/runtime/public-export validation, graph/count sanity and synthetic output-format tests only. No new quantum reference, calibrated scoring or scientific PASS is claimed.','papers':PER,'results':TESTS}
if __name__=='__main__':
 try:report=main()
 except Exception as e:
  report={'batch':3,'status':'failed','error':repr(e),'papers':PER,'results':TESTS};(B/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');raise
 (B/'validation_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ['results','papers']},ensure_ascii=False))
