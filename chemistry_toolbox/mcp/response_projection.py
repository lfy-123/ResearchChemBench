"""Deterministic public projections. Scientific validity is never inferred here."""
from __future__ import annotations

from collections import Counter
from datetime import datetime, timezone
import json

from .execution_store import execution_store
from .response_pages import create_page, read_page
from .response_policy import compact_enabled, MAX_RESPONSE_BYTES, TARGET_RESPONSE_BYTES, response_bytes

JOB_FIELDS = ("entity_id", "run_id", "submission_key", "entity_type", "state", "updated_at",
              "result_state", "result_receipt_id")


def diagnostic_summary(value):
    if not isinstance(value, dict):
        return {"message_excerpt": str(value)[:800]} if value else None
    result = {k:value[k] for k in ("code", "category", "source", "stage", "retryable", "failure_stage") if k in value}
    if value.get("message"):
        result["message_excerpt"] = str(value["message"])[:800]
        result["message_complete"] = len(str(value["message"])) <= 800
    return result


def job_summary(row, record=None, *, include_result_facts=False):
    record = record or {}
    view = {k:row[k] for k in JOB_FIELDS if k in row}
    payload = row.get("state_json") or {}
    if isinstance(payload, str):
        try: payload = json.loads(payload)
        except ValueError: payload = {}
    if not isinstance(payload, dict): payload = {}
    status = payload.get("status") if isinstance(payload.get("status"), dict) else payload
    action = record.get("action_result") or {}
    if not isinstance(action, dict): action = {}
    error = status.get("error") or action.get("error") or record.get("result_diagnostic")
    view["has_diagnostic"] = bool(error)
    view["has_warnings"] = bool(action["warnings"]) if "warnings" in action else None
    if error: view["diagnostic"] = diagnostic_summary(error)
    for k in ("job_type", "action", "backend", "runtime"):
        value = status.get(k) or action.get(k)
        if value is not None: view[k] = value
    identity = row["entity_id"]
    if row.get("entity_type") == "batch":
        view["next_tool_calls"] = [{"tool":"wait_execution_events", "arguments":{"request":{"batch_ids":[identity]}}}]
    else:
        view["next_tool_calls"] = [{"tool":"get_execution_job", "arguments":{"request":{"job_id":identity,"tail_chars":0}}}]
    if include_result_facts:
        view["result_facts"] = {"action_status":action.get("status"), "scientific_validation_status":"not_assessed",
                                "full_result_ref":record.get("full_result_ref"),
                                "result_revision":record.get("terminal_revision")}
        # Facts remain attached to a result receipt and method/geometry evidence.
        result = action.get("result") or {}
        if isinstance(result, dict):
            view["result_facts"]["scalars"] = {k:v for k,v in result.items()
                if isinstance(v,(bool,int,float)) or v is None or isinstance(v,str) and len(v)<=160}
        provenance=action.get("provenance") or {}
        if isinstance(provenance,dict):
            view["result_facts"]["method_spec"]=provenance.get("agent_selected_method_spec")
            effective=provenance.get("effective_inputs") or {}
            view["result_facts"]["electronic_state"]=effective.get("electronic_state") if isinstance(effective,dict) else None
        view["result_facts"]["input_artifacts"]=[{k:a[k] for k in ("artifact_id","semantic_type","path","sha256") if k in a}
            for a in action.get("input_artifacts",[]) if isinstance(a,dict)]
        view["result_facts"]["has_unexpanded_values"]=any(isinstance(v,(dict,list)) for v in result.values()) if isinstance(result,dict) else False
    return view


def list_job_page(request):
    if request.cursor:
        return read_page(request.cursor, tool="list_execution_jobs")
    store = execution_store()
    rows, results = store.list_job_results_snapshot()
    if request.states is not None:
        rows = [r for r in rows if r["state"] in request.states]
    if request.entity_types is not None:
        rows = [r for r in rows if r["entity_type"] in request.entity_types]
    jobs = []
    for row in rows:
        result = results[row["entity_id"]]
        from chemistry_toolbox.src.execution_states import TERMINAL_STATES
        row["result_state"] = result.get("result_state", "pending" if row["state"] not in TERMINAL_STATES else "unavailable")
        row["result_receipt_id"] = result.get("result_receipt_id")
        jobs.append(job_summary(row,result,include_result_facts=request.include_result_facts))
    summary = {"total_matching":len(jobs),"computation_jobs":sum(j["entity_type"]=="job" for j in jobs),
               "batches":sum(j["entity_type"]=="batch" for j in jobs),
               "state_counts":dict(Counter(j["state"] for j in jobs))}
    base = {"status":"success", "run_id":store.run_id,"snapshot_at":datetime.now(timezone.utc).isoformat(),
            "summary":summary,"filters":{"states":request.states,"entity_types":request.entity_types}}
    return create_page({**base,"jobs":rows},tool="list_execution_jobs",base=base,
                       collections={"jobs":jobs}, page_size=request.page_size)


def _scalar_summary(value):
    if not isinstance(value, dict): return {}
    return {k:v for k,v in value.items() if isinstance(v,(bool,int,float)) or v is None
            or isinstance(v,str) and len(v)<=160}


def _terminal_item(item, pointer):
    action = item.get("action_result") or item.get("result") or {}
    if not isinstance(action, dict): action = {}
    feedback = item.get("execution_feedback") or action.get("execution_feedback") or {}
    identity = {k:item[k] for k in ("job_id","batch_id","item_id","status","previous_status","collection_manifest","output_count",
                                   "resource_limits","duration_seconds","resource_usage") if k in item}
    fields = ("schema_version","job_id","job_type","action","backend","job_status","terminal","action_status",
              "process_status","process_exit_code","software_status","convergence_status","scientific_validation_status",
              "result_state","result_revision","result_receipt_id","full_result_ref","artifact_count","process")
    view = {k:feedback[k] for k in fields if k in feedback}
    view.setdefault("scientific_validation_status","not_assessed")
    for key in ("diagnostic","result_diagnostic"):
        if feedback.get(key): view[key] = diagnostic_summary(feedback[key])
    if action.get("error") and not view.get("diagnostic"):
        view["diagnostic"] = diagnostic_summary(action["error"])
    warnings = feedback.get("warnings", action.get("warnings"))
    view["has_warnings"] = bool(warnings) if warnings is not None else None
    if feedback.get("observations"):
        view["observations"] = _scalar_summary(feedback["observations"])
        view["observations_detail_pointer"] = pointer + "/execution_feedback/observations"
    identity["execution_feedback"] = view
    identity["result_summary"] = {"action":action.get("action"),"backend":action.get("backend"),
                                  "status":action.get("status"),"scalars":_scalar_summary(action.get("result"))}
    identity["details_pointer"] = pointer
    return identity


def wait_projection(value, tool, arguments):
    terminal = "newly_terminal_items" if tool=="wait_execution_events" else "newly_terminal_jobs"
    if terminal not in value:
        return bounded_projection(value,tool)
    collection_names = (terminal,"running_jobs","queued_jobs","held_jobs","running_items","queued_items","held_items","state_transitions")
    collections = {}
    for name in collection_names:
        if isinstance(value.get(name),list):
            collections[name] = [_terminal_item(x, f"/body/{name}/{i}") if name==terminal and isinstance(x,dict)
                                 else x for i,x in enumerate(value[name])]
    base = {k:v for k,v in value.items() if k not in collections and k not in {"resource_snapshot","batches"}}
    resources = value.get("resource_snapshot") or {}
    base["resource_snapshot"] = {k:resources[k] for k in (
        "budget","available","currently_reserved","active_job_count","execution_mode","cpu_core_semantics",
        "total_cpu_cores","total_memory_mb","available_cpu_cores","available_memory_mb","available_gpu_count",
        "maximum_cpu_cores_per_job","maximum_memory_mb_per_job","active_reservation_count") if k in resources}
    base["resource_details_pointer"] = "/body/resource_snapshot"
    base["summary_scope"] = "complete_wait_snapshot"
    final, pending = {}, {}
    if tool=="wait_execution_events":
        after = (arguments or {}).get("request",arguments or {}).get("after_sequences",{})
        final["next_sequences"] = base.pop("next_sequences",{})
        pending["next_sequences"] = {k:after.get(k,0) for k in final["next_sequences"]}
        base["batches"] = [{k:b[k] for k in ("batch_id","status","terminal","has_more_events","item_status_counts") if k in b}
                           for b in value.get("batches",[])]
    return create_page(value,tool=tool,base=base,collections=collections,final_fields=final,pending_fields=pending)


def analysis_projection(value, tool, *, root=None, scope=None):
    if response_bytes(value) <= TARGET_RESPONSE_BYTES:
        return value
    if tool=="inspect_analysis_inputs":
        inputs=value.get("inputs",[])
    else:
        inputs=(value.get("input_inspection") or {}).get("inputs",[])
    summaries=[]
    for i,item in enumerate(inputs):
        row={k:v for k,v in item.items() if k in {"name","path","source_path","sha256","size_bytes","semantic_type","format","valid","error","shape","observed_rows","columns","truncated_columns","row_limit","truncated_rows"}}
        prefix="/body/inputs" if tool=="inspect_analysis_inputs" else "/body/input_inspection/inputs"
        row["details_pointer"]=prefix+"/"+str(i)
        if isinstance(row.get("shape"),dict):
            shape=row["shape"]
            basic={"type","field_count","fields","truncated_fields","length","item_types","null_count","profiled_item_count","dimensions"}
            row["shape"]={k:v for k,v in shape.items() if k in basic}
            row["shape"]["details_omitted"]=bool(set(shape)-basic)
            row["shape_details_pointer"]=row["details_pointer"]+"/shape"
        if isinstance(row.get("columns"),list):
            columns=row.pop("columns")
            row["profiled_column_count"]=len(columns)
            row["column_names_preview"]=[v for v in columns[:8] if isinstance(v,str) and len(v)<=120]
            row["column_names_complete"]=len(row["column_names_preview"])==len(columns) and not row.get("truncated_columns",False)
        summaries.append(row)
    # Keep failures and validation findings inline; only verbose profiles become references.
    fields = {"status","valid","runtime","script_source","script_target","script_sha256","inspection_boundary",
              "execution_feedback","error","resource_limits","module_status","external_execution_findings",
              "runtime_path_injection_findings"}
    base={k:v for k,v in value.items() if k in fields}
    compliance=value.get("job_context_compliance")
    if isinstance(compliance,dict):
        relevant={"status","job_context_imported","missing_input_helpers","missing_output_helpers",
                  "unknown_input_helpers","unknown_output_helpers","directory_helper_mismatches",
                  "case_mismatches","candidate_fixes","bypass_findings","warnings","enforcement_boundary"}
        base["job_context_compliance"]={k:v for k,v in compliance.items() if k in relevant}
    for key in ("module_details","analysis_contract","job_context_compliance","resource_availability"):
        if key in value: base[key+"_pointer"]="/body/"+key
    return create_page(value,tool=tool,base=base,collections={"inputs":summaries},root=root,scope=scope)


def bounded_projection(value, tool, *, root=None, scope=None):
    """Fallback directory retains the complete value and all identity/status fields."""
    if response_bytes(value)<=MAX_RESPONSE_BYTES:
        return value
    from .response_pages import pointer_part
    identities={k:value[k] for k in ("status","job_id","batch_id","item_id","operation_id","submission_key","request_digest",
                                   "action_id","backend_id","result_state","result_receipt_id","ready","valid") if k in value}
    feedback=value.get("execution_feedback") or {}
    identities["execution_feedback"]={k:feedback[k] for k in ("job_status","action_status","process_status","software_status","convergence_status","scientific_validation_status","result_state","result_receipt_id","full_result_ref") if k in feedback}
    error=feedback.get("diagnostic") or value.get("error")
    if error: identities["diagnostic"]=diagnostic_summary(error)
    identities["response_mode"]="field_directory"
    fields=[{"field":k,"json_pointer":"/body/"+pointer_part(k),"value_type":type(v).__name__} for k,v in value.items()]
    return create_page(value,tool=tool,base=identities,collections={"fields":fields},root=root,scope=scope)


def project_response(value, tool, arguments=None):
    if not compact_enabled() or not isinstance(value,dict): return value
    if value.get("response_snapshot"):
        return value
    if tool == "list_execution_jobs" and isinstance(value.get("jobs"), list):
        base = {k:v for k,v in value.items() if k != "jobs"}
        return create_page(value, tool=tool, base=base, collections={"jobs":[job_summary(row) for row in value["jobs"]]})
    if tool in {"wait_execution_jobs","wait_execution_events"}:
        return wait_projection(value,tool,arguments)
    if tool in {"inspect_analysis_inputs","validate_analysis_program"} and value.get("status")=="success":
        return analysis_projection(value,tool)
    return bounded_projection(value,tool)
