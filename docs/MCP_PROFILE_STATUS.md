# MCP 分环境安装与检查状态

- 生成时间：2026-07-18T08:12:22.428751+00:00
- MCP profiles：12
- 必需检查通过：12
- 工具总数：41
- Materials Project key：已配置
- Materials Project live smoke：not_requested
- 模型功能检查：3/3 passed
- 项目模型缓存：`/inspire/hdd/global_user/lifangyuan-253108110077/lifangyuan/benchmark/ResearchChemBench/.model_cache`

## MCP profiles

| Profile | Conda environment | MCP server | Tools | Required checks | Detail |
|---|---|---|---:|---|---|
| `core` | `researchchem-core` | `researchchem_core` | 12 | 通过 | ready |
| `services` | `researchchem-services` | `researchchem_services` | 4 | 通过 | ready |
| `quantum` | `researchchem-quantum` | `researchchem_quantum` | 4 | 通过 | ready; manual: orca |
| `psi4` | `researchchem-psi4` | `researchchem_psi4` | 1 | 通过 | ready |
| `reaction` | `researchchem-reaction` | `researchchem_reaction` | 8 | 通过 | ready; manual: orca |
| `qe` | `researchchem-qe` | `researchchem_qe` | 1 | 通过 | ready |
| `cp2k` | `researchchem-cp2k` | `researchchem_cp2k` | 1 | 通过 | ready |
| `periodic` | `researchchem-periodic` | `researchchem_periodic` | 1 | 通过 | ready |
| `phonons` | `researchchem-phonons` | `researchchem_phonons` | 1 | 通过 | ready |
| `md` | `researchchem-md` | `researchchem_md` | 6 | 通过 | ready |
| `mlip` | `researchchem-mlip` | `researchchem_mlip` | 1 | 通过 | ready |
| `docking` | `researchchem-docking` | `researchchem_docking` | 1 | 通过 | ready; manual: gnina |

## 仅可执行程序环境

| Environment | Conda environment | Check | Commands |
|---|---|---|---|
| `abinit` | `researchchem-abinit` | 通过 | abinit |

## 说明

- `manual: orca` 与 `manual: gnina` 不影响对应 profile 的基础可用性；它们需要人工接受许可/下载二进制。
- 周期计算拆成 QE、CP2K、DFTB+/SIESTA 调度、ABINIT 支撑环境和 Phonopy 环境，避免求解器互相降级。
- NequIP、DeepMD、FAIRChem、AIMNet2 尚无完成的模型加载 adapter，因此没有作为 `run_mlip` 的必需依赖安装。
- 每个 profile 和支撑环境都执行独立的 `pip check`；依赖冲突会使必需检查失败。
- 该报告不会记录或输出 API key 的具体值。
