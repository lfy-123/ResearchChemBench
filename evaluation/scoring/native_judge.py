"""One persistent Codex session reads complete evidence and returns a judgment."""
import json
import os
from pathlib import Path
import signal
import subprocess
import sys

from chemistry_toolbox.src.recovery_io import atomic_json
from evaluation.settings import PROJECT_ROOT
from . import sandbox

CODEX_VERSION = "0.165.0"
CODEX = PROJECT_ROOT / f".envs/eval-cli/codex-{CODEX_VERSION}/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex"


def output_schema(truth):
    def obj(properties):
        return {"type": "object", "properties": properties, "required": list(properties), "additionalProperties": False}
    text = {"type": "string"}
    nullable_text = {"type": ["string", "null"]}
    citation = obj({"ref": text, "pointer": nullable_text,
                    "line_start": {"type": ["integer", "null"]}, "line_end": {"type": ["integer", "null"]}})
    citations = {"type": "array", "items": citation}
    assessment = {"type": "string", "enum": ["pass", "fail", "need_review"]}
    numeric = obj({"rule_id": text, "observed": {"type": "number"}, "unit": text, "citations": citations})
    numeric_limit = int(any(r["rule"]["type"] == "numeric" for r in truth["rule_table"]))
    review = obj({"conflict_rule_ids": {"type": "array", "items": text}, "conflict": text,
                  "supporting_evidence": text, "resolution_question": text})
    outcome = obj({"id": {"type": "string", "enum": [r["id"] for r in truth["scientific_conclusion_rubric"]]},
                   "assessment": assessment, "evidence_status": {"type": "string", "enum": ["supported", "partially_supported", "unsupported", "contradicted"]},
                   "rationale": text, "citations": citations, "numeric_results": {"type": "array", "items": numeric, "maxItems": numeric_limit},
                   "review_details": {"anyOf": [review, {"type": "null"}]}})
    rule = obj({"rule_id": {"type": "string", "enum": [r["rule_id"] for r in truth["rule_table"]]},
                "assessment": assessment, "rationale": text, "citations": citations})
    verdict = obj({"scientific_conclusions": {"type": "array", "items": outcome},
                   "rule_assessments": {"type": "array", "items": rule},
                   "submission_validity": {"type": "string", "enum": ["valid", "invalid_submission"]},
                   "evidence_qualification": {"type": "string", "enum": ["pass", "fail"]},
                   "evidence_notes": text, "evidence_citations": citations,
                   "objective_issue_flags": {"type": "array", "items": text},
                   "critical_failures": {"type": "array", "items": text}, "rationale": text})
    return obj({"judgment": {"anyOf": [verdict, {"type": "null"}]}, "technical_error": nullable_text})


def run_agent(directory, config, prompt):
    directory = Path(directory).resolve()
    executable = Path(os.environ.get("RCB_JUDGE_CODEX_EXECUTABLE", str(CODEX))).resolve()
    version = subprocess.check_output([str(executable), "--version"], text=True).strip()
    if version != f"codex-cli {CODEX_VERSION}":
        raise ValueError(f"Judge requires Codex {CODEX_VERSION}; got {version}")
    evidence = directory / "evidence"
    for name in ("session", "output", "scratch"):
        (directory / name).mkdir(exist_ok=True)
    state_path = directory / "native_session.json"
    state = json.loads(state_path.read_text()) if state_path.exists() else {"turns": 0, "usage": {}}
    state["completed"] = False
    atomic_json(state_path, state)
    output = directory / "output/judgment.json"
    output.unlink(missing_ok=True)
    settings = {
        "model": config["judge_model"], "model_reasoning_effort": config["reasoning_effort"],
        "model_context_window": config["context_window_tokens"], "model_auto_compact_token_limit": config["auto_compact_token_limit"],
        "model_provider": "judge", "model_providers.judge.name": "ResearchChemBench Judge",
        "model_providers.judge.base_url": config["judge_base"], "model_providers.judge.env_key": "RCB_JUDGE_API_KEY",
        "model_providers.judge.wire_api": "responses", "approval_policy": "never", "sandbox_mode": "danger-full-access",
        "web_search": "disabled",
        "shell_environment_policy.inherit": "none", "shell_environment_policy.set.PATH": f"{sys.prefix}/bin:/usr/local/bin:/usr/bin:/bin",
        "shell_environment_policy.set.LD_LIBRARY_PATH": f"{sys.prefix}/lib",
    }
    argv = [str(executable), "exec"]
    if state.get("session_id"):
        argv += ["resume", state["session_id"]]
    argv += ["--ignore-user-config", "--skip-git-repo-check", "--json",
             "--output-schema", str(evidence / "judge_schema.json"), "--output-last-message", str(output)]
    for key, value in settings.items():
        argv += ["-c", key + "=" + json.dumps(value)]
    argv.append(prompt)
    # The outer Landlock policy also covers native tools; no namespace creation is needed.
    readable = [evidence, executable.parent.parent, Path(sys.prefix), Path(sys.base_prefix)]
    readable += [Path(p) for p in ("/usr", "/bin", "/lib", "/lib64", "/etc/ssl", "/etc/ld.so.cache",
        "/etc/resolv.conf", "/etc/hosts", "/etc/nsswitch.conf", "/etc/services", "/etc/protocols",
        "/etc/passwd", "/etc/group", "/etc/localtime",
        "/proc/cpuinfo", "/proc/meminfo", "/sys/devices/system/cpu", "/dev/urandom", "/dev/random") if Path(p).exists()]
    policy = {"readable": list(dict.fromkeys(str(p.resolve()) for p in readable)),
              "writable": [str(directory / n) for n in ("session", "output", "scratch")] + ["/dev/null"]}
    atomic_json(directory / "sandbox.json", policy)
    env = {"HOME": str(directory / "session"), "CODEX_HOME": str(directory / "session"), "SHELL": "/bin/bash",
           "PATH": settings["shell_environment_policy.set.PATH"], "LD_LIBRARY_PATH": f"{sys.prefix}/lib",
           "RCB_JUDGE_API_KEY": os.environ["JUDGE_API_KEY"], "GIT_CEILING_DIRECTORIES": str(evidence),
           "TMPDIR": str(directory / "scratch"), "PYTHONDONTWRITEBYTECODE": "1"}
    env.update({k: v for k, v in os.environ.items() if k.lower() in {"http_proxy", "https_proxy", "all_proxy", "no_proxy"}})
    command = [sys.executable, str(Path(sandbox.__file__).resolve()), str(directory / "sandbox.json"), *argv]
    with (directory / "events.jsonl").open("a") as events, (directory / "stderr.log").open("a") as errors:
        process = subprocess.Popen(command, cwd=evidence, env=env, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=errors,
                                   text=True, start_new_session=True)
        completed = False
        try:
            for line in process.stdout:
                events.write(line); events.flush()
                event = json.loads(line)
                if event.get("type") == "thread.started":
                    state["session_id"] = event["thread_id"]
                elif event.get("type") == "turn.completed":
                    completed = True
                    state["completed"] = True
                    state.pop("error", None)
                    state["turns"] += 1
                    # Codex reports cumulative session usage, including earlier resumed turns.
                    state["usage"] = event.get("usage", {})
                elif event.get("type") in {"turn.failed", "error"}:
                    state["error"] = event.get("error") or event.get("message")
                atomic_json(state_path, state)
            code = process.wait()
        finally:
            if process.poll() is None:
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
    if code or not completed or not output.is_file():
        raise RuntimeError(f"Judge CLI did not complete (exit={code}): {state.get('error', 'see stderr.log')}")
    value = json.loads(output.read_text())
    if value.get("technical_error"):
        raise RuntimeError(value["technical_error"])
    return value["judgment"]
