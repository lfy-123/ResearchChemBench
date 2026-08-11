# 数据管线 GPU Worker 启动规范

## 推荐的手动启动命令

不限定 GPU 型号、以较小的主机内存请求启动一个通用 worker：

```bash
rlaunch \
  --gpu=1 \
  --cpu=16 \
  --memory=16000 \
  --charged-group=ai4chem_gpu \
  --private-machine=group \
  --mount=gpfs://gpfs1/liyuqiang:/mnt/shared-storage-user/liyuqiang \
  -- bash
```

不要默认添加 `--positive-tags=h200`。只有任务明确要求 H200，且确认集群有空闲 H200 时才添加；
GPU 型号限制与大内存请求会显著缩小可调度节点范围。

## 数据管线自动创建

`scripts/stage03_llm/manage_rlaunch_worker.sh` 使用相同资源基线，并额外使用：

- `-d`：后台提交；
- `--worker-garbage-collection-time=24h`：限制 worker 生命周期；
- `-w <data_pipeline>`：设置共享存储中的工作目录；
- `sleep infinity`：保持 worker 存活，服务由管理脚本通过 SSH 部署。

默认参数是 1 GPU、16 CPU、16000 MiB 主机内存、无 GPU 型号标签。一个任务只创建一个
worker；SSH 或服务启动失败时任务退出，不会创建替代 worker。

## 复用已运行的 Worker

优先复用已经成功调度并可 SSH 的 worker：

```bash
bash scripts/workflows/run_stage00_04_batches.sh \
  --run-root runs/stage00-04-batches-10000 \
  --total 10000 \
  --batch-size 1000 \
  --initial-delay-hours 0 \
  --existing-worker 'ws-...liyuqiang+root.ailab-ai4chem.pod@h.pjlab.org.cn'
```

此模式不会调用 `rlaunch`。任务结束时只停止 Qwen/MinerU 服务和本地 SSH 隧道，不会停止
外部 worker。

提交前应先验证：

```bash
ssh -CAXY -o BatchMode=yes -o ConnectTimeout=15 '<完整 worker SSH 地址>' \
  'hostname; nproc; free -h; ls -l /dev/nvidia*'
```

## MinerU 并发与主机内存

GPU 显存充足不代表主机内存充足。当前 MinerU API 的每个并发请求会启动独立处理进程，实测
单进程峰值约 13.5 GB 主机内存。因此：

- 16000 MiB worker：`--stage04-concurrency 1`；
- 96 GiB worker：建议不超过 4；
- 196000 MiB worker：建议不超过 8。

需要 Stage04 高并发时，应显式增加 `--worker-memory-mib`，并接受更长的资源排队时间；不能在
16 GB worker 上使用 8 路 MinerU 并发。

## 常见失败判断

- rlaunch 很快返回 worker 名称但 SSH 长时间不通：worker 仍在调度队列，并非部署脚本卡死。
- 日志出现“资源不足，无可用机器”：减少内存或移除不必要的 `positive-tags`。
- SSH 正常但服务启动失败：检查共享 Conda 环境、模型缓存及 GPU 设备，不要申请第二个 worker。
- 使用外部 worker 时状态文件的 `worker_ownership` 必须为 `external`。
