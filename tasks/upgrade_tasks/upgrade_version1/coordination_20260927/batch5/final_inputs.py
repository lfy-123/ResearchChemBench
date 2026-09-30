from pathlib import Path
import json,hashlib,re
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors,rdFMCS
B=Path(__file__).resolve().parent;O=B/'prepared_inputs'
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
def graph(m,label):
 m=Chem.AddHs(m)
 for i,a in enumerate(m.GetAtoms()):a.SetAtomMapNum(i+1)
 return {'id':label,'formula':rdMolDescriptors.CalcMolFormula(m),'charge':Chem.GetFormalCharge(m),'mapped_smiles':Chem.MolToSmiles(m),'atoms':[{'atom_id':a.GetAtomMapNum(),'element':a.GetSymbol(),'formal_charge':a.GetFormalCharge()} for a in m.GetAtoms()],'bonds':[{'a':b.GetBeginAtom().GetAtomMapNum(),'b':b.GetEndAtom().GetAtomMapNum(),'order':str(b.GetBondType())} for b in m.GetBonds()],'source_coordinates_public':False}
# Bounded seeds from parent IDs, not source endpoint coordinates.
p='paper_988bc12ae3768679';parent=json.loads((O/p/'parent_identity.json').read_text());par=Chem.SmilesParserParams();par.removeHs=False;base=Chem.MolFromSmiles(parent['mapped_smiles'],par)
seeds=[]
for label,sites,delta in [('acid_O',[57,58],1),('acid_azoN',[33,34],1),('base_O',[57,58],-1),('base_lactamN',[11,12],-1)]:
 rw=Chem.RWMol(base);edits=[]
 for site in sites:
  atom=next(a for a in rw.GetAtoms() if a.GetAtomMapNum()==site)
  if delta==1:
   h=Chem.Atom('H');h.SetAtomMapNum(1000+site);idx=rw.AddAtom(h);rw.AddBond(atom.GetIdx(),idx,Chem.BondType.SINGLE);atom.SetFormalCharge(atom.GetFormalCharge()+1);edits.append({'add_H_id':1000+site,'to_atom_id':site,'formal_charge_change':1})
  else:
   hs=[a for a in atom.GetNeighbors() if a.GetSymbol()=='H'];assert len(hs)==1
   hid=hs[0].GetAtomMapNum();atom.SetFormalCharge(atom.GetFormalCharge()-1);rw.RemoveAtom(hs[0].GetIdx());edits.append({'remove_H_id':hid,'from_atom_id':site,'formal_charge_change':-1})
 m=rw.GetMol();Chem.SanitizeMol(m);seeds.append({'candidate_id':label,'mapped_smiles':Chem.MolToSmiles(m),'formula':rdMolDescriptors.CalcMolFormula(m),'charge':2*delta,'multiplicity':1,'proton_change':2*delta,'edits':edits,'role':'Required competitor seed; no stability or assignment asserted'})
dump(O/p/'candidate_seeds.json',{'parent_file':'parent_identity.json','required_seeds':seeds,'neutral':'Include unchanged parent; acid_O and acid_azoN are site competitors, base_O and base_lactamN are site competitors. Additional single-proton or hydrazone/lactim alternatives are allowed, not mandatory.','proton_mapping':'Existing atom IDs retained; added H uses 1000+attached atom ID; remove the listed original H only.','conformer_starts':'At least two independent phenyl-azo torsion arrangements per seed. Optimize without preserving an assumed endpoint assignment.','proton_reference':'Use a declared isodesmic acid/base pair with all species computed in the same solvent; tabulate coefficients, charges and H counts. Absolute H+ solvation conventions must be explicit if used.'})
# Full Egan and exact tert-butyl truncation; quinonoid Lewis graph is one resonance form.
p='paper_e31cc7bc7b21b610'
full='O=C(OCCOC(=O)c1ccccc1N=C1C(=O)C(C(C)(C)C)=CC(C(C)(C)C)=C1)c1ccccc1N=C1C(=O)C(C(C)(C)C)=CC(C(C)(C)C)=C1'
m=Chem.MolFromSmiles(full);g=graph(m,'Egan');assert g['formula']=='C44H52N2O6',g['formula']
g['source']='Main chemical synthesis name/elemental formula C44H52N2O6 and Scheme1/Figure5; quinonoid connectivity, not a forced ligand oxidation state.'
qm=Chem.MolFromSmiles(g['mapped_smiles']);rings={a.GetAtomMapNum() for a in qm.GetAtoms() if a.IsInRing()};cuts=[]
for a in qm.GetAtoms():
 if a.GetSymbol()=='C' and not a.IsInRing() and len([n for n in a.GetNeighbors() if n.GetSymbol()=='C'])==4:
  ring=next((n for n in a.GetNeighbors() if n.IsInRing()),None)
  if ring:cuts.append({'ring_atom':ring.GetAtomMapNum(),'tert_butyl_center':a.GetAtomMapNum(),'delete_heavy_ids':[a.GetAtomMapNum()]+[n.GetAtomMapNum() for n in a.GetNeighbors() if n.GetIdx()!=ring.GetIdx()]})
assert len(cuts)==4
# Truncated graph independent, with MCS atom map to full skeleton.
trunc='O=C(OCCOC(=O)c1ccccc1N=C1C(=O)C=CC=C1)c1ccccc1N=C1C(=O)C=CC=C1'
tg=graph(Chem.MolFromSmiles(trunc),'egan');assert tg['formula']=='C28H20N2O6',tg['formula']
g['truncation_rule']=cuts;tg['source']='Same Egan heavy skeleton with each of four ring tert-butyl groups replaced by H; source computational-method definition.'
for gg in [g,tg]:
 mm=Chem.MolFromSmiles(gg['mapped_smiles']);nit=[a.GetAtomMapNum() for a in mm.GetAtoms() if a.GetSymbol()=='N'];ox=[]
 for a in mm.GetAtoms():
  if a.GetSymbol()=='O' and len(a.GetNeighbors())==1:
   c=a.GetNeighbors()[0]
   if c.IsInRing():ox.append(a.GetAtomMapNum())
 gg['metal_donor_atoms']={'N':nit,'quinonoid_O':ox};gg['assembly']='Each Egan/egan chelates one Ir via both iminoxolene N,O pairs (four-coordinate Ir); two Ir fragments form a dimer with opposite local helicities A,C. Ester O atoms are not assigned Ir bonds in this dimer.'
 dump(O/p/(gg['id']+'_identity.json'),gg)
dump(O/p/'dimer_definition.json',{'full_dimer':{'formula':'C88H104Ir2N4O12','charge':0,'multiplicities':[1,3],'ligands':['Egan_A','Egan_B'],'metal_ids':['Ir_A','Ir_B']},'truncated_dimer':{'formula':'C56H40Ir2N4O12','charge':0,'multiplicities':[1,3],'ligands':['egan_A','egan_B']},'mapping':'Prefix all ligand atom IDs by A/ or B/. Four tert-butyl removals per ligand are listed in Egan_identity.json; retain all remaining heavy atoms and replace deleted substituents by H. Derive one-to-one retained-heavy mapping by graph isomorphism, report it.','fragments':'For each dimer split into neutral (ligand)Ir_A and neutral (ligand)Ir_B doublets, multiplicity2; compare their opposite-spin-coupled singlet and triplet whole dimers. Fixed neutral doublet fragments define this benchmark energy decomposition, not formal localized oxidation states.','geometry_control':'For both sizes scan Ir-Ir distance at R_eq and R_eq+0.2 and +0.5 angstrom with rigid neutral fragments; same relative twist. Compare a 30-degree relative twist at fixed R_eq. Retain mapped ligand coordinates.','source_boundary':'Full Egan-to-egan pair is a benchmark extension of source Hap simplification. No crystal/optimized coordinates, measured Ir-Ir bond length or electronic state winner is provided. Source Hap4Ir2 may be used only as optional additional calibration.'})
# Ln model requirements, exact source ECP gate retained.
p='paper_d8e5490cd9942f4f'
dump(O/p/'metal_and_hydration_definition.json',{'metals':{'La':{'Z':57,'f_core_electrons':46,'explicit_electrons_neutral_atom':11},'Tb':{'Z':65,'f_core_electrons':54,'explicit_electrons_neutral_atom':11},'Lu':{'Z':71,'f_core_electrons':60,'explicit_electrons_neutral_atom':11}},'formal_complex_charge':1,'model_multiplicity':1,'spin_warning':'Pseudo-singlet in the 4f-core model does not assert physical Tb spin zero.','source_basis':'Dolg (7s6p5d)/[5s4p3d] with 46+4f^n electron core. Exact numerical coefficients/ECP files have not been verified in this development audit.','starting_structures':'Use both La XYZs as starting topology. Replace only La element at its existing row with Tb or Lu. This generates starting guesses, not source optimized Tb/Lu structures. Preserve original row IDs.','hydration':'For each syn/anti metal complex add one neutral H2O with O ID82 and H83/84, plus a free-water reference; trial Mn-O starts at 2.6 and 3.0 angstrom along the least-occupied coordination direction. Original O,N donor set unchanged initially. Allow water loss/collapse with evidence; never count disconnected water as a bound minimum.','required_matrix':'La/Tb/Lu x syn/anti x zero/one water; compare frozen La skeleton metal substitutions separately from relaxed states.','blocked_release':'Stage independently verified Gaussian/ORCA numerical molecular ECP+basis for each of La/Tb/Lu, verify core counts and contraction, then pilot one minimum. BSE Stuttgart RLC metadata does not cover these Ln entries; name alone is insufficient.'})
print('Generated candidate, full/truncated Ir and Ln identity contracts')
