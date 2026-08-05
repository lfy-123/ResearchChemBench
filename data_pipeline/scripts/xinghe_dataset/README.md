# Xinghe 数据集读取说明

本目录提供 Xinghe/Petrel 对象存储的只读访问工具。凭证不会写入代码；
`read_xinghe_dataset.py` 会读取 `xinghe.txt`，生成临时 Petrel 配置，并在退出时删除。

## 当前授权的数据集

凭证允许读取以下五个 S3 前缀：

1. ACS 网页抓取压缩数据

   ```text
   s3://crawl-data/www_acs_org/gz_file/1734329655/
   ```

2. 英文论文数据集 `en-paper-hzzj`

   ```text
   s3://private-cooperate-data/en-paper-hzzj/
   ```

   PDF 位于：

   ```text
   s3://private-cooperate-data/en-paper-hzzj/pdf/
   ```

3. KPS 数据集 `20260603_bu` 版本

   ```text
   s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/
   ```

4. KPS 数据集 `2026-06-18` 版本

   ```text
   s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/
   ```

5. KPS 数据集 `2026-05-07` 版本

   ```text
   s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/
   ```

## 1. 激活环境

```bash
source /mnt/shared-storage-user/liyuqiang/anaconda3/etc/profile.d/conda.sh
conda activate /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline/.envs/researchchem-data-pipeline
cd /mnt/shared-storage-user/liyuqiang/benchmark/ResearchChemBench/data_pipeline
```

设置凭证路径，后面的命令可以直接复用该环境变量：

```bash
export XINGHE_CREDENTIALS=/mnt/shared-storage-user/liyuqiang/benchmark/pipline_demo/pdfs/xinghe.txt
```

## 2. 查看授权数据集

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  datasets
```

## 3. 列出数据对象

列出 `en-paper-hzzj` 的前 20 篇 PDF：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  list 's3://private-cooperate-data/en-paper-hzzj/pdf/' \
  --limit 20
```

递归列出 KPS 数据集的前 20 个对象：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  list 's3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/' \
  --recursive \
  --limit 20
```

`--limit` 用于防止误列举整个大型数据集。

## 4. 检查并下载文件

检查对象是否存在：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  contains 's3://private-cooperate-data/en-paper-hzzj/pdf/10.1002_anie.202310798.pdf'
```

查看对象大小，输出单位为字节：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  size 's3://private-cooperate-data/en-paper-hzzj/pdf/10.1002_anie.202310798.pdf'
```

下载 PDF：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  download \
  's3://private-cooperate-data/en-paper-hzzj/pdf/10.1002_anie.202310798.pdf' \
  data/xinghe/10.1002_anie.202310798.pdf
```

目标文件已经存在时，需要明确允许覆盖：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  download \
  's3://private-cooperate-data/en-paper-hzzj/pdf/10.1002_anie.202310798.pdf' \
  data/xinghe/10.1002_anie.202310798.pdf \
  --overwrite
```

## 5. 在 Python 代码中调用

完整示例见 `example_python.py`。从当前目录执行：

```bash
python scripts/xinghe_dataset/example_python.py
```

## 6. 实验室网络外访问

在子命令前增加 `--outside`：

```bash
python scripts/xinghe_dataset/read_xinghe_dataset.py \
  --credentials "$XINGHE_CREDENTIALS" \
  --outside \
  list 's3://private-cooperate-data/en-paper-hzzj/pdf/' \
  --limit 20
```

只允许访问 `xinghe.txt` 中列出的前缀，不能从 bucket 根目录开始列举。

## 7. 按批次下载并避免重复

批量下载脚本会在每个输出目录中维护两个文件：

- `download_manifest.jsonl`：已经成功下载的完整 S3 URI 清单；
- `.download_state.json`：上一次扫描到的对象位置。

后续批次必须继续使用同一个输出目录。脚本会从上次位置继续，并根据清单跳过
已经存在的论文，因此不会反复下载前一批文件。

如果下载文件所在目录是一次性工作区，可通过 `--state-directory` 把游标、清单和锁保存在
另一个持久目录中。`run_stage_01_04_batches.py` 使用这种方式：每批 PDF 可以在筛选完成后
删除，但下一批仍会从上一次远端对象之后继续。

```bash
bash scripts/xinghe_dataset/download_xinghe_batch.sh \
  --dataset en-paper-hzzj \
  --count 1000 \
  --output runs/current_batch/input \
  --state-directory runs/download_state
```

`--count` 表示本次需要新增下载的文件数。输出目录中原本已有但尚未登记的 PDF 会
自动写入清单并跳过，不计入本次新增数量。请保留 `download_manifest.jsonl` 和
`.download_state.json`；如果本地 PDF 被误删，脚本再次遇到该对象时会重新下载。

查看可用的数据集别名：

```bash
bash scripts/xinghe_dataset/download_xinghe_batch.sh \
  --list-datasets
```

从 `en-paper-hzzj` 下载下一批 100 篇：

```bash
bash scripts/xinghe_dataset/download_xinghe_batch.sh \
  --dataset en-paper-hzzj \
  --count 100
```

默认保存到：

```text
datasets/xinghe/en-paper-hzzj/
```

再次执行相同命令会继续下载后面的 100 篇：

```bash
bash scripts/xinghe_dataset/download_xinghe_batch.sh \
  --dataset en-paper-hzzj \
  --count 100
```

下载指定 KPS 数据集：

```bash
bash scripts/xinghe_dataset/download_xinghe_batch.sh \
  --dataset kps-2026-05-07 \
  --count 1000
```

指定输出目录：

```bash
bash scripts/xinghe_dataset/download_xinghe_batch.sh \
  --dataset kps-2026-06-18 \
  --count 200 \
  --output datasets/xinghe/my_kps_batch
```

实验室网络外增加 `--outside`。同一数据集不要在不同批次间更换输出目录，否则新的
目录没有之前的下载清单，无法判断其他目录中已经下载过哪些论文。
