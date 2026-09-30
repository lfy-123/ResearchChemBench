from pathlib import Path
import re,json
from collections import Counter
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds
B=Path(__file__).parent;E=B/'evidence';OUT=B/'extracted_objects.json'
def xyzlines(s):
 out=[]
 for l in s.splitlines():
  m=re.fullmatch(r'\s*(?:\d+\s+)?([A-Z][a-z]?)\s+([-+]?\d+\.?\d*)\s+([-+]?\d+\.?\d*)\s+([-+]?\d+\.?\d*)\s*',l)
  if m:out.append([m[1],*[float(m[i]) for i in [2,3,4]]])
 return out
def section(pid,a,b):
 s=(E/f'paper_{pid}_supplementary_001.txt').read_text();s=s[s.rindex(a):];return xyzlines(s[:s.index(b)] if b and b in s else s)
objects={}
for pid,specs in {
 '9a58a1fa6ed7d780':[('CC_AkFlu','Table S22.','Table S23.')],
 '9f4c259696ad2f87':[('PXX2','Cartesian coordinates for optimized geometry of 2 in solution','Cartesian coordinates for optimized geometry of 3')],
 'b276b18215cba283':[('three_arm','Table S10. Cartesian coordinates','Table S11.')],
 '43d74f8a469d9ad3':[('dye1','Table S5\n','Table S6'),('dye3','Table S7\n','Table S8')]
}.items():
 for name,a,b in specs:
  try:atoms=section(pid,a,b);objects[pid+'_'+name]=atoms;print(pid,name,len(atoms),dict(Counter(x[0] for x in atoms)))
  except Exception as e:print(pid,name,e)
for pid in json.load(open(B/'assignment.json'))['batch']['papers']:
 p=Path('tasks/final_verified_autonomous_research')/pid/'agent_input/data/inputs'
 for f in p.glob('*.xyz'):
  rows=[]
  for l in f.read_text().splitlines()[2:]:
   t=l.split()
   if len(t)==4:rows.append([Chem.GetPeriodicTable().GetElementSymbol(int(t[0])) if t[0].isdigit() else t[0],*map(float,t[1:])])
  objects[pid[6:]+'_'+f.stem]=rows
for name,atoms in objects.items():
 if not atoms:continue
 xyz=str(len(atoms))+'\nprivate topology extraction only\n'+'\n'.join(a[0]+' '+' '.join(f'{v:.9f}' for v in a[1:]) for a in atoms)+'\n'
 try:
  mol=Chem.MolFromXYZBlock(xyz);rdDetermineBonds.DetermineBonds(mol,charge=0,allowChargedFragments=True,embedChiral=False)
  print('GRAPH OK',name,Chem.MolToSmiles(Chem.RemoveHs(mol)))
 except Exception as e: print('GRAPH CHECK',name,str(e)[:150])
OUT.write_text(json.dumps(objects,indent=2))
