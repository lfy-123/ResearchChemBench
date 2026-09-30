from pathlib import Path
import sys,json,dataclasses
ROOT=Path('/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench')
sys.path.insert(0,str(ROOT));sys.path.insert(0,str(Path(__file__).resolve().parent))
from rcb_audit_20260929 import IDS,group
from evaluation.contracts import validate_task_package
from evaluation.scoring.adapters import _runtime_contract
from evaluation.scoring.rules import check_rule
import jsonschema
out={}
for i in IDS:
 for mode in ['autonomous_research','paper_reproduction']:
  p=ROOT/'tasks'/mode/('paper_'+i);s=json.loads((p/'agent_input/submission_schema.json').read_text())
  ref={fn:json.loads((p/'evaluation'/fn).read_text()) for fn in ['scoring_rules.json','reference_key_points.json','reference_conclusions.json','critical_failures.json','evidence_map.json']}
  r=json.loads((group(i)/'report/results.json').read_text())
  try: errs=[{'path':e.json_path,'message':e.message[:300]} for e in jsonschema.validators.validator_for(s['result_schema'])(s['result_schema']).iter_errors(r)]
  except Exception as e:errs=[{'exception':str(e)[:300]}]
  runtime=_runtime_contract(task_type=mode,reference=ref,submission=s)
  check=dataclasses.asdict(validate_task_package(p));checks=[check_rule(e,{'report/results.json':r}) for e in runtime['rule_table']]
  d={'package_check':check,'schema_errors':errs,'policy':runtime['dual_axis_scoring_policy']['policy_id'],'rubric':[{'id':c['id'],'max_score':c['max_score']} for c in runtime['scientific_conclusion_rubric']], 'standalone_rules':[e['rule_id'] for e in runtime['rule_table'] if e['association']=='standalone'],'rule_checks':checks}
  out[mode+'/'+i]=d
  print(i,mode,'PACKAGE',check['status'],'SCHEMA',len(errs),'POLICY',d['policy'],'NUMCHECK',[(c['rule_id'],c['assessment']) for c in checks if c['assessment']!='requires_semantic_review'],'STANDALONE',d['standalone_rules'])
  if errs:print('ERRORS',errs[:3])
Path('/tmp/rcb_contract_audit_20260929.json').write_text(json.dumps(out,indent=2))
