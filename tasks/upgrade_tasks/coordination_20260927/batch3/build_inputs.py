"""Construct public identities from source graphs, never publish optimized answers."""
from pathlib import Path
import json,copy,math,re,hashlib
from collections import Counter
import numpy as np
import networkx as nx
from rdkit import Chem
from rdkit.Chem import rdDetermineBonds,AllChem,rdMolDescriptors
from ase.io import read as ase_read
B=Path(__file__).parent;ROOT=B.resolve().parents[3];DEST=ROOT/'tasks/upgrade_tasks';EX=json.load(open(B/'extracted_objects.json'));PT=Chem.GetPeriodicTable()
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
def source(pid,name):return ROOT/'tasks/final_verified_autonomous_research'/pid/'agent_input/data/inputs'/name
def formula(atoms):
 c=Counter(a['element'] for a in atoms);return ''.join(e+(str(c[e]) if c[e]>1 else '') for e in sorted(c,key=lambda e:(e not in ['C','H'],{'C':0,'H':1}.get(e,2),e)))
def from_mol(m,id,q=0,mult=1,prov='',ids=None):
 atoms=[{'id':ids[i] if ids else i+1,'element':a.GetSymbol(),'formal_charge':a.GetFormalCharge()} for i,a in enumerate(m.GetAtoms())]
 for a,record in zip(m.GetAtoms(),atoms):
  if a.GetAtomMapNum():record['source_atom_map']=a.GetAtomMapNum()
 bonds=[{'a':atoms[b.GetBeginAtomIdx()]['id'],'b':atoms[b.GetEndAtomIdx()]['id'],'order':str(b.GetBondType()),'kind':'covalent'} for b in m.GetBonds()]
 return {'id':id,'formula':formula(atoms),'charge':q,'multiplicity':mult,'atoms':atoms,'bonds':bonds,'provenance':prov,'coordinates_policy':'Only topology is public. Independently construct and optimize geometries; no source optimized coordinates or energies are provided.'}
def from_smi(smiles,id,q=0,mult=1,prov='explicit chemical definition'):
 m=Chem.AddHs(Chem.MolFromSmiles(smiles));return from_mol(m,id,q,mult,prov)
def from_xyz(rows,id,q=0,mult=1,prov='',skip=()):
 selected=[(i+1,a) for i,a in enumerate(rows) if a[0] not in skip];ids=[i for i,a in selected];ar=[a for i,a in selected]
 xyz=str(len(ar))+'\nidentity extraction\n'+'\n'.join(a[0]+' '+' '.join(f'{v:.9f}' for v in a[1:]) for a in ar)+'\n'
 m=Chem.MolFromXYZBlock(xyz);rdDetermineBonds.DetermineBonds(m,charge=q,embedChiral=False)
 return from_mol(m,id,q,mult,prov,ids)
def simple_adjacency(rows,id,q,mult,prov,metal=False,cage=False):
 atoms=[{'id':i+1,'element':a[0]} for i,a in enumerate(rows)];edges=[]
 for i,a in enumerate(rows):
  for j in range(i):
   c=rows[j];d=math.dist(a[1:],c[1:]);limit=1.20*(PT.GetRcovalent(a[0])+PT.GetRcovalent(c[0]));ismetal=a[0] in ['Ir','Cd','Co','Ni'] or c[0] in ['Ir','Cd','Co','Ni']
   if ismetal:limit=2.65 if 'Cd' in [a[0],c[0]] else 2.45
   if 0.4<d<limit:
    edges.append({'a':j+1,'b':i+1,'kind':'coordination' if ismetal else ('cage_adjacency' if cage and a[0] in ['B','C'] and c[0] in ['B','C'] and (a[0]=='B' or c[0]=='B') else 'covalent_adjacency'),'order':'not_a_two_center_bond_order' if cage else 'connectivity_only'})
 return {'id':id,'formula':formula(atoms),'charge':q,'multiplicity':mult,'atoms':atoms,'bonds':edges,'provenance':prov,'graph_convention':'Edges specify atom adjacency, not a valence-bond electronic solution. Metal coordination or closo multicenter bonding must be represented with the stated total charge/spin; no inferred S-S edge is permitted. Validate chemical valence before 3D preparation.'}
def cif_graph(pid,name,id):
 a=ase_read(source(pid,name),store_tags=True);info=a.info;labels=info['_atom_site_label'];syms=info['_atom_site_type_symbol'];f=np.array([[float(info['_atom_site_fract_'+k][i]) for k in ['x','y','z']] for i in range(len(labels))]);rows=[[syms[i],*map(float,p)] for i,p in enumerate(f@a.cell.array)]
 # Deposited asymmetric molecule: preserve public experimental connectivity labels.
 try:g=from_xyz(rows,id,prov='Immutable public '+name+' asymmetric molecular component',ids=None)
 except TypeError:g=from_xyz(rows,id,prov='Immutable public '+name+' asymmetric molecular component')
 g['cif_atom_labels']={str(i+1):l for i,l in enumerate(labels)};return g

def variants(g,states):
 return [dict(copy.deepcopy(g),id=name,charge=q,multiplicity=m) for name,q,m in states]
def fragments(id,parts,graphs,charge=0,mult=1,definition=''):
 return {'id':id,'components':[{'object_id':k,'count':v} for k,v in parts.items()],'charge':charge,'multiplicity':mult,'component_atom_map':'Use component ID, copy number, and source atom ID as tuple; never merge atom IDs across copies.','assembly_definition':definition,'coordinates_policy':'Build independent relative orientations; all intermolecular contacts are candidates, not fixed minima.'}
def build(pid):
 short=pid[6:];objects=[];controls={};files=[];block=[];additional={}
 get=lambda n:EX[short+'_'+n]
 if short=='36722b90a0c12825':
  host=from_xyz(get('e_ab_mtta_13ph_cl_open'),'host',skip=['Cl'],prov='Final source host composition/graph; SI1 pp2-8; coordinates withheld')
  el={a['id']:a['element'] for a in host['atoms']};adj={i:[] for i in el}
  for edge in host['bonds']:adj[edge['a']].append(edge['b']);adj[edge['b']].append(edge['a'])
  nns=[b for b in host['bonds'] if b['order']=='DOUBLE' and all(el[b[x]]=='N' and any(el[v]=='C' for v in adj[b[x]]) and sum(el[v]=='N' for v in adj[b[x]])==1 for x in ['a','b'])];assert len(nns)==1
  for name in ['E_free','Z_free']:
   g=copy.deepcopy(host);g['id']=name;g['stereochemistry']={'azo_bond':[nns[0]['a'],nns[0]['b']],'configuration':name[0],'other_torsions':'sample independently'};objects.append(g)
  objects+=[from_smi('[Cl-]','chloride',-1),from_smi('CCCC[N+](CCCC)(CCCC)CCCC','TBA',1)]
  for st in ['E','Z']:objects.append(fragments(st+'_bound',{st+'_free':1,'chloride':1},objects,-1,definition='Multiple triazole-facing chloride starts; allow rearrangement within host stereochemical family.'))
  controls={'azo_bond':list(nns[0][x] for x in ['a','b']),'primary_medium':'acetone','temperature_K':298.15,'standard_state':'1 M','reaction_coefficients':{'E_bind':{'E_bound':1,'E_free':-1,'chloride':-1},'Z_bind':{'Z_bound':1,'Z_free':-1,'chloride':-1}}}
 elif short=='9455a82229de2427':
  objects=[{'id':'SiN','charge':0,'multiplicity':2,'formula':'NSi','atoms':[{'id':'Si1','element':'Si'},{'id':'N1','element':'N'}],'bonds':[{'a':'Si1','b':'N1','kind':'covalent','order':'diatomic_identity_not_closed_shell_assignment'}]},from_smi('[CH2:1]=[C:2]([CH3:5])[CH:3]=[CH2:4]','isoprene'),from_smi('[H]','H_atom',0,2)]
  controls={'isoprene_map':'C1=C2(C5)-C3=C4; numbered atom-map labels in original SMILES, explicit stable graph IDs in object table','mapped_smiles':'[CH2:1]=[C:2]([CH3:5])[CH:3]=[CH2:4]','attack_pairs':[['Si1','C1'],['Si1','C4'],['N1','C1'],['N1','C4']],'candidate_rule':'Enumerate graph edits preserving Si1/N1 and all carbon labels. Ring closures join the unattached heteroatom to the opposite terminal carbon; include nonclosure/H-shift alternatives. Tag each removed H explicitly. Product graph not provided; discovery is scored.','product_composition':{'C':5,'H':7,'Si':1,'N':1},'intermediate_charge':0,'intermediate_multiplicity':2,'product_charge':0,'product_multiplicity':1,'energy_zero':'separated_SiN_plus_isoprene_E0_0K'}
  files=['reactants.json']
 elif short=='9a58a1fa6ed7d780':
  objects=[from_xyz(get('bn_akflu_s0'),'BN',prov='SI TableS21, pp49-50; graph only'),from_xyz(get('CC_AkFlu'),'CC',prov='SI TableS22 pp50-51; graph only')]
  graphs=[]
  for o in objects:
   g=nx.Graph();g.add_nodes_from((a['id'],{'role':'H' if a['element']=='H' else 'heavy'}) for a in o['atoms']);g.add_edges_from((b['a'],b['b']) for b in o['bonds']);graphs.append(g)
  matcher=nx.algorithms.isomorphism.GraphMatcher(*graphs,node_match=lambda a,b:a['role']==b['role']);assert matcher.is_isomorphic();mapping=matcher.mapping
  controls={'common_map':sorted([k,v] for k,v in mapping.items()),'common_adjacency_equal':True,'mapping_definition':'Graph isomorphism retaining H/heavy identity; source tables use different atom ordering. BN atom ID is first, CC atom ID second.','BN_sites':[{**a,'CC_atom_id':mapping[a['id']],'CC_element':'C'} for a in objects[0]['atoms'] if a['element'] in ['B','N']],'cross_geometry':'Use the two chemical graphs at each relaxed mapped heavy-atom frame; all 40 atoms map one-to-one, with the four listed B/N atoms replaced by C. Report constraints.','Sr_definition':'integral sqrt(normalized rho_hole * normalized rho_electron) dV'}
 elif short=='9f4c259696ad2f87':
  objects=[from_xyz(get('compound_1_start'),'PXX1',prov='SI pp144-146 graph'),from_xyz(get('PXX2'),'PXX2',prov='SI pp147-149 graph'),from_smi('B(c1c(F)c(F)c(F)c(F)c1F)(c1c(F)c(F)c(F)c(F)c1F)c1c(F)c(F)c(F)c(F)c1F','acid')]
  sites={}
  for o in objects[:2]:
   oxy={a['id'] for a in o['atoms'] if a['element']=='O'};sites[o['id']]={'carbonyl_O':[b[x] for b in o['bonds'] if b['order']=='DOUBLE' for x in ['a','b'] if b[x] in oxy],'other_O':[x for x in oxy if all(not(b['order']=='DOUBLE' and x in [b['a'],b['b']]) for b in o['bonds'])]}
  controls={'donor_sites':sites,'acid_binding':'Place acid B near each allowed O and include opposite-side orientations; compare all chemically distinct O sites at each stoichiometry. PXX1 acid2 can dissociate, which must be demonstrated.'}
  for name in ['PXX1','PXX2']:
   for n in [1,2]:objects.append(fragments(f'{name}_acid{n}',{name:1,'acid':n},objects,definition='O...B association at the enumerated donor sites; total charge0.'))
  additional['experimental_observations.json']={'source':'Main Table1 and Fig6 (PDF pp6,9); SI FigS102 PDFp87 and Lewis-adduct discussion p167','medium':'CH2Cl2, room temperature, air-equilibrated','free_absorption_nm':{'PXX1':543,'PXX2':555},'PXX1_titration':{'initial_chromophore_M':9.6e-6,'acid_equivalents_range':[0,150],'observed_features':['red-shifted absorption with acid addition','reported isosbestic points']},'PXX2_observation':'The source reports only one equivalence feature and no resolved separate spectra for multiple acid-bound species; occupancy is the inference to test.','SI_S102_caveat':'Reaction drawing says compound2, caption calls titrated material1 at4.5e-6 M and0-160eq. Do not silently resolve this label conflict or transfer its concentration to the main PXX1 series.','data_limit':'No digitized full concentration-resolved traces are supplied. Core comparison is signed optical trend and ability to distinguish calculated species within computed uncertainty, not a fit of an unavailable titration curve. All numeric values here are experimental inputs, not calculated targets.'}
 elif short=='a0f6b899582cb9f7':
  objects=[from_smi('c1ccsc1-c2cnc(-c3cccs3)cn2','M3')];files=['m3_identity.json','m3.xyz'];controls={'required_missing_objects':['source_PM6_BDD_capped_graph','source_BTP_eC9_core_capped_graph','enlarged_matched_fragment'],'blocker':'The main Fig1 identifies regions but does not give unambiguous cap atoms or a digitized complete pair graph. No invented fragment supplied.'}
 elif short=='b276b18215cba283':
  objects=[from_xyz(get('transoid'),'single_arm',prov='SI TableS8 graph'),from_xyz(get('three_arm'),'three_arm',prov='SI TableS10 pp51-58 graph')]
  controls={'arm_graph_matching':'Map the exocyclic merocyanine chain connecting each heterocycle N-adjacent C to the central 1,3,5-tricarbonyl ring. Single-arm saturation replaces the other two exocyclic chains by CH2. Preserve all atoms of the selected arm.','cis_trans_control':'Rotate the first single C-C bond outside each N-adjacent exocyclic C=C; publish its four graph IDs and complete connected branch. Use transoid/cisoid relative to carbonyl side, not a changed C=C bond identity.','three_arm_requirement':'All three branches, not a repeated scalar from one isolated arm.'}
  for o in objects:
   adj={a['id']:[] for a in o['atoms']}
   for e in o['bonds']:adj[e['a']].append(e['b']);adj[e['b']].append(e['a'])
   o['arm_N_atoms']=[a['id'] for a in o['atoms'] if a['element']=='N'];o['carbonyl_C_atoms']=[e[x] for e in o['bonds'] if e['order']=='DOUBLE' and any(next(a['element'] for a in o['atoms'] if a['id']==e[k])=='O' for k in ['a','b']) for x in ['a','b'] if next(a['element'] for a in o['atoms'] if a['id']==e[x])=='C']
   edges={frozenset([e['a'],e['b']]):e['order'] for e in o['bonds']};el={a['id']:a['element'] for a in o['atoms']};tors=[]
   for n in o['arm_N_atoms']:
    found=[]
    for a in adj[n]:
     for b in adj[a]:
      if b==n or el[b]!='C' or edges[frozenset([a,b])]!='DOUBLE':continue
      for c in adj[b]:
       if c==a or el[c]!='C' or edges[frozenset([b,c])]!='SINGLE':continue
       for d in adj[c]:
        if d!=b and el[d]=='C' and edges[frozenset([c,d])]=='DOUBLE':
         gg=nx.Graph();gg.add_edges_from((e['a'],e['b']) for e in o['bonds']);gg.remove_edge(b,c)
         if not nx.has_path(gg,b,c):found.append([a,b,c,d])
    assert len(found)==1,(o['id'],n,found);tors.append({'N_atom':n,'torsion_atom_ids':found[0]})
   controls[o['id']+'_arm_torsions']=tors
  heavy=[]
  for o in objects:
   gr=nx.Graph();gr.add_nodes_from((a['id'],{'element':a['element']}) for a in o['atoms'] if a['element']!='H');gr.add_edges_from((e['a'],e['b']) for e in o['bonds'] if e['a'] in gr and e['b'] in gr);heavy.append(gr)
  matcher=nx.algorithms.isomorphism.GraphMatcher(heavy[1],heavy[0],node_match=lambda a,b:a['element']==b['element']);maps={};n_single=objects[0]['arm_N_atoms'][0]
  for mapping in matcher.subgraph_isomorphisms_iter():
   inverse={v:k for k,v in mapping.items()};n_full=inverse[n_single]
   if n_full not in maps:maps[n_full]=sorted([a,b] for a,b in inverse.items())
   if len(maps)==3:break
  assert len(maps)==3
  controls['single_to_three_heavy_atom_maps']=maps;controls['cap_rule']='Retain mapped central tricarbonyl ring and selected full arm. Remove the other two exocyclic arms; replace each central-ring-to-removed-arm C=C with two C-H single bonds on the retained central ring carbon. New H atoms are cap atoms, not mapped full-model atoms; relax only those H during frozen-arm extraction.'
 elif short=='fda8b9b53f8276db':
  g=cif_graph(pid,'ccdc_2433822.cif','ligand');objects=[g];files=['ccdc_2433822.cif','ccdc_record.json','experimental_bonds.json'];controls={'torsion_CIF_labels':['N1','C1','C2','N2'],'families':{'cis':'same-side N atoms','trans':'opposite-side N atoms'},'media':['gas','acetonitrile'],'temperature_K':298.15}
 elif short=='0de37d01e35c27df':
  definition=json.load(open(source(pid,'starting_geometry_definition.json')));params=Chem.SmilesParserParams();params.removeHs=False;m=Chem.MolFromSmiles(definition['mapped_smiles'],params);m=Chem.AddHs(m);g=from_mol(m,'nor',prov='Verified preexisting final atom-mapped topology; do not infer S-S edge from geometry',ids=[a.GetAtomMapNum() for a in m.GetAtoms()]);assert len({a['id'] for a in g['atoms']})==26 and all(a['id'] for a in g['atoms']);dt=from_smi('S1CCCSCCC1','DTCO',prov='SI TableS4 p11; 1,5-dithiacyclooctane C6H12S2')
  objects=variants(g,[('nor_neutral',0,1),('nor_cation',1,2)])+variants(dt,[('DTCO_neutral',0,1),('DTCO_cation',1,2)]);controls={'SS_maps':{'nor':[16,17],'DTCO':[a['id'] for a in dt['atoms'] if a['element']=='S']},'vertical_protocol':'Use each relaxed neutral geometry for cation single point and each cation geometry for neutral single point with no change in atom graph.'};files=['starting_geometry_definition.json','norDTCO_neutral.xyz']
 elif short=='43d74f8a469d9ad3':
  g=cif_graph(pid,'ccdc_2441197.cif','dye1');objects=[g];files=['ccdc_2441197.cif','ccdc_record.json']
  # Correct source Scheme1 matched derivative. Find phenoxy carbon and its para hydrogen by graph distance.
  elems={a['id']:a['element'] for a in g['atoms']};adj={i:[] for i in elems}
  for e in g['bonds']:adj[e['a']].append(e['b']);adj[e['b']].append(e['a'])
  bid=next(i for i,e in elems.items() if e=='B');phenoxy=None
  for oi in adj[bid]:
   if elems[oi]=='O':
    for ci in adj[oi]:
     if elems[ci]=='C' and len([j for j in adj[ci] if elems[j]=='C'])==2:phenoxy=ci
  assert phenoxy
  ring=Chem.GetSymmSSSR(Chem.MolFromSmiles('c1ccccc1')) # algorithm below uses graph, no source geometry
  paths=[(phenoxy,[phenoxy])];target=None
  for depth in range(3):
   new=[]
   for at,path in paths:
    for n in adj[at]:
     if elems[n]=='C' and n not in path:new.append((n,path+[n]))
   paths=new
  candidates=Counter(x for x,path in paths)
  for i,n in candidates.items():
   if n==2 and any(elems[j]=='H' for j in adj[i]):target=i
  assert target
  h=next(j for j in adj[target] if elems[j]=='H');g2=copy.deepcopy(g);g2['id']='dye2';g2['atoms']=[a for a in g2['atoms'] if a['id']!=h];g2['bonds']=[e for e in g2['bonds'] if h not in [e['a'],e['b']]];start=max(elems)+1
  for off,sym in enumerate(['O','C','H','H','H']):g2['atoms'].append({'id':start+off,'element':sym,'formal_charge':0})
  for a,c in [(target,start),(start,start+1),*[(start+1,start+k) for k in [2,3,4]]]:g2['bonds'].append({'a':a,'b':c,'order':'SINGLE','kind':'covalent'})
  g2['formula']=formula(g2['atoms']);g2['provenance']='Main Scheme1 compound2; add OMe para to phenoxy O on salicylidene ring; incompatible SI S5 labels not used';objects.append(g2)
  aryl=next(i for i in adj[bid] if elems[i]=='C');ortho=next(i for i in adj[aryl] if elems[i]=='C');x=next(i for i in adj[bid] if elems[i]=='O');controls={'torsion_graph_ids':[x,bid,aryl,ortho],'substitution_parent_C':target,'removed_H':h,'new_O_Me_ids':[start,start+1],'common_scaffold_ids':sorted(set(elems)-{h}),'source_conflict':'SI TableS5 labeled1 has C25H25BN2O3, incompatible with CCDC/Scheme1. Use CCDC graph and Scheme1 substitution; not those coordinates.'}
 elif short=='86a0b654270a8ce7':
  for i in [1,2]:
   rows=get('complex_'+str(i));o=simple_adjacency(rows,f'isomer{i}',0,1,'SI pp11-18; full coordination adjacency retained, source geometry withheld',metal=True)
   ir=next(a['id'] for a in o['atoms'] if a['element']=='Ir');donors=[e['b'] if e['a']==ir else e['a'] for e in o['bonds'] if e['kind']=='coordination'];pairs=[]
   for a in donors:
    for b in donors:
     if a>=b:continue
     u=np.array(rows[a-1][1:])-np.array(rows[ir-1][1:]);v=np.array(rows[b-1][1:])-np.array(rows[ir-1][1:])
     if np.dot(u,v)/np.linalg.norm(u)/np.linalg.norm(v)<-0.75:pairs.append([a,b])
   assert len(donors)==6 and len(pairs)==3
   o['coordination_stereochemistry']={'metal_atom':ir,'donor_atom_ids':donors,'trans_donor_pairs':pairs,'meaning':'Categorical isomer identity from source; no target distances, angles or Cartesian endpoint supplied. Remaining donor pairs are cis. Preserve connectivity and trans pairing during independent embedding.'};objects.append(o)
  controls={'temperature_K':339,'medium':'THF','metal_geometry':'Preserve isomer-specific adjacency and donor relative arrangement; reconstruct ligand valence with Ir(III), salen dianion and cyclometalated NHC anion. Total neutral singlet.','stacking_atoms':'Choose closest two aromatic rings from each reconstructed graph; publish all ring atom IDs and centroid/normal definitions. Compare same rings in contact-separated and released structures.'}
 elif short=='94e7481ded3b6a75':
  g=from_xyz(get('pbna'),'PBNA',prov='SI TableS12 p19 graph only');objects=[g];adj={a['id']:[] for a in g['atoms']};el={a['id']:a['element'] for a in g['atoms']}
  for e in g['bonds']:adj[e['a']].append(e['b']);adj[e['b']].append(e['a'])
  tors=[]
  for bi in [i for i,e in el.items() if e=='B']:
   for edge in g['bonds']:
    if bi in [edge['a'],edge['b']] and edge['order']=='SINGLE':
     ci=edge['b'] if edge['a']==bi else edge['a']
     if el[ci]=='C':
      ni=next((n for n in adj[bi] if el[n]=='N'),None);co=next((n for n in adj[ci] if el[n]=='C'),None)
      graph=nx.Graph();graph.add_edges_from((e['a'],e['b']) for e in g['bonds']);graph.remove_edge(bi,ci)
      if ni and co and not nx.has_path(graph,bi,ci):tors.append([ni,bi,ci,co])
  assert len(tors)==2
  controls={'torsion_maps':tors,'restriction':'Set both B-phenyl torsions to a common stated angle; preserve rings. Include at least two angular settings and released S0/S1 controls.','primary_medium':'gas','sensitivity_medium':'CH2Cl2'}
 elif short=='9aa6d5655edfeb52':
  rows=get('2a');g=simple_adjacency(rows,'fused2a',0,1,'SI p19; cage graph only, no source coordinates',cage=True);objects=[g];p=copy.deepcopy(g);p['id']='nonfused1a';p['bonds']=[e for e in p['bonds'] if set([e['a'],e['b']])!={1,28}];assert len(p['bonds'])==len(g['bonds'])-1
  p['atoms'] +=[{'id':49,'element':'H'},{'id':50,'element':'Br'}];p['bonds'] +=[{'a':28,'b':49,'order':'SINGLE','kind':'covalent'},{'a':1,'b':50,'order':'SINGLE','kind':'covalent'}];p['formula']=formula(p['atoms']);p['provenance']='SI pp4-5 source precursor1a; break B3/aryl1 fusion, restore B-H and aryl-Br';objects.append(p);controls={'cage_C_atom_ids':[4,13],'fusion_edge':[1,28],'displacement_A':[-0.05,0.05],'chemical_confound':'Br-containing precursor vs dehydrohalogenated fused product; cannot interpret as pure geometric fusion.','cage_atom_ids':[4,13]+[a['id'] for a in g['atoms'] if a['element']=='B']}
 elif short=='a6e8c57709329bdb':
  d=json.load(open(source(pid,'hl_ligand.json')));objects=[from_smi(d['smiles'],'HL')];files=['hl_ligand.json'];controls={'source_medium':'DMF','competitor':'Co(II)','FeIII_multiplicities':[2,4,6],'CoII_multiplicities':[2,4],'unresolved':['sensing_salt_counterions','pH_or_proton_reservoir','water_content','finite_coordination_water_DMF_inventory'],'not_a_complete_model':'Do not construct calibrated exchange cycles by freely guessing these missing conditions.'}
 elif short=='b1467cd61ca8022d':
  for n,s in [('PM','COCCC'),('BM','COCCCC'),('TFPM','COCCC(F)(F)F'),('TFBM','COCCCC(F)(F)F'),('Li','[Li+]'),('FSI','FS(=O)(=O)[N-]S(=O)(=O)F')]:objects.append(from_smi(s,n,1 if n=='Li' else -1 if n=='FSI' else 0))
  for n in ['PM','BM','TFPM','TFBM']:objects.append(fragments(n+'_salt_cluster',{'Li':1,'FSI':1,n:1},objects,definition='Competing solvent O-facing and FSI-O-facing positions; fluorinated solvent includes O/F contact and O-only starts.'))
  controls={'fixed_cluster_stoichiometry':'1 Li+:1 FSI-:1 solvent','atom_sites':{o['id']:{e:[a['id'] for a in o['atoms'] if a['element']==e] for e in ['O','F','N','Li']} for o in objects if 'atoms' in o},'primary_medium':'gas-phase finite clusters; paired continuum sensitivity separately defined','ESP_vs_RESP':'ESP oxygen descriptor in eV requires specified density surface and potential convention; RESP is fitted atomic charge in e.'}
 elif short=='c28b0a1c549f4575':
  for n,s,q in [('TEA','CC[N+](CC)(CC)CC',1),('DED','CC[N+]12CC[N+](CC)(CC1)CC2',2),('BF4','F[B-](F)(F)F',-1),('PC','CC1COC(=O)O1',0)]:objects.append(from_smi(s,n,q))
  for ion in ['TEA','DED']:
   for n in [0,1,2]:objects.append(fragments(f'{ion}_salt_PC{n}',{ion:1,'BF4':1 if ion=='TEA' else 2,**({'PC':n} if n else {})},objects,definition='Prepare contact and solvent-separated ion-pair families with same PC stereochemistry and atom inventory.'))
  controls={'exchange_1':{'TEA_salt_PC1':-1,'DED_salt_PC0':-1,'TEA_salt_PC0':1,'DED_salt_PC1':1},'exchange_2':{'TEA_salt_PC2':-1,'DED_salt_PC1':-1,'TEA_salt_PC1':1,'DED_salt_PC2':1},'contact_definition':'Map the shortest cation-N...anion-F approach and PC carbonyl-O locations; separated candidates place PC between ions. Release optimization may remove distinction with evidence.','standard_state':'298.15 K, 1 M, common PC continuum sensitivity'};files=['system_definition.json']
 elif short=='2877efc02814175d':
  ligand=from_xyz(get('cd_complex'),'DQCS',skip=['Cd'],prov='SI TableS1 graph after metal removal; all 27 H retained; neutral ligand verified by electron count');objects=[ligand]
  for el in ['Cd','Co','Ni']:
   row=get(el.lower()+'_complex');met=next(i for i,a in enumerate(row) if a[0]==el);assert met+1 not in {a['id'] for a in ligand['atoms']};o=copy.deepcopy(ligand);o['id']=el+'_DQCS';o['charge']=2;o['multiplicity']=2 if el=='Co' else 1;o['atoms'].append({'id':met+1,'element':el,'formal_charge':2})
   donors=[i+1 for i,a in enumerate(row) if a[0] in ['N','O'] and math.dist(a[1:],row[met][1:])<2.7]
   for at in donors:o['bonds'].append({'a':at,'b':met+1,'order':'DATIVE','kind':'coordination'})
   o['formula']=formula(o['atoms']);o['metal_donor_atom_ids']=donors;objects.append(o)
  controls={'common_ligand_map':[[a['id'],a['id']] for a in ligand['atoms']],'solvent':'DMSO','Co_reference':'charge+2, doublet; S8 singlet table heading cannot override explicit spin in S2','frozen_ligand_charge':0}
 elif short=='2f2aa11ea61a32bb':
  objects=[from_xyz(get(n),n,prov='Source SI molecule graph; optimized coordinates withheld') for n in ['1a','1b','1c','1d']];files=['experimental_absorption.json'];controls={'common_anchors':{o['id']:{e:[a['id'] for a in o['atoms'] if a['element']==e] for e in ['B','N','O','F']} for o in objects},'common_geometry':'Map B, N, O, two F and adjacent chelate carbons by graph; fix those shared internal distances/angles to a stated released member. Do not impose whole fused-ring bijection.','solvent':'toluene','validation_split':'Preselect one published band trend for transfer testing; since public observations are visible call this retrospective unless genuinely preregistered.'}
  controls['ordered_common_chelate_map']={}
  for o in objects:
   el={a['id']:a['element'] for a in o['atoms']};g=nx.Graph();g.add_edges_from((e['a'],e['b']) for e in o['bonds']);bid=next(i for i,x in el.items() if x=='B');g.remove_node(bid);n=next(i for i,x in el.items() if x=='N');ox=next(i for i,x in el.items() if x=='O');controls['ordered_common_chelate_map'][o['id']]=[bid]+nx.shortest_path(g,n,ox)
  controls['map_slots']=['B','N','N_adjacent_C','aryl_ipso_C','phenoxy_C','O'];controls['F_map_policy']='Two B-bound F are chemically equivalent; enumerate both permutations when aligning and report chosen mapping, never change charge or geometry to force fit.'
 elif short=='3a22e838133b906d':
  for n,s,q in [('full_neutral','CCOP(=O)(OCC)c1ccccc1B(C1CCCCC1)C1CCCCC1',0),('full_anion','CCOP(=O)([O-])c1ccccc1B(C1CCCCC1)C1CCCCC1',-1),('Li','[Li+]',1),('MeCN','CC#N',0),('iodide','[I-]',-1),('EtI','CCI',0)]:objects.append(from_smi(s,n,q))
  for o in objects[:2]:o['contact_roles']={'P':4,'intramolecular_O_to_B_donor':5,'B':15 if o['id']=='full_neutral' else 13,'remaining_OEt_oxygen':3,**({'deethylated_O_for_Li_bridge':6} if o['id']=='full_anion' else {'departing_OEt_oxygen':6})};o['coordination_note']='Uncoordinated phosphonate formal resonance graph is supplied; O5->B contact forms the five-membered chelate without changing atom inventory or total charge. Use dative or charge-separated resonance convention consistently. In anion, O6 bridges Li; O5 remains distinguishable.'
  old=json.load(open(source(pid,'starting_geometry_definition.json')))
  for key,definition in old['states'].items():
   params=Chem.SmilesParserParams();params.removeHs=False;m=Chem.MolFromSmiles(definition['mapped_smiles'],params);objects.append(from_mol(m,'small_'+key.split('.')[0],definition['charge'],definition['multiplicity'],'Original verified truncation control only',ids=[a.GetAtomMapNum() for a in m.GetAtoms()]))
  for n,parts in [('Li_anion',{'full_anion':1,'Li':1}),('Li_anion_2MeCN',{'full_anion':1,'Li':1,'MeCN':2}),('crystal_supported_dimer',{'full_anion':2,'Li':2,'MeCN':4}),('LiI',{'Li':1,'iodide':1})]:objects.append(fragments(n,parts,objects,definition='Dimer: both Li bridge the exposed phosphoryl O of both anions in a Li2O2 ring; each Li also has two MeCN N donors. Preserve intramolecular phosphonate O...B candidate contact. Source main Fig1; no experimental Cartesian geometry claimed.'))
  controls={'dimerization_coefficients':{'crystal_supported_dimer':1,'Li_anion_2MeCN':-2},'deethylation_coefficients':{'full_neutral':-1,'LiI':-1,'Li_anion':1,'EtI':1},'source_contact_atom_maps':{o['id']:{e:[a['id'] for a in o['atoms'] if a['element']==e] for e in ['P','O','B','Li','N']} for o in objects if 'atoms' in o},'truncation':'Old BMe2/OMe graphs are separate controls. Do not relabel their results as full Cy/OEt species.'};files=['starting_geometry_definition.json','experimental_crystal_boundary.json','neutral.xyz','anion.xyz']
 elif short=='98b6f8a0352f72c2':
  objects=[from_smi('CN(C)c1ccc(cc1)c2cc3nc4ccccc4nc3c5ccccc25','12a',prov='Existing verified graph/main identity'),from_smi('CCN(CC)c1ccc(cc1)c2cc3nc4ccccc4nc3c5ccccc25','12d',prov='Source main pp6-7 N,N-diethyl derivative; formal SI member12d')];controls={'solvents':['CHCl3','EtOAc'],'torsion_definition':'Single bond joining dimethyl/diethylaminophenyl ipso carbon to benzo[a]phenazine C5, using an adjacent aromatic carbon on each side. Full exact per-member graph maps below.','required_excitation_geometries':['vertical_absorption_at_S0','vertical_emission_at_S1','adiabatic_S1_minus_S0'],'experimental_rate_policy':'Use Phi/tau only if both real measured values and same conditions exist; otherwise explicitly unavailable, never filled from theoretical SI TableS1.'}
  for o in objects:
   m=Chem.AddHs(Chem.MolFromSmiles('CN(C)c1ccc(cc1)c2cc3nc4ccccc4nc3c5ccccc25' if o['id']=='12a' else 'CCN(CC)c1ccc(cc1)c2cc3nc4ccccc4nc3c5ccccc25'))
   es=[b for b in m.GetBonds() if b.GetBondType()==Chem.BondType.SINGLE and b.GetBeginAtom().GetIsAromatic() and b.GetEndAtom().GetIsAromatic()]
   assert len(es)==1;b=es[0];i,j=b.GetBeginAtomIdx(),b.GetEndAtomIdx();x=next(a.GetIdx() for a in m.GetAtomWithIdx(i).GetNeighbors() if a.GetIdx()!=j and a.GetIsAromatic());y=next(a.GetIdx() for a in m.GetAtomWithIdx(j).GetNeighbors() if a.GetIdx()!=i and a.GetIsAromatic());controls[o['id']+'_torsion']=[x+1,i+1,j+1,y+1]
 # Public old source optimized coordinate payloads are replaced by graph-only identities.
 for mode in ['autonomous_research','paper_reproduction']:
  inp=DEST/mode/pid/'agent_input/data/inputs'
  for p in list(inp.rglob('*')):
   if p.is_file():p.unlink()
  for name in files:
   p=source(pid,name);(inp/name).parent.mkdir(parents=True,exist_ok=True);(inp/name).write_bytes(p.read_bytes())
  for name,data in additional.items():dump(inp/name,data)
  dump(inp/'objects.json',{'paper_id':pid,'object_definition_status':'blocked' if short in ['a0f6b899582cb9f7','a6e8c57709329bdb'] else 'development_defined','objects':objects,'atom_mapping':'IDs are stable within each object; related objects explicitly state common maps. Composites use (object_id,copy_number,atom_id).','not_scientific_validation':'Topology preparation only. No electronic energies, stationary points or new reference calculations have been produced.'})
  dump(inp/'controls.json',controls)
  dump(inp/'data_provenance.json',{'paper_id':pid,'public_sources':'Source molecular identity/experimental observations only; no computational endpoint coordinates or reference numeric targets.','retained_final_inputs':files,'source_graph_derivation':'Mapped final identity or source coordinate topology; source coordinates retained privately in legacy snapshots/source evidence, not exposed as new answers.','new_controls':'Benchmark-defined, not asserted to have been performed by authors.','generation_script':'coordination_20260927/batch3/build_inputs.py'})
 return {'paper_id':pid,'objects':[(o['id'],o.get('formula'),o['charge'],o['multiplicity']) for o in objects],'controls':controls}
if __name__=='__main__':
 ids=json.load(open(B/'assignment.json'))['batch']['papers'];res=[]
 for pid in ids:
  try:r=build(pid);res.append(r);print(pid,'prepared',len(r['objects']),flush=True)
  except Exception as e:print(pid,'ERROR',repr(e),flush=True);raise
 dump(B/'input_preparation_report.json',res)
