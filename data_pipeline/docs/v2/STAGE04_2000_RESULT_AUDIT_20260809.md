# Stage04 旧 2000 篇结果复核

日期：2026-08-09

## 1. 范围与阶段编号

复核对象为 `runs/v2_shadow_2000_stage04_05_rerun_20260809` 的 76 篇候选。该历史目录生成于阶段重排
之前，因此其中 `stage_04_toolbox_resource_gate` 同时包含软件/资源筛选和 MinerU 深解析。按当前
`v2.1-split-normalization` 布局解释：

- 历史 Stage04 的软件清单、工具箱映射和资源信息对应当前 Stage03；
- 历史 Stage04 的 MinerU 结果对应当前 Stage04；
- 当前 Stage04 本身不再做科学筛选，只检查深解析是否成功且质量达标。

能力快照 hash 为
`2f8e8e58b6d7054833558715dbf7bde374ddc860d4423a094a1fd45248ac0103`，与当前数据管线资产一致，
因此本次复核不存在“用新工具箱范围解释旧结果”的口径漂移。

## 2. 原始结果

| 决策 | 数量 | 当前含义 |
| --- | ---: | --- |
| `core_software_uncovered` | 44 | 必要软件映射不到工具箱 |
| `software_inventory_unconfirmed` | 14 | 软件清单不完整，保守 hold |
| `software_covered` | 16 | 软件门控通过且 MinerU 成功 |
| `deep_parse_failed` | 1 | 软件门控通过，但 MinerU 失败 |
| `processing_failed` | 1 | Qwen 上下文超限 |

软件门控实际通过 17/76；MinerU 成功 16/17。失败论文
`paper_b975183360fa593f` 的 SI 为 337 页，CPU MinerU 在 3600 秒超时。这是可重试的基础设施失败，
不是科学筛选结论。

## 3. 确定性检查

最终门控实现和保存结果内部一致：44 个 `core_software_uncovered` 均至少包含一个
`actual_use=true`、角色属于必要角色且 `catalog_present=false` 的映射；17 个软件通过项均不存在这种
缺失映射。目录 hash、映射字段和最终 decision 之间没有发现写盘或聚合错误。

但“按模型抽出的实体正确执行门控”不等于“模型抽出的实体正确”。76 条中有 67 条包含模型输出清洗
警告。主要警告为无证据 quote、错误字段结构、非软件实体和资源数字无法回映原文，说明上游抽取质量
不足以支持全量结果直接作为金标。

## 4. 已确认的问题

### 4.1 明确的错误放行

`paper_a94ab9737dd05015`（DOI `10.1021/acscatal.5c03215`）的关键恒电位/隐式溶剂步骤明确使用
`VASP sol module`。模型在 workflow 中保留了该事实，却只输出 `VASP` 软件实体，使确定性映射把论文
判为 `software_covered`。当前工具箱没有 VASPsol，这篇应为 `core_software_uncovered`。因此历史 16 个
最终通过项中至少有 1 个明确假阳性；按已确认问题计算，通过集精度上限为 15/16（93.75%）。

### 4.2 明确或高度可信的错误淘汰

- `paper_2b5f254d7a98422b`：ORCA、OpenMolcas 和 Multiwfn 均在工具箱中；`RASSCF` 是方法/模块，不是
  独立软件，却被当作缺失核心程序。这是明确假阴性。
- `paper_7a1f440fe7c68e38`：Quantum ESPRESSO 已覆盖；`CCCDB database` 是数据来源，不是必要软件，
  但被标为缺失 `required_preprocessing`。当前淘汰依据错误，应重新审查自定义 HoleMass 计算是否可由
  第三层 Python 实现。
- `paper_965a2b6ac5174a7b`：RDKit 和 QVina2 已覆盖；`QSAR model` 是模型而非软件名。当前淘汰依据错误，
  应按第三层 Python 可实现性重新判断。
- `paper_41602c28cd56f3fc`：清洗后只剩 ChEMBL 和 ZINC20，并把两个数据库当作核心软件；模型 rationale
  中实际还提及 PharmacoNet、RDKit、Open Babel、PyTorch 和 AutoDock Vina。最终是否可覆盖仍需判断
  PharmacoNet，但当前 `core_software_uncovered` 的证据链不成立。

其他结果也出现 logistic regression、random forest、DBSCAN、MCTS、Adam optimizer、PDB/MaveDB 等
算法或数据库被当成软件的情况。部分论文同时还依赖 Q-Chem、TensorFlow、AiZynthFinder 等确实缺失的
程序，所以最终淘汰可能仍正确，但保存的理由不能直接用于审计或训练。

### 4.3 五条模型合同被静默降级

以下论文的 Qwen 响应把 `software_mentions` 返回为字符串数组，而不是要求的对象数组：

- `paper_57df85fa160273e8`
- `paper_7970bfff30eb8db0`
- `paper_a47b8a356658bbf4`
- `paper_dea440679364ac58`
- `paper_e300e76b3b6d1452`

清洗器把字符串全部删除，随后统一得到 `software_inventory_unconfirmed`，没有触发合同重试。其中
`paper_57df85fa160273e8` 明确包含工具箱缺失的 Q-Chem，应为未覆盖；
`paper_7970bfff30eb8db0` 的核心 DeePMD-kit、LAMMPS、VASP 和 PACKMOL 均有映射，VMD/VESTA 仅为
可视化，因而很可能是被错误 hold 的可用候选。其余三篇至少需要按正确 schema 重试，不能沿用当前
结论。

### 4.4 资源信息未形成有效筛选

本轮资源事实几乎全部为空或 `cost_unconfirmed`，并有 29 条“资源数值无法由 quote 支持”的清洗警告。
因此历史结果中的资源部分没有提供可靠的成本筛选；17 篇通过主要由软件存在性决定。

## 5. 结论与修复边界

本轮结果的确定性映射和聚合没有错误，但软件实体抽取并不完全可靠。已确认至少 1 个假阳性、1 个
假阴性，另有 3 个淘汰依据错误和 5 个模型合同损坏结果。当前 16 个 `software_covered` 不能原样作为
最终候选集，44 个 `core_software_uncovered` 也不能全部当作可靠负样本。

建议下一轮修复聚焦三个边界：

1. 将扩展/插件作为独立实体保留，尤其禁止把 VASPsol 折叠为 VASP；
2. 增强非软件词表和实体类型校验，数据库、方法、模型、优化器及通用算法不得触发软件缺失；
3. `software_mentions` 中任一元素合同错误时触发 compact/minimal retry，不能静默清空后 hold。

修复后只需重放这 76 篇当前 Stage03，不需要重跑 Stage00-02；通过集再进入 GPU MinerU 的当前
Stage04。资源抽取应单独建立有 evidence 的字段校验和重试，避免与软件覆盖结论混为一谈。
