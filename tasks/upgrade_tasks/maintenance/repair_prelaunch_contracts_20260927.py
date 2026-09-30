"""Bounded supervisor repair after batch 1/3 author ownership transfer.

Only diagnostic submission semantics and density-analysis job fields change.
The full scientific matrix, numbers, evaluator weights and references do not.
"""
from pathlib import Path
import datetime as dt
import json
import sys
from copy import deepcopy

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from evaluation.contracts.task_package import PackageManifest, package_payload_entries, package_content_hash
from tasks.upgrade_tasks.maintenance.check_precompute_failures import inspect

DEST = ROOT / 'tasks/upgrade_tasks'
SUP = ROOT / 'docs/upgrade_tasks_verification/supervisor'
sys.path.insert(0, str(DEST / 'coordination_20260927/batch3'))
import implement

NOTE = ('A prerequisite failure before engine launch may use empty object_records and '
        'calculation_records (where defined), empty conclusion.supporting_record_ids, and '
        'zero allocated_cores/engine_starts/core_hours (where defined), with real diagnostic '
        'evidence and failure_report. Describe the intended protocol and identify software '
        'that was not run. Do not invent a geometry, frequency, energy or job. Complete '
        'submissions retain every required scientific endpoint and actual successful engine evidence.')

def dump(p, value):
    p.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def main():
    for pid in [1735493]:
        p = Path(f'/proc/{pid}/cmdline')
        if p.exists() and b'codex' in p.read_bytes():
            raise RuntimeError('Batch 3 author may still own these packages')
    groups = json.loads((ROOT / 'docs/upgrade_tasks_verification/manifest.json').read_text())['groups']
    ids = [pid for g in groups if g['group'] in [1, 3] for pid in g['paper_ids']]
    before = inspect(ids)
    dump(SUP / 'prelaunch_reproduction_before.json', before)
    changed = []
    for g in groups:
        if g['group'] not in [1, 3]:
            continue
        for pid in g['paper_ids']:
            for mode in ['autonomous_research', 'paper_reproduction']:
                pkg = DEST / mode / pid
                p = pkg / 'agent_input/submission_schema.json'
                contract = json.loads(p.read_text())
                old = deepcopy(contract)
                previous_hash = json.loads((pkg / 'package_manifest.json').read_text())['package_content_sha256']
                if g['group'] == 1:
                    s = contract['result_schema']
                    s['properties']['calculation_records']['minItems'] = 0
                    s['properties']['conclusion']['properties']['supporting_record_ids']['minItems'] = 0
                    complete = next(b for b in s['oneOf'] if b['properties']['status']['const'] == 'complete')
                    complete['properties']['calculation_records']['minItems'] = 1
                    complete['properties']['conclusion'] = {'properties': {'supporting_record_ids': {'minItems': 1}}}
                else:
                    objects = json.loads((pkg / 'agent_input/data/inputs/objects.json').read_text())['objects']
                    contract = implement.schema(pid, implement.S[pid], objects)
                if contract == old:
                    continue
                backup = SUP / 'repair_backups' / previous_hash
                backup.mkdir(parents=True, exist_ok=True)
                for rel in ['agent_input/submission_schema.json', 'agent_input/submission_guide.md', 'evaluation/task_provenance/upgrade_audit.json', 'package_manifest.json']:
                    q = backup / rel
                    q.parent.mkdir(parents=True, exist_ok=True)
                    if not q.exists():
                        q.write_bytes((pkg / rel).read_bytes())
                dump(p, contract)
                gp = pkg / 'agent_input/submission_guide.md'
                guide = gp.read_text()
                if g['group'] == 3:
                    guide = guide.replace('`successful` requires actual geometry, energy and convergence evidence.',
                        'Successful engine jobs require actual geometry, energy and convergence evidence. Density-analysis records require actual input/output and validation evidence without inventing geometry or electronic energy; analysis alone cannot establish complete engine coverage.')
                if NOTE not in guide:
                    guide += '\n\n## Prelaunch diagnostic reporting\n\n' + NOTE + '\n'
                gp.write_text(guide)
                ap = pkg / 'evaluation/task_provenance/upgrade_audit.json'
                audit = json.loads(ap.read_text())
                audit.setdefault('supervisor_contract_repairs', []).append({
                    'at': dt.datetime.now(dt.timezone.utc).isoformat(),
                    'issue': 'prelaunch_failure_requires_fake_job',
                    'previous_package_content_sha256': previous_hash,
                    'changes': ['zero-launch diagnostics allowed', 'complete requirements preserved'] + (['density-analysis records do not invent energy or geometry'] if g['group'] == 3 else []),
                    'scientific_thresholds_changed': False, 'new_scientific_computations': 0})
                dump(ap, audit)
                entries = package_payload_entries(pkg)
                manifest = PackageManifest(paper_id=pid, task_type=mode, entries=entries, package_content_sha256=package_content_hash(entries))
                dump(pkg / 'package_manifest.json', manifest.model_dump(mode='json'))
                changed.append({'paper_id': pid, 'mode': mode, 'old_hash': previous_hash, 'new_hash': manifest.package_content_sha256})
    # Keep development manifests current without rewriting historical validation reports.
    p = DEST / 'batch1_implementation_manifest.json'
    m = json.loads(p.read_text())
    for row in m['packages']:
        row['package_content_sha256'] = json.loads((ROOT / row['path'] / 'package_manifest.json').read_text())['package_content_sha256']
    m['supervisor_repair_report'] = 'docs/upgrade_tasks_verification/supervisor/prelaunch_repair.json'
    dump(p, m)
    p = DEST / 'coordination_20260927/batch3/manifest.json'
    m = json.loads(p.read_text())
    for row in m['papers']:
        row['package_content_sha256'] = {key: json.loads((ROOT / row[key] / 'package_manifest.json').read_text())['package_content_sha256'] for key in ['AR', 'PR']}
    m['supervisor_repair_report'] = 'docs/upgrade_tasks_verification/supervisor/prelaunch_repair.json'
    dump(p, m)
    after = inspect(ids)
    dump(SUP / 'prelaunch_reproduction_after.json', after)
    dump(SUP / 'prelaunch_repair.json', {'at': dt.datetime.now(dt.timezone.utc).isoformat(), 'changed_packages': changed, 'before_failed_papers': before['failed'], 'after_failed_papers': after['failed'], 'scientific_verification': False})
    print(json.dumps({'changed_packages': len(changed), 'before_failed': before['failed'], 'after_failed': after['failed']}))
    if after['failed']:
        print(json.dumps([{'paper_id': r['paper_id'], 'errors': [{'path': e.get('instance_path'), 'message': e.get('message', '')[:160]} for e in r.get('errors', [])]} for r in after['results'] if r['status'] != 'passed']))
        raise SystemExit(1)

if __name__ == '__main__':
    main()
