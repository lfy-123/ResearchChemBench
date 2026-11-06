#!/usr/bin/env bash
# Use the requested gpt-test2 provider with the ARCHE scientific flow.
# RCB_CODEX_* overrides are accepted; ARCHE_EVAL_* takes precedence.
# 本文件只保留 GPT 模型/资源/路径覆盖值；流程参数统一在 run_arche_eval.sh 修改，避免重复配置。
# 全部参数的含义与范围见同目录 run_arche_eval.sh；本文件覆盖项也在每行前注明范围。
# 重叠参数改本文件；命令行开关优先于环境变量，环境变量优先于默认值。
# standard 执行全部 Top N；smoke 只调查第 1 项且附加简化指导。
# 4候选/Top2/逐个执行：NUM_QUERIES=2，HYPOTHESES_PER_QUERY=2，TOP_N=2，PARALLEL_INVESTIGATIONS=1。
# TOP_N 可设 1..5，初始候选乘积须 >=TOP_N；每项调查内部可提交多个计算作业。
# 兼容变量：RCB_CODEX_API_KEY（私有字符串）、RCB_CODEX_BASE_URL（HTTP(S) URL）、
# RCB_CODEX_MODEL（模型名）、RCB_CODEX_REASONING_EFFORT（同 REASONING 枚举）。
# 自定义配置后可追加 --dry-run 预检；不要附加 --smoke，否则会覆盖数量/预算/时限。
set +x
set -euo pipefail
umask 077
ARCHE_GPT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# 私有凭据文件路径；存在时须属当前用户且权限 0600；勿在本脚本明文写密钥。
export ARCHE_EVAL_ENV_FILE="${ARCHE_EVAL_ENV_FILE:-$ARCHE_GPT_ROOT/custom_agents/Arche-Harness/benchmark_adapter/gpt_test2.local.env}"
if [[ -n "${RCB_CODEX_API_KEY:-}" && -z "${ARCHE_EVAL_API_KEY:-}" ]]; then
  export ARCHE_EVAL_API_KEY="$RCB_CODEX_API_KEY"
fi
# 非空模型名；所有 Agent 角色使用该模型；judge 默认跟随，可用 --judge-model 独立指定。
export ARCHE_EVAL_MODEL="${ARCHE_EVAL_MODEL:-${RCB_CODEX_MODEL:-gpt-5.6-sol}}"
# default=使用模型默认值；其余 none|minimal|low|medium|high|xhigh|max。
export ARCHE_EVAL_REASONING="${ARCHE_EVAL_REASONING:-${RCB_CODEX_REASONING_EFFORT:-high}}"
# ARCHE_EVAL_BASE_URL：HTTP(S) API 根地址；裸 host 自动补 /v1，无凭据/query/fragment。
ARCHE_GPT_BASE="${ARCHE_EVAL_BASE_URL:-${RCB_CODEX_BASE_URL:-http://35.220.164.252:3888}}"
ARCHE_GPT_BASE="${ARCHE_GPT_BASE%/}"
# Match the existing Codex entrypoint: a bare host needs the /v1 API prefix.
if [[ "$ARCHE_GPT_BASE" =~ ^https?://[^/]+$ ]]; then
  ARCHE_GPT_BASE="$ARCHE_GPT_BASE/v1"
fi
# 标准化后的 API 根地址；上方已为裸 host 补 /v1。
export ARCHE_EVAL_BASE_URL="$ARCHE_GPT_BASE"
# 任务 ID：一个 paper_<ID> 或逗号分隔多个；必须存在于 TASKS_ROOT/final_verified_autonomous_research，顺序执行。
export ARCHE_EVAL_PAPERS="${ARCHE_EVAL_PAPERS:-paper_3a22e838133b906d}"
# 布尔 true|false；true 搜索/下载文献并覆盖任务禁网默认，来源论文/SI 仍过滤；false 仅检索公开输入。
export ARCHE_EVAL_PAPER_SEARCH="${ARCHE_EVAL_PAPER_SEARCH:-false}"
# 整数核 >=1；全部科学作业共享的宿主 CPU 配额，不超过宿主可用 affinity；不是每假设独占核数。
export ARCHE_EVAL_CPU_CORES="${ARCHE_EVAL_CPU_CORES:-48}"
# 整数 MiB >=1；同一 run 的宿主计算内存总配额，应 <=宿主可用内存。
export ARCHE_EVAL_MEMORY_MB="${ARCHE_EVAL_MEMORY_MB:-204800}"
# 整数 1..5；同时调查的假设数，1=逐个执行；实际最多 TOP_N，不改变调查总数。
export ARCHE_EVAL_PARALLEL_INVESTIGATIONS="${ARCHE_EVAL_PARALLEL_INVESTIGATIONS:-2}"
# 整数秒 >=1；单个科学计算动作超时，仍受 TIMEOUT 限制；GPT 默认 14400=4 小时。
export ARCHE_EVAL_COMPUTE_TIMEOUT="${ARCHE_EVAL_COMPUTE_TIMEOUT:-14400}"
# 整数秒 >=1；MCP 调用超时；建议 >=COMPUTE_TIMEOUT+60，且与 TIMEOUT 相容。
export ARCHE_EVAL_MCP_TIMEOUT="${ARCHE_EVAL_MCP_TIMEOUT:-14460}"
# 整数秒 >=1；单次任务总期限，43200=12 小时；重复任务分别计时，不保证期限内完成。
export ARCHE_EVAL_TIMEOUT="${ARCHE_EVAL_TIMEOUT:-43200}"
# 布尔 true|false；true 请求 Responses JSON-object，false 保留原生 schema；均继续校验输出。
export ARCHE_EVAL_JSON_OBJECT="${ARCHE_EVAL_JSON_OBJECT:-false}"
# 布尔 true|false；模型 HTTP/2；当前 GPT 网关使用 false，其他端点按实际支持设置。
export ARCHE_EVAL_HTTP2="${ARCHE_EVAL_HTTP2:-false}"
# 可写目录路径；在其下创建 paper_*；禁止指向受保护的 workspaces/codex_gpt56。
export ARCHE_EVAL_OUTPUT_ROOT="${ARCHE_EVAL_OUTPUT_ROOT:-$ARCHE_GPT_ROOT/workspaces/arche_gpt56}"
# 预检/旧部署兼容目录；新任务的部署、锁和指针自动放入各自结果目录/.runtime。
export ARCHE_EVAL_STATE_DIR="${ARCHE_EVAL_STATE_DIR:-$ARCHE_EVAL_OUTPUT_ROOT/.runtime}"
exec bash "$ARCHE_GPT_ROOT/scripts/run_arche_eval.sh" "$@"
