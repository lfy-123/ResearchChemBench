"""Test honest pre-engine failure contracts with synthetic temporary fixtures.

Missing public prerequisites must be reportable without inventing a quantum job,
validated geometry, energy or CPU allocation. This is not scientific validation.
"""
from copy import deepcopy
import argparse
import json
from pathlib import Path
import sys
import tempfile
import jsonschema

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from chemistry_toolbox.src.output_contract import validate_output_contract
COORD = ROOT / 'tasks/upgrade_tasks/coordination_20260927'


def merge(a, b):
    a = deepcopy(a)
    for key, value in b.items():
        if key == 'required':
            a[key] = list(dict.fromkeys(a.get(key, []) + value))
        elif isinstance(value, dict) and isinstance(a.get(key), dict):
            a[key] = merge(a[key], value)
        else:
            a[key] = deepcopy(value)
    return a


def sample(schema, defs):
    s = deepcopy(schema)
    if '$ref' in s:
        s = merge(defs[s.pop('$ref').split('/')[-1]], s)
    if 'const' in s:
        return s['const']
    if 'enum' in s:
        return s['enum'][0]
    for choice in ['oneOf', 'anyOf']:
        if choice in s:
            choices = s.pop(choice)
            # Respect the requested diagnostic status when a root oneOf also
            # defines complete. Previously merging its first branch replaced
            # bounded_failure with complete and produced false diagnostics.
            desired = s.get('properties', {}).get('status', {}).get('const')
            selected = next((c for c in choices if desired is not None and
                             c.get('properties', {}).get('status', {}).get('const') == desired), choices[0])
            s = merge(s, selected)
    typ = s.get('type', 'object' if 'properties' in s else 'string')
    if isinstance(typ, list):
        typ = next((t for t in typ if t != 'null'), 'null')
    if typ == 'object':
        value = {k: sample(s.get('properties', {}).get(k, {}), defs) for k in s.get('required', [])}
        additions = {}
        for condition in s.get('allOf', []):
            if 'if' in condition:
                branch = 'then' if jsonschema.Draft202012Validator(condition['if']).is_valid(value) else 'else'
                additions = merge(additions, condition.get(branch, {}))
        if additions:
            s.pop('allOf', None)
            return sample(merge(s, additions), defs)
        return value
    if typ == 'array':
        return [sample(s.get('items', {}), defs) for _ in range(s.get('minItems', 0))]
    if typ in ['number', 'integer']:
        return min(s.get('maximum', 1), max(s.get('minimum', 0), s.get('exclusiveMinimum', -1) + 1))
    if typ == 'boolean':
        return False
    if typ == 'null':
        return None
    if s.get('pattern') == '^[0-9a-f]{64}$':
        return '0' * 64
    if s.get('pattern'):
        return 'outputs/SYNTHETIC_DIAGNOSTIC.txt'
    return 'SYNTHETIC PRECOMPUTATION DIAGNOSTIC TEST; NOT SCIENTIFIC EVIDENCE'


def inspect(pids):
    rows = []
    for pid in pids:
        path = ROOT / 'tasks/upgrade_tasks/autonomous_research' / pid / 'agent_input/submission_schema.json'
        if not path.exists():
            rows.append({'paper_id': pid, 'status': 'not_authored'})
            continue
        contract = json.loads(path.read_text())
        sc = deepcopy(contract['result_schema'])
        st = sc['properties']['status']
        choices = st.get('enum', [])
        target = next((s for s in ['bounded_failure', 'blocked', 'partial'] if s in choices), None)
        if target is None:
            rows.append({'paper_id': pid, 'status': 'unsupported_failure_state'})
            continue
        st['const'] = target
        data = sample(sc, sc.get('$defs', {}))
        for key in ['calculation_records', 'object_records']:
            if key in data:
                data[key] = []
        conclusion = data.get('conclusion', {})
        for key in ['comparison_ids', 'evidence_records', 'record_ids', 'supporting_record_ids']:
            if key in conclusion:
                conclusion[key] = []
        for key in ['resources', 'resource_usage', 'resource_record']:
            if key in data:
                for k, v in data[key].items():
                    if isinstance(v, (int, float)) and not isinstance(v, bool):
                        data[key][k] = 0
        with tempfile.TemporaryDirectory(prefix='rcb_parent_precompute_FORMAT_ONLY_') as tmp:
            work = Path(tmp)
            (work / 'report').mkdir()
            (work / 'outputs').mkdir()
            (work / 'report/report.md').write_text('SYNTHETIC failure-format regression only. No engine ran and no scientific result exists.\n')
            (work / 'outputs/SYNTHETIC_DIAGNOSTIC.txt').write_text('Synthetic prerequisite diagnostic for schema test only.\n')
            (work / 'report/results.json').write_text(json.dumps(data))
            result = validate_output_contract(work, json.dumps(contract).encode())
        rows.append({'paper_id': pid, 'status': 'passed' if result['valid'] else 'failed', 'errors': result.get('errors', [])})
    failed = [r for r in rows if r['status'] != 'passed']
    return {'status': 'failed' if failed else 'passed', 'papers': len(pids), 'failed': len(failed), 'scientific_reference_validation': False, 'results': rows}


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--batch', type=int, action='append')
    ap.add_argument('--output', type=Path, default=COORD / 'parent_precompute_failure_report.json')
    args = ap.parse_args()
    spec = json.loads((ROOT / 'docs/evalution/update/upgrade_guidance_review_manifest_20260927.json').read_text())
    ids = [r['paper_id'] for r in spec['records'] if (r['batch'] in args.batch if args.batch else r['batch'] > 1)]
    report = inspect(ids)
    args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k != 'results'}))
    for row in report['results']:
        if row['status'] != 'passed':
            print(json.dumps(row, ensure_ascii=False))
    raise SystemExit(bool(report['failed']))
