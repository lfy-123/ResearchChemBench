from pathlib import Path
import sys,json,math,re,collections,bisect
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rcb_audit_20260929 import ROOT,IDS,D,group,resolve,read,NUM,num,gaussian_geometry
A=json.loads(Path('/tmp/rcb_raw_audit_20260929.json').read_text())['papers']
BY={r['parsed']['log']:r['parsed'] for xs in A.values() for r in xs}
K=627.5094740631; EV=27.211386245988; R=.00198720425864083
out={'geometry_parents':[], 'results':{}, 'errors':[]}
def raw(i,p):
 p=resolve(i,p)
 if p.is_dir():p=p/'stdout.log'
 return BY[str(p.relative_to(ROOT))]
def compare(i,label,parent,child):
 a=raw(i,parent)['geometry'];b=raw(i,child)['input_geometry']
 assert len(a)==len(b) and a,(label,len(a),len(b))
 symbols={1:'H',5:'B',6:'C',7:'N',8:'O',9:'F',16:'S',17:'Cl',26:'Fe',34:'Se',35:'Br',42:'Mo',45:'Rh',53:'I',79:'Au'}
 assert all(symbols[x[0]]==str(y[0]) or str(x[0])==str(y[0]) for x,y in zip(a,b)),label
 err=max(abs(x[j]-y[j]) for x,y in zip(a,b) for j in [1,2,3])
 pair=max(abs(math.dist(x[1:],y[1:])-math.dist(b[n][1:],b[m][1:])) for n,x in enumerate(a) for m,y in enumerate(a))
 row={'paper':i,'label':label,'parent':str(resolve(i,parent).relative_to(ROOT)),'child':str(resolve(i,child).relative_to(ROOT)),'atoms':len(a),'max_coordinate_error_A':err,'max_pair_distance_error_A':pair}
 out['geometry_parents'].append(row)
 if pair>4e-6:out['errors'].append(row)
 return row
# Fe: actual optimized electronic energies, not free energies or target labels.
i=IDS[0];out['results'][i]={c:(raw(i,s['HS']['directory'])['E_SCF_Eh']-raw(i,s['LS']['directory'])['E_SCF_Eh'])*2625.499638 for c,s in D[i]['systems'].items()}
# Rh: independently reconstruct common-state energies from three native calculations.
i=IDS[1];gs={};terms={}
for name,r in D[i]['records'].items():
 lo=raw(i,r['low_directory']);sol=raw(i,r['solvent_directory']);hi=raw(i,r['high_directory'])
 for level in ['solvent','high']:compare(i,name+' low -> '+level,r['low_directory'],r[level+'_directory'])
 text=(ROOT/lo['log']).read_text();T0=298.;T=298.15
 entropy=float(re.findall(r'^ Total\s+[-\d.]+\s+[-\d.]+\s+([-\d.]+)\s*$',text,re.M)[-1])/1000
 theta=[1.4387768775039338*f for f in lo['frequency_cm1'] if f>0]
 def fv(t):return R*t*sum(math.log(-math.expm1(-x/t)) for x in theta)
 sv=R*sum((x/T0)/math.expm1(x/T0)-math.log(-math.expm1(-x/T0)) for x in theta)
 delta=-(entropy-sv)*(T-T0)-(3.5 if name=='CO' else 4)*R*(T*math.log(T/T0)-(T-T0))+fv(T)-fv(T0)
 std=R*T*math.log(r['standard_concentration_M']*.08205736608096*T)/K
 g=hi['E_ORCA_Eh']+lo['Gcorr_Eh']+sol['E_SCF_Eh']-lo['E_SCF_Eh']+delta/K+std
 assert abs(g-r['G_solution_298p15K_Eh'])<1e-8,(name,g,r['G_solution_298p15K_Eh'])
 gs[name]=g;terms[name]={'G_solution_Eh':g,'temperature_shift_kcal_mol':delta,'standard_state_correction_Eh':std}
ref=.5*gs['Rh_dimer']+gs['1D']
profile={n:(gs[n]+v['released_CO']*gs['CO']-ref)*K for n,v in D[i]['profiles']['G_solution_298p15K_Eh'].items()}
out['results'][i]={'terms':terms,'profile':profile,'activation':profile['TS1endo']-profile['INT11'],'exo_minus_endo':profile['TS1exo']-profile['TS1endo']}
# c499 and c56: verify the optimized parent geometry used by every high-level SP.
i=IDS[2]
for n,r in D[i]['records'].items():compare(i,n,r['low']['directory'],r['high']['directory'])
i=IDS[3]
for fn,key in [('QRRHO_REFERENCE_AUDIT','records'),('BALANCED_REFERENCE_AUDIT','components')]:
 for n,r in read(i,'provenance/author_answer_validation_20260926/'+fn+'.json')[key].items():compare(i,n,r['low_directory'],r['high_directory'])
# JY: four-point energy cycle and terminal orbital block.
i=IDS[4];out['results'][i]={}
for r in D[i]['molecules']:
 n=r['molecule'];v=r['native_calculations'];p={k:raw(i,x['path']) for k,x in v.items()};e={k:x['E_SCF_Eh'] for k,x in p.items()}
 compare(i,n+' R0 -> cation SP',v['neutral']['path'],v['cation_at_neutral']['path'])
 compare(i,n+' R+ -> neutral SP',v['cation']['path'],v['neutral_at_cation']['path'])
 orb=p['neutral']['last_orbital_block']
 out['results'][i][n]={'HOMO_eV':orb['occ.'][-1]*EV,'LUMO_eV':orb['virt.'][0]*EV,'lambda_eV':(e['cation_at_neutral']-e['cation']+e['neutral_at_cation']-e['neutral'])*EV,'energies_Eh':e}
# Mo: balanced arithmetic and direct geometric nitrosyl diagnostic.
i=IDS[5];v={n:raw(i,r['log']) for n,r in D[i]['records'].items()};e={n:p['G_Eh'] for n,p in v.items()};rawg=(e['product_3']-e['im5']-e['water'])*K
shift=R*298.15*math.log(.08205736608096*298.15);bulk=R*298.15*math.log(55.34)
g=v['product_3']['geometry'];mo,nn,oo=[g[n-1][1:] for n in [1,24,25]]
u=[x-y for x,y in zip(mo,nn)];w=[x-y for x,y in zip(oo,nn)];angle=math.degrees(math.acos(sum(x*y for x,y in zip(u,w))/math.dist(mo,nn)/math.dist(oo,nn)))
out['results'][i]={'G_Eh':e,'raw':rawg,'source_recipe':rawg-bulk,'all_solute_1M':rawg-shift,'bulk_water_1M':rawg-shift-bulk,'MoNO_angle_deg':angle,'NO_A':math.dist(nn,oo),'NO_frequency_cm1':v['product_3']['frequency_cm1'][63]}
# ESIPT: bound root records by each accepted point, independently parse all six roots.
def path_roots(log,maxpoint=None):
 text=Path(log).read_text();starts=[m.start() for m in re.finditer(r'Excited State\s+1:',text)];rows=[]
 for p in re.finditer(r'^\s*Point Number:\s*(\d+)\s+Path Number:\s*(\d+)\s*$',text,re.M):
  pn=int(p[1])
  if maxpoint is not None and pn>maxpoint:continue
  st=starts[bisect.bisect_right(starts,p.start())-1];seg=text[st:p.start()]
  matches=list(re.finditer(r'Excited State\s+(\d+):\s+(\S+)\s+([\d.]+) eV\s+[\d.]+ nm\s+f=([\d.]+)\s+<S\*\*2>=([\d.]+)',seg))
  assert [int(m[1]) for m in matches]==list(range(1,7)),(log,pn)
  assert all(m[2].startswith('Singlet') and float(m[5])==0 for m in matches)
  first=seg[:matches[1].start()];assert 'This state for optimization and/or second-order correction.' in first
  td=float(re.search(r'Total Energy, E\(TD-HF/TD-DFT\)\s*=\s*([-\d.]+)',first)[1])
  es=[float(m[3]) for m in matches];rows.append({'point':pn,'gap':min(es[1:])-es[0],'TD':td})
 assert rows and min(r['gap'] for r in rows)>0,(log,'inverted root')
 return rows
i=IDS[6];out['results'][i]={}
for el,r in D[i]['records'].items():
 ts=raw(i,r['TS']['log']);en=raw(i,r['endpoints']['enol']['log']);dG=(ts['G_Eh']-en['G_Eh'])*K
 item={'barrier_kcal_mol':dG,'rate_s_inv':1.380649e-23*298.15/6.62607015e-34*math.exp(-dG*4184/(8.31446261815324*298.15)),'paths':{}}
 for direction,p in r['paths'].items():
  if el=='Se' and direction=='reverse':
   prefix=p['accepted_prefix'];aa=path_roots(prefix['parent_log'],17);bb=path_roots(p['log']);pts=aa+bb[1:]
   compare(i,'Se TS -> original reverse IRC',r['TS']['log'],prefix['parent_log'])
   item['Se_splice_TD_difference_Eh']=abs(aa[-1]['TD']-bb[0]['TD']);assert item['Se_splice_TD_difference_Eh']<1e-6
  else:
   pts=path_roots(p['log']);compare(i,el+' TS -> '+direction+' IRC',r['TS']['log'],p['log'])
  item['paths'][direction]={'accepted_points':len(pts),'minimum_other_root_minus_S1_eV':min(x['gap'] for x in pts)}
  assert len(pts)==p['state_audit']['accepted_count']
 out['results'][i][el]=item
# Au: CP descriptors, real-space bond paths, atom-to-basin mapping and raw DI matrices.
i=IDS[7];base=group(i)/'au1_20260928';cptext=(base/'topology_complete/CPprop.txt').read_text();cp={}
sections=re.split(r'-+\s+CP\s+(\d+),\s+Type \(([^)]+)\)\s+-+',cptext)
for n in range(1,len(sections),3):
 cid=int(sections[n]);seg=sections[n+2]
 if cid not in [5,6,7,8]:continue
 x={'signature':sections[n+1]}
 for key,lab in [('rho','Density of all electrons:'),('laplacian','Laplacian of electron density:'),('G','Lagrangian kinetic energy G(r):'),('V','Potential energy density V(r):'),('H','Energy density E(r) or H(r):'),('elf','Electron localization function (ELF):')]:
  x[key]=float(re.search(re.escape(lab)+r'\s*('+NUM+')',seg)[1])
 x['ratio']=abs(x['V'])/x['G'];assert x['signature']=='3,-1' and x['laplacian']>0 and 1<x['ratio']<2;cp[cid]=x
di={}
for mesh in ['020','010']:
 d=base/('di_'+mesh+'_hpc20');s=(d/'stdout').read_text()
 mapping={int(a):int(b) for b,a in re.findall(r'Attractor\s+(\d+) corresponds to atom\s+(\d+)\s+\(Au\)',s)}
 t=(d/'LIDI.txt').read_text().split('Total delocalization index matrix (basin index)',1)[1];matrix={};cols=[]
 for line in t.splitlines()[1:]:
  if '*****' in line:break
  tokens=line.split()
  if not tokens:continue
  if all(x.isdigit() for x in tokens):cols=list(map(int,tokens));continue
  if cols and tokens[0].isdigit() and len(tokens)==len(cols)+1:
   for col,val in zip(cols,tokens[1:]):matrix[(int(tokens[0]),col)]=float(val)
 di[mesh]={'mapping':mapping,'contacts':[matrix[(mapping[a],mapping[b])] for a,b in [(1,2),(2,3),(3,4),(4,1)]]}
assert len(cp)==4
out['results'][i]={'CPs':cp,'DI':di,'mean_rho':sum(x['rho'] for x in cp.values())/4,'literal_DI_range_pass':[.374<=x<=.376 for x in di['010']['contacts']]}
Path('/tmp/rcb_post_audit_20260929.json').write_text(json.dumps(out,indent=2))
print('geometry_pairs',len(out['geometry_parents']),'errors',out['errors'])
for i,r in out['results'].items():print(i,json.dumps(r if i!=IDS[1] else {k:v for k,v in r.items() if k!='terms'})[:2600])
