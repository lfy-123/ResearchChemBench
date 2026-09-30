# paper_ef26687d63a37e29：V2 特定升级方案

方案时间：2026-09-28T17:14:58.654815+00:00；先于该篇 V2 包创建。

## 来源与问题

How does adding phthalic anhydride change the local molecular interactions in the (Et2N)3P/Et3B system, and what can those changes establish about epoxide activation and chain-end stabilization during CO2/propylene-oxide copolymerization?

Address the source local molecular interaction question using (Et2N)3P, phthalic anhydride (PA), Et3B, propylene oxide (PO) and CO2. Source probe identities and interaction measurements are available; their use is a research decision. Define any adduct, association or chain-end model explicitly and justify its representativeness. Bulk polymer molecular weight, productivity, a complete polymerization network and extrapolation to other catalyst families are outside scope.

The source compares PO/CO2 copolymerization with phosphine/Et3B and with PA added. A representative source feed is [PO]/[PA]/[(Et2N)3P]/[Et3B]=2000/1/1/2, neat,80 °C,initial CO2 pressure2.0 MPa. Separate stoichiometric interaction experiments use TFPO as an epoxide probe and sodium ethoxide as a chain-end probe in stated NMR solvents. These probes and short molecular models are not actual long growing polymer chains. Neither a unique reactive adduct nor a propagation/backbiting barrier is given as a public fact.

- papers/paper_ef26687d63a37e29/documents/main.pdf；SHA256 bf0ec692ef2eec7d4342ed722884bcabb2137396dcb3fc6c6a867eed7f62b0b8；PDF页 9,10
- papers/paper_ef26687d63a37e29/documents/supplementary_001.pdf；SHA256 bc6f2dea0dc2ca97f7ae56c8bdda09c32be5fd0656a670db51c46cf023cebf96；PDF页 4,5,7,8,9,10,11,12

## 旧版约束与公开改造

从强制人工短链传播/回咬矩阵退回源文有证据支持的局部活化和链端相互作用问题。PA、膦、硼与探针身份充分公开，活性物种、链长和判别路线由agent负责；私有评价同样不再强制旧路径。
- Et2N3P*_identity.json and *.xyz：retain only free phosphine identity; adduct/coordinate answers private；Agent constructs chemically supported local species instead of receiving source/benchmark conformations as answers.
- species_registry.json：retain source reagents; add PA and source probe identities; remove PA_chain/noPA_chain；Fixed two-PO/one-CO2 oligomer and its control were benchmark constructions, not experimentally established active species.
- research_matrix.json：private_snapshot_only；Remove obligatory propagation/backbite sequence, two-Et3B cluster and tenfold dilution test.

## Agent 自主决策

- Determine which local species and molecular models are chemically justified by the source mixture.
- Choose evidence able to test epoxide activation and chain-end stabilization claims.
- Design comparisons that distinguish interaction changes from model or inventory confounding.
- Determine how far local results support a polymerization interpretation and where they remain insufficient.

## 提交、评价和 PR

Agent-defined objects/models/methods/records/quantities/claims/decisions; no named mechanism keys or hypothesis-count minimum. report/results.json and report/report.md required. Claim-triggered validity, not mandatory TS/IRC for every investigation.

The authors propose that PA reacts with the Lewis base to generate an intramolecular phosphonium/carboxylate zwitterion, interacting with Et3B and influencing both epoxide activation and chain-end association (main pp9–10). Their DFT comparison concerns free(Et2N)3P, the PO adduct and the PA adduct, not a full polymer propagation/backbiting network. SI pp4–5 specifies Gaussian16 B3LYP/6-31G(d) with D3(BJ), with ADCH populations from Multiwfn using vibrational-analysis wavefunctions. The source does not explicitly specify a continuum solvent for these molecular calculations. Main p10 reports PO-adduct O···P1.828 Å versus PA-adduct2.651 Å and differing O···H contacts/populations; those local observations support an interpretation but do not directly prove suppressed backbiting. Reproduce and assess the local molecular baseline or justify controlled substitutions. NMR probe results use TFPO/C6D6 and sodium ethoxide/CDCl3, with preparation details inSI p4. Source polymer kinetics and dilution behavior are a separate scale. The fixed PA-containing two-PO/one-CO2 oligomer, no-PA chain pair, two-Et3B path inventory and tenfold-PO test inV1 were benchmark additions.

- identity (20/100)：Preserve source reagent identities and explicitly define any adduct/chain-end graph, charge/spin and composition. Constructed oligomers must be labeled models. Reference comparisons must conserve inventories or account for reservoirs and coproducts.
- interactions (30/100)：Generate results that address how PA addition changes relevant molecular interactions. Distances, populations, binding thermodynamics and reactivity metrics support different claims; their interpretation must match their definition. No mandatory PA/no-PA chain or named pathway matrix.
- mechanistic (20/100)：Assess whether evidence establishes activation, association or a kinetic effect. A contact or more positiveP charge alone does not prove faster propagation or suppressed backbiting. If a reaction barrier is claimed, establish the corresponding physical path; alternative bounded interaction arguments remain eligible.
- sensitivity (15/100)：Address model uncertainties capable of changing the conclusion with actual evidence. Association comparisons must use consistent standard states and concentration/solvent assumptions. No forced10-fold dilution or fixedEt3B count per molecular cluster.
- scope (15/100)：Relate local findings to source probe observations with explicit representativeness limits. Support, correction and well-investigated unresolved conclusions are eligible. No direct prediction of bulk molecular weight, productivity or antidilution performance from a short isolated model.

## 旧证据、可行性与限制

Source molecular structures, adduct DFT and NMR probes establish a feasible bounded interaction question. Earlier free/adduct computations can be reused only for their exact local identity and method; old constructed-chain jobs do not certify an actual polymer mechanism. No scientific engine was started.

- workspaces/codex_gpt56/paper_ef26687d63a37e29_20260921_064813_89a050/runs/cli_runs/batch_20260921_064818_61a71a/autonomous_research-paper_ef26687d63a37e29-codex-20260921_064818-303244/report/results.json；Earlier narrow endpoint only; re-audit identity, model, raw artifacts and reference before reuse. No inherited PASS.
- docs/upgrade_tasks_v2_review_20260928/group_4/phase1/DEVELOPMENT_FREEZE_HANDOFF.json；旧磷鎓PA/PO加合物不等于增长链。PA/noPA完整链、CO2/PO和双Et3B等核素传播/回咬图已建立；12组分和6基本步独立通过全H图、电荷、价态、CIP核查，环状副产物的映射复用已验证。另备5个Et3B配位起点，几何回读通过；未运行新DFT。十倍PO稀释1.61591 kcal/mol仅单位PO级数的化学势恒等式。
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/legacy/inventory.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/provenance/chain_reaction_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/provenance/chain_reaction_input_audit.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/provenance/borane_association_preparation.json；Private feasibility/reference evidence only; apply paper-specific limits, not the old mandatory workflow.

- New association/reactivity free-energy and model-representativeness calibration remains pending.
- The source local DFT solvent specification is incomplete and is not silently replaced byV1 THF353.15K.
- Actual semantic judge and runtime isolation remain pending.

方案写好后立即实施；不启动新科学任务。完整结构化方案见同名JSON。

## 收尾来源与旧证据复用补充

Historical PA/phosphine/PO adducts and later finite chain/reaction constructions; the simple tenfold concentration chemical-potential calculation is an algebraic identity.

可复用：Reuse the actual adduct identities and graph/inventory diagnostics. Distinguish source PA/Et3B molecular evidence from later author-created chain preparations.

不可据此声称：Old adducts are not validated growing chains; prepared reactions are not calculated selectivity. A concentration identity does not prove a chain-end mechanism or polymer yield.

逐文件版本绑定：

- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/legacy/inventory.json；SHA256 83510dac047aee8366d2c37c5dcff88f4cb7fbb016847c8732beeb50eeeb4a2a；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/provenance/chain_reaction_preparation.json；SHA256 ecf8723e34ba1908bfc33957ebc0c3a8ec47bdb4e3f82439044485ec1db37854；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/provenance/chain_reaction_input_audit.json；SHA256 0f51c490e6d50147b0d7273053190984d89808ac98e023cbd1ee4982cad6c3b0；冻结哈希一致=True
- docs/upgrade_tasks_verification/group_4/papers/paper_ef26687d63a37e29/provenance/borane_association_preparation.json；SHA256 ee7d9f00c69ababd0b86d9d232e52b0367dfcf7432d3cff98c1c937e1d3fc171；冻结哈希一致=True

原始旧矩阵及活动作业状态仅在冻结行中保留为历史；不进入V2必做项目，不代表现时作业状态或新任务PASS。
