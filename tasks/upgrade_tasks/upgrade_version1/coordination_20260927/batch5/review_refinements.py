"""Final identity/control refinements; no conformer, minimum, or engine prediction."""
from pathlib import Path
import json
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors,rdFMCS
B=Path(__file__).resolve().parent;R=B.parents[3];P=B/'prepared_inputs'
def dump(p,d):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n')
def mol(d,hs=False):
 p=Chem.SmilesParserParams();p.removeHs=not hs
 return Chem.MolFromSmiles(d['mapped_smiles'],p)
def graph(m,label,source):
 m=Chem.AddHs(m)
 for i,a in enumerate(m.GetAtoms()):a.SetAtomMapNum(i+1)
 return {'id':label,'formula':rdMolDescriptors.CalcMolFormula(m),'charge':Chem.GetFormalCharge(m),'mapped_smiles':Chem.MolToSmiles(m),'atoms':[{'atom_id':a.GetAtomMapNum(),'element':a.GetSymbol(),'formal_charge':a.GetFormalCharge()} for a in m.GetAtoms()],'bonds':[{'a':b.GetBeginAtom().GetAtomMapNum(),'b':b.GetEndAtom().GetAtomMapNum(),'order':str(b.GetBondType())} for b in m.GetBonds()],'source':source,'source_coordinates_public':False,'mapping':'One-based benchmark IDs. No optimized geometry or state result is implied.'}
def torsion(m,a,b):
 ns=lambda atom,other: sorted([x for x in atom.GetNeighbors() if x.GetIdx()!=other.GetIdx() and x.GetSymbol()!='H'],key=lambda x:x.GetAtomMapNum())
 return [ns(a,b)[0].GetAtomMapNum(),a.GetAtomMapNum(),b.GetAtomMapNum(),ns(b,a)[0].GetAtomMapNum()]
# Common complete graph metadata, identically available to AR and PR.
p='paper_b5c446c7067dd511';src=R/'tasks/final_verified_paper_reproduction'/p/'agent_input/data/inputs/molecular_identities.json';d=json.loads(src.read_text());d.pop('source_evidence',None)
for row in d['molecules']:
 g=graph(Chem.MolFromSmiles(row['connectivity_smiles']),row['id'],'SI systematic name, source identity SMILES and formula; no state assignment.');assert g['formula']==row['formula'];dump(P/p/(row['id']+'_identity.json'),g)
 m=mol(g);cuts=[]
 for bond in m.GetBonds():
  a,b=bond.GetBeginAtom(),bond.GetEndAtom()
  if bond.IsInRing() or bond.GetBondType()!=Chem.BondType.SINGLE or not(a.GetIsAromatic() and b.GetIsAromatic()):continue
  fr=Chem.GetMolFrags(Chem.FragmentOnBonds(m,[bond.GetIdx()],addDummies=False))
  # Terminal fused/phenyl carbon-only aromatic fragment; p-tolyl N-link is excluded.
  for f in fr:
   if len(f)=={'Ph-mP':6,'Na-mP':10,'An-mP':14,'Py-mP':16}[row['id']] and all(m.GetAtomWithIdx(i).GetSymbol()=='C' and m.GetAtomWithIdx(i).GetIsAromatic() for i in f):
    if a.GetIdx() in f:a,b=b,a
    cuts.append({'torsion_atom_ids':torsion(m,a,b),'terminal_atom_ids':sorted(m.GetAtomWithIdx(i).GetAtomMapNum() for i in f),'target_degrees':45})
 assert len(cuts)==1,(row['id'],cuts)
 row['identity_file']=row['id']+'_identity.json';row['terminal_bridge_control']=cuts[0]
dump(P/p/'molecular_identities.json',d)
# Three core-to-linker bonds, same signed four-atom orientation convention.
p='paper_3316e45a74258fb7';out={}
for label in ['TD_2T','CD_2T','TD_2C']:
 d=json.loads((P/p/(label+'_identity.json')).read_text());m=mol(d);cuts=[]
 for bond in m.GetBonds():
  a,b=bond.GetBeginAtom(),bond.GetEndAtom()
  if bond.IsInRing() or bond.GetBondType()!=Chem.BondType.SINGLE or not(a.GetIsAromatic() and b.GetIsAromatic()):continue
  fr=Chem.GetMolFrags(Chem.FragmentOnBonds(m,[bond.GetIdx()],addDummies=False))
  # Each donor fragment has one N; complementary core and two donors contain six N.
  cf=[f for f in fr if len(f)==19 and sum(m.GetAtomWithIdx(i).GetSymbol()=='N' for i in f)==1]
  if len(cf)!=1:continue
  donor=cf[0]
  if a.GetIdx() in donor:a,b=b,a
  cuts.append({'torsion_atom_ids':torsion(m,a,b),'donor_atom_ids':sorted(m.GetAtomWithIdx(i).GetAtomMapNum() for i in donor),'target_degrees':45})
 assert len(cuts)==3,(label,cuts)
 out[label]=cuts
dump(P/p/'torsion_control_mapping.json',{'objects':out,'convention':'For every quadruple [core-neighbor, core attachment, linker attachment, linker-neighbor], set the signed dihedral to +45 degrees using the standard right-handed bond-axis convention; verify achieved angles. Atom IDs match the object identity. These are imposed benchmark interventions, not equilibrium predictions.','state_partition':'Use the three listed donor atom sets, with remaining heavy atoms as common core; assign bonded H to its heavy-atom fragment.'})
# Planar Cy2 conjugated bridge: the path between the two heterocyclic bridge endpoints.
p='paper_e0791c047a731974';d=json.loads((P/p/'Cy2_identity.json').read_text());m=mol(d);byid={a.GetAtomMapNum():a.GetIdx() for a in m.GetAtoms()};path=Chem.GetShortestPath(m,byid[18],byid[28]);ids=[m.GetAtomWithIdx(i).GetAtomMapNum() for i in path];assert ids==[18,9,8,3,2,1,4,5,28],ids
qs=[ids[i:i+4] for i in range(len(ids)-3)]
dump(P/p/'Cy2_planar_control.json',{'chain_endpoint_path':ids,'dihedral_atom_quadruples':qs,'target_degrees':[180]*len(qs),'definition':'All consecutive carbon-backbone dihedrals on the specified conjugated chain are trans planar (180 degrees). This is a deliberately imposed all-trans planar intervention, not the source optimized state. Preserve connectivity/charge, relax other coordinates, then release all constraints and classify the endpoint. Compare the same physical states by density.','scope':'This single representative geometry control separates geometry response within Cy2; it does not make the three sensitizers an isostructural series.'})
# Neutral single lactam-to-lactim tautomer, with explicit H and bond changes.
p='paper_988bc12ae3768679';d=json.loads((P/p/'parent_identity.json').read_text());m=mol(d,True);rw=Chem.RWMol(m);byid={a.GetAtomMapNum():a.GetIdx() for a in rw.GetAtoms()};rw.RemoveBond(byid[11],byid[8]);rw.AddBond(byid[9],byid[8],Chem.BondType.SINGLE);rw.GetBondBetweenAtoms(byid[11],byid[6]).SetBondType(Chem.BondType.DOUBLE);rw.GetBondBetweenAtoms(byid[6],byid[9]).SetBondType(Chem.BondType.SINGLE);taut=rw.GetMol();Chem.SanitizeMol(taut);assert rdMolDescriptors.CalcMolFormula(taut)=='C30H20N6O4'
sf=P/p/'candidate_seeds.json';s=json.loads(sf.read_text());s['required_seeds']=[x for x in s['required_seeds'] if x['candidate_id']!='neutral_lactim'];s['required_seeds'].append({'candidate_id':'neutral_lactim','mapped_smiles':Chem.MolToSmiles(taut),'formula':'C30H20N6O4','charge':0,'multiplicity':1,'proton_change':0,'tautomer_class':'lactim','edits':[{'move_H_id':8,'from_atom_id':11,'to_atom_id':9},{'bond':[11,6],'from':'SINGLE','to':'DOUBLE'},{'bond':[6,9],'from':'DOUBLE','to':'SINGLE'}],'role':'Required neutral tautomer seed, not a predicted minimum or winning assignment'})
s['neutral']='Include unchanged parent (candidate_id neutral_parent) and one explicit neutral_lactim seed. Acid_O/acid_azoN and base_O/base_lactamN test distinct proton sites. Other single-proton/hydrazone alternatives are optional unless needed to resolve observations.';dump(sf,s)
# Exact retained heavy map for Egan -> egan by applying stated deletions.
p='paper_e31cc7bc7b21b610';full=json.loads((P/p/'Egan_identity.json').read_text());trunc=json.loads((P/p/'egan_identity.json').read_text());mf=mol(full);mt=mol(trunc);remove={i for cut in full['truncation_rule'] for i in cut['delete_heavy_ids']};rw=Chem.RWMol(mf)
for idx in sorted([a.GetIdx() for a in mf.GetAtoms() if a.GetAtomMapNum() in remove],reverse=True):rw.RemoveAtom(idx)
# Explicit-H graph lost substituent bonds: allow valence restoration to H when sanitized.
remaining=rw.GetMol();Chem.SanitizeMol(remaining);query=Chem.MolFromSmarts(Chem.MolToSmarts(remaining));match=mt.GetSubstructMatch(query)
if not match:
 result=rdFMCS.FindMCS([remaining,mt],timeout=20,atomCompare=rdFMCS.AtomCompare.CompareElements,bondCompare=rdFMCS.BondCompare.CompareOrderExact,ringMatchesRingOnly=True,completeRingsOnly=True)
 assert not result.canceled and result.numAtoms==remaining.GetNumAtoms()==mt.GetNumAtoms()
 q=Chem.MolFromSmarts(result.smartsString);left=remaining.GetSubstructMatch(q);right=mt.GetSubstructMatch(q)
else:left=range(remaining.GetNumAtoms());right=match
pairs=[[remaining.GetAtomWithIdx(i).GetAtomMapNum(),mt.GetAtomWithIdx(j).GetAtomMapNum()] for i,j in zip(left,right)];assert len(pairs)==36
for i,j in pairs:
 for k,l in pairs:
  a=mf.GetBondBetweenAtoms(next(a.GetIdx() for a in mf.GetAtoms() if a.GetAtomMapNum()==i),next(a.GetIdx() for a in mf.GetAtoms() if a.GetAtomMapNum()==k));b=mt.GetBondBetweenAtoms(next(a.GetIdx() for a in mt.GetAtoms() if a.GetAtomMapNum()==j),next(a.GetIdx() for a in mt.GetAtoms() if a.GetAtomMapNum()==l));assert (a is None)==(b is None)
dump(P/p/'retained_heavy_mapping.json',{'pairs_full_Egan_to_egan':pairs,'per_ligand_retained_heavy_count':36,'deleted_heavy_atom_ids':sorted(remove),'prefix':'Apply this map separately to A/ and B/ ligand copies. Ir_A maps to Ir_A and Ir_B to Ir_B.','hydrogen_policy':'Rebuild hydrogens by valence after the four tBu-to-H substitutions; retained-heavy coordinates match exactly for paired frozen controls. No source geometry is supplied.'})
print('Refined b5 identities, three torsion definitions, explicit neutral tautomer and exact Ir mapping.')
