# Model input/output trajectory format

Each Agent run now writes `_model_io.jsonl` in its workspace. The file records
the complete observable model trajectory across the primary OpenCode session
and any child/subagent sessions.

## Why the file is event-sourced

A later model request contains the initial task plus all earlier messages and
tool results. Copying that full context into every line would multiply storage
by the number of turns and can turn a single run into many gigabytes.

The trajectory therefore stores each input or output once and represents the
input to every model step as ordered references:

- the initial `input_message` record;
- prior `model_step:*:output` records in the same session;
- `INSTRUCTIONS.md`, `_toolbox_catalog.json`, and `opencode.json` artifact
  references with SHA-256 hashes.

Following `input.context_refs` in order reconstructs the semantic message
history supplied to that step without duplicating the full history.

## Record types

| `record_type` | Meaning |
|---|---|
| `trajectory_manifest` | Format version, capture mode, artifact hashes, session/step/error counts, and capture limitations |
| `session` | Primary or child OpenCode session metadata and parent-session relationship |
| `input_message` | User/subagent input message and its ordered parts |
| `model_step` | One model response, including session-local step number, input references, assistant message metadata, text/reasoning parts, tool calls/results, token counts, cost, and finish reason when supplied by OpenCode |
| `model_error` | A failed model/API event and the session context available at failure time |

## Main fields of a model step

```json
{
  "record_type": "model_step",
  "step_index": 12,
  "session_id": "ses_...",
  "session_step_index": 9,
  "parent_session_id": null,
  "input": {
    "representation": "event_sourced_refs",
    "context_refs": [
      "input_message:msg_user",
      "model_step:1:output"
    ],
    "new_context_refs_since_previous_step": [
      "model_step:1:output"
    ],
    "initial_instruction_ref": "artifact:INSTRUCTIONS.md",
    "tool_catalog_ref": "artifact:_toolbox_catalog.json",
    "provider_config_ref": "artifact:opencode.json"
  },
  "output": {
    "record_ref": "model_step:12:output",
    "message": {
      "role": "assistant",
      "providerID": "...",
      "modelID": "...",
      "tokens": {},
      "cost": 0,
      "finish": "tool-calls"
    },
    "parts": []
  }
}
```

`step_index` is global within the run. `session_step_index` is local to the
primary Agent or one child Agent. Context references never cross sessions, so
subagent prompts and outputs are not incorrectly merged into the parent
conversation.

## Security and fidelity

- API keys, authorization headers, access/refresh tokens, passwords, common
  bearer tokens, and `sk-...` strings are redacted.
- The file does not record raw HTTP headers or a byte-for-byte provider
  request. It records the complete observable semantic trajectory available
  from OpenCode plus hashes of the prompt, tool catalog, provider config, and
  raw event stream.
- Provider-private reasoning that is never returned cannot be captured.
  Reasoning parts actually returned and stored by OpenCode are preserved.
- `_agent_output.jsonl`, `_tool_trace.jsonl`, and `_tool_results/` remain the
  authoritative raw event and Chemistry Action traces; `_model_io.jsonl`
  connects them at model-step level.

## Automatic generation and backfill

`TaskRunner.run()` generates the file after normal completion, timeout,
process failure, or a recorded model/API error whenever sufficient artifacts
exist. Existing workspaces can be backfilled with:

```bash
python - <<'PY'
from evaluation.provenance.model_io import export_model_io_trace
export_model_io_trace("workspaces/cli_runs/batch_.../run_...")
PY
```
