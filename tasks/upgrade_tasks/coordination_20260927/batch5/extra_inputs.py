from prepare_inputs import smi_graph,dump,O,S,B,graph,coords
from pathlib import Path
import requests,re,json
from rdkit import Chem
names={
'TD_2T':"4,4',4''-(dibenzo[f,h]pyrazino[2,3-b]quinoxaline-3,6,11-triyl)tris(N,N-diphenylaniline)",
'CD_2T':"4,4'-(11-(4-(9H-carbazol-9-yl)phenyl)dibenzo[f,h]pyrazino[2,3-b]quinoxaline-3,6-diyl)bis(N,N-diphenylaniline)",
'TD_2C':"4-(3,6-bis(4-(9H-carbazol-9-yl)phenyl)dibenzo[f,h]pyrazino[2,3-b]quinoxalin-11-yl)-N,N-diphenylaniline",
'rubrene':'5,6,11,12-tetraphenyltetracene'}
results=[]
for k,n in names.items():
 cache=S/(k+'.opsin.json')
 if not cache.exists():
  r=requests.get('https://opsin.ch.cam.ac.uk/opsin/'+requests.utils.quote(n,safe='')+'.json',timeout=45);cache.write_text(r.text)
 d=json.loads(cache.read_text());results.append([k,d.get('status'),d.get('message')])
 if d.get('status')=='SUCCESS':
  pid='paper_e0791c047a731974' if k=='rubrene' else 'paper_3316e45a74258fb7'
  g=smi_graph(d['smiles'],k,'Publisher SI synthesis heading and HRMS formula; main Figure 1 donor positions' if k!='rubrene' else 'Named experimental acceptor: 5,6,11,12-tetraphenyltetracene')
  g.update(systematic_name=n,multiplicity=1,excited_multiplicities=[1,3],identity_parser='OPSIN name-to-graph; no geometry or energy prediction')
  dump(O/pid/(k+'_identity.json'),g);results[-1].append(g['formula'])
dump(B/'extra_identity_checks.json',results);print(results)
