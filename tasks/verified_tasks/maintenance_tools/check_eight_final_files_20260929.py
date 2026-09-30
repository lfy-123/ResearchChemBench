"""Finalize manifests and inspect only the authorized 16 staging packages.

Checks file integrity, retained evidence, current mappings and actual public
materialization. This is not new computational chemistry or deployment QA.
"""
from pathlib import Path
from collections import Counter
import json,sys,re,tempfile,tarfile,hashlib,math
from urllib.parse import unquote

ROOT=Path(__file__).resolve().parents[3]
BASE=ROOT/'tasks/verified_tasks'
BACKUP=ROOT/'.git/maintenance_backups/20260929_eight_papers_repair'
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).parent))
from rcb_audit_20260929 import IDS
from scripts.rebuild_final_manifests import rebuild
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
from pymatgen.io.cif import CifFile

output=BASE/'maintenance_tools/final_checks_20260929.json'
output.write_text(json.dumps({'status':'running','scope':'16 staging packages only'})+'\n')
checks=[];counters=Counter();packages=[]
def check(ok,label,detail=None):
 checks.append({'check':label,'passed':bool(ok),'detail':detail})
def load(p):return json.loads(p.read_text())
def links(path,text=None):
 for target in re.findall(r'\]\(([^)]+)\)',path.read_text() if text is None else text):
  if target.startswith(('http:','https:','#','mailto:')):continue
  target=unquote(target.split('#')[0]);counters['local_link_occurrences']+=1
  check((path.parent/target).exists(),'local link '+str(path.relative_to(ROOT)),target)
def section(text,start,end=None):
 value=text[text.index(start):]
 return value[:value.index(end)] if end else value

paths=[BASE/mode/('paper_'+i) for mode in ['autonomous_research','paper_reproduction'] for i in IDS]
for p in paths:rebuild(p)
repository=TaskRepository(roots=[BASE])
with tarfile.open(BACKUP/'before_repair.tar.gz') as tar:
 for p in paths:
  label=str(p.relative_to(BASE));mode=p.parent.name;i=p.name.removeprefix('paper_')
  report=validate_task_package(p);check(report.status=='passed','package '+label,report.findings)
  counters['packages']+=1
  rt=load_runtime_evaluation(paper_id=p.name,task_type=mode,repository=repository)
  check(rt.policy_id=='dual_axis_100.scientific_results.v1','runtime policy '+label)
  prefix=str(p.relative_to(ROOT))+'/'
  old={m.name[len(prefix):]:m for m in tar.getmembers() if m.isfile() and m.name.startswith(prefix)}
  current={str(f.relative_to(p)):f for f in p.rglob('*') if f.is_file()}
  removed=set(old)-set(current);added=set(current)-set(old)
  expected_removed={'agent_input/data/inputs/README_coordinates.xyz'} if i==IDS[1] else set()
  expected_added={'evaluation/author_results/invalid_mixed_coordinate_fragment.xyz','evaluation/author_results/README.md'} if i==IDS[1] else set()
  check(removed==expected_removed,'only approved file removal '+label,sorted(removed))
  check(added==expected_added,'only approved new package files '+label,sorted(added))
  changed=[]
  for rel,f in current.items():
   check(not f.is_symlink(),'no symlink '+label+'/'+rel)
   if f.suffix=='.json':load(f);counters['json_files_parsed']+=1
   if rel in old:
    oldbytes=tar.extractfile(old[rel]).read()
    if f.read_bytes()!=oldbytes:changed.append(rel)
    if rel.startswith('agent_input/data/'):
     check(f.read_bytes()==oldbytes,'scientific input unchanged '+label+'/'+rel);counters['unchanged_scientific_inputs']+=1
  if i==IDS[1]:
   oldbytes=tar.extractfile(old['agent_input/data/inputs/README_coordinates.xyz']).read()
   check(current['evaluation/author_results/invalid_mixed_coordinate_fragment.xyz'].read_bytes()==oldbytes,'Rh private fragment byte equality '+label)
  allowed={'agent_input/task.md','agent_input/submission_schema.json','task_info.json','paper_route.md','package_manifest.json','evaluation/scoring_rules.json','evaluation/reference_key_points.json','evaluation/reference_conclusions.json','evaluation/critical_failures.json','evaluation/evidence_map.json','evaluation/verified_computation_reference.md','evaluation/task_provenance/maintenance_audit.md'}
  check(set(changed)<=allowed,'changes restricted to maintenance scope '+label,changed)
  ref=p/'evaluation/verified_computation_reference.md';txt=ref.read_text();previous=tar.extractfile(old['evaluation/verified_computation_reference.md']).read().decode()
  for start,end in [('## 2.','## 3.'),('## 4.','## 5.'),('## 5.','## 6.')]:
   check(section(txt,start,end)==section(previous,start,end),'raw scientific record retained '+label+'/'+start)
  current_map=section(txt,'## 3.','## 4.')
  kp=load(p/'evaluation/reference_key_points.json')['items'];cons=load(p/'evaluation/reference_conclusions.json')['items']
  expected_ids={x['key_point_id'] for x in kp}|{x['conclusion_id'] for x in cons}
  map_ids={l.split(' / ')[0].strip('| ') for l in current_map.splitlines() if re.match(r'^\| [a-zA-Z0-9_]+ / ',l)}
  check(map_ids==expected_ids,'reference maps exactly current IDs '+label,sorted(map_ids^expected_ids))
  audit=p/'evaluation/task_provenance/maintenance_audit.md'
  current_audit=audit.read_text().split('## 修前初审历史')[0]
  check(all(x in current_audit for x in expected_ids),'current audit maps live IDs '+label)
  check('未获迁移确认' in txt and '没有执行 final/hold 迁移' in current_audit,'current no-migration statements '+label)
  for f in [ref,audit,p/'paper_route.md']:links(f)
  for f in (p/'agent_input').rglob('*'):
   if f.suffix=='.xyz':
    lines=f.read_text().splitlines();n=int(lines[0]);coords=[x.split() for x in lines[2:] if x.strip()]
    good=len(coords)==n and all(len(x)==4 and re.fullmatch('[A-Z][a-z]?',x[0]) and all(math.isfinite(float(v)) for v in x[1:]) for x in coords)
    check(good,'parse XYZ '+label+'/'+f.name);counters['public_xyz_files']+=1
   if f.suffix=='.cif':
    data=next(iter(CifFile.from_file(str(f)).data.values())).data
    check(data['_database_code_depnum_ccdc_archive']=='CCDC 2500223' and len(data['_atom_site_label'])==238,'parse source CIF identity and sites '+label)
    check(set(data['_atom_site_occupancy'])=={'1','0.698(13)','0.302(13)'},'CIF disorder retained '+label,sorted(set(data['_atom_site_occupancy'])))
    counters['public_cif_files']+=1
  with tempfile.TemporaryDirectory(prefix='rcb-eight-final-export-') as tmp:
   copied=materialize_agent_files(paper_id=p.name,task_type=mode,destination=tmp,repository=repository)
   expected={str(f.relative_to(p/'agent_input')) for f in (p/'agent_input').rglob('*') if f.is_file()}
   check(set(copied)==expected,'real public export exact file list '+label)
   check(not any('evaluation' in Path(x).parts or 'reference' in x or 'paper_route' in x or 'README_coordinates' in x for x in copied),'private files absent from export '+label)
   counters['public_files_materialized']+=len(copied)
   for rel in copied:check((Path(tmp)/rel).read_bytes()==(p/'agent_input'/rel).read_bytes(),'export content '+label+'/'+rel)
  for dest in (ROOT/'tasks').iterdir():
   if dest.name.startswith(('final','hold')):check(not(dest/p.name).exists(),'no migration '+dest.name+'/'+p.name)
  packages.append({'package':label,'status':report.status,'manifest_hash':load(p/'package_manifest.json')['package_content_sha256'],'changed_files':sorted(changed),'removed_files':sorted(removed),'added_files':sorted(added),'public_files':len(copied)})

baseline=load(BACKUP/'baseline.json')
for rel,digest in baseline['source_files'].items():
 f=ROOT/rel;check(f.is_file() and hashlib.sha256(f.read_bytes()).hexdigest()==digest,'canonical unchanged '+rel);counters['canonical_unchanged_files']+=1
report=BASE/'MAINTENANCE_REPORT.md';txt=report.read_text();links(report,section(txt,'## 30.'))
regression=load(BASE/'maintenance_tools/repair_checks_20260929.json')
check(regression['failed']==0 and len(regression['packages'])==16,'contract regression has no failures')
check(f"{regression['passed']} 项" in txt,'report matches regression count')
failures=[x for x in checks if not x['passed']]
data={'date':'2026-09-29','status':'passed' if not failures else 'failed','counts':dict(counters),'checks':len(checks),'failed':len(failures),'failures':failures,'packages':packages,'scope':'Local files, manifest/package, mappings and real agent-input materialization only. No new QM/HPC, LLM judging, independent AR replay, deployment isolation or migration.','checks_detail':checks}
output.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in data.items() if k not in ['checks_detail','packages']},ensure_ascii=False,indent=2))
raise SystemExit(bool(failures))
