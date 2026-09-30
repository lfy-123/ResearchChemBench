"""Offline molecular-identity checks; no optimization, energies, minima or science PASS."""
from pathlib import Path
from collections import Counter
import json
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
B=Path(__file__).resolve().parent;ROOT=B.parents[3];DEST=ROOT/'tasks/upgrade_tasks/autonomous_research'
IDS=json.loads((B/'assignment.json').read_text())['batch']['papers']
def run():
 out=[]
 def check(n,ok,detail=None):out.append({'test':n,'passed':bool(ok),**({'detail':detail} if detail else {})})
 registries={}
 for pid in IDS:
  folder=DEST/pid/'agent_input/data/inputs';reg=json.loads((folder/'species_registry.json').read_text());registries[pid]=reg
  for s in reg['species']:
   tag=pid+':identity:'+s['id']
   if 'mapped_smiles' in s:
    pa=Chem.SmilesParserParams();pa.removeHs=False;m=Chem.MolFromSmiles(s['mapped_smiles'],pa)
    check(tag+':parse',m is not None)
    if m is not None:
     check(tag+':charge',sum(a.GetFormalCharge() for a in m.GetAtoms())==s['charge'])
     check(tag+':formula',rdMolDescriptors.CalcMolFormula(m)==s['formula'],{'observed':rdMolDescriptors.CalcMolFormula(m),'expected':s['formula']})
     maps=[a.GetAtomMapNum() for a in m.GetAtoms()];check(tag+':complete_unique_maps',all(maps) and len(maps)==len(set(maps)))
     ne=sum(a.GetAtomicNum() for a in m.GetAtoms())-s['charge'];check(tag+':electron_spin_parity',ne%2==(s['multiplicity']-1)%2)
   if 'coordinates' in s:
    lines=(folder/s['coordinates']).read_text().splitlines();n=int(lines[0]);check(tag+':xyz_atom_count',len([x for x in lines[2:] if x.strip()])==n and len(s['atoms'])==n)
   if s.get('atoms') and s.get('bonds'):
    ids={a['map_id'] for a in s['atoms']}
    check(tag+':bond_endpoints_exist',all(set(bd.get('atoms',bd.get('atoms_1based',[])))<=ids for bd in s['bonds']))
 def species(pid,name):return next(s for s in registries[pid]['species'] if s['id']==name)
 en=species('paper_4e9774f4128551d3','enol_TMS');check('harziane:enol_formula',en['formula']=='C23H38O3Si')
 acid=species('paper_4e9774f4128551d3','CSA_connectivity');check('harziane:CSA_enantiomer_pair',len(acid['stereo_variants'])==2,acid['stereo_variants'])
 dpph=species('paper_fcc3c7f2c46a0fbe','DPPH');check('antioxidant:DPPH_radical_formula',dpph['formula']=='C18H12N5O6' and sum(a['radical_electrons'] for a in dpph['atoms'])==1)
 for name in ['4b','4c','4h','4i']:
  s=species('paper_fcc3c7f2c46a0fbe',name);oh=any(a['element']=='O' for a in s['real_H_donors'])
  check('antioxidant:'+name+':actual_OH_identity',oh==(name in ['4c','4i']))
 reg=registries['paper_e2d9397dff2a3f0f'];state=reg['construction_definitions']['state_definition'];check('Ru:changed_ligand_inventory',state['bcs']['atom_count']==49 and state['bcs']['replace_element']=={'28':'S'})
 reg=registries['paper_9132719dbf91c978'];check('Pd:full_hydride_inventory',reg['metal_graph']['hydride_maps']==[76,77])
 short=species('paper_8fefc96b015c4577','radical_starter');long=species('paper_8fefc96b015c4577','long_radical')
 check('radical:long_complete_homologous_atoms',len(long['homologous_atoms'])==56 and len({a['map_id'] for a in long['homologous_atoms']})==56)
 counts=Counter(a['element'] for a in long['homologous_atoms']);check('radical:homologous_formula',counts==Counter({'C':22,'H':26,'F':2,'N':1,'O':4,'S':1}),dict(counts))
 edges={frozenset(b['atoms']) for b in long['homologous_bonds']};check('radical:sole_CH2_insertion',frozenset([13,14]) not in edges and all(frozenset(x) in edges for x in [[13,54],[54,14],[54,55],[54,56]]))
 for pid in ['paper_4e9774f4128551d3','paper_db6c4e0558113873']:
  check(pid+':old_answer_XYZ_private',not list((DEST/pid/'agent_input/data/inputs').glob('*.xyz')))
 for pid in IDS:
  matrix=json.loads((DEST/pid/'agent_input/data/inputs/research_matrix.json').read_text());check(pid+':three_core_panels',len(matrix['panels'])==3)
 return out
if __name__=='__main__':
 r=run();(B/'chemical_input_check_report.json').write_text(json.dumps({'boundary':'Graph/identity only; no quantum calculation','checks':r},ensure_ascii=False,indent=2)+'\n');print(json.dumps([x for x in r if not x['passed']],ensure_ascii=False,indent=2));print('checks',len(r))
