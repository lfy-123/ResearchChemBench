"""Source-grounded final specification refinements; no scientific solver is run."""
from author_last_four import *

def mol(x):
 p=Chem.SmilesParserParams();p.removeHs=False
 return Chem.MolFromSmiles(x['mapped_smiles'],p)
def byid(s):return {x['id']:x for x in s['species']}
def mapidx(m):return {a.GetAtomMapNum():a.GetIdx() for a in m.GetAtoms()}
def quad(m,i,j):
 left=sorted((a.GetAtomMapNum(),a.GetIdx()) for a in m.GetAtomWithIdx(i).GetNeighbors() if a.GetIdx()!=j and a.GetAtomicNum()>1)
 right=sorted((a.GetAtomMapNum(),a.GetIdx()) for a in m.GetAtomWithIdx(j).GetNeighbors() if a.GetIdx()!=i and a.GetAtomicNum()>1)
 return [left[0][0],m.GetAtomWithIdx(i).GetAtomMapNum(),m.GetAtomWithIdx(j).GetAtomMapNum(),right[0][0]]
def query_subgraph(m,indices):
 r=Chem.RWMol();pos={}
 for i in indices:pos[i]=r.AddAtom(Chem.AtomFromSmarts('[#'+str(m.GetAtomWithIdx(i).GetAtomicNum())+']'))
 for b in m.GetBonds():
  i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx()
  if i in pos and j in pos:r.AddBond(pos[i],pos[j],b.GetBondType())
 return r.GetMol()

def arm_map(a,b):
 ma,mb=mol(a),mol(b);rw=Chem.RWMol(ma)
 for bo in ma.GetBonds():
  i,j=bo.GetBeginAtomIdx(),bo.GetEndAtomIdx();aa,bb=ma.GetAtomWithIdx(i),ma.GetAtomWithIdx(j)
  if aa.GetIsAromatic()!=bb.GetIsAromatic() and aa.GetSymbol()==bb.GetSymbol()=='C':
   non=bb if aa.GetIsAromatic() else aa
   if non.GetHybridization() in (Chem.HybridizationType.SP3,Chem.HybridizationType.SP) and not any(n.GetAtomicNum()==7 for n in non.GetNeighbors()):rw.RemoveBond(i,j)
 frags=[list(f) for f in Chem.GetMolFrags(rw.GetMol()) if sum(ma.GetAtomWithIdx(i).GetIsAromatic() for i in f)>20]
 assert len(frags)==2
 used=set();pairs=[]
 for frag in frags:
  q=query_subgraph(ma,frag);matches=mb.GetSubstructMatches(q,uniquify=False,maxMatches=1000)
  good=next(t for t in matches if not set(t)&used);used.update(good)
  pairs.extend([[ma.GetAtomWithIdx(i).GetAtomMapNum(),mb.GetAtomWithIdx(j).GetAtomMapNum()] for i,j in zip(frag,good)])
 return {'from':a['id'],'to':b['id'],'atom_map_pairs':pairs,'meaning':'Full unchanged two-arm correspondence with identical elements and bond orders. Central C(CF3)2 and C≡C bridge atoms are unmatched intervention atoms.'}

s=SPECS['paper_3c058fa17fa7c54e'];d=byid(s)
s['controls']['mapping']=[arm_map(d['An_sigma_Ph'],d['An_pi_Ph']),arm_map(d['An_sigma_DA'],d['An_pi_DA'])]
s['controls']['torsion_quadruples']={}
for pair in s['controls']['mapping']:
 a,b=d[pair['from']],d[pair['to']];ma=mol(a);mp=dict(pair['atom_map_pairs']);qs=[]
 for bo in ma.GetBonds():
  aa,bb=bo.GetBeginAtom(),bo.GetEndAtom()
  if not bo.IsInRing() and bo.GetBondType()==Chem.BondType.SINGLE and aa.GetIsAromatic() and bb.GetIsAromatic():qs.append(quad(ma,aa.GetIdx(),bb.GetIdx()))
 assert len(qs)==4
 s['controls']['torsion_quadruples'][a['id']]=qs;s['controls']['torsion_quadruples'][b['id']]=[[mp[x] for x in q] for q in qs]
s['corrections'].append('Complete two-arm mapping excludes changed bridge carbons; both ethynyl attachment sites retain para-arm connectivity.')

s=SPECS['paper_746e066c163800d8'];path5=[1,66,65,64,63,62,61,59];mp=dict(s['controls']['paired_comparisons'][1]['atom_map_pairs']);path7=[mp[x] for x in path5]
s['controls']['matched_inner_rim']={'5_path':path5,'7_path':path7,'5_quadruples':[path5[i:i+4] for i in range(5)],'7_quadruples':[path7[i:i+4] for i in range(5)],'target_signed_degrees':[20]*5,'definition':'Ordered mapped graph paths; signed +20° is a benchmark geometry intervention, not an equilibrium value. Its all-negative mirror is equivalent in gas-phase scalar HRS if used consistently.'}
s['controls']['core_control']='Use exactly matched_inner_rim paths/quadruples and the +20° signed targets in both 5 and 7. Compare against independently relaxed structures. Verify each consecutive pair is bonded and preserve correspondence; no source terminal torsions are provided.'

s=SPECS['paper_0a62b797f51de2c0'];d=byid(s);a,b=d['CN1_n2'],d['CN1_n2_regio'];ma,mb=mol(a),mol(b)
# Core rings have identical insertion-order atom map identities; cyano branches move.
pa={a.GetAtomMapNum():a.GetIdx() for a in ma.GetAtoms() if a.IsInRing()};pb={a.GetAtomMapNum():a.GetIdx() for a in mb.GetAtoms() if a.IsInRing()}
# Full ring-topology query, irrespective of moved nitrile branches.
q=query_subgraph(ma,list(pa.values()));targets=mb.GetSubstructMatch(q);assert len(targets)==len(pa)
mp={ma.GetAtomWithIdx(i).GetAtomMapNum():mb.GetAtomWithIdx(j).GetAtomMapNum() for i,j in zip(pa.values(),targets)}
qa=[]
for bo in ma.GetBonds():
 if not bo.IsInRing() and bo.GetBeginAtom().GetIsAromatic() and bo.GetEndAtom().GetIsAromatic():qa.append(quad(ma,bo.GetBeginAtomIdx(),bo.GetEndAtomIdx()))
s['controls']['explicit_regio_map']={'from':a['id'],'to':b['id'],'atom_map_pairs':list(map(list,mp.items())),'meaning':'All ring atoms map; nitrile branch attachment is the intervention.'}
s['controls']['matched_torsion_quadruples']={a['id']:qa,b['id']:[[mp[x] for x in q] for q in qa]}
s['controls']['matched_torsion_signed_targets_deg']=[45]*len(qa)

s=SPECS['paper_9ec8c4761c4f171b'];d=byid(s);ref=mol(d['7a_ZHK']);coreq=Chem.RWMol(ref)
for a in ref.GetAtoms():coreq.ReplaceAtom(a.GetIdx(),Chem.AtomFromSmarts('[#'+str(a.GetAtomicNum())+']'))
for bo in ref.GetBonds():coreq.ReplaceBond(bo.GetIdx(),Chem.BondFromSmarts('~'))
q=coreq.GetMol()
pairs={};parents={}
for id in ['7a_ZHK','7a_EHK','7a_AE','7a_AK']:
 m=mol(d[id]);t=m.GetSubstructMatch(q);assert len(t)==ref.GetNumAtoms(),id
 pairs[id]=[[a.GetAtomMapNum(),m.GetAtomWithIdx(t[a.GetIdx()]).GetAtomMapNum()] for a in ref.GetAtoms()]
 mp=dict(pairs[id]);parent=5 if id.endswith('HK') else (1 if id.endswith('AE') else 3);parents[id]={'mobile_H_map':900,'parent_heavy_atom_map':mp[parent],'diagnostic_ring_C_map':mp[2]}
s['controls']['explicit_tautomer_atom_pairs_from_ZHK']=pairs;s['controls']['mobile_H_and_NMR_maps']=parents
s['controls']['H_mapping']='Use explicit_tautomer_atom_pairs_from_ZHK and mobile_H_and_NMR_maps. One tracked hydrogen900 moves N5→O1 or corresponding C4 in the mapped graphs. Other hydrogens remain attached to their corresponding heavy atoms; no change of total formula/charge is allowed.'
s['data']['experimental_observations.json']['spectral_diagnostics']['specific_7a_NH_ppm_CDCl3']=14.07
s['data']['experimental_observations.json']['spectral_diagnostics']['specific_7a_source']='SI p155 annotated 1H NMR peak at14.07ppm, CDCl3,296.4K; source-series rounded range12–14 is contextual.'
s['source_review']['paper_si']+=' Correct compound7a spectra are on154–157, not113–116; p155 NH14.07ppm/CDCl3 inspected visually.'

s=SPECS['paper_46f6118697c6397c'];d=byid(s);ref=mol(d['2'])
# In all constructed SMILES, preserved core insertion order is stable before first B substituents; derive matching subgraph by element/path.
core=[a.GetIdx() for a in ref.GetAtoms() if a.GetSymbol() in ['B','N'] or (a.GetSymbol()=='C' and any(n.GetSymbol()=='N' for n in a.GetNeighbors()))]
q=query_subgraph(ref,core);maps={}
for id in ['1','2','3','4']:
 m=mol(d[id]);t=m.GetSubstructMatch(q);assert len(t)==len(core)
 maps[id]=[[ref.GetAtomWithIdx(i).GetAtomMapNum(),m.GetAtomWithIdx(j).GetAtomMapNum()] for i,j in zip(core,t)]
s['controls']['common_core_atom_pairs_from_2']=maps

s=SPECS['paper_35a6749f3bae345b'];d=byid(s);ma=mol(d['DBC_Ph']);qs=[]
for bo in ma.GetBonds():
 aa,bb=bo.GetBeginAtom(),bo.GetEndAtom()
 if not bo.IsInRing() and aa.GetIsAromatic() and bb.GetIsAromatic():qs.append(quad(ma,aa.GetIdx(),bb.GetIdx()))
assert len(qs)==2
mp=dict(s['controls']['pair_map']['atom_map_pairs']);s['controls']['common_torsion_quadruples']={'DBC_Ph':qs,'DBC_Nap':[[mp[x] for x in q] for q in qs]};s['controls']['matched_signed_targets_deg']=[45,45]

# Fix fold identities at schema level; arbitrary duplication of an AZ member cannot fill ten folds.
s=SPECS['paper_5d94285cfbd51973'];p=next(p for p in s['panels'] if p['id']=='out_of_fold')
for name,sch in p['schema']['properties'].items():
 sch['properties']['heldout_id']=C(name);sch['properties']['training_ids']['items']=E(*[x for x in p['schema']['properties'] if x!=name]);sch['properties']['observed_bin']['maximum']=2
# Identity-correct, evidence-backed collapse has a physical branch in schemas; absence does not invent frequency data.

s=SPECS['paper_3e4cad1d1d650d0c']
s['data']['quenching_figure3.png']=B/'source_reviews'/s['id']/'quenching_figure3.png'
s['data']['observations.json']['challenge_only']['plot_file']='quenching_figure3.png'
s['data']['observations.json']['challenge_only']['plot_interpretation']='Cropped original experimental Figure3 axes and plotted observations; estimate a plot-resolution bound, not instrument error bars. No calculated or author-assigned molecular outcome is included.'
p=next(p for p in s['panels'] if p['id']=='quenching_challenge')
p['schema']['properties']['lifetime_change_fraction']={'type':['number','null'],'description':'Null if no resolved change is measurable from the public raster; never a fabricated instrument measurement.'}
p['schema']['properties']['lifetime_evidence_kind']=E('plot_resolution_bound','qualitative_only')
p['schema']['required'].append('lifetime_evidence_kind')
p['schema']['properties']['lifetime_change_upper_bound_fraction']={'type':'number','minimum':0}
p['schema']['properties']['public_plot_file']=C('data/inputs/quenching_figure3.png')
p['schema']['required'].append('public_plot_file')
p['schema']['allOf']=[{'if':{'properties':{'lifetime_evidence_kind':C('plot_resolution_bound')}},'then':{'required':['lifetime_change_upper_bound_fraction']}},{'if':{'properties':{'lifetime_evidence_kind':C('qualitative_only')}},'then':{'properties':{'lifetime_change_fraction':C(None)}}}]
p['criteria']='Freeze the redox cycle before evaluating the intensity/lifetime challenge. Use the supplied original Figure3 crop to test dynamic and static/association explanations. A numerical lifetime-change upper bound must explicitly be a plot-resolution estimate, with axis/marker calibration and analysis evidence; it is not an instrument uncertainty. If a quantitative bound cannot be justified, submit lifetime_evidence_kind=qualitative_only and lifetime_change_fraction=null with the supported qualitative challenge and its resolution limit. Raw individual lifetime measurements and errors are unavailable and must not be invented. Favorable ΔGET does not settle the quenching mechanism or yield.'
s['corrections'].append('The original experimental Figure3 crop is public. The contract separates a plot-resolution upper bound from unavailable numerical lifetime measurements; justified qualitative-only challenge is admissible.')

if __name__=='__main__':
 for pid in sys.argv[1:] or IDS:build(SPECS[pid])
 dump(B/'final_specs.json',SPECS) if False else None
