"""Correct the historical n2 gate without changing the expanded scientific contract.

Historical numerical evidence remains private. Rebuilding the package reapplies
the correction so a later build cannot resurrect the incomplete history audit.
"""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parents[4]
AUDIT = ROOT / 'docs/upgrade_tasks_verification/supervisor/cluster_n2_independent_readback.json'
PID = 'paper_c7217910ecbee1d9'
STATUS = 'implemented_pending_expanded_reference'
GAPS = [
    'The expanded n0/n1/n2 free, common-core constrained and vertical matrix remains incomplete.',
    'Same-geometry added-electron density, normalization/grid controls and diffuse-basis/state sensitivity remain unvalidated.',
    'Expanded uncertainty references and independent mode trials have not been calibrated; historical local minima do not prove a global minimum or superatomic shell character.',
]
NEXT = [
    'Developers may reuse the independently audited historical n2 free-minimum pair after checking raw hashes, native-to-public atom mapping, charge/spin and ligand attachment. Preserve failed and detached candidates. Evaluated agents must still establish their own authorized evidence.',
    'Complete the missing n2 vertical-anion and same-geometry density pilot, with normalization/grid and diffuse-basis/state sensitivity; do not repeat equivalent Opt/Freq work merely because a later run failed.',
    'Build and validate mapped n0/n1 free endpoints and the shared bare-neutral-core constrained series, then complete signed comparisons and independently calibrate uncertainty from actual method/numerical controls.',
]
REUSE = ('The 2026-09-27 verification inventory recovered eight historical Gaussian '
         'PBE0/def2SVP n2 local-minimum candidates with 81 atoms and 237 positive frequencies. '
         'An independent supervisor parse checks raw log/input hashes, stationarity, the '
         'P-centered icosahedral Al12 adjacency and both element-labelled ligand graphs. '
         'The selected opposite-site neutral doublet and anion singlet retain the complete '
         'object; their electronic AEA is 3.9455364457428788 eV and ZPE-corrected AEA is '
         '3.959169350252118 eV. These are historical baseline values, never expanded '
         'acceptance targets or tolerances. Native atom order differs from the public map; '
         'use the explicit graph mapping in task_provenance/historical_n2_reaudit.json. '
         'Other local minima include long Al-B contacts and require candidate-specific '
         'attachment interpretation. No global-minimum or shell-orbital claim follows. '
         'The later AR GFN2 reconstructed aggregate and unconverged PBEh-3c runs remain '
         'invalid intact endpoints, but do not erase the earlier valid Gaussian evidence. '
         'The full expanded reference remains pending.')


def update_spec(original):
    c = copy.deepcopy(original)
    c['development_status'] = STATUS
    c['reuse'] = REUSE
    c['blockers'] = GAPS
    c['unblock'] = NEXT
    c['public']['data_provenance.json']['missing'] = (
        'Full Cartesian source tables are absent. Historical developer-only n2 evidence '
        'has been recovered; expanded vertical/density, common-core and uncertainty '
        'controls remain pending. No endpoint coordinates or target values are supplied.')
    c['public']['controls.json']['historical_developer_gate'] = (
        'Historical n2 local-minimum evidence permits targeted missing-control validation. '
        'The original-object and density gates still require actual submitted evidence; '
        'a developer readiness statement is not an agent result.')
    return c


def update_metadata(dst):
    data = json.loads(AUDIT.read_text())
    assert data['paper_id'] == PID and data['valid_local_minimum_candidates'] == 8
    assert sum(bool(x['selected_for_pair']) for x in data['candidates']) == 2
    for row in data['candidates']:
        assert hashlib.sha256((ROOT / row['raw_log']).read_bytes()).hexdigest() == row['raw_log_sha256']
        assert hashlib.sha256((ROOT / row['input_path']).read_bytes()).hexdigest() == row['input_sha256']
    target = dst / 'evaluation/task_provenance/historical_n2_reaudit.json'
    target.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    source = dst / 'evaluation/task_provenance/source_review.json'
    review = json.loads(source.read_text())
    review['prior_review_finding'] = review.get('prior_review_finding', review.get('finding'))
    review['status'] = STATUS
    review['finding'] = REUSE
    review['historical_correction'] = {
        'audited_at': data['audited_at'], 'audit_path': 'evaluation/task_provenance/historical_n2_reaudit.json',
        'audit_sha256': hashlib.sha256(target.read_bytes()).hexdigest(),
        'new_engine_launches': 0, 'expanded_reference_verified': False,
        'supersedes': 'The prior assertion that no intact n2 DFT pair exists.'}
    source.write_text(json.dumps(review, ensure_ascii=False, indent=2) + '\n')
    audit_path = dst / 'evaluation/task_provenance/upgrade_audit.json'
    audit = json.loads(audit_path.read_text())
    audit['historical_reference_correction'] = review['historical_correction']
    audit_path.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + '\n')
