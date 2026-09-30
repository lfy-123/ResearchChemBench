"""Short graph/stoichiometry checks. No coordinates optimized and no physics predicted."""
from pathlib import Path
import json,hashlib,re,sys
from collections import Counter
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from ase.io import read
B=Path(__file__).resolve().parent;ROOT=B.parents[3];sys.path.insert(0,str(B))
from build_batch import IDS,dump,sha
P=B/'prepared_inputs';checks=[];graphs={}
def check(name,ok,detail=None):
 checks.append({'test':name,'passed':bool(ok),'detail':detail})
 if not ok:raise AssertionError((name,detail))
def mol(smiles):
 p=Chem.SmilesParserParams();p.removeHs=False;m=Chem.MolFromSmiles(smiles,p)
 assert m is not None
 return m
def amap(m):return {a.GetAtomMapNum():a for a in m.GetAtoms()}
def torsion(label,m,ids):
 a=amap(m);check(label+':four_distinct',len(set(ids))==4)
 check(label+':connected',all(i in a for i in ids) and all(m.GetBondBetweenAtoms(a[i].GetIdx(),a[j].GetIdx()) is not None for i,j in zip(ids,ids[1:])))
def mapping(label,m,n,pairs,strict=True):
 a,b=amap(m),amap(n);mp=dict(pairs)
 check(label+':one_to_one',len(mp)==len(pairs)==len(set(mp.values())))
 check(label+':elements',all(i in a and j in b and a[i].GetAtomicNum()==b[j].GetAtomicNum() and a[i].GetAtomicNum()>1 for i,j in pairs))
 edges_m={frozenset([x.GetBeginAtom().GetAtomMapNum(),x.GetEndAtom().GetAtomMapNum()]):str(x.GetBondType()) for x in m.GetBonds()}
 edges_n={frozenset([x.GetBeginAtom().GetAtomMapNum(),x.GetEndAtom().GetAtomMapNum()]):str(x.GetBondType()) for x in n.GetBonds()}
 for edge,order in edges_m.items():
  if all(i in mp for i in edge):
   e=frozenset(mp[i] for i in edge);check(label+':bond:'+str(sorted(edge)),e in edges_n and (not strict or edges_n[e]==order))
def main():
 for p in sorted(P.rglob('*identity.json')):
  d=json.loads(p.read_text())
  if 'mapped_smiles' not in d:continue
  m=mol(d['mapped_smiles']);a=amap(m);label=str(p.relative_to(P));graphs[(p.parent.name,p.stem.removesuffix('_identity'))]=m
  check(label+':valence_and_formula',rdMolDescriptors.CalcMolFormula(m)==d['formula'])
  check(label+':charge',Chem.GetFormalCharge(m)==d['charge'])
  check(label+':unique_map',0 not in a and len(a)==m.GetNumAtoms())
  check(label+':connected',len(Chem.GetMolFrags(m))==1)
  if 'atoms' in d:
   check(label+':atom_table',len(d['atoms'])==m.GetNumAtoms() and all(x['atom_id'] in a and x['element']==a[x['atom_id']].GetSymbol() and x['formal_charge']==a[x['atom_id']].GetFormalCharge() for x in d['atoms']))
   edges={frozenset([x.GetBeginAtom().GetAtomMapNum(),x.GetEndAtom().GetAtomMapNum()]):str(x.GetBondType()) for x in m.GetBonds()}
   check(label+':bond_table',len(d['bonds'])==m.GetNumBonds() and all(edges.get(frozenset([x['a'],x['b']]))==x['order'] for x in d['bonds']))
  if 'intervention_torsion_atoms' in d:torsion(label,m,d['intervention_torsion_atoms'])
 pid='paper_3316e45a74258fb7';d=json.loads((P/pid/'torsion_control_mapping.json').read_text())
 for oid,controls in d['objects'].items():
  m=graphs[(pid,oid)];a=amap(m);donors=[]
  for i,c in enumerate(controls):
   torsion(oid+str(i),m,c['torsion_atom_ids']);donors+=c['donor_atom_ids']
   check(oid+str(i)+':donor_C18N',Counter(a[x].GetSymbol() for x in c['donor_atom_ids'])=={'C':18,'N':1})
  check(oid+':disjoint_donors',len(donors)==len(set(donors)))
 pid='paper_b5c446c7067dd511';d=json.loads((P/pid/'molecular_identities.json').read_text())
 for row in d['molecules']:torsion(row['id'],graphs[(pid,row['id'])],row['terminal_bridge_control']['torsion_atom_ids'])
 pid='paper_e0791c047a731974';d=json.loads((P/pid/'Cy2_planar_control.json').read_text())
 for i,t in enumerate(d['dihedral_atom_quadruples']):torsion('Cy2 planar '+str(i),graphs[(pid,'Cy2')],t)
 pid='paper_c23cfabbd34b087f';d=json.loads((P/pid/'common_scaffold_mapping.json').read_text())
 for pair in d['pairs']:
  check(pair['topology']+':common_count',len(pair['shared_atom_id_pairs'])==pair['common_heavy_atoms'])
  mapping(pair['topology'],graphs[(pid,pair['from'])],graphs[(pid,pair['to'])],pair['shared_atom_id_pairs'],False)
 pid='paper_e31cc7bc7b21b610';d=json.loads((P/pid/'retained_heavy_mapping.json').read_text())
 mapping('Egan_egan',graphs[(pid,'Egan')],graphs[(pid,'egan')],d['pairs_full_Egan_to_egan'])
 check('Egan deletion:four_tBu',len(d['deleted_heavy_atom_ids'])==16)
 pid='paper_988bc12ae3768679';d=json.loads((P/pid/'candidate_seeds.json').read_text());parent=graphs[(pid,'parent')];a=amap(parent)
 for row in d['required_seeds']:
  m=mol(row['mapped_smiles']);b=amap(m);label=row['candidate_id']
  check(label+':formula',rdMolDescriptors.CalcMolFormula(m)==row['formula'])
  check(label+':proton_charge',Chem.GetFormalCharge(m)==row['charge']==row['proton_change'])
  check(label+':conserved_heavy_atoms',{i:x.GetSymbol() for i,x in a.items() if x.GetAtomicNum()>1}=={i:x.GetSymbol() for i,x in b.items() if x.GetAtomicNum()>1})
  for edit in row['edits']:
   if 'move_H_id' in edit:
    h=edit['move_H_id'];check(label+':H_relocation',m.GetBondBetweenAtoms(b[h].GetIdx(),b[edit['from_atom_id']].GetIdx()) is None and m.GetBondBetweenAtoms(b[h].GetIdx(),b[edit['to_atom_id']].GetIdx()) is not None)
 pid='paper_d8e5490cd9942f4f';d=json.loads((P/pid/'ecp_basis_manifest.json').read_text())
 for row in d['elements']:
  for kind in ['ecp','basis']:check(row['element']+':'+kind+'_hash',sha(P/pid/row[kind+'_file'])==row[kind+'_sha256'])
  check(row['element']+':11_explicit_electrons',Chem.GetPeriodicTable().GetAtomicNumber(row['element'])-row['core_electrons']==11)
  check(row['element']+':shells',row['primitive_shells']=={'S':7,'P':6,'D':5} and row['contracted_shells']=={'S':5,'P':4,'D':3})
 # Existing coordinate inputs preserve their chemical identity; this says nothing about minima.
 expected={'paper_3d1d9b7f6df049da':{'y2_d5h.xyz':'C87H7Y2','y2_ih.xyz':'C87H7Y2'},'paper_72822e4ddb5d9b11':{'complex_4.xyz':'C87H72Cl2N2NiO'},'paper_80441aced6051d86':{'g1_monomer.xyz':'C34H28N2','g1_dimer.xyz':'C68H56N4'},'paper_d8e5490cd9942f4f':{'anti_La_KHQ.xyz':'C32H38LaN4O6','syn_La_KHQ.xyz':'C32H38LaN4O6'}}
 for pid,files in expected.items():
  for name,formula in files.items():
   at=read(ROOT/'tasks/upgrade_tasks/autonomous_research'/pid/'agent_input/data/inputs'/name)
   check(pid+':'+name+':composition',at.get_chemical_formula()==formula,at.get_chemical_formula())
 tube=read(P/'paper_94b0a8ae694590ea/benchmark_10_10_12repeat.extxyz')
 check('tube:480_carbon',len(tube)==480 and set(tube.get_chemical_symbols())=={'C'})
 b2=read(P/'paper_eda19e7c8edd4b39/benchmark_B2_start.extxyz');l12=read(P/'paper_eda19e7c8edd4b39/benchmark_L12_start.extxyz')
 check('B2:start_stoichiometry',Counter(b2.get_chemical_symbols())=={'Ni':1,'Al':1})
 check('L12:start_stoichiometry',Counter(l12.get_chemical_symbols())=={'Ni':3,'Al':1})
 return {'status':'passed','checks':len(checks),'mapped_graphs':len(graphs),'scientific_engine_starts':0,'scope':'Graph identities, atom mappings, formula/charge, declared input coefficients and ideal starter counts only. Not a physical validation, minimum search or scientific pass.','results':checks}
if __name__=='__main__':
 try:report=main()
 except Exception as e:
  dump(B/'identity_validation_report.json',{'status':'failed','error':repr(e),'results':checks});raise
 dump(B/'identity_validation_report.json',report);print(json.dumps({k:v for k,v in report.items() if k!='results'}))
