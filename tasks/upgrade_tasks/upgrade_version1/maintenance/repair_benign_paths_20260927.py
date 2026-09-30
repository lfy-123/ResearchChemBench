"""Accept benign ./ in owned contracts; preserve traversal rejection and science."""
from pathlib import Path
from copy import deepcopy
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0,str(ROOT/'docs/upgrade_tasks_verification/supervisor'))
import publish_packages as pub
from evaluation.contracts.task_package import package_payload_entries,package_content_hash,validate_task_package


def normalize(pattern):
    if not pattern.startswith('^') or 'outputs' not in pattern:
        return pattern
    if pattern.startswith('^(?:\\./)?'):
        return pattern
    return '^(?:\\./)?'+pattern[1:].replace(r'\.{1,2}',r'\.\.')


def rewrite(node, results):
    if isinstance(node,dict):
        if isinstance(node.get('pattern'),str) and 'outputs' in node['pattern']:
            old=node['pattern'];new=normalize(old)
            for good in ['outputs/a.log','./outputs/a.log','outputs/./a.log','./outputs/sub/./a.log']:
                assert re.search(new,good),(new,good)
            for bad in ['../outputs/a.log','outputs/../x','outputs/a/../../x','./outputs/../x','/outputs/a.log','evaluation/secret.json']:
                assert not re.search(new,bad),(new,bad)
            node['pattern']=new
            if new!=old:results.append({'before':old,'after':new})
        for value in node.values():rewrite(value,results)
    elif isinstance(node,list):
        for value in node:rewrite(value,results)


def main():
    ownership=pub.read(pub.COORD/'paper_ownership.json')['papers'];rows=[]
    for pid,owner in ownership.items():
        batch=owner['upgrade_batch']
        if batch not in [1,3,6]:continue
        assert not pub.author_alive(batch)
        ready=pub.read(pub.COORD/'ready'/f'{pid}.json')
        prior_status=ready['status']
        changed=[]
        for mode in pub.MODES.values():
            p=ROOT/'tasks/upgrade_tasks'/mode/pid
            schema=p/'agent_input/submission_schema.json';old=pub.read(schema);new=deepcopy(old);changes=[]
            rewrite(new,changes)
            if not changes:continue
            ready.update(status='revising',reason='Benign relative-path notation repair; prior immutable snapshot remains usable.')
            pub.atomic(pub.COORD/'ready'/f'{pid}.json',ready)
            manifest=pub.read(p/'package_manifest.json');before=manifest['package_content_sha256']
            backup=pub.BASE/'supervisor/repair_backups'/before
            for rel in ['agent_input/submission_schema.json','evaluation/task_provenance/upgrade_audit.json','package_manifest.json']:
                target=backup/rel;target.parent.mkdir(parents=True,exist_ok=True)
                if not target.exists():target.write_bytes((p/rel).read_bytes())
            pub.atomic(schema,new)
            audit_path=p/'evaluation/task_provenance/upgrade_audit.json';audit=pub.read(audit_path)
            audit.setdefault('supervisor_repairs',[]).append({'date':'2026-09-27','id':'benign_relative_paths','change':'Accept ./outputs and internal ./; reject any .. traversal. Scientific fields, matrices and scoring unchanged.'})
            pub.atomic(audit_path,audit)
            entries=package_payload_entries(p);manifest.update(entries=[e.model_dump(mode='json') for e in entries],package_content_sha256=package_content_hash(entries));pub.atomic(p/'package_manifest.json',manifest)
            v=validate_task_package(p);assert v.status=='passed',v.findings
            changed.append({'mode':mode,'before':before,'after':manifest['package_content_sha256'],'patterns_changed':len(changes)})
        if changed:rows.append({'paper_id':pid,'upgrade_batch':batch,'previous_status':prior_status,'packages':changed})
    # Keep maintained generators aligned without rebuilding any package.
    for rel in ['coordination_20260927/batch3/implement.py','coordination_20260927/batch6/build_batch.py']:
        p=ROOT/'tasks/upgrade_tasks'/rel;s=p.read_text()
        s=re.sub(r"r'([^'\n]*outputs[^'\n]*)'",lambda m:"r'"+normalize(m.group(1))+"'",s)
        compile(s,str(p),'exec');p.write_text(s)
    report={'updated_at':pub.now(),'status':'repaired_pending_scoped_runtime_readback','papers':len(rows),'packages':sum(len(r['packages']) for r in rows),'scientific_criteria_changed':False,'rows':rows}
    pub.atomic(pub.BASE/'supervisor/benign_path_repair.json',report)
    print(json.dumps({k:v for k,v in report.items() if k!='rows'}))


if __name__=='__main__':main()
