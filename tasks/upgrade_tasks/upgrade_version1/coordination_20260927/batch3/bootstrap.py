from pathlib import Path
import json,hashlib,shutil
ROOT=Path(__file__).resolve().parents[4];B=Path(__file__).parent;D=ROOT/'tasks/upgrade_tasks'
ids=json.load(open(B/'assignment.json'))['batch']['papers']
for pid in ids:
 for mode in ['autonomous_research','paper_reproduction']:
  source=ROOT/'tasks'/('final_verified_'+mode)/pid;dest=D/mode/pid
  if dest.exists():
   print('RESUME',dest);continue
  shutil.copytree(source,dest)
  snapshots={}
  for p in sorted(source.rglob('*')):
   if p.is_file():
    rel=p.relative_to(source);target=dest/'evaluation/legacy_final_snapshot'/str(rel.with_name(rel.name+'.snapshot'));target.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,target)
    snapshots[str(rel)]={'snapshot':str(target.relative_to(dest)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()}
  a={'source':str(source.relative_to(ROOT)),'source_package_sha256':json.load(open(source/'package_manifest.json'))['package_content_sha256'],'source_payload_snapshots':snapshots,'status':'development_in_progress','new_scientific_calculations_performed':False}
  t=dest/'evaluation/task_provenance';t.mkdir(exist_ok=True);(t/'upgrade_audit.json').write_text(json.dumps(a,indent=2)+'\n')
  print('COPIED',pid,mode,len(snapshots))
