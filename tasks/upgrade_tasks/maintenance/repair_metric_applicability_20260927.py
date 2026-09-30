"""Fix object-specific inapplicable metrics without removing scientific rows."""
from pathlib import Path
from copy import deepcopy
import json
import sys

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT/'docs/upgrade_tasks_verification/supervisor'))
import publish_packages as pub
from evaluation.contracts.task_package import package_payload_entries, package_content_hash, validate_task_package

RULES = {
    'paper_b276b18215cba283': {
        'panel':'arm_geometry_control',
        'rows':{'single_on_three_transoid':['interarm_transfer_fraction'],
                'single_on_three_cisoid':['interarm_transfer_fraction']},
        'note': 'For single_on_three_transoid and single_on_three_cisoid, interarm_transfer_fraction is null with metric_applicability_reason: the capped single-arm object has no second arm. Excitation, oscillator strength and the mapped frozen-arm calculation remain mandatory. The three_fixed_arm row still requires a numeric interarm transfer fraction from the full three-arm transition density, with explicit fragment partitions and normalization; null is forbidden there.',
    },
    'paper_a0f6b899582cb9f7': {
        'panel':'truncation_and_tensor',
        'rows':{'M3_tensor':['primary_interaction_kJ_mol','control_interaction_kJ_mol']},
        'note': 'For the isolated M3_tensor row, primary_interaction_kJ_mol and control_interaction_kJ_mol are null with metric_applicability_reason because no partner is present. The full quadrupole tensor, declared origin/axes and numeric quadrupole_zz_eA2 remain mandatory. The larger_fragment row still requires both real interaction energies, a mapped larger-fragment pair and the shared M3 tensor; null cannot waive that truncation comparison. The capped-fragment input gate remains blocked.',
    },
}

def patch_schema(contract, rule):
    panel=contract['result_schema']['properties']['results']['properties'][rule['panel']]['properties']
    for row, fields in rule['rows'].items():
        metrics=panel[row]['properties']['metrics']
        for field in fields:
            metrics['properties'][field]={'const':None, 'description':rule['note']}
        metrics['properties']['metric_applicability_reason']={'type':'string','minLength':1,'description':rule['note']}
        if 'metric_applicability_reason' not in metrics['required']:
            metrics['required'].append('metric_applicability_reason')
        if rule['note'] not in panel[row]['description']:
            panel[row]['description']+=' '+rule['note']

def append_bound_rule(node, panel, note):
    if isinstance(node,dict):
        selected = node.get('rule_id') == 'rule_'+panel or node.get('key_point_id') == 'kp_'+panel
        if selected:
            for key in ['expected','statement']:
                if isinstance(node.get(key),str) and note not in node[key]:node[key]+=' '+note
            if isinstance(node.get('binding'),dict) and note not in node['binding'].get('comparison',''):
                node['binding']['comparison']+=' '+note
        for value in node.values():append_bound_rule(value,panel,note)
    elif isinstance(node,list):
        for value in node:append_bound_rule(value,panel,note)

def main():
    assert not pub.author_alive(3)
    rows=[]
    for pid,rule in RULES.items():
        ready=pub.read(pub.COORD/'ready'/f'{pid}.json');status=ready['status'];changes=[]
        for mode in pub.MODES.values():
            p=ROOT/'tasks/upgrade_tasks'/mode/pid
            manifest=pub.read(p/'package_manifest.json');oldhash=manifest['package_content_sha256']
            schema=pub.read(p/'agent_input/submission_schema.json');new=deepcopy(schema);patch_schema(new,rule)
            if schema==new:continue
            ready.update(status='revising',reason='Narrow object-specific metric applicability correction; prior snapshot retained.')
            pub.atomic(pub.COORD/'ready'/f'{pid}.json',ready)
            files=['agent_input/submission_schema.json','agent_input/submission_guide.md','agent_input/task.md',
                   'evaluation/reference_key_points.json','evaluation/scoring_rules.json',
                   'evaluation/reference_validation_plan.md','evaluation/task_provenance/upgrade_audit.json','package_manifest.json']
            backup=pub.BASE/'supervisor/repair_backups'/oldhash
            for rel in files:
                dest=backup/rel;dest.parent.mkdir(parents=True,exist_ok=True)
                if not dest.exists():dest.write_bytes((p/rel).read_bytes())
            pub.atomic(p/'agent_input/submission_schema.json',new)
            for rel in ['agent_input/task.md','agent_input/submission_guide.md','evaluation/reference_validation_plan.md']:
                f=p/rel;s=f.read_text()
                if rule['note'] not in s:f.write_text(s+'\nMetric applicability clarification: '+rule['note']+'\n')
            for rel in ['evaluation/reference_key_points.json','evaluation/scoring_rules.json']:
                d=pub.read(p/rel);append_bound_rule(d,rule['panel'],rule['note']);pub.atomic(p/rel,d)
            audit=pub.read(p/'evaluation/task_provenance/upgrade_audit.json')
            audit.setdefault('supervisor_repairs',[]).append({'date':'2026-09-27','id':'object_metric_applicability','change':rule['note'],'scientific_reference_generated':False})
            pub.atomic(p/'evaluation/task_provenance/upgrade_audit.json',audit)
            entries=package_payload_entries(p);manifest.update(entries=[e.model_dump(mode='json') for e in entries],package_content_sha256=package_content_hash(entries));pub.atomic(p/'package_manifest.json',manifest)
            v=validate_task_package(p);assert v.status=='passed',v.findings
            changes.append({'mode':mode,'before':oldhash,'after':manifest['package_content_sha256']})
        rows.append({'paper_id':pid,'previous_status':status,'change':rule['note'],'packages':changes})
    pub.atomic(pub.BASE/'supervisor/metric_applicability_repair.json',{'updated_at':pub.now(),'state':'repaired_pending_regression','rows':rows,'scientific_verified':False})
    print(json.dumps({'papers':len(rows),'packages':sum(len(r['packages']) for r in rows)}))

if __name__=='__main__':main()
