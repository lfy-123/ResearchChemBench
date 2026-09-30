"""Read-back checks for this documentation/staging batch only; no QM or task repair."""
from pathlib import Path
import sys,json,re,tempfile,tarfile,hashlib,dataclasses,collections
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rcb_audit_20260929 import ROOT,IDS
sys.path.insert(0,str(ROOT))
from evaluation.contracts import validate_task_package
from evaluation.repository import TaskRepository,materialize_agent_files
from evaluation.scoring.adapters import load_runtime_evaluation
BASE=json.loads((ROOT/'.git/maintenance_backups/20260929_eight_papers/baseline.json').read_text())
work=ROOT/'tasks/verified_tasks';errors=[];checks=[];links=0;xyzs=[];copied_public=0;source_unchanged=0;stage_same=0
def check(ok,label,detail=None):
 checks.append({'check':label,'pass':bool(ok),'detail':detail})
 if not ok:errors.append(checks[-1])
with tarfile.open(BASE['archive']) as tf:
 for mode in ['autonomous_research','paper_reproduction']:
  for i in IDS:
   src=ROOT/'tasks'/mode/('paper_'+i);dst=work/mode/('paper_'+i)
   previous=[m for m in tf.getmembers() if m.isfile() and m.name.startswith(str(src.relative_to(ROOT))+'/')]
   for m in previous:
    if m.name.endswith('/package_manifest.json'):continue
    check((ROOT/m.name).read_bytes()==tf.extractfile(m).read(),'source unchanged '+m.name);source_unchanged+=1
   srcfiles={str(p.relative_to(src)) for p in src.rglob('*') if p.is_file()};dstfiles={str(p.relative_to(dst)) for p in dst.rglob('*') if p.is_file()}
   check(dstfiles==srcfiles|{'evaluation/task_provenance/maintenance_audit.md'},'complete copied file set '+mode+'/'+i)
   for rel in srcfiles-{'package_manifest.json','evaluation/verified_computation_reference.md'}:
    check((src/rel).read_bytes()==(dst/rel).read_bytes(),'staged scientific byte equality '+mode+'/'+i+'/'+rel);stage_same+=1
   for p in [src,dst]:
    v=validate_task_package(p);check(v.status=='passed','package '+str(p.relative_to(ROOT)),v.findings)
    manifest=json.loads((p/'package_manifest.json').read_text());check(any(e['path']=='evaluation/verified_computation_reference.md' for e in manifest['entries']),'reference in manifest '+str(p.relative_to(ROOT)))
    ref=p/'evaluation/verified_computation_reference.md';text=ref.read_text()
    for fn,key in [('reference_key_points.json','key_point_id'),('reference_conclusions.json','conclusion_id')]:
     for x in json.loads((p/'evaluation'/fn).read_text())['items']:check(x[key] in text,'current evidence ID '+mode+'/'+i+'/'+x[key])
   for f in [src/'evaluation/verified_computation_reference.md',dst/'evaluation/verified_computation_reference.md',dst/'evaluation/task_provenance/maintenance_audit.md']:
    for target in re.findall(r'\]\(([^)]+)\)',f.read_text()):
     if target.startswith(('http:','https:','#')):continue
     links+=1;check((f.parent/target.split('#')[0]).exists(),'link '+str(f.relative_to(ROOT)),target)
   for f in (dst/'agent_input').rglob('*'):
    check(not f.is_symlink(),'no public symlink '+str(f.relative_to(ROOT)))
    if f.suffix=='.json':
     json.loads(f.read_text());check(True,'public json '+str(f.relative_to(ROOT)))
    if f.suffix=='.xyz':
     lines=f.read_text().splitlines();n=int(lines[0]);coords=[l.split() for l in lines[2:] if l.strip()]
     good=len(coords)==n and all(len(x)==4 and re.match('^[A-Z][a-z]?$',x[0]) for x in coords)
     for x in coords:
      for y in x[1:]:float(y)
     check(good,'xyz '+str(f.relative_to(ROOT)));xyzs.append(str(f.relative_to(ROOT)))
   for parent in (ROOT/'tasks').iterdir():
    if parent.name.startswith(('final','hold')):check(not (parent/('paper_'+i)).exists(),'no unapproved migration '+parent.name+'/'+i)
repo=TaskRepository([work])
for mode in ['autonomous_research','paper_reproduction']:
 for i in IDS:
  d=work/mode/('paper_'+i);rt=load_runtime_evaluation(paper_id='paper_'+i,task_type=mode,repository=repo)
  check(rt.policy_id=='dual_axis_100.v1','actual unchanged runtime policy '+mode+'/'+i,rt.policy_id)
  with tempfile.TemporaryDirectory(prefix='rcb_visible_') as t:
   files=materialize_agent_files(paper_id='paper_'+i,task_type=mode,destination=t,repository=repo)
   expect={str(p.relative_to(d/'agent_input')) for p in (d/'agent_input').rglob('*') if p.is_file()}
   check(set(files)==expect,'public materialization '+mode+'/'+i)
   check(not any('evaluation' in Path(x).parts or 'reference' in x or 'paper_route' in x for x in files),'private evidence not exported '+mode+'/'+i)
   copied_public+=len(files)
   for name in files:check((Path(t)/name).read_bytes()==(d/'agent_input'/name).read_bytes(),'export identical '+mode+'/'+i+'/'+name)
report=work/'MAINTENANCE_REPORT.md';batch=report.read_text().split('## 29. 2026-09-29',1)[1]
for target in re.findall(r'\]\(([^)]+)\)',batch):
 if not target.startswith(('http:','https:','#')):links+=1;check((report.parent/target.split('#')[0]).exists(),'batch report link',target)
out={'date':'2026-09-29','checks':len(checks),'failures':errors,'source_unchanged_files':source_unchanged,'source_to_stage_identical_files':stage_same,'local_link_occurrences':links,'public_files_materialized':copied_public,'public_XYZ_files':len(xyzs),'checks_detail':checks}
(work/'maintenance_tools/write_verification_20260929.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='checks_detail'},ensure_ascii=False))
if errors:raise SystemExit(1)
