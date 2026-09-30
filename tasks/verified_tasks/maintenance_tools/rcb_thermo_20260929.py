import sys,json,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rcb_audit_20260929 import D,IDS,group
from goodvibes import compute_thermo
from goodvibes.constants import GAS_CONSTANT,J_TO_AU
K=627.5094740631;RT=GAS_CONSTANT*298.15/J_TO_AU
protocol=dict(QS='grimme',QH=False,s_freq_cutoff=100.,temperature=298.15,concentration=1.,freq_scale_factor=1.,zpe_scale_factor=1.,inertia='global')
out={}
i=IDS[2];d=D[i];gs={};err=[]
for name,r in d['records'].items():
 log=group(i)/r['low']['directory']/'stdout.log';gv=compute_thermo(str(log),symm=True,**protocol)
 correction=gv.qh_gibbs_free_energy-gv.scf_energy-RT*math.log(gv.symmno)
 corrected=r['high']['electronic_E_Eh']+correction+RT*math.log(r['symmetry']['diagnostic_sigma_by_max_displacement_A']['0.001']/r['symmetry']['native_sigma'])
 gs[name]=corrected
 if abs(corrected-r['G_high_geometry_sigma_sensitivity_Eh']['0.001'])>1e-8:err.append([name,corrected,r['G_high_geometry_sigma_sensitivity_Eh']['0.001']])
profile=d['profiles']['.001_dedup0.1']; ens={}
for family,e in profile['ensembles'].items():
 vals=[gs[x] for x in e['representatives']];v=min(vals);ens[family]=v-RT*math.log(sum(math.exp(-(x-v)/RT) for x in vals))
 assert abs(ens[family]-e['G_Eh'])<1e-8
states={k:(sum(ens[n] for n in s['products'])-sum(ens[n] for n in s['reactants']))*K for k,s in profile['states'].items()}
out[i]={'method':'GoodVibes 4.3 full qRRHO reread, single symmetry divisor, archived geometry sigma and dedup identities','records':len(gs),'qrrho_errors':err,'recomputed_G_by_candidate':gs,'ensemble_G':ens,'states':states}
print(i,out[i]['records'],states,'ERRORS',err,flush=True)
i=IDS[3];p=group(i);q=json.loads((p/'provenance/author_answer_validation_20260926/QRRHO_REFERENCE_AUDIT.json').read_text());b=json.loads((p/'provenance/author_answer_validation_20260926/BALANCED_REFERENCE_AUDIT.json').read_text());gs={};err=[]
for name,r in {**q['records'],**b['components']}.items():
 gv=compute_thermo(str(p/r['low_directory']/'stdout.log'),symm=False,**protocol)
 g=r['high_E_Eh']+gv.qh_gibbs_free_energy-gv.scf_energy;gs[name]=g
 if abs(g-r['G_high_qRRHO_Eh'])>1e-8:err.append([name,g,r['G_high_qRRHO_Eh']])
ref=sum(gs[n] for n in ['catalyst_4i','reactant_1a','reactant_2a'])
vals={n:(gs[n]+2*gs['MeOH']-ref)*K for n in q['records']}
out[i]={'records':len(gs),'qrrho_errors':err,'G_by_state':gs,'reference_G':ref,'balanced_values':vals,'delta_delta_G':vals['TSCC_S']-vals['TSCC_R']}
print(i,out[i],flush=True)
Path('/tmp/rcb_thermo_audit_20260929.json').write_text(json.dumps(out,indent=2))
