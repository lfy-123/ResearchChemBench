"""Audit assigned existing sources only; write evidence into this batch workspace."""
from pathlib import Path
import sys,json,hashlib,subprocess,collections
ROOT=Path(__file__).resolve().parents[4];B=Path(__file__).resolve().parent
IDS=['paper_5ea491c741fbd8d4','paper_72f60526b64ce1b6','paper_c7217910ecbee1d9']
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def record(p,scope):return {'path':str(p.relative_to(ROOT)),'sha256':digest(p),'scope':scope}
for pid in IDS:
 r={'date':'2026-09-27','paper_id':pid,'status':'blocked','new_scientific_calculations_performed':False,'source_reread':[],'history':[],'source_access_checks':[]}
 for f in (ROOT/'papers'/pid/'documents').glob('*'):r['source_reread'].append(record(f,'Substantive relevant methods, structures and figure/table evidence; detailed locations in reference_validation_plan.md.'))
 ws=next((ROOT/'workspaces/codex_gpt56').glob(pid+'*'))
 for p in ws.glob('runs/cli_runs/*/*/report/results.json'):
  d=json.load(open(p));r['history'].append(record(p,'Existing report inspected; no new scientific result.'))
  if pid==IDS[2]:
   ep=p.parent.parent/'outputs/endpoints/analysis.json';r['history'].append(record(ep,'Raw historical analysis confirms broken core/ligand identity.'));a=json.load(open(ep));r['history_diagnosis']={'reported_status':d['status'],'neutral_core_retained':a['neutral']['structural_checks']['framework_retained'],'anion_core_retained':a['anion']['structural_checks']['framework_retained'],'neutral_ligands_intact':a['neutral']['structural_checks']['ligands_intact'],'anion_ligands_intact':a['anion']['structural_checks']['ligands_intact'],'raw_AEA_is_for_wrong_object':a['aea']['zpe_corrected_ev']}
  elif pid==IDS[1]:r['history_diagnosis']={'only':'Fixed isolated-AD dipole/force validation; no electrodes, NEGF, current or transmission.'}
  else:r['history_diagnosis']={'only':'Isolated molecule orbital/conformer study; no source packing or neighbor interaction evidence.'}
 if pid==IDS[0]:
  r['source_access_checks']=json.load(open(B/'source_review/public_retrieval.json'))[:3]
  r['local_cif_search']=json.load(open(B/'source_review/local_cif_search.json'))
  r['finding']='CCDC returns a validation/CAPTCHA page. No source CIF recovered. Local numeric-substring matches belonged to another deposition (2512981), not 2445596; rejected.'
  r['read_pages']={'main':[2,3,4,6],'SI':[1,2,3,4]}
 elif pid==IDS[1]:
  r['read_pages']={'main':[2,3,4,8,9,10,11],'SI':[1,2,5,6,7,8,9,10,16]}
  rows=json.load(open(B/'source_review/transport_source_coordinate_blocks.json'));r['coordinate_inventory']=[{'label':x['label'],'kind':x['kind'],'pages':x['pages'],'counts':dict(collections.Counter(y[0] for y in x['rows'])),'atom_count':len(x['rows'])} for x in rows]
  r['tool_configuration']=[record(ROOT/'chemistry_toolbox'/f,'Read-only capability audit; allowed siesta but no reviewed full transport chain.') for f in ['README.md','config/native_software_guides.yaml','config/mcp_profiles.yaml']]
  r['transport_chain_search']={'roots':['chemistry_toolbox/config','chemistry_toolbox/src','chemistry_toolbox/evidence'],'pattern':'transiesta|tbtrans','matches':subprocess.run(['rg','-n','-i','transiesta|tbtrans',*['chemistry_toolbox/'+s for s in ['config','src','evidence']]],cwd=ROOT,capture_output=True,text=True).stdout.splitlines()}
  r['finding']='Corrected missing-input scope: full Group A junction coordinates are present in SI and lose exactly two thiol H atoms. This does not close the allowed-chain or finite-bias-pilot gates. Author optimized coordinates stay private.'
 else:
  r['read_pages']={'main':[2,3,4,5],'SI_sections':['Computational details','Figures S1-S9','Table S1']}
  r['short_historical_audit']=json.load(open(B/'source_review/cluster_raw_recheck.json'))
  r['finding']='Formal SI is present and establishes source method. It supplies images rather than complete Cartesian coordinates. Historical intact-core DFT minima remain absent; no new run was launched.'
 (B/'source_review'/f'{pid}_review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print('Saved three read-only source reviews')
