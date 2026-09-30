from pathlib import Path
from copy import deepcopy
import json
from rdkit import Chem
from rdkit.Chem import rdFMCS
B=Path(__file__).resolve().parent;O=B/'prepared_inputs'
def dump(p,x):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(x,indent=2)+'\n')
# Structural mapping based on graph, never a source answer geometry.
p='paper_c23cfabbd34b087f';pairs=[]
for topology in ['1M','2M']:
 ds=[json.loads((O/p/(topology+'_'+k+'_identity.json')).read_text()) for k in ['OMe','TIPS']]
 ms=[Chem.RemoveHs(Chem.MolFromSmiles(d['mapped_smiles'])) for d in ds]
 q=rdFMCS.FindMCS(ms,timeout=15,ringMatchesRingOnly=True,completeRingsOnly=True,bondCompare=rdFMCS.BondCompare.CompareAny,atomCompare=rdFMCS.AtomCompare.CompareElements)
 assert not q.canceled
 query=Chem.MolFromSmarts(q.smartsString);ma=[m.GetSubstructMatch(query) for m in ms]
 mapping=[[ms[0].GetAtomWithIdx(i).GetAtomMapNum(),ms[1].GetAtomWithIdx(j).GetAtomMapNum()] for i,j in zip(*ma)]
 pairs.append({'topology':topology,'from':topology+'_OMe','to':topology+'_TIPS','shared_atom_id_pairs':mapping,'common_heavy_atoms':len(mapping),'definition':'Ring-conserving maximal common heavy subgraph, allowing resonance bond-order differences; no inter-topology total-energy mapping. Inspect attachment boundaries before constraining.','shared_graph_smarts':q.smartsString})
dump(O/p/'common_scaffold_mapping.json',{'pairs':pairs,'frozen_reference':'Independently computed OMe triplet geometry for each topology; no coordinates supplied.'})
# Exact Sn intervention quadruples, unaffected by aromatic atom numbering.
p='paper_a21b91f97ce3c68f'
for fn in (O/p).glob('pair_*_identity.json'):
 d=json.loads(fn.read_text());m=Chem.MolFromSmiles(d['mapped_smiles']);alpha=min(d['butyl_carbon_ids']);atom=next(a for a in m.GetAtoms() if a.GetAtomMapNum()==alpha);beta=next(n for n in atom.GetNeighbors() if n.GetSymbol()=='C')
 d['intervention_torsion_atoms']=[beta.GetAtomMapNum(),alpha,d['sn_atom_id'],d['anomeric_carbon_id']];d['held_distance_atoms']=[d['sn_atom_id'],alpha];dump(fn,d)
# Anonymous public source descriptions do not disclose the coordinate state's label.
for fn in (O/'paper_c23cfabbd34b087f').glob('*identity.json'):
 d=json.loads(fn.read_text());d['source']='Source SI named model connectivity block; only molecular graph and atom correspondence are released. Electronic-state labels, coordinates and energies are withheld.';dump(fn,d)
print([(x['topology'],x['common_heavy_atoms']) for x in pairs])
