#!/usr/bin/env python3
"""Offline compact-response replay. No model/API calls or scientific calculations."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
import os
from pathlib import Path
import statistics
import sys
import tempfile

sys.path.insert(0,str(Path(__file__).resolve().parents[2]))
from chemistry_toolbox.src.execution_feedback import normalize_tool_feedback
from chemistry_toolbox.mcp.response_projection import project_response
from chemistry_toolbox.mcp.response_pages import read_page
from chemistry_toolbox.mcp.response_policy import response_bytes,MAX_RESPONSE_BYTES


def stats(values):
    values=sorted(values)
    return {"count":len(values),"sum":sum(values),"median":statistics.median(values),
            "p95":values[math.ceil(.95*len(values))-1],"max":max(values)} if values else {"count":0}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root",type=Path,required=True)
    parser.add_argument("--evidence",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    evidence=json.loads(args.evidence.read_text())
    failures=[];results=[];by_tool=defaultdict(list);validated_snapshots=0
    os.environ["RESEARCHCHEMBENCH_TOOL_RESPONSE_PROFILE"]="compact_v1"
    os.environ.pop("RESEARCHCHEM_MCP_WORKSPACE",None)
    with tempfile.TemporaryDirectory(prefix="rcb-context-replay-") as scratch:
        root=Path(scratch);os.environ["RESEARCHCHEMBENCH_WORKSPACE"]=str(root)
        os.environ["RESEARCHCHEMBENCH_RUN_ID"]="offline-replay"
        for row in evidence["projection_rows"]:
            try:
                data=(args.source_root/row["source"]).read_bytes()
                if hashlib.sha256(data).hexdigest()!=row["source_sha256"]:
                    raise ValueError("source_changed_since_audit")
                saved=json.loads(data);metadata=saved["display_projection"]
                os.environ["RESEARCHCHEMBENCH_FEEDBACK_SCHEMA_VERSION"]=str(metadata["schema_version"])
                original=normalize_tool_feedback(saved["result"],tool=row["tool"])
                encoded=json.dumps(original,sort_keys=True,ensure_ascii=False).encode()
                if hashlib.sha256(encoded).hexdigest()!=metadata["sha256"]:
                    raise ValueError("historical_projection_mismatch")
                page=project_response(original,row["tool"])
                pages=[];seen=set();collected=defaultdict(list)
                while True:
                    if response_bytes(page)>MAX_RESPONSE_BYTES:
                        raise ValueError("final_response_budget_exceeded")
                    if page.get("status") in {"invalid_request","failed"} and original.get("status") not in {"invalid_request","failed"}:
                        raise ValueError("projection_introduced_request_error:"+str(page.get("error")))
                    pages.append(len(json.dumps(page,ensure_ascii=False)))
                    for key in page.get("pagination",{}):
                        collected[key].extend(page.get(key,[]))
                    ref=page.get("full_response_ref")
                    if ref:
                        raw=(root/ref["path"]).read_bytes()
                        if hashlib.sha256(raw).hexdigest()!=ref["sha256"]:raise ValueError("snapshot_hash_mismatch")
                        if json.loads(raw)["body"]!=original:raise ValueError("snapshot_content_changed")
                        validated_snapshots+=1
                    cursor=page.get("next_cursor")
                    if not cursor:break
                    if cursor in seen:raise ValueError("cursor_cycle")
                    seen.add(cursor);page=read_page(cursor)
                for key in ("jobs","newly_terminal_jobs","newly_terminal_items"):
                    if key in original and key in collected:
                        identifiers=lambda items:[tuple(x.get(k) for k in ("entity_id","job_id","batch_id","item_id","state","status")) for x in items]
                        if identifiers(original[key])!=identifiers(collected[key]):raise ValueError("identity_or_state_lost:"+key)
                result={"tool":row["tool"],"paper_id":row["paper_id"],"old_chars":row["chars"],
                        "new_all_pages_chars":sum(pages),"pages":len(pages),"max_page_chars":max(pages)}
                results.append(result);by_tool[row["tool"]].append(result)
            except Exception as exc:
                failures.append({"source":row["source"],"tool":row["tool"],"error":str(exc),"type":type(exc).__name__})
    report={"scope":"Historical tool projection replay; includes every returned page, excludes later detail retrieval and model history/billing.",
            "matched_input_records":len(evidence["projection_rows"]),"replayed":len(results),"failures":failures,
            "snapshot_page_hash_checks":validated_snapshots,"maximum_response_bytes":MAX_RESPONSE_BYTES,
            "tools":{tool:{"old_chars":stats([r["old_chars"] for r in rows]),
                           "new_all_pages_chars":stats([r["new_all_pages_chars"] for r in rows]),
                           "total_pages":sum(r["pages"] for r in rows)} for tool,rows in by_tool.items()}}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
    print(json.dumps({k:v for k,v in report.items() if k!="tools" and k!="failures"},ensure_ascii=False))
    print("failures",len(failures))
    for item in failures[:8]:print(json.dumps(item,ensure_ascii=False))
    return bool(failures)


if __name__=="__main__":raise SystemExit(main())
