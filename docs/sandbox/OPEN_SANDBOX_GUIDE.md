# ResearchChemBench OpenSandbox 创建、管理与使用手册

本文档供 ResearchChemBench 的维护者和自动化 Agent 使用，说明如何在 `ailab-ai4chem` 项目中创建、管理和调用 Brainbox/OpenSandbox 兼容沙箱。

本文基于以下本地参考文档及 2026-07-31 的实际验证结果：

- 项目根目录：`/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench`
- API 参考：`沙箱 API 参考文档（OpenSandbox 兼容路径）.docx`
- API Base URL：`https://h.pjlab.org.cn/brainbox`
- 项目：`ailab-ai4chem`

## 1. 安全说明

本文不保存可直接使用的 API Key、SAT 或其他凭据。真实凭据只能放在本地
`config.local.env` 或受控的密钥管理系统中。

- 不要把真实凭据提交到仓库、Issue、日志或聊天系统。
- 本地凭据文件权限建议保持为 `600`。
- API Key 轮换时只更新本地凭据，不修改本文档。
- 沙箱实例的 SAT（Sandbox Access Token）不要长期保存。续期或修改生命周期后，旧 SAT 会立即失效。
- 调用命令时不要把 API Key 或 SAT 输出到评测日志。

## 2. 固定配置

在项目根目录执行以下命令。其他 Agent 可以直接复制本节变量：

```bash
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench

export RCB_SANDBOX_BASE_URL='https://h.pjlab.org.cn/brainbox'
export RCB_SANDBOX_PROJECT='ailab-ai4chem'
export RCB_SANDBOX_IMAGE='registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_cpu/base:python312-20260627215752'
export RCB_PROJECT_ROOT='/mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench'
export RCB_FRAMEWORK_PYTHON="$RCB_PROJECT_ROOT/.envs/researchchembench/bin/python"

set -a
source "$RCB_PROJECT_ROOT/config.local.env"
set +a
: "${RCB_SANDBOX_API_KEY:?set RCB_SANDBOX_API_KEY in config.local.env}"
```

后续示例都假定以上变量已经设置。

## 3. 已知环境与实例

### 3.1 原始环境

用户最初创建的环境：

```text
Environment ID: env-example-original
Environment name: test
Image: registry.h.pjlab.org.cn/ailab-ai4chem-ai4chem_cpu/base:python312-20260627215752
CPU: 80
Memory: 180Gi
Command port: 44772
Default lifecycle: 120 minutes
Instance capacity: 100
Prewarm size: 0
Configured ratio: 2
GPFS mount: /mnt/shared-storage-user/liyuqiang
GPFS mode: read-only
```

已知实例：

```text
sbx-example-stopped-1  已停止
sbx-example-stopped-2  兼容性测试实例，已停止
```

停止后的实例不能作为运行中的 worker 使用。需要重新创建实例并取得新的 Sandbox ID 和 SAT。

### 3.2 原始环境的限制

原始环境只有端口 `44772`，适合执行命令和小型 JSON 结果返回，但没有单独的 ResearchChemBench RPC/产物流式传输端口。

此外，当前项目不允许创建可写 GPFS volume。实测创建可写挂载会返回：

```text
writable GPFS volume "volume-0" is disabled;
set readOnly=true or enable featureGates.allowWritableGPFS
```

因此，在没有平台管理员开启 `featureGates.allowWritableGPFS` 的情况下：

- 共享项目目录只能用于读取代码、环境和软件；
- 作业必须在沙箱本地 `/tmp` 中运行；
- 状态、日志和最终产物必须通过 HTTP/RPC 同步回主节点；
- 不得假设沙箱可以直接写主节点 workspace。

## 4. 推荐的正式环境配置

ResearchChemBench 推荐使用两个端口：

- `44772`：OpenSandbox 自带的命令执行服务 `execd`；
- `44773`：ResearchChemBench worker RPC、状态查询和产物流式传输。

推荐将 `ratio` 设置为 `1`。实测原环境报告 `ratio=2`，但实例实际 cgroup 和资源统计仍为 80 CPU、180 GiB，不应在没有平台确认的情况下依赖 `ratio` 扩容。

### 4.1 创建环境

```bash
ENV_RESPONSE="$($RCB_FRAMEWORK_PYTHON - <<'PY' | \
curl -fsS -X POST \
  "$RCB_SANDBOX_BASE_URL/v1/sandbox-environments?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @-
import json
import os

print(json.dumps({
    "name": "researchchembench-sandbox-20cpu",
    "description": "ResearchChemBench distributed OpenSandbox workers",
    "image": {"uri": os.environ["RCB_SANDBOX_IMAGE"]},
    "entrypoint": ["sleep", "inf"],
    # resources 是“每个实例”的资源，不是整个环境内所有实例的总和。
    "resources": {"cpu": "20", "memory": "48Gi"},
    "ports": [
        {"containerPort": 44772, "purpose": "system service"},
        {"containerPort": 44773, "purpose": "ResearchChemBench worker RPC"}
    ],
    "defaultLifecycleMinutes": 1440,
    "instanceCapacity": 4,
    "prewarmSize": 0,
    "ratio": 1,
    "volumes": [{
        "name": "storage-vol-1",
        "mountPath": "/mnt/shared-storage-user/liyuqiang",
        "readOnly": True,
        "host": {"path": "gpfs://gpfs1/liyuqiang"}
    }]
}))
PY
)"

printf '%s\n' "$ENV_RESPONSE" | "$RCB_FRAMEWORK_PYTHON" -m json.tool

export RCB_SANDBOX_ENV_ID="$({
  printf '%s\n' "$ENV_RESPONSE"
} | "$RCB_FRAMEWORK_PYTHON" -c 'import json,sys; print(json.load(sys.stdin)["id"])')"

echo "Environment ID: $RCB_SANDBOX_ENV_ID"
```

保存输出的 `Environment ID`。后续创建实例需要它。

说明：

- `resources.cpu=20` 表示由该环境创建的每个实例拥有 20 个逻辑 CPU；
- `resources.memory=48Gi` 为每个实例配置 48 GiB，调度配置保守登记为 45000 MiB；
- `instanceCapacity=4` 表示该环境最多允许 4 个实例，因此整个池合计为 80 个逻辑 CPU 和 180000 MiB 可调度内存；
- 如果需要更多实例，更新环境容量后再创建；
- `prewarmSize=0` 可以避免未使用的预热实例占用配额；
- `defaultLifecycleMinutes=1440` 是 API 允许的最大值，即 24 小时。

### 4.2 查询环境

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandbox-environments/$RCB_SANDBOX_ENV_ID?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

### 4.3 列出环境

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandbox-environments?project=$RCB_SANDBOX_PROJECT&page=1&pageSize=200" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

## 5. 创建沙箱实例

### 5.1 创建一个实例

```bash
SBX_RESPONSE="$($RCB_FRAMEWORK_PYTHON - <<'PY' | \
curl -fsS -X POST \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  -H 'Content-Type: application/json' \
  --data-binary @-
import json
import os

print(json.dumps({
    "environmentId": os.environ["RCB_SANDBOX_ENV_ID"],
    "name": "researchchembench-worker-1",
    "type": "code",
    "lifecycleMinutes": 1440
}))
PY
)"

printf '%s\n' "$SBX_RESPONSE" | "$RCB_FRAMEWORK_PYTHON" -m json.tool

export RCB_SANDBOX_ID="$({
  printf '%s\n' "$SBX_RESPONSE"
} | "$RCB_FRAMEWORK_PYTHON" -c 'import json,sys; print(json.load(sys.stdin)["id"])')"

echo "Sandbox ID: $RCB_SANDBOX_ID"
```

实例初始通常为 `Pending`，需要等待变成 `Running`。

### 5.2 等待实例运行

```bash
for attempt in $(seq 1 60); do
  DETAIL="$(curl -fsS \
    "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID?project=$RCB_SANDBOX_PROJECT" \
    -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY")"

  STATE="$(printf '%s\n' "$DETAIL" | "$RCB_FRAMEWORK_PYTHON" -c \
    'import json,sys; print((json.load(sys.stdin).get("status") or {}).get("state", ""))')"

  echo "attempt=$attempt state=$STATE"

  if [[ "$STATE" == 'Running' ]]; then
    break
  fi
  if [[ "$STATE" == 'Failed' || "$STATE" == 'Terminated' ]]; then
    echo "Sandbox failed to start" >&2
    exit 1
  fi
  sleep 5
done
```

### 5.3 创建四个 worker 实例

```bash
for worker_number in 1 2 3 4; do
  WORKER_NUMBER="$worker_number" "$RCB_FRAMEWORK_PYTHON" - <<'PY' | \
  curl -fsS -X POST \
    "$RCB_SANDBOX_BASE_URL/v1/sandboxes?project=$RCB_SANDBOX_PROJECT" \
    -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
    -H 'Content-Type: application/json' \
    --data-binary @- \
    | "$RCB_FRAMEWORK_PYTHON" -m json.tool
import json
import os

number = os.environ["WORKER_NUMBER"]
print(json.dumps({
    "environmentId": os.environ["RCB_SANDBOX_ENV_ID"],
    "name": f"researchchembench-worker-{number}",
    "type": "code",
    "lifecycleMinutes": 1440
}))
PY
done
```

记录每个响应中的 `id`。一个 Sandbox ID 对应一个调度 worker。

## 6. 获取实例详情、端点和 SAT

### 6.1 获取详情

```bash
DETAIL="$(curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY")"

printf '%s\n' "$DETAIL" | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

### 6.2 获取当前 SAT

详情响应中的 SAT 通常位于 `endpoints.accessToken`。兼容顶层字段的提取方式如下：

```bash
export RCB_SANDBOX_SAT="$(printf '%s\n' "$DETAIL" | "$RCB_FRAMEWORK_PYTHON" -c '
import json
import sys

data = json.load(sys.stdin)
token = data.get("accessToken") or (data.get("endpoints") or {}).get("accessToken") or ""
print(token)
')"

test -n "$RCB_SANDBOX_SAT" || {
  echo 'Sandbox access token was not returned' >&2
  exit 1
}
```

不要输出 `$RCB_SANDBOX_SAT`。

也可以直接查询端点：

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/endpoints?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

## 7. 在沙箱中执行命令

命令执行使用 SAT，不使用 API Key：

```bash
COMMAND_BODY="$(COMMAND='echo hello from sandbox' "$RCB_FRAMEWORK_PYTHON" -c '
import json
import os
print(json.dumps({"command": os.environ["COMMAND"]}))
')"

curl -fsS -X POST \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/proxy/44772/command" \
  -H 'Content-Type: application/json' \
  -H "X-Sandbox-Access-Token: $RCB_SANDBOX_SAT" \
  --data-binary "$COMMAND_BODY"
```

响应是流式 NDJSON，常见事件包括：

```text
init
ping
stdout
stderr
execution_complete
error
```

HTTP 状态为 200 不代表远端命令成功。远端非零退出码会出现在 `error.error.evalue` 中，因此调用端必须解析 NDJSON，而不能只检查 `curl` 返回码。

### 7.1 检查 CPU、内存和共享目录

```bash
PROBE_COMMAND="python3 -c 'import json,os; from pathlib import Path; p=Path(\"$RCB_PROJECT_ROOT\"); print(json.dumps({\"affinity\":sorted(os.sched_getaffinity(0)),\"cpu_count\":len(os.sched_getaffinity(0)),\"project_exists\":p.is_dir(),\"project_readable\":os.access(p,os.R_OK),\"project_writable\":os.access(p,os.W_OK),\"framework_python\":(p/\".envs/researchchembench/bin/python\").is_file(),\"memory_max\":Path(\"/sys/fs/cgroup/memory.max\").read_text().strip()}))'"

COMMAND="$PROBE_COMMAND" "$RCB_FRAMEWORK_PYTHON" -c \
  'import json,os; print(json.dumps({"command":os.environ["COMMAND"]}))' \
  | curl -fsS -X POST \
      "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/proxy/44772/command" \
      -H 'Content-Type: application/json' \
      -H "X-Sandbox-Access-Token: $RCB_SANDBOX_SAT" \
      --data-binary @-
```

每个新实例都必须重新探测 CPU ID。不同 Sandbox ID 的 Linux CPU 编号通常不同，不能复用另一个实例的 `compute_cpu_ids`。

### 7.2 调用项目环境

```bash
PROJECT_COMMAND="cd $RCB_PROJECT_ROOT && PYTHONDONTWRITEBYTECODE=1 .envs/researchchembench/bin/python -c 'import chemistry_toolbox.src; print(chemistry_toolbox.src.__file__)'"

COMMAND="$PROJECT_COMMAND" "$RCB_FRAMEWORK_PYTHON" -c \
  'import json,os; print(json.dumps({"command":os.environ["COMMAND"]}))' \
  | curl -fsS -X POST \
      "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/proxy/44772/command" \
      -H 'Content-Type: application/json' \
      -H "X-Sandbox-Access-Token: $RCB_SANDBOX_SAT" \
      --data-binary @-
```

实测共享目录中的 ResearchChemBench framework Python 和科学环境可以直接运行。

## 8. 后台进程与第二 RPC 端口

OpenSandbox 命令结束后，正确脱离终端的后台进程可以继续运行。

### 8.1 启动一个临时 HTTP 服务

此例仅用于验证端口，不是正式 worker 服务：

```bash
START_RPC="bash -c 'printf sandbox-rpc-ok > /tmp/rcb-rpc-probe.txt; python3 -m http.server 44773 --directory /tmp >/tmp/rcb-rpc-http.log 2>&1 </dev/null & echo server_pid=\$!'"

COMMAND="$START_RPC" "$RCB_FRAMEWORK_PYTHON" -c \
  'import json,os; print(json.dumps({"command":os.environ["COMMAND"]}))' \
  | curl -fsS -X POST \
      "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/proxy/44772/command" \
      -H 'Content-Type: application/json' \
      -H "X-Sandbox-Access-Token: $RCB_SANDBOX_SAT" \
      --data-binary @-
```

访问第二端口：

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/proxy/44773/rcb-rpc-probe.txt" \
  -H "X-Sandbox-Access-Token: $RCB_SANDBOX_SAT"
```

预期输出：

```text
sandbox-rpc-ok
```

项目现在已经提供正式 worker RPC：

```text
chemistry_toolbox.src.sandbox_worker_rpc
```

inventory 更新脚本和运行时会通过 `44772` 自动启动它，并通过 `44773` 完成健康检查、Action 输入/产物传输、持久作业提交、状态轮询、取消和最终目录回传。通常不需要手工启动。

## 9. 沙箱本地作业目录

由于 GPFS 是只读的，推荐使用：

```text
/tmp/researchchembench/jobs/<job_id>/
├── inputs/
├── outputs/
├── report/
├── stdout.log
├── stderr.log
├── status.json
├── supervisor_spec.json
└── cancel_requested
```

作业流程：

1. 主节点在本地创建作业和 reservation；
2. 通过 RPC 把输入、spec 和必要的小文件上传到沙箱；
3. 沙箱调用现有 `chemistry_toolbox.mcp.remote_job_launcher`；
4. 现有 `chemistry_toolbox.mcp.job_supervisor` 在 `/tmp` 中运行科学程序；
5. 主节点通过 RPC 查询 `status.json` 和日志；
6. 取消作业时，在沙箱作业目录写 `cancel_requested`；
7. 作业终态后，将 outputs/report/logs 流式下载回主节点 workspace；
8. 校验同步完成后，清理沙箱本地作业目录。

不要将大型 VASP、ORCA、Gaussian、轨迹或波函数产物通过 command 的 base64 stdout 返回。应使用 `44773` 流式下载，避免内存膨胀和响应长度限制。

## 10. 列出和查询实例

列出全部实例：

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes?project=$RCB_SANDBOX_PROJECT&page=1&pageSize=200" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

只查询一个环境的运行实例：

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes?project=$RCB_SANDBOX_PROJECT&environmentId=$RCB_SANDBOX_ENV_ID&runState=running&pageSize=200" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

查询一个实例：

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

## 11. 生命周期与续期

ResearchChemBench 默认单个 Agent 任务最长约 4 小时，计算 Action 最长约 3 小时。120 分钟生命周期不足以覆盖一次完整评测。

建议：

- 创建实例时设置 `lifecycleMinutes=1440`；
- 调度前检查 `expiresAt`；
- 剩余时间小于“作业 walltime + 安全余量”时先续期；
- 续期后立即重新获取 SAT。

### 11.1 修改生命周期

设置为 1440 分钟：

```bash
curl -fsS -X PATCH \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/lifecycle?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"lifecycleMinutes":1440,"mode":"set"}' \
  | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

该响应包含新 SAT，旧 SAT 会立即失效。

### 11.2 按明确时间续期

`expiresAt` 必须是 RFC3339 时间：

```bash
NEW_EXPIRES_AT='2026-08-02T12:00:00Z'

EXPIRES_AT="$NEW_EXPIRES_AT" "$RCB_FRAMEWORK_PYTHON" -c '
import json
import os
print(json.dumps({"expiresAt": os.environ["EXPIRES_AT"]}))
' | curl -fsS -X POST \
      "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/renew-expiration?project=$RCB_SANDBOX_PROJECT" \
      -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
      -H 'Content-Type: application/json' \
      --data-binary @- \
      | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

## 12. 停止和删除实例

### 12.1 停止实例

停止后状态变为 `Terminated`：

```bash
curl -fsS -X POST \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/stop?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY"
```

成功状态为 HTTP 204，没有响应体。

### 12.2 删除实例

确认不再需要实例后执行：

```bash
curl -fsS -X DELETE \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY"
```

### 12.3 批量停止四个实例

```bash
export RCB_SANDBOX_IDS='["sbx-worker-1","sbx-worker-2","sbx-worker-3","sbx-worker-4"]'

printf '%s\n' "$RCB_SANDBOX_IDS" | "$RCB_FRAMEWORK_PYTHON" -c '
import json
import sys
print(json.dumps({"ids": json.load(sys.stdin)}))
' | curl -fsS -X POST \
      "$RCB_SANDBOX_BASE_URL/v1/sandboxes/batch/stop?project=$RCB_SANDBOX_PROJECT" \
      -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
      -H 'Content-Type: application/json' \
      --data-binary @- \
      | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

将示例 ID 替换为真实 ID。

### 12.4 批量删除实例

```bash
printf '%s\n' "$RCB_SANDBOX_IDS" | "$RCB_FRAMEWORK_PYTHON" -c '
import json
import sys
print(json.dumps({"ids": json.load(sys.stdin)}))
' | curl -fsS -X POST \
      "$RCB_SANDBOX_BASE_URL/v1/sandboxes/batch/delete?project=$RCB_SANDBOX_PROJECT" \
      -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY" \
      -H 'Content-Type: application/json' \
      --data-binary @- \
      | "$RCB_FRAMEWORK_PYTHON" -m json.tool
```

## 13. 删除环境

环境下不能存在运行中的实例。先停止并删除全部实例，再删除环境：

```bash
curl -fsS -X DELETE \
  "$RCB_SANDBOX_BASE_URL/v1/sandbox-environments/$RCB_SANDBOX_ENV_ID?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY"
```

成功状态为 HTTP 204。

## 14. 故障诊断

### 14.1 获取日志

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/diagnostics/logs?project=$RCB_SANDBOX_PROJECT&tailLines=500" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY"
```

### 14.2 获取事件

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/diagnostics/events?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY"
```

### 14.3 Inspect

```bash
curl -fsS \
  "$RCB_SANDBOX_BASE_URL/v1/sandboxes/$RCB_SANDBOX_ID/diagnostics/inspect?project=$RCB_SANDBOX_PROJECT" \
  -H "OPEN-SANDBOX-API-KEY: $RCB_SANDBOX_API_KEY"
```

### 14.4 常见问题

#### HTTP 401/403

- API 管理接口检查 `OPEN-SANDBOX-API-KEY`；
- proxy/command/RPC 检查 `X-Sandbox-Access-Token`；
- 实例续期后重新获取 SAT；
- 不要混用 API Key 和 SAT。

#### HTTP 400 writable GPFS disabled

保持 volume 的 `readOnly=true`，或者联系平台管理员开启 `featureGates.allowWritableGPFS`。

#### 命令接口 HTTP 200，但科学程序失败

解析 NDJSON 中的 `stderr` 和 `error` 事件。不能只依赖 curl 返回码。

#### CPU affinity 不匹配

每个 Sandbox ID 启动后重新探测 `os.sched_getaffinity(0)`，inventory 中只能保存该实例自己的 CPU ID。

#### 沙箱突然终止

检查：

- `expiresAt`；
- 环境/实例事件；
- cgroup 内存限制；
- 是否在作业完成前续期；
- 产物是否已同步回主节点。

## 15. ResearchChemBench 正式集成

现有分布式调度器可以继续负责：

- worker 容量统计；
- CPU、内存和 GPU reservation；
- largest-CPU-first 排队策略；
- 作业 timeout；
- native/analysis supervisor；
- 取消语义；
- 结果和 provenance 记录。

当前已经实现的 OpenSandbox 适配层包括：

1. inventory 支持 `transport: sandbox`、`sandbox_id`、端口和环境 ID；
2. inventory 更新脚本通过 command API 探测 CPU、内存、hostname 和项目环境；
3. Action 将 SSH stdin 调用替换成 OpenSandbox HTTP command/RPC；
4. native/analysis 作业在沙箱 `/tmp` 建立镜像作业目录；
5. 通过 `44773` 上传输入、查询状态、取消作业和下载产物；
6. 调度前检查实例状态和过期时间；
7. 每次续期后刷新 SAT；
8. HTTP/SAT 失效后自动刷新一次 token；
9. Action 链会自动上传被引用的 workspace 文件，保证 ArtifactRef 跨 Sandbox 调用可继续使用；
10. 沙箱终止或 RPC 连续失败时将作业标记为 worker failure。

不要把 proxy URL 填入现有的 `execution_ssh_target`。proxy URL 是 HTTP 地址，不是 SSH target。

### 15.1 本地配置文件

正式配置位于项目根目录的 `.sandboxes.local.yaml`。它与 `.workers.local.yaml` 的定位相同：人工维护 Sandbox ID 和可调度资源，脚本负责探测实际 CPU 拓扑、内存、端口和项目环境并生成 inventory。

也可以使用一条命令自动创建 Environment、指定数量的实例、更新 `.sandboxes.local.yaml` 并生成 inventory：

```bash
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench

bash scripts/create_sandbox_pool.sh \
  --count 4 \
  --cpu 20 \
  --memory 48Gi \
  --available-memory-mb 45000 \
  --lifecycle-minutes 1440 \
  --replace
```

其中：

- `--count` 是创建的 Sandbox 实例数量；
- `--cpu` 和 `--memory` 是每个实例的实际配置，不是整个池的总量；
- `--available-cpu` 和 `--available-memory-mb` 控制每个实例向调度器暴露的资源；
- 未指定 `--available-cpu` 时默认等于 `--cpu`；
- 未指定 `--available-memory-mb` 时，默认从实例内存中减去 `--reserve-memory-mb`，为 RPC 和系统进程保留空间；
- `--replace` 只替换本地 YAML 和 inventory，并在替换前生成带 UTC 时间戳的备份；它不会停止旧的远端 Environment 或 Sandbox；
- API Key 仍从 `config.local.env` 的 `RCB_SANDBOX_API_KEY` 读取，不会写入 YAML 或 inventory。

查看全部参数：

```bash
bash scripts/create_sandbox_pool.sh --help
```

只生成 YAML、不调用 API：

```bash
bash scripts/create_sandbox_pool.sh \
  --count 2 \
  --cpu 32 \
  --memory 96Gi \
  --name-prefix rcb-large \
  --output .sandboxes.large.yaml \
  --inventory .sandbox_inventory.large.json \
  --generate-only
```

如果已经有可复用的 Environment，可以通过 `--environment-id env-...` 跳过 Environment 创建，只在该 Environment 下创建实例。

当前正式环境为：

```text
Environment ID: env-example-production
Environment resource per instance: 20 CPU / 48 GiB
RPC ports: 44772, 44773
Lifecycle: 1440 minutes
Instance capacity: 4
```

当前四个实例：

```text
sandbox-1  sbx-example-worker-1
sandbox-2  sbx-example-worker-2
sandbox-3  sbx-example-worker-3
sandbox-4  sbx-example-worker-4
```

每个实例在 inventory 中暴露 20 CPU 和 45,000 MiB，整个池为 80 CPU 和 180,000 MiB。配置中的 `sandbox_id: null` 配合 `create_if_missing: true` 可自动创建新实例；创建成功后脚本会把新 ID 写回源 YAML。

配置中的几个名称不要混用：

- `environment.name` 是创建 Environment 时的显示名称，平台要求非空，建议稳定且可读；
- worker 条目中的 `name` 主要是本地显示标签。已有 `sandbox_id` 时修改它不会重命名远端实例；只有自动新建实例时，它才会作为创建请求的显示名称。它可以自定义，但建议四个实例使用不重复且稳定的名称；
- `worker_id` 是 ResearchChemBench 调度器的逻辑身份，必须在 inventory 内唯一，运行期间不要随意修改；
- `sandbox_id`（`sbx-...`）才是 OpenSandbox API 查找、续期、停止和代理访问实例时使用的真实身份。

因此，`.sandboxes.local.yaml` 中的 `name` 不是连接凭据，也不参与实例寻址。即使平台详情接口把远端 `name` 显示为 `sbx-...`，只要 `sandbox_id` 正确，调度和执行不受影响。

生成或刷新 inventory：

```bash
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench

.envs/researchchembench/bin/python scripts/update_sandbox_inventory.py \
  --input .sandboxes.local.yaml \
  --output .sandbox_inventory.local.json
```

该命令会对每个实例执行真实探测并自动确认 RPC 健康。任何一个实例不可用时，命令返回非零，不会生成不完整的新 inventory；已经创建成功的 ID 仍会写回源 YAML，便于修复后重试。

`config.local.env` 中使用：

```bash
RCB_DISTRIBUTED_SANDBOX_SOURCE=".sandboxes.local.yaml"
RCB_DISTRIBUTED_SANDBOX_INVENTORY=".sandbox_inventory.local.json"
RCB_SANDBOX_API_KEY="REPLACE_WITH_LOCAL_SECRET"
```

### 15.2 选择 SSH 或 Sandbox

SSH worker 仍然是默认分布式传输，不传 `--distributed-transport` 时原有行为不变。

使用 Sandbox：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --distributed-transport sandbox \
  --distributed-inventory .sandbox_inventory.local.json \
  Task_A
```

使用原有 SSH worker：

```bash
bash scripts/submit_evaluation.sh submit \
  --execution-mode distributed \
  --distributed-transport ssh \
  --distributed-inventory .worker_inventory.local.json \
  Task_A
```

两个分支共享同一个资源池、reservation、排队、超时、取消、Action 和 persistent-job 核心逻辑，仅远端传输边界不同。

## 16. 已完成的兼容性验证

2026-07-31 已实际验证：

- 80 个可见 CPU；
- 180 GiB cgroup 内存；
- 项目和 `.envs` 可读；
- 项目 GPFS 不可写；
- framework Python 和现有包可以运行；
- 现有 `remote_worker_launcher -> worker_launcher -> RDKit backend` 成功执行；
- 乙醇描述符计算成功：`MolWt=46.069`、`TPSA=20.23`、`MolLogP=-0.0014`；
- 后台进程可以跨 command 请求存活；
- marker-based cancellation 可用；
- 非零退出码以结构化 error 返回；
- 同一实例的并发 command 请求可并行执行；
- 现有 `remote_job_launcher + job_supervisor` 可在 `/tmp` 异步运行；
- 状态、日志、资源统计和产物生成正常；
- 第二端口 `44773` 可通过 proxy 流式访问。
- Sandbox inventory 可从源 YAML 自动生成；
- 4 个 20 CPU Sandbox 可同时获得独立满核 reservation 并并发执行；
- 带 SDF 文件产物的 Action 可同步回主节点；
- 上一次 Action 的 ArtifactRef 可作为下一次 Sandbox Action 输入；
- native job 和 programmable analysis 均可在 `/tmp` 持久运行，轮询终态并同步完整目录。
- 四个实例的真实边界探测均为：项目目录可读、不可写，`/tmp` 可写，stdout、stderr 和 RPC JSON 均可正确返回；
- `PV_Protonation_Barrier_Trend_Reproduction` 使用 Sandbox 完整结束并完成评分：2648.4 秒、56 次工具调用、58.32 分；
- 更简单的 `PV_CC_CO_Pathway_Selectivity_Reproduction` 使用 Sandbox 完整结束：1868.2 秒、32 次工具调用、评测进程无工具调用失败，所有规定报告文件非空；
- 两次约 83.4 MB 的 author-output 作业目录和一次约 72.3 MB 的 GoodVibes 作业目录均完成上传、运行、下载和本地落盘；
- 只读输入文件在同步前会临时增加 owner 写权限，归档解包后恢复归档中的 `0444` 模式，避免覆盖已有只读 staged input 时出现 `Permission denied`；
- 远端计算先结束而大结果仍在下载时，本地状态保持 `running` 并标记 `sandbox_artifacts_synchronizing=true`，结果完整落盘后才公开终态；
- 下载遇到 `Broken pipe`、5xx、408、409 或 429 时最多重试三次；永久 4xx 不重试；
- pysisyphus 等程序生成的内部符号链接会在远端安全解引用为普通文件，失效链接忽略，指向作业目录外部的链接拒绝。真实 IRC 作业回归归档为 4.14 MB、924 个成员、0 个链接，并包含 314 个 IRC/XYZ/trajectory 相关产物；
- Sandbox 传输专项、提交脚本和分布式资源池测试合计 27 项通过。

资源池容量是调度上限，不代表每个评测都会自动占满。上述简单任务的实际峰值是 1 个并行作业、8 CPU/8192 MiB；另一项评测的峰值是 4 CPU。原因是 Agent 顺序提交作业且每个作业只申请 1、2、4 或 8 核。另行执行的四作业并发容量测试中，四个作业各申请 20 CPU，分别落到四个 Sandbox 并同时成功，证明 80 CPU 池可以被完整利用。要提高真实利用率，任务本身必须存在独立计算，并以并发方式提交且声明相应 `resource_limits`；传输层不会自行放大资源请求。

这些验证说明 OpenSandbox 已可作为当前 SSH compute worker 的兼容替代传输；SSH 分支仍保留并继续作为默认值。
