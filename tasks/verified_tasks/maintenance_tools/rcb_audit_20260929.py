from pathlib import Path
import json,re,math,collections
ROOT=Path('/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench')
IDS=['589f72ac15eb7acd','3c3d73b8715d5fcd','c49993ae88ffa0e3','c56ec62e92dbdfbc','1e3a1d290a02e5f0','9e7293af88532cd4','1255ed42fa7e12ff','3c89b494a1645491']
def group(i):return ROOT/'docs/verification'/('group_2' if i in IDS[:4] else 'group_4')/('paper_'+i)
def read(i,p):return json.loads((group(i)/p).read_text())
FILES={
IDS[0]:'provenance/six_state_closure_20260926/INDEPENDENT_RESULTS.json',
IDS[1]:'provenance/resumption_20260925/COMPUTED_HIGH_LEVEL_PROFILE.json',
IDS[2]:'provenance/resumption_20260925/thermochemistry/consistent_symmetry_v2/CURRENT_THERMOCHEMISTRY.json',
IDS[3]:'provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json',
IDS[4]:'provenance/source_cycle_closure_20260926/result.json',
IDS[5]:'provenance/balanced_reference_closure_20260926/result.json',
IDS[6]:'provenance/repaired_path_closeout_20260928/result.json',
IDS[7]:'provenance/au1_closeout_20260928/result.json'}
D={i:read(i,FILES[i]) for i in IDS}
NUM=r'[-+]?\d+(?:\.\d*)?(?:[EeDd][-+]?\d+)?'
def num(v):return float(v.replace('D','E').replace('d','e'))
def last(pattern,s):
 a=re.findall(pattern,s);return num(a[-1]) if a else None
def gaussian_geometry(s):
 matches=list(re.finditer(r'(?:Standard|Input) orientation:',s))
 for m in reversed(matches):
  seg=s[m.end():]; lines=seg.splitlines(); sep=[n for n,l in enumerate(lines[:12]) if re.match(r'\s*-{5,}',l)]
  if len(sep)<2:continue
  arr=[]
  for l in lines[sep[1]+1:]:
   if '-----' in l:break
   a=l.split()
   if len(a)==6:arr.append([int(a[1]),*[num(t) for t in a[3:]]])
  if arr:return arr
 return []
def parse(log,input_file=None):
 log=Path(log);s=log.read_text(errors='replace'); o={}
 o['log']=str(log.relative_to(ROOT));o['normal']=('Normal termination of Gaussian' in s or 'ORCA TERMINATED NORMALLY' in s)
 o['error_count']=s.count('Error termination');o['optimization_completed']='Optimization completed' in s
 o['optimization_negligible_forces']='Optimization completed on the basis of negligible forces' in s
 o['E_SCF_Eh']=last(r'SCF Done:.*?=\s*('+NUM+r')',s)
 o['E_ORCA_Eh']=last(r'FINAL SINGLE POINT ENERGY\s+('+NUM+r')',s)
 o['E_TD_Eh']=last(r'Total Energy, E\(TD-HF/TD-DFT\)\s*=\s*('+NUM+r')',s)
 o['G_Eh']=last(r'Sum of electronic and thermal Free Energies=\s*('+NUM+r')',s)
 o['Gcorr_Eh']=last(r'Thermal correction to Gibbs Free Energy=\s*('+NUM+r')',s)
 f=[]
 # Gaussian prints one complete normal-mode set per frequency calculation.
 for l in s.splitlines():
  if re.match(r'\s*Frequencies --',l):f.extend(num(v) for v in l.split('--',1)[1].split())
 geom=gaussian_geometry(s);o['geometry']=geom;o['atoms']=len(geom)
 n=len(geom); nmode=3*n-6 if n>2 else 1
 if f and nmode>0:f=f[-nmode:]
 o['frequency_count']=len(f);o['negative_cm1']=[x for x in f if x<0];o['minimum_cm1']=min(f) if f else None
 o['frequency_cm1']=f
 state=re.findall(r'Charge\s*=\s*(-?\d+)\s+Multiplicity\s*=\s*(\d+)',s)
 o['state']=list(map(int,state[-1])) if state else None
 o['S2']=re.findall(r'S\*\*2 before annihilation\s+('+NUM+r'),\s+after\s+('+NUM+r')',s)[-1:]
 o['version']=(re.findall(r'Gaussian 16:.*',s) or re.findall(r'Program Version.*',s))[:1]
 if input_file is None:
  input_file=next((log.parent/x for x in ['input.com','input.inp'] if (log.parent/x).exists()),None)
 if input_file:
  inp=Path(input_file);t=inp.read_text(errors='replace');o['input']=str(inp.relative_to(ROOT))
  r=re.search(r'(?m)^\s*#.*?(?:\n\s*\n)',t,re.S)
  o['route']=' '.join(r.group().split()) if r else t.splitlines()[0]
  lines=t.splitlines();ig=[]
  for j,line in enumerate(lines):
   if re.match(r'^\s*(?:\* xyz\s+)?-?\d+\s+\d+\s*$',line):
    for l in lines[j+1:]:
     a=l.split()
     if len(a)!=4:break
     try:ig.append([a[0],*[num(x) for x in a[1:]]])
     except ValueError:break
    if ig:break
  o['input_geometry']=ig
 o['last_orbital_block']={}
 blocks=re.findall(r'(?:[ \t]*Alpha\s+(?:occ\.|virt\.) eigenvalues --[^\n]*\n)+',s)
 if blocks:
  for typ in ['occ.','virt.']:
   lines=re.findall(r'Alpha\s+'+re.escape(typ)+r' eigenvalues --(.*)',blocks[-1])
   o['last_orbital_block'][typ]=[num(x) for l in lines for x in re.findall(r'-?\d+\.\d{5}',l)]
 return o
def resolve(i,p):
 p=Path(p)
 if p.is_absolute():return p
 if str(p).startswith('docs/'):return ROOT/p
 return group(i)/p
def collect():
 jobs={i:{} for i in IDS}
 def add(i,label,log,inp=None,expected=None):
  log=resolve(i,log)
  if log.is_dir():log=log/'stdout.log'
  if not log.is_file():raise FileNotFoundError(log)
  key=str(log)
  if key not in jobs[i]:jobs[i][key]={'labels':[label],'parsed':parse(log,resolve(i,inp) if inp else None),'expected':[]}
  else:jobs[i][key]['labels'].append(label)
  if expected:jobs[i][key]['expected'].append(expected)
 i=IDS[0]
 for c,states in D[i]['systems'].items():
  for st,r in states.items():add(i,c+'_'+st,r['directory'],expected={'E_SCF_Eh':r['E_Eh'],'G_Eh':r['G_RRHO_Eh'],'frequency_count':r['full_mode_count']})
 i=IDS[1]
 for name,r in D[i]['records'].items():
  for level,efield in [('low','E_low_Eh'),('solvent','E_SMD_low_Eh'),('high','E_high_Eh')]:
   add(i,name+'_'+level,r[level+'_directory'],expected={('E_ORCA_Eh' if level=='high' else 'E_SCF_Eh'):r[efield]})
 # Explicit connectivity evidence: accepted summaries contain only adopted endpoints/paths.
 a=read(i,'provenance/author_answer_validation_20260926/FINAL_REFERENCE_AUDIT.json')
 for e in a['evidence']:
  if 'COMPUTED_HIGH_LEVEL_PROFILE' not in e['path']:
   p=resolve(i,e['path']); ed=json.loads(p.read_text())
   def walk_conn(x,label):
    if isinstance(x,dict):
     if 'directory' in x and (resolve(i,x['directory'])/'stdout.log').exists():add(i,label,x['directory'])
     if 'IRC_origin' in x:
      ds=[d for d in (group(i)/'provenance/qzcli_hpc').glob(x['IRC_origin']+'_*') if (d/'stdout.log').is_file()]
      assert len(ds)==1,(x['IRC_origin'],ds)
      add(i,label+'/IRC_parent',ds[0])
     for k,v in x.items():walk_conn(v,label+'/'+k)
    elif isinstance(x,list):
     for n,v in enumerate(x):walk_conn(v,label+'/'+str(n))
   walk_conn(ed.get('paths',ed.get('records',{})),p.parent.name)
 i=IDS[2]
 for r in D[i]['records'].values():
  for level in ['low','high']:
   v=r[level];add(i,r['label']+'_'+level,v['directory'],expected={'E_SCF_Eh':v['SCF_E_Eh'],**({'E_TD_Eh':v['electronic_E_Eh']} if r['S1'] else {})})
 i=IDS[3]
 for e in D[i]['evidence']:
  if e['path'].endswith('/stdout.log'):add(i,Path(e['path']).parent.name,e['path'])
 i=IDS[4]
 for r in D[i]['molecules']:
  for k,v in r['native_calculations'].items():add(i,r['molecule']+'_'+k,v['path'],v['input'],{'E_SCF_Eh':v['energy_hartree']})
 i=IDS[5]
 for r in D[i]['records'].values():add(i,r['name'],r['log'],r['input'],{'G_Eh':r['G_1atm_Eh']})
 i=IDS[6]
 def walk(x,label=''):
  if isinstance(x,dict):
   if 'log' in x and 'input' in x:add(i,label,x['log'],x['input'],{'G_Eh':x['G_hartree']} if 'G_hartree' in x else None)
   for k,v in x.items():
    if k not in ['state_audit','stationary_state','proton_transfer_mode']:walk(v,label+'/'+k)
  elif isinstance(x,list):
   for n,v in enumerate(x):walk(v,label+'/'+str(n))
 walk(D[i]['records'])
 for e in D[i]['author_route_evidence']:
  add(i,'adopted_chain/'+e['route_step'],e['path'])
 i=IDS[7];a=read(i,'provenance/au1_closeout_20260928/topology_review.json')['parent']
 add(i,'Au1_optimization_frequency',a['native_log'],a['native_input'],{'frequency_count':546})
 return jobs
if __name__=='__main__':
 jobs=collect();out={};errors=[]
 for i,items in jobs.items():
  out[i]=list(items.values())
  for r in out[i]:
   p=r['parsed']
   for e in r['expected']:
    for k,v in e.items():
     if p[k] is None or abs(p[k]-v)>1e-7:errors.append([i,r['labels'],k,p[k],v])
  print(i,'logs',len(items),'normal',sum(x['parsed']['normal'] for x in items.values()),'freq',sum(bool(x['parsed']['frequency_count']) for x in items.values()),'neg_modes',collections.Counter(len(x['parsed']['negative_cm1']) for x in items.values() if x['parsed']['frequency_count']),flush=True)
 Path('/tmp/rcb_raw_audit_20260929.json').write_text(json.dumps({'papers':out,'value_errors':errors},indent=2))
 print('VALUE_ERRORS',json.dumps(errors))
