from package_builder import *
import re
from rdkit.Chem import rdDetermineBonds,Draw,rdDepictor
def from_xyz(xyz):
 m=Chem.MolFromXYZBlock(xyz)
 rdDetermineBonds.DetermineBonds(m,charge=0,allowChargedFragments=False,embedChiral=True)
 for a in m.GetAtoms():a.SetAtomMapNum(a.GetIdx()+1)
 return m
def graph(m,id,source):
 m.RemoveAllConformers()
 return molecule(id,Chem.MolToSmiles(m),source=source,keep_maps=True)
pid='paper_746e066c163800d8';txt=(B/'source_reviews'/pid/'supplementary_001.txt').read_text();results=[]
for n in [1,3,5,7]:
 block=txt.split('Compound '+str(n)+' \n',1)[1].split('Compound '+str(n+1)+' \n',1)[0]
 coords=re.findall(r'^\s*([A-Z][a-z]?)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)\s+(-?\d+\.\d+)',block,re.M)
 xyz=str(len(coords))+'\nprivate source geometry used only for graph transcription\n'+'\n'.join(' '.join(r) for r in coords)+'\n'
 mol=from_xyz(xyz)
 rec=graph(mol,str(n),'SI Cartesian coordinates (PDF pp40 onward), graph-only transcription checked against main Fig1; source optimized coordinates withheld.')
 results.append(rec);print(n,len(coords),rec['formula'])
dump(B/'source_reviews'/pid/'derived_graphs.json',results)
pid='paper_5286f393dfa5a49a'
m=from_xyz(source_input(pid,'rrrr.xyz').read_text());dump(B/'source_reviews'/pid/'di_graph.json',graph(Chem.Mol(m),'di_RRRR','SI table S4 graph transcription; author coordinates withheld.'))
m=Chem.RemoveHs(m)
for a in m.GetAtoms():a.SetProp('atomNote',str(a.GetAtomMapNum()))
rdDepictor.Compute2DCoords(m)
Draw.MolToFile(m,str(B/'source_reviews'/pid/'di_graph.png'),size=(1800,1200))
print('PDI',rdMolDescriptors.CalcMolFormula(m),Chem.MolToSmiles(m))
