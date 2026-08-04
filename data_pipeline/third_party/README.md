# Third-Party Runtime Sources

`third_party/` 用于保存数据管线运行所需的固定版本第三方源码。实际 checkout 已被父仓库 `.gitignore` 排除，不直接提交到 ResearchChemBench；GitHub 仓库只保存本说明、bootstrap 脚本、固定版本和兼容补丁。

| 本地目录 | 上游仓库 | 固定版本 | 阶段 |
|---|---|---|---|
| `grobid/` | https://github.com/grobidOrg/grobid | tag `0.9.0` | Stage 02 |
| `software-mentions/` | https://github.com/softcite/software-mentions | `c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a` | Stage 03 |
| `delft/` | https://github.com/kermitt2/delft | `d8505592c38058b9b0abbde14d4ddedff3ad7d0f` | Stage 03 |
| `grobid-quantities/` | https://github.com/lfoppiano/grobid-quantities | `d0d55592f4d0ddbe6a549e06613349adaa2d1cd7` | Stage 04 |
| `MinerU/` | https://github.com/opendatalab/MinerU | `79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7` | Stage 05 |

## 推荐下载方式

在 `data_pipeline/` 根目录、激活 `researchchem-data-pipeline` Conda 环境后执行：

```bash
export HF_ENDPOINT=https://hf-mirror.com
bash scripts/bootstrap_all.sh
```

分步执行：

```bash
bash scripts/bootstrap_grobid.sh
bash scripts/bootstrap_stage_gates.sh
bash scripts/bootstrap_mineru.sh
```

脚本负责：

- clone 并 checkout 固定版本；
- 应用 `scripts/patches/` 中的兼容补丁；
- 构建 GROBID、Softcite 和 GROBID Quantities；
- 将 DeLFT、JEP 和 MinerU 安装到当前 Conda 环境；
- 下载 Softcite BERT 与 MinerU 模型；
- 将运行模型和相对路径配置写入 `.model_cache/`。

## 手工 clone

```bash
git clone --branch 0.9.0 --depth 1 \
  https://github.com/grobidOrg/grobid.git third_party/grobid

git clone https://github.com/softcite/software-mentions.git third_party/software-mentions
git -C third_party/software-mentions checkout c7c83852a3cad8f2d9d07ce3de6fbe852e23c19a

git clone https://github.com/kermitt2/delft.git third_party/delft
git -C third_party/delft checkout d8505592c38058b9b0abbde14d4ddedff3ad7d0f

git clone https://github.com/lfoppiano/grobid-quantities.git third_party/grobid-quantities
git -C third_party/grobid-quantities checkout d0d55592f4d0ddbe6a549e06613349adaa2d1cd7

git clone https://github.com/opendatalab/MinerU.git third_party/MinerU
git -C third_party/MinerU checkout 79d6d8d79fb8f3ddba5cc34c07a16f0ec36f56c7
```

手工 clone 后仍应运行对应 bootstrap 脚本，以应用补丁、安装依赖、构建服务并准备模型。

## 模型与研究资产边界

第三方运行模型统一位于 `.model_cache/`。执行：

```bash
python scripts/prepare_model_cache.py
```

可重新生成 Java 服务和 MinerU 使用的相对路径配置。

Stage 05 下载的论文补充材料、数据和代码是研究资产，不是运行时依赖。它们保存在每次 `runs/<run>/outputs/stage_05_asset_collection/` 的内容寻址目录中，不写入 `third_party/`。

使用或重新分发第三方源码、二进制和模型前，应分别检查各上游项目的许可证。
