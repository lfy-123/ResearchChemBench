"""Flask UI/API for ResearchChemBench task execution and scoring."""

from __future__ import annotations

import argparse
import json
import mimetypes
import shutil
import threading
import time

from flask import Flask, Response, jsonify, request, send_file, send_from_directory
from flask_cors import CORS

from ..execution.runner import TaskRunner
from ..provenance.trace import load_tool_trace
from ..repository import (
    build_file_tree,
    get_run_workspace,
    list_runs,
    list_tasks_grouped,
    load_task_info,
    safe_resolve,
)
from ..scoring.service import score_run
from ..settings import AGENT_PRESETS, TASKS_DIR

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
app.json.sort_keys = False
CORS(app)

_ACTIVE_RUNNERS: dict[str, TaskRunner] = {}
_ACTIVE_LOCK = threading.Lock()


@app.route("/")
def index():
    return send_from_directory(app.template_folder, "index.html")


@app.route("/api/config")
def api_config():
    presets = {
        key: {
            "label": value["label"],
            "icon": value.get("icon", ""),
            "logo": value.get("logo", ""),
        }
        for key, value in AGENT_PRESETS.items()
    }
    return jsonify({"presets": presets})


@app.route("/api/tasks")
def api_tasks():
    return jsonify(list_tasks_grouped())


@app.route("/api/tasks/<task_id>/info")
def api_task_info(task_id: str):
    try:
        return jsonify(load_task_info(task_id))
    except (FileNotFoundError, ValueError):
        return jsonify({"error": "Task not found"}), 404


@app.route("/api/tasks/<task_id>/files")
def api_task_files(task_id: str):
    data_dir = TASKS_DIR / task_id / "data"
    if not data_dir.is_dir():
        return jsonify([])
    return jsonify(build_file_tree(data_dir, "data"))


@app.route("/api/tasks/<task_id>/file")
def api_task_file(task_id: str):
    data_dir = TASKS_DIR / task_id / "data"
    user_path = request.args.get("path", "")
    if user_path.startswith("data/"):
        user_path = user_path[5:]
    path = safe_resolve(data_dir, user_path)
    if path is None or not path.is_file():
        return jsonify({"error": "File not found"}), 404
    mime, _ = mimetypes.guess_type(path.name)
    return send_file(path, mimetype=mime or "application/octet-stream")


@app.route("/api/runs", methods=["GET"])
def api_list_runs():
    return jsonify(list_runs(request.args.get("task_id")))


@app.route("/api/runs", methods=["POST"])
def api_start_run():
    data = request.get_json(silent=True) or {}
    task_id = data.get("task_id", "")
    agent_key = data.get("agent", "")
    if not (TASKS_DIR / task_id / "task_info.json").is_file():
        return jsonify({"error": "Unknown task"}), 404
    if agent_key not in AGENT_PRESETS:
        return jsonify({"error": "Unknown agent preset"}), 400
    runner = TaskRunner(task_id, agent_key=agent_key)
    run_id = runner.run_async()
    with _ACTIVE_LOCK:
        _ACTIVE_RUNNERS[run_id] = runner
        finished = [
            key
            for key, value in _ACTIVE_RUNNERS.items()
            if key != run_id and value.thread is not None and not value.thread.is_alive()
        ]
        for key in finished:
            _ACTIVE_RUNNERS.pop(key, None)
    return jsonify(
        {
            "run_id": run_id,
            "task_id": task_id,
            "agent": agent_key,
            "status": "running",
            "workspace": str(runner.workspace),
        }
    )


@app.route("/api/runs/<run_id>/stop", methods=["POST"])
def api_stop_run(run_id: str):
    with _ACTIVE_LOCK:
        runner = _ACTIVE_RUNNERS.get(run_id)
    if runner is None:
        return jsonify({"error": "Run is not active"}), 404
    runner.request_stop()
    return jsonify({"status": "stopping", "run_id": run_id})


@app.route("/api/runs/<run_id>/meta")
def api_run_meta(run_id: str):
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    try:
        return jsonify(json.loads((workspace / "_meta.json").read_text(encoding="utf-8")))
    except (FileNotFoundError, json.JSONDecodeError):
        return jsonify({"error": "Metadata unavailable"}), 404


@app.route("/api/runs/<run_id>/output")
def api_run_output(run_id: str):
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    path = workspace / "_agent_output.jsonl"
    if not path.exists():
        return jsonify([])
    lines = [line for line in path.read_text(encoding="utf-8", errors="replace").splitlines() if line]
    tail = request.args.get("tail", type=int)
    if tail and tail > 0:
        lines = lines[-tail:]
    return jsonify(lines)


@app.route("/api/runs/<run_id>/trace")
def api_run_trace(run_id: str):
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    return jsonify(load_tool_trace(workspace))


@app.route("/api/runs/<run_id>/stream")
def api_run_stream(run_id: str):
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    output_path = workspace / "_agent_output.jsonl"
    trace_path = workspace / "_tool_trace.jsonl"
    meta_path = workspace / "_meta.json"

    def generate():
        output_offset = 0
        trace_offset = 0
        keepalive = 0
        while True:
            for event_type, path, offset_name in (
                ("agent", output_path, "output"),
                ("tool", trace_path, "trace"),
            ):
                if not path.exists():
                    continue
                lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
                offset = output_offset if offset_name == "output" else trace_offset
                for line in lines[offset:]:
                    payload = {"stream": event_type, "line": line}
                    yield f"data: {json.dumps(payload, ensure_ascii=False)}\n\n"
                if offset_name == "output":
                    output_offset = len(lines)
                else:
                    trace_offset = len(lines)

            if meta_path.exists():
                try:
                    meta = json.loads(meta_path.read_text(encoding="utf-8"))
                    if meta.get("status") in {"completed", "failed"}:
                        yield f"data: {json.dumps({'stream': 'system', 'status': meta['status']})}\n\n"
                        break
                except (json.JSONDecodeError, OSError):
                    pass
            keepalive += 1
            if keepalive >= 40:
                yield ": keepalive\n\n"
                keepalive = 0
            time.sleep(0.5)

    return Response(
        generate(),
        mimetype="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"},
    )


@app.route("/api/runs/<run_id>/files")
def api_run_files(run_id: str):
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    return jsonify(build_file_tree(workspace))


@app.route("/api/runs/<run_id>/file")
def api_run_file(run_id: str):
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    path = safe_resolve(workspace, request.args.get("path", ""))
    if path is None or not path.is_file():
        return jsonify({"error": "File not found"}), 404
    mime, _ = mimetypes.guess_type(path.name)
    return send_file(path, mimetype=mime or "text/plain")


@app.route("/api/runs/<run_id>/score", methods=["POST"])
def api_score_run(run_id: str):
    result = score_run(run_id)
    return jsonify(result), (400 if result.get("error") else 200)


@app.route("/api/runs/<run_id>", methods=["DELETE"])
def api_delete_run(run_id: str):
    with _ACTIVE_LOCK:
        runner = _ACTIVE_RUNNERS.pop(run_id, None)
    if runner:
        runner.request_stop()
    workspace = get_run_workspace(run_id)
    if workspace is None:
        return jsonify({"error": "Run not found"}), 404
    shutil.rmtree(workspace)
    return jsonify({"status": "deleted", "run_id": run_id})


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=5000)
    parser.add_argument("--debug", action="store_true")
    args = parser.parse_args(argv)
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        threaded=True,
        use_reloader=False,
    )
    return 0


if __name__ == "__main__":
    main()
