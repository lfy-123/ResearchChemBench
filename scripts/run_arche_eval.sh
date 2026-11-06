#!/usr/bin/env bash
# ARCHE 一键评估：所有可调整参数集中在这里；环境变量可覆盖默认值。
# 密钥只从私有 env 文件或进程环境读取，不写入生成的 YAML / 参数快照。
set +x
set -euo pipefail
umask 077
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$PROJECT_ROOT"

# 参数总则：全部可配置变量列在下方，默认值就在每行 :- 后。
# 日常只改科学流程/计算配额即可；路径和部署为原有高级设置，通常沿用默认。
# 优先级：命令行开关 > 已设置环境变量 > 脚本默认值。GPT 入口先设置自身默认值，重叠项请改 GPT 脚本。
# 布尔值仅用小写 true/false；整数不用小数；>=1 表示无代码硬上限，仍受资源/期限约束。
# 初始候选=NUM_QUERIES×HYPOTHESES_PER_QUERY；TOP_N=1..5；standard 执行全部 Top N。
# 4候选/Top2/逐个执行：NUM_QUERIES=2，HYPOTHESES_PER_QUERY=2，TOP_N=2，PARALLEL_INVESTIGATIONS=1。
# --smoke 为固定诊断预设，会覆盖数量/并发/批数/预算/时限；自定义参数时不要附加它。
# --resume 沿用原科学/模型/部署配置；所有模型请求统一不发送采样参数。
# 合并后候选不足 TOP_N 会报错，不补造假设；1 批内一项调查仍可提交多个计算作业。
# 固定接口：新任务 hypothesis_output_layout=isolated_v2，旧任务沿用冻结协议；resume_protocol=arche-checkpoint-v1。
# 追加 --dry-run 仅检查配置；--check 检查部署；均不调用模型、不启动付费科学评估。
# ARCHE_EVAL_API_KEY 为私有凭据字符串，也可通过 ENV_FILE 提供；私有文件只放凭据，勿覆盖流程变量。

set -a
# ---- 任务、模型、凭据 ----
# 任务 ID：一个 paper_<ID> 或逗号分隔多个；必须存在于 TASKS_ROOT/final_verified_autonomous_research，顺序执行。
ARCHE_EVAL_PAPERS="${ARCHE_EVAL_PAPERS:-paper_72f60526b64ce1b6}"
# 任务库根目录路径，包含 final_verified_autonomous_research；建议绝对路径。
ARCHE_EVAL_TASKS_ROOT="${ARCHE_EVAL_TASKS_ROOT:-$PROJECT_ROOT/tasks}"
# 非空模型名；所有生成角色、调查和 Review 使用该模型，judge 默认跟随。
ARCHE_EVAL_MODEL="${ARCHE_EVAL_MODEL:-deepseek-v4.1-flash}"
# HTTP(S) API 根地址；无账号密码/query/fragment；本入口需自行包含 /v1 等 API 前缀。
ARCHE_EVAL_BASE_URL="${ARCHE_EVAL_BASE_URL:-https://apicz.boyuerichdata.com/v1}"
# 私有凭据文件路径；存在时须属当前用户且权限 0600；勿在本脚本明文写密钥。
ARCHE_EVAL_ENV_FILE="${ARCHE_EVAL_ENV_FILE:-$PROJECT_ROOT/custom_agents/Arche-Harness/benchmark_adapter/deepseek_flash.local.env}"
# 密钥变量：ARCHE_EVAL_API_KEY；未设置时使用私有文件中的 ARCHE_CHEM_API_KEY。
# default=不发送推理强度，使用模型默认值；none=显式关闭思考，二者不同。
# 其余枚举 minimal|low|medium|high|xhigh|max；供应商与模型也须支持所选值。
ARCHE_EVAL_REASONING="${ARCHE_EVAL_REASONING:-high}"
# 枚举 agent_a1|codex；原生假设生成路由，沿用统一 MODEL/API。
ARCHE_EVAL_HYPOTHESIS_PROVIDER="${ARCHE_EVAL_HYPOTHESIS_PROVIDER:-agent_a1}"
# 布尔 true|false；模型 HTTP/2；当前 GPT 网关使用 false，其他端点按实际支持设置。
ARCHE_EVAL_HTTP2="${ARCHE_EVAL_HTTP2:-true}"
# 布尔 true|false；true 请求 Responses JSON-object，false 保留原生 schema；均继续校验输出。
ARCHE_EVAL_JSON_OBJECT="${ARCHE_EVAL_JSON_OBJECT:-true}"
# 所有模型统一省略 temperature、top_p 等采样参数，使用供应商默认值；无需开关。
# 整数秒 >=1；单模型请求读等待上限，仍受 TIMEOUT 限制。
ARCHE_EVAL_MODEL_TIMEOUT="${ARCHE_EVAL_MODEL_TIMEOUT:-1800}"
# 布尔 true|false；完成规范提交后是否正式评分，true 会调用评分模型。
ARCHE_EVAL_JUDGE_ENABLED="${ARCHE_EVAL_JUDGE_ENABLED:-true}"
# 空=跟随 MODEL；或独立评分模型名；仅新任务生效。
ARCHE_EVAL_JUDGE_MODEL="${ARCHE_EVAL_JUDGE_MODEL:-}"
# 空=跟随 BASE_URL；独立评分端点需包含 /v1 等前缀。
ARCHE_EVAL_JUDGE_BASE_URL="${ARCHE_EVAL_JUDGE_BASE_URL:-}"
# 可选私有变量 ARCHE_EVAL_JUDGE_API_KEY；未设置时沿用 ARCHE_EVAL_API_KEY，不写入配置快照。
# 空=跟随 REASONING；或同一枚举，供独立 judge 保留自己的推理配置。
ARCHE_EVAL_JUDGE_REASONING="${ARCHE_EVAL_JUDGE_REASONING:-}"
# 枚举 responses|chat_completions；须与供应商评分 API 匹配。
ARCHE_EVAL_JUDGE_WIRE_API="${ARCHE_EVAL_JUDGE_WIRE_API:-responses}"
# 整数秒 >=1；每次 judge 请求超时。
ARCHE_EVAL_JUDGE_TIMEOUT="${ARCHE_EVAL_JUDGE_TIMEOUT:-300}"
# 枚举 compact_v1|legacy；推荐 compact_v1，复用 benchmark 紧凑返回、分页和按需读取。
ARCHE_EVAL_TOOL_RESPONSE_PROFILE="${ARCHE_EVAL_TOOL_RESPONSE_PROFILE:-compact_v1}"
# 空=新运行；或本版外层 paper_<ID>_<时间>_<标识> 目录；恢复沿用原冻结科学配置。
ARCHE_EVAL_RESUME_DIR="${ARCHE_EVAL_RESUME_DIR:-}"
# 原完整主机名；仅跨主机 resume 使用，表示操作者已确认旧实例停止。
ARCHE_EVAL_MIGRATE_FROM_HOST="${ARCHE_EVAL_MIGRATE_FROM_HOST:-}"
# 整数 >=0；仅 resume 生效，增加累计调用额度上限；0 不追加，不清零历史消耗。
ARCHE_EVAL_EXTRA_CALLS="${ARCHE_EVAL_EXTRA_CALLS:-0}"
# 空=沿用旧期限；或整数秒 >=1，指定从 resume 开始的新窗口；延时要求原作业/管理器已结束。
ARCHE_EVAL_RESUME_TIMEOUT="${ARCHE_EVAL_RESUME_TIMEOUT:-}"
# Judge 使用 benchmark 原生评分器：新评分不设置请求次数/累计用量配额，
# 不额外指定单请求输出 token 上限；证据按页读取，所有实际用量继续记录。

# ---- 原生科学流程 ----
# 枚举 standard|smoke；standard 执行全部 Top N；smoke 只调查第 1 项且附加简化计算指导。
ARCHE_EVAL_PROFILE="${ARCHE_EVAL_PROFILE:-standard}"
# 整数 >=1；研究角度数量；初始候选总数=本值×HYPOTHESES_PER_QUERY。
ARCHE_EVAL_NUM_QUERIES="${ARCHE_EVAL_NUM_QUERIES:-3}"
# 整数 >=1；每角度初始候选数；乘积须 >=TOP_N；原生关系合并后候选可能减少。
ARCHE_EVAL_HYPOTHESES_PER_QUERY="${ARCHE_EVAL_HYPOTHESES_PER_QUERY:-3}"
# 整数 1..5；排序后入选假设数，standard 全部执行；初始和合并后候选均须足够，默认 5，可设 2。
ARCHE_EVAL_TOP_N="${ARCHE_EVAL_TOP_N:-5}"
# 整数 1..5；同时调查的假设数，1=逐个执行；实际最多 TOP_N，不改变调查总数。
ARCHE_EVAL_PARALLEL_INVESTIGATIONS="${ARCHE_EVAL_PARALLEL_INVESTIGATIONS:-5}"
# 整数 >=1；每个假设调查在 Review 后允许的科学返修次数；不限制调查内部计算次数。
ARCHE_EVAL_INVESTIGATION_REPAIRS="${ARCHE_EVAL_INVESTIGATION_REPAIRS:-3}"
# 整数 >=1；包含初始批，只限制生成新假设，不跳过同一假设的 Review/返修；建议保持 1。
ARCHE_EVAL_HYPOTHESIS_BATCHES="${ARCHE_EVAL_HYPOTHESIS_BATCHES:-1}"
# 整数 >=1；按查询生成候选的并发，建议 <=NUM_QUERIES；不改变候选数。
ARCHE_EVAL_GENERATION_WORKERS="${ARCHE_EVAL_GENERATION_WORKERS:-3}"
# 整数 >=1；关系比较/排序并发；本脚本不接受 0/auto；增加可能加重限流。
ARCHE_EVAL_COMPARISON_WORKERS="${ARCHE_EVAL_COMPARISON_WORKERS:-3}"
# 整数 0..6；存活进程内假设生成传输暂停的恢复次数，0=关闭，仍共享额度/期限。
ARCHE_EVAL_TRANSPORT_RESUMES="${ARCHE_EVAL_TRANSPORT_RESUMES:-3}"
# 整数 0|1；每原生阶段格式错误最多重答次数；不自动修复化学计算错误。
ARCHE_EVAL_CONTRACT_REANSWERS="${ARCHE_EVAL_CONTRACT_REANSWERS:-1}"
# 默认关闭；用户显式 true 可覆盖任务禁网说明，来源论文/SI 过滤仍强制执行。
# 布尔 true|false；true 搜索/下载文献并覆盖任务禁网默认，来源论文/SI 仍过滤；false 仅检索公开输入。
ARCHE_EVAL_PAPER_SEARCH="${ARCHE_EVAL_PAPER_SEARCH:-false}"
# Empty preserves legacy PAPER_SEARCH settings; explicit modes override that switch.
ARCHE_EVAL_RETRIEVAL_MODE="${ARCHE_EVAL_RETRIEVAL_MODE:-}"
ARCHE_EVAL_LOCAL_CORPUS_ROOT="${ARCHE_EVAL_LOCAL_CORPUS_ROOT:-}"
# 整数 >=1；去重/过滤后的目标 PDF 数；不是假设数；关闭搜索时无效。
ARCHE_EVAL_PAPER_SEARCH_TARGET="${ARCHE_EVAL_PAPER_SEARCH_TARGET:-50}"
# 整数秒 >=1；单关键词搜索时间上限，非整轮总时长；关闭搜索时无效；resume 沿用原值。
ARCHE_EVAL_PAPER_SEARCH_TIMEOUT="${ARCHE_EVAL_PAPER_SEARCH_TIMEOUT:-600}"

# ---- 宿主科学计算配额与预算 ----
# 整数核 >=1；全部科学作业共享的宿主 CPU 配额，不超过宿主可用 affinity；不是每假设独占核数。
ARCHE_EVAL_CPU_CORES="${ARCHE_EVAL_CPU_CORES:-8}"
# 整数 MiB >=1；同一 run 的宿主计算内存总配额，应 <=宿主可用内存。
ARCHE_EVAL_MEMORY_MB="${ARCHE_EVAL_MEMORY_MB:-32768}"
# 整数 >=0；宿主科学计算 GPU 配额，0=不用 GPU，应 <=可用设备数。
ARCHE_EVAL_GPU_COUNT="${ARCHE_EVAL_GPU_COUNT:-0}"
# 整数 >=1；ARCHE 全角色共享的应计模型调用上限；纯供应商限流不占额度，judge 另计。
ARCHE_EVAL_MAX_CALLS="${ARCHE_EVAL_MAX_CALLS:-2000}"
# null=无 token 阈值；或整数 >=1；按已知输入+输出量限制准入，未知用量单列；不是硬费用上限。
ARCHE_EVAL_MAX_TOKENS="${ARCHE_EVAL_MAX_TOKENS:-null}"
# 整数秒 >=1；单次任务总期限，43200=12 小时；重复任务分别计时，不保证期限内完成。
ARCHE_EVAL_TIMEOUT="${ARCHE_EVAL_TIMEOUT:-43200}"
# 整数秒 >=1；单个科学计算动作超时，仍受 TIMEOUT 限制；GPT 默认 14400=4 小时。
ARCHE_EVAL_COMPUTE_TIMEOUT="${ARCHE_EVAL_COMPUTE_TIMEOUT:-1800}"
# 整数秒 >=1；快速工具动作超时。
ARCHE_EVAL_FAST_TIMEOUT="${ARCHE_EVAL_FAST_TIMEOUT:-60}"
# 整数秒 >=1；MCP 调用超时；建议 >=COMPUTE_TIMEOUT+60，且与 TIMEOUT 相容。
ARCHE_EVAL_MCP_TIMEOUT="${ARCHE_EVAL_MCP_TIMEOUT:-1860}"
# 整数秒 >=1；benchmark 内部等待心跳，adapter 吸收空心跳，不按此周期调用模型。
ARCHE_EVAL_WAIT_HEARTBEAT="${ARCHE_EVAL_WAIT_HEARTBEAT:-120}"
# 整数秒 >=1；作业事件稳定等待窗口，建议 <=EVENT_BATCH。
ARCHE_EVAL_EVENT_SETTLE="${ARCHE_EVAL_EVENT_SETTLE:-1}"
# 整数秒 >=1；作业事件聚合最大等待，建议 >=EVENT_SETTLE。
ARCHE_EVAL_EVENT_BATCH="${ARCHE_EVAL_EVENT_BATCH:-5}"
# 整数 >=1；每项任务独立重复次数，每次新建目录并顺序运行。
ARCHE_EVAL_REPEATS="${ARCHE_EVAL_REPEATS:-1}"
# 整数 GiB >=1；正式启动前最小剩余磁盘空间；计算/归档可能需要更多空间。
ARCHE_EVAL_MIN_FREE_GIB="${ARCHE_EVAL_MIN_FREE_GIB:-100}"

# ---- 输出、解释器与本地模型 ----
# 可写目录路径；在其下创建 paper_*；禁止指向受保护的 workspaces/codex_gpt56。
ARCHE_EVAL_OUTPUT_ROOT="${ARCHE_EVAL_OUTPUT_ROOT:-$PROJECT_ROOT/workspaces/arche_eval}"
# 预检目录及旧部署的兼容路径；正式新任务自动使用各自结果目录/.runtime，不共用此部署目录。
ARCHE_EVAL_STATE_DIR="${ARCHE_EVAL_STATE_DIR:-$ARCHE_EVAL_OUTPUT_ROOT/.runtime}"
# 已有任务结果目录；仅管理 status/cancel/down/up/check 时选择目标，不启动新的科学评估。
ARCHE_EVAL_RUN_DIR="${ARCHE_EVAL_RUN_DIR:-}"
# 可执行文件路径；现有 benchmark Python，复用共享环境，不重新安装。
ARCHE_EVAL_FRAMEWORK_PYTHON="${ARCHE_EVAL_FRAMEWORK_PYTHON:-$PROJECT_ROOT/.envs/researchchembench/bin/python}"
# 可执行文件路径；现有 ARCHE 协调器 Python，宿主和 guest 中须可达相同路径。
ARCHE_EVAL_CLIENT_PYTHON="${ARCHE_EVAL_CLIENT_PYTHON:-$PROJECT_ROOT/.envs/arche-client/bin/python}"
# 可执行文件路径；BGE 服务 Python，须包含现有嵌入依赖。
ARCHE_EVAL_EMBEDDING_PYTHON="${ARCHE_EVAL_EMBEDDING_PYTHON:-$PROJECT_ROOT/.envs/arche-benchmark/bin/python}"
# 现有 BGE-M3 模型目录路径；共享存储直接复用，不填写在线模型 API。
ARCHE_EVAL_BGE_MODEL="${ARCHE_EVAL_BGE_MODEL:-/inspire/hdd/global_user/lifangyuan-253108110077/Models/bge-m3}"
# 现有原生 Codex runtime 缓存目录路径；仍执行原生完整性检查。
ARCHE_EVAL_RUNTIME_CACHE="${ARCHE_EVAL_RUNTIME_CACHE:-$PROJECT_ROOT/workspaces/arche_e2e_20260928/uml/probe/codex_runtime}"
# 整数秒 >=1；原生部署预检超时，不是科学作业时限。
ARCHE_EVAL_PREFLIGHT_TIMEOUT="${ARCHE_EVAL_PREFLIGHT_TIMEOUT:-600}"

# ---- 部署：每次新评估独占 QEMU/SSH/BGE；旧任务恢复时仍使用保存的部署配置 ----
# 枚举 managed|auto|existing；新任务 managed/auto 均独立自建，existing 仅兼容旧任务恢复。
ARCHE_EVAL_DEPLOYMENT="${ARCHE_EVAL_DEPLOYMENT:-managed}"
# 共享根目录路径；须覆盖项目、Python 环境、BGE 等 guest/宿主共用文件。
ARCHE_EVAL_SHARED_ROOT="${ARCHE_EVAL_SHARED_ROOT:-/inspire/hdd/global_user/lifangyuan-253108110077}"
# 已解包 Linux 内核目录路径；自建部署时使用。
ARCHE_EVAL_KERNEL_ROOT="${ARCHE_EVAL_KERNEL_ROOT:-$PROJECT_ROOT/workspaces/arche_e2e_20260929/qemu/kernel}"
# 内核版本字符串；必须与 KERNEL_ROOT 内已有内核匹配。
ARCHE_EVAL_KERNEL_VERSION="${ARCHE_EVAL_KERNEL_VERSION:-6.8.0-101-generic}"
# 现有 qemu-system-x86_64 可执行文件路径；科学计算仍使用宿主环境。
ARCHE_EVAL_QEMU_BIN="${ARCHE_EVAL_QEMU_BIN:-/usr/bin/qemu-system-x86_64}"
# 现有 virtiofsd 可执行文件路径；用于自建共享文件系统。
ARCHE_EVAL_VIRTIOFSD_BIN="${ARCHE_EVAL_VIRTIOFSD_BIN:-/usr/lib/qemu/virtiofsd}"
# 布尔 true|false；自建部署的 CPU affinity 兼容处理。
ARCHE_EVAL_AFFINITY_COMPAT="${ARCHE_EVAL_AFFINITY_COMPAT:-true}"
# 整数 >=1；协调器 guest vCPU 数，建议 <=宿主可用核数；科学作业由 CPU_CORES 控制。
ARCHE_EVAL_GUEST_CPUS="${ARCHE_EVAL_GUEST_CPUS:-4}"
# 整数 MiB >=1；协调器 guest 内存，自建时生效，不替代宿主 MEMORY_MB 配额。
ARCHE_EVAL_GUEST_MEMORY_MB="${ARCHE_EVAL_GUEST_MEMORY_MB:-8192}"
# 0=自动分配，或整数 1024..65535；宿主 SSH 端口；实际值保存在任务目录，恢复时复用。
ARCHE_EVAL_HOST_SSH_PORT="${ARCHE_EVAL_HOST_SSH_PORT:-0}"
# 0=自动分配，或整数 1024..65535；guest SSH 映射端口；手工设置的端口须互不相同且空闲。
ARCHE_EVAL_GUEST_SSH_PORT="${ARCHE_EVAL_GUEST_SSH_PORT:-0}"
# 0=自动分配，或整数 1024..65535；本任务 BGE 服务端口。
ARCHE_EVAL_BGE_PORT="${ARCHE_EVAL_BGE_PORT:-0}"
# 0=自动分配，或整数 1024..65535；本任务 guest 内模型出口 SOCKS 端口。
ARCHE_EVAL_SOCKS_PORT="${ARCHE_EVAL_SOCKS_PORT:-0}"
# 整数秒 >=1；每个部署启动就绪检查的超时。
ARCHE_EVAL_STARTUP_TIMEOUT="${ARCHE_EVAL_STARTUP_TIMEOUT:-600}"

# 当前节点已有、经验证的部署。只有身份与健康检查通过才复用；不停止借用的服务。
# 已有部署目录路径；auto/existing 用于读取进程身份；不关闭借用服务。
ARCHE_EVAL_EXISTING_DIR="${ARCHE_EVAL_EXISTING_DIR:-$PROJECT_ROOT/workspaces/arche_e2e_20260929}"
# 已有 guest SSH 传输 JSON 文件路径；共享路径、端口和固定主机密钥须匹配部署。
ARCHE_EVAL_EXISTING_GUEST_TRANSPORT="${ARCHE_EVAL_EXISTING_GUEST_TRANSPORT:-$ARCHE_EVAL_EXISTING_DIR/qemu/virtiofs_transport.json}"
# 已有宿主 MCP SSH 传输 JSON 文件路径；须匹配实际执行宿主。
ARCHE_EVAL_EXISTING_HOST_TRANSPORT="${ARCHE_EVAL_EXISTING_HOST_TRANSPORT:-$ARCHE_EVAL_EXISTING_DIR/hybrid/host_transport.json}"
# guest 可达的 BGE HTTP(S) URL；已有部署生效，须与服务地址一致。
ARCHE_EVAL_EXISTING_BGE_URL="${ARCHE_EVAL_EXISTING_BGE_URL:-http://10.0.2.2:18766}"
# 宿主可达的 BGE HTTP(S) URL；用于已有部署健康检查。
ARCHE_EVAL_EXISTING_BGE_HOST_URL="${ARCHE_EVAL_EXISTING_BGE_HOST_URL:-http://127.0.0.1:18766}"
# 已有 BGE capability 文件路径；不将令牌写入命令或公共配置。
ARCHE_EVAL_EXISTING_BGE_TOKEN_FILE="${ARCHE_EVAL_EXISTING_BGE_TOKEN_FILE:-$PROJECT_ROOT/workspaces/arche_e2e_20260928/embedding.token}"
# guest 可达的 SOCKS URL；当前网关要求无凭据的 socks5/socks5h loopback 地址与端口。
ARCHE_EVAL_EXISTING_PROXY_URL="${ARCHE_EVAL_EXISTING_PROXY_URL:-socks5h://127.0.0.1:18770}"
set +a

ACTION=run
while (($#)); do
  case "$1" in
    --dry-run) ACTION=dry-run; shift ;;
    --check) ACTION=check; shift ;;
    --status) ACTION=status; shift ;;
    --cancel) ACTION=cancel; shift ;;
    --up) ACTION=up; shift ;;
    --down) ACTION=down; shift ;;
    --paper|--model|--judge-model|--deployment|--resume|--run-dir|--extra-calls|--resume-timeout|--migrate-from-host)
      [[ $# -ge 2 && -n "$2" ]] || { echo "$1 需要参数" >&2; exit 2; }
      case "$1" in
        --paper) export ARCHE_EVAL_PAPERS="$2" ;;
        --model) export ARCHE_EVAL_MODEL="$2" ;;
        --judge-model) export ARCHE_EVAL_JUDGE_MODEL="$2" ;;
        --deployment) export ARCHE_EVAL_DEPLOYMENT="$2" ;;
        --resume) export ARCHE_EVAL_RESUME_DIR="$2" ;;
        --migrate-from-host) export ARCHE_EVAL_MIGRATE_FROM_HOST="$2" ;;
        --run-dir) export ARCHE_EVAL_RUN_DIR="$2" ;;
        --extra-calls) export ARCHE_EVAL_EXTRA_CALLS="$2" ;;
        --resume-timeout) export ARCHE_EVAL_RESUME_TIMEOUT="$2" ;;
      esac
      shift 2 ;;
    --no-score) export ARCHE_EVAL_JUDGE_ENABLED=false; shift ;;
    --paper-search) export ARCHE_EVAL_PAPER_SEARCH=true; shift ;;
    --no-paper-search) export ARCHE_EVAL_PAPER_SEARCH=false; shift ;;
    --smoke)
      export ARCHE_EVAL_PROFILE=smoke
      export ARCHE_EVAL_NUM_QUERIES=1 ARCHE_EVAL_HYPOTHESES_PER_QUERY=5
      export ARCHE_EVAL_TOP_N=5 ARCHE_EVAL_PARALLEL_INVESTIGATIONS=1
      export ARCHE_EVAL_HYPOTHESIS_BATCHES=1
      export ARCHE_EVAL_COMPUTE_TIMEOUT=1200 ARCHE_EVAL_MCP_TIMEOUT=1260
      export ARCHE_EVAL_TIMEOUT=3600 ARCHE_EVAL_MAX_CALLS=400
      shift ;;
    -h|--help)
      cat <<'EOF'
用法：bash scripts/run_arche_eval.sh [选项]
  无选项         预检后启动一次真实评估；默认包括正式 judge（会调用付费模型）。
  --dry-run      在 .runtime/preflight 下生成配置并预检；不启动服务或调用模型。
  --check        创建独立部署并检查沙箱/BGE/宿主连接，完成后关闭；不调用模型。
  --status       查看现有 ARCHE 运行及结果路径；不启动新评估。
  --cancel       取消 --run-dir 指定的运行；不指定时要求只有一个活跃运行。
  --up           启动并验证独立部署，保持运行；可配合 --run-dir 复用该任务的部署。
  --down         关闭 --run-dir 指定任务的闲置部署，不影响其他任务。
  --run-dir DIR  指定已有任务结果目录，用于 status/cancel/down/up/check。
  --paper ID     指定 final_verified 任务；逗号分隔多个任务，逐项创建 paper_<ID>_<时间>_<标识> 目录并顺序执行。
  --model NAME   所有 Agent 角色使用该模型，judge 默认跟随。
  --judge-model NAME 新任务独立指定评分模型；API、凭据和推理强度沿用 Agent 配置。
  --deployment auto|managed|existing
  --no-score     明确跳过评分；默认会评分。
  --paper-search 用户显式启用原生 Scholar 搜索/下载，覆盖任务禁网默认；来源论文/SI 仍强制排除。
  --no-paper-search 关闭外部论文搜索（默认）；仍检索公开输入。
  --smoke        简化诊断：每批5候选中只执行第1项；单计算20分钟、总计1小时、400请求；终态提交后评分。
  --resume DIR   从支持 arche-checkpoint-v1 的原任务目录恢复；--check 只检查保存状态。
  --migrate-from-host HOST 旧实例已停止时，迁移终态任务到当前主机；保留检查点和作业记录。
  --extra-calls N 恢复时增加 N 次应计调用额度，历史用量不清零。
  --resume-timeout SEC 恢复开始后的新时间窗口；原期限过期时显式指定。

参数集中在脚本顶部；也可用同名 ARCHE_EVAL_* 环境变量覆盖。
ARCHE_EVAL_RETRIEVAL_MODE=local|online|off 显式选择文献来源；local 同时设置 ARCHE_EVAL_LOCAL_CORPUS_ROOT。
未设置新模式时兼容 PAPER_SEARCH；resume 始终沿用原运行的文献配置。
每次新评估的部署位于结果目录/.runtime/deployment；不同终端/服务器可同时启动不同评估。
新运行结束后自动关闭本任务部署，文件保留；跨主机 resume 须显式迁移并通过终态和锁检查。
密钥：ARCHE_EVAL_API_KEY 或私有 ARCHE_EVAL_ENV_FILE 中的 ARCHE_CHEM_API_KEY。
旧版本缺少恢复检查点的运行会明确报错，不会自动清空账本或重新计算。
详细说明：scripts/run_arche_eval.md
EOF
      exit 0 ;;
    *) echo "未知参数：$1；使用 --help 查看帮助" >&2; exit 2 ;;
  esac
done

[[ -x "$ARCHE_EVAL_FRAMEWORK_PYTHON" ]] || { echo "缺少 benchmark Python：$ARCHE_EVAL_FRAMEWORK_PYTHON" >&2; exit 2; }
if [[ "$ACTION" == run || "$ACTION" == check || "$ACTION" == up ]]; then
  if [[ -f "$ARCHE_EVAL_ENV_FILE" ]]; then
    "$ARCHE_EVAL_FRAMEWORK_PYTHON" -c 'import os,sys; from pathlib import Path; s=Path(sys.argv[1]).stat(); sys.exit(0 if s.st_uid==os.getuid() and not s.st_mode & 0o077 else "凭据文件须为当前用户所有且权限0600")' "$ARCHE_EVAL_ENV_FILE"
    set -a
    # shellcheck disable=SC1090
    source "$ARCHE_EVAL_ENV_FILE"
    set +a
  fi
  export ARCHE_EVAL_API_KEY="${ARCHE_EVAL_API_KEY:-${ARCHE_CHEM_API_KEY:-}}"
fi
exec "$ARCHE_EVAL_FRAMEWORK_PYTHON" "$PROJECT_ROOT/custom_agents/Arche-Harness/benchmark_adapter/deploy/launch_evaluation.py" "$ACTION"
