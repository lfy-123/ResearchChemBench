import sys,json,tempfile,copy,re,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from rcb_audit_20260929 import ROOT,IDS,group
sys.path.insert(0,str(ROOT))
from chemistry_toolbox.src.output_contract import validate_output_contract
OUT={}
for i in IDS:
 for mode in ['autonomous_research','paper_reproduction']:
  p=ROOT/'tasks'/mode/('paper_'+i);contract=(p/'agent_input/submission_schema.json').read_bytes();data=json.loads((group(i)/'report/results.json').read_text())
  def run(d):
   with tempfile.TemporaryDirectory(prefix='rcb_contract_') as t:
    w=Path(t);(w/'report').mkdir();(w/'report/results.json').write_text(json.dumps(d));r=validate_output_contract(w,contract,max_errors=4)
    return {'valid':r['valid'],'error_count':r['error_count'],'errors':r['errors']}
  row={'historical_report':run(data)}
  if i==IDS[3]:
   more=copy.deepcopy(data);more['unresolved_blockers']=[];row['successful_result_plus_empty_blockers']=run(more)
   empty={'status':'success','method':data['method'],'coverage':data['coverage'],'candidates':[],'unresolved_blockers':['synthetic early failure'],'limitations':[]};row['success_without_scientific_results']=run(empty)
   early={'status':'bounded_failure','method':data['method'],'coverage':data['coverage'],'candidates':[{'candidate_id':'synthetic_failure','pathway_family':'attempt','product_configuration':'unknown','forming_atom_pair':'unresolved','validation':{'disposition':'failed_before_TS'}}],'unresolved_blockers':['synthetic SCF failure before saddle'],'limitations':[]};row['honest_early_failure_no_TS']=run(early)
  if i==IDS[2] and mode=='autonomous_research':
   mapped=copy.deepcopy(data);mapped['states']=[dict(v,state_id=k) for k,v in data['states'].items()];row['private_lossless_states_array_mapping']=run(mapped)
  OUT[mode+'/'+i]=row
  print(mode,i,[(k,v['valid']) for k,v in row.items()])
Path('/tmp/rcb_runtime_audit_20260929.json').write_text(json.dumps(OUT,indent=2))
