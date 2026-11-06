#!/usr/bin/env python3
"""Aggregate blinded chemical judgments; never infer mechanism validity from text."""
import argparse,json,math
from pathlib import Path

def read(p):return json.loads(Path(p).read_text(encoding='utf-8'))
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--rules',required=True);ap.add_argument('--results',required=True);ap.add_argument('--adjudication',required=True);ap.add_argument('--submission-root',required=True);ap.add_argument('--output')
 args=ap.parse_args();rub=read(args.rules);res=read(args.results);judge=read(args.adjudication);root=Path(args.submission_root).resolve()
 if not (rub['case_id']==res.get('case_id')==judge.get('case_id')):raise ValueError('case_id mismatch')
 verdicts={x['id']:x for x in judge['items']}
 expected={x['id'] for x in rub['scientific_rubric']}
 if len(verdicts)!=len(judge['items']) or set(verdicts)!=expected:raise ValueError('missing/duplicate/extra adjudication items')
 metrics={x['id']:x for x in res.get('metrics',[])}
 if len(metrics)!=len(res.get('metrics',[])):raise ValueError('duplicate metric IDs')
 evidence={x['id']:x for x in res.get('evidence',[])}
 if len(evidence)!=len(res.get('evidence',[])):raise ValueError('duplicate evidence IDs')
 rules={x['rule_id']:x for x in rub['rules']};out=[]
 qualification=judge.get('evidence_qualification','needs_review')
 if qualification not in ['pass','fail','needs_review']:raise ValueError('invalid evidence qualification')
 def safe_file(name):
  p=(root/name).resolve()
  if root not in p.parents:raise ValueError('evidence path escapes submission root: '+str(name))
  return p.is_file()
 for item in rub['scientific_rubric']:
  j=verdicts[item['id']];v=j.get('verdict','needs_review');notes=[j.get('notes','')]
  if v not in ['pass','fail','needs_review']:raise ValueError('invalid item verdict')
  if v in ['pass','fail'] and (not judge.get('reviewer','').strip() or not j.get('notes','').strip()):
   v='needs_review';notes.append('Named independent reviewer and scientific justification required.')
  if v=='pass':
   files=j.get('evidence_files',[])
   if not files or not all(safe_file(f) for f in files):v='needs_review';notes.append('Missing linked native evidence files.')
  checks=[]
  for rid in item['rule_ids']:
   r=rules[rid]
   if r.get('type')!='numeric' or v!='pass':continue
   mid=j.get('selected_metric_id');m=metrics.get(mid)
   if m is None:v='needs_review';notes.append('A manually matched physical metric is required.');continue
   value=m.get('value');unit=m.get('unit')
   if not isinstance(value,(int,float)) or isinstance(value,bool) or not math.isfinite(value):v='needs_review';notes.append('Invalid numerical value.');continue
   if unit!=r.get('unit'):
    v='needs_review';notes.append('Unit must explicitly match the reference; no silent conversion.');continue
   evs=m.get('evidence_ids',[])
   if not evs or any(e not in evidence for e in evs):v='needs_review';notes.append('Metric lacks resolvable evidence IDs.');continue
   valid_evidence=True
   for e in evs:
    ee=evidence[e]
    if not ee.get('native_input') or not ee.get('native_output') or not safe_file(ee['native_input']) or not safe_file(ee['native_output']):valid_evidence=False
   if not valid_evidence:v='needs_review';notes.append('Missing metric-linked native inputs/outputs.');continue
   error=value-r['target'];ok=abs(error)<=r['tolerance']+1e-12
   checks.append(dict(rule_id=rid,metric_id=mid,value=value,target=r['target'],tolerance=r['tolerance'],unit=unit,error=error,numeric_window_pass=ok))
   if not ok:v='fail';notes.append('The pre-existing numeric window was not met; tolerance unchanged.')
  if qualification=='fail':v='fail';notes.append('Global evidence disqualification established by reviewer.')
  out.append(dict(id=item['id'],points=item['max_score'],verdict=v,required=item['required_for_whole_case_success'],notes=notes,numeric_checks=checks))
 certain=sum(x['points'] for x in out if x['verdict']=='pass');possible=certain+sum(x['points'] for x in out if x['verdict']=='needs_review')
 if qualification=='needs_review':overall='needs_review';confirmed=0;upper=possible
 elif qualification=='fail':overall='fail';confirmed=0;upper=0
 else:
  required=[x for x in out if x['required']]
  overall='fail' if any(x['verdict']=='fail' for x in required) else ('needs_review' if any(x['verdict']=='needs_review' for x in required) else 'pass')
  confirmed=certain;upper=possible
 result=dict(case_id=rub['case_id'],whole_case_verdict=overall,confirmed_science_score=confirmed,possible_science_score_upper_bound=upper,max_score=100,evidence_qualification=qualification,items=out,failure_modes=judge.get('failure_modes',[]),automated_semantic_judging=False,note='Scores aggregate explicit human scientific judgments. This tool cannot certify a TS, connectivity, spin state, comparability, or alternative mechanism. Status/completed and prose keywords earn no credit.')
 text=json.dumps(result,ensure_ascii=False,indent=2)+'\n'
 if args.output:Path(args.output).write_text(text,encoding='utf-8')
 else:print(text)
if __name__=='__main__':main()
