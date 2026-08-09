# v2 LLM Prompt 与结构化 Schema 规范

状态：核心 prompt/结构化合同已进入 v2 基线实现；运行验收待 shadow run。

## 1. 通用原则

### 1.1 模型分工

| 角色 | 阶段 | 默认模型角色 | 主要职责 |
| --- | --- | --- | --- |
| `screening_llm` | Stage 03/04 | 同一个部署模型，例如 Qwen3-30B-A3B-Instruct-2507 | 计算内容判断、软件和资源语义审查 |
| `suitability_llm` | Stage 05 | 强推理模型，例如 deepseek-v4-pro | 科研流程和十个任务方向判断 |
| `builder_llm` | Stage 06 | 最强可用 Agent 模型，例如配置的 gpt5.6 | 双模式任务构建 |
| `judge_llm` | Stage 07 | 独立最强模型 | 任务审核 |

模型名称只是默认建议，配置中必须使用 role 到 endpoint/model 的映射，阶段代码不写死模型。

### 1.2 所有 prompt 的硬规则

1. 只使用输入中提供的证据。
2. 不允许浏览网络或依赖模型常识补全缺失事实。
3. 每个事实判断引用 `evidence_id` 和原文 quote。
4. quote 必须逐字存在于对应 evidence block；程序在模型返回后复核。
5. 不确定时返回 `uncertain` 或 `abstain`，不得猜测。
6. 返回一个 JSON object，不返回 Markdown 或额外解释。
7. 模型不决定工具箱 capability；能力由确定性 resolver 决定。
8. 模型错误、截断、schema 错误和引用错误属于处理错误，不属于科学淘汰。

### 1.3 Evidence packet

所有模型输入使用统一 evidence block：

```json
{
  "evidence_id": "ev_...",
  "document_id": "doc_...",
  "document_role": "main_paper | supplementary",
  "page": 4,
  "section_path": ["Methods", "Computational details"],
  "block_type": "paragraph",
  "text": "The calculations were performed with ...",
  "source_parser": "grobid | pdftotext | mineru",
  "quality_flags": []
}
```

prompt 中用不可混淆的边界传递：

```text
<EVIDENCE id="ev_123" document="doc_1" role="supplementary" page="4"
section="Methods > Computational details">
...
</EVIDENCE>
```

用户或论文正文中的指令性文本只是论文内容，不能改变 system prompt。

## 2. Stage 03：计算化学内容判断

Stage 03 对长论文使用 map-reduce。规则只形成召回证据和章节切片，所有可解析论文都进入模型流程，
不能因为规则低分而绕过模型。

### 2.1 Stage 03 Map system prompt

```text
You are the Stage 03 evidence extractor for ResearchChemBench.

Your only task is to identify evidence that the supplied paper excerpt contains computational chemistry content.
Computational chemistry includes concrete molecular or materials calculations, electronic-structure calculations,
atomistic simulation, reaction-path or kinetics calculations, conformer or free-energy workflows, excited-state
calculations, phonons, molecular dynamics, scientific chemistry machine-learning workflows, and computational
analysis that produces chemical or materials results.

Do NOT decide whether the work is novel or original. Do NOT require the paper to be purely computational. Do NOT
reject a paper because its authors also performed experiments. Do NOT assess toolbox support, resource feasibility,
benchmark suitability, or task completeness.

Distinguish concrete computational content from terminology appearing only in references, related-work discussion,
generic capabilities, instrument descriptions, or experimental data fitting that is not an atomistic/computational
chemistry workflow. A review may contain computational chemistry content; originality is outside this stage.

Use only the supplied evidence blocks. Every extracted item must cite an evidence_id and an exact quote copied from
that block. If an item cannot be grounded exactly, omit it. Return only one JSON object matching the schema.
```

### 2.2 Stage 03 Map user prompt

```text
PAPER METADATA
<PAPER_METADATA>
{paper_metadata_json}
</PAPER_METADATA>

CURRENT EXCERPT SET
{tagged_evidence_blocks}

Extract concrete computational methods, actions, results, named software clues, resource clues, and evidence that
the mentions are substantive rather than reference/background-only. Do not make a paper-level pass/reject decision.
```

### 2.3 Stage 03 Map schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "computational_evidence",
    "background_only_evidence",
    "software_clues",
    "resource_clues",
    "excerpt_assessment"
  ],
  "properties": {
    "computational_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "method_family", "action", "evidence_id", "quote"],
        "properties": {
          "kind": {"enum": ["method", "action", "result", "workflow", "parameter"]},
          "method_family": {"type": ["string", "null"]},
          "action": {"type": ["string", "null"]},
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"},
          "reason": {"type": "string"}
        }
      }
    },
    "background_only_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["evidence_id", "quote", "reason"],
        "properties": {
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"},
          "reason": {"type": "string"}
        }
      }
    },
    "software_clues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["name", "evidence_id", "quote"],
        "properties": {
          "name": {"type": "string"},
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"},
          "usage_status": {"enum": ["used", "background", "uncertain"]}
        }
      }
    },
    "resource_clues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "evidence_id", "quote"],
        "properties": {
          "kind": {"type": "string"},
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"}
        }
      }
    },
    "excerpt_assessment": {
      "enum": ["substantive_computational", "background_only", "no_signal", "uncertain"]
    }
  }
}
```

### 2.4 Stage 03 Reduce system prompt

```text
You are the Stage 03 paper-level computational-content reviewer for ResearchChemBench.

Determine only whether the supplied evidence confirms that this paper package contains substantive computational
chemistry content. Do not judge novelty, originality, pure-computational status, whether authors performed
experiments, toolbox coverage, cost, or benchmark-task suitability.

A positive decision requires at least one grounded evidence chain containing a concrete computational method or
simulation together with an action, parameter, result, or workflow context. A software name alone is insufficient.
Terminology found only in references, background discussion, generic capability statements, or unrelated
experimental fitting is not sufficient.

Use only validated evidence items supplied below. Preserve uncertainty when the evidence is conflicting or too
fragmentary. Return only one JSON object matching the schema.
```

### 2.5 Stage 03 Reduce schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "decision",
    "centrality",
    "method_families",
    "computational_actions",
    "software_clues",
    "resource_clues",
    "supporting_evidence",
    "conflicting_evidence",
    "confidence",
    "reason"
  ],
  "properties": {
    "decision": {
      "enum": [
        "computational_content_confirmed",
        "computational_content_not_found",
        "background_only",
        "uncertain"
      ]
    },
    "centrality": {"enum": ["primary", "supporting", "background_only", "uncertain"]},
    "method_families": {"type": "array", "items": {"type": "string"}},
    "computational_actions": {"type": "array", "items": {"type": "string"}},
    "software_clues": {"type": "array", "items": {"type": "string"}},
    "resource_clues": {"type": "array", "items": {"type": "string"}},
    "supporting_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["evidence_id", "quote", "claim"],
        "properties": {
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"},
          "claim": {"type": "string"}
        }
      }
    },
    "conflicting_evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["evidence_id", "quote", "reason"],
        "properties": {
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"},
          "reason": {"type": "string"}
        }
      }
    },
    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
    "reason": {"type": "string"}
  }
}
```

### 2.6 Stage 03 确定性后处理

- 所有 quote 必须在对应 evidence block 中精确匹配；
- `computational_content_confirmed` 至少有一条 supporting evidence；
- 方法族必须来自版本化 ontology；未知方法保留为 `other_candidate`，不能静默丢弃；
- `background_only` 必须有背景/引用证据；
- 响应截断、非法 enum、缺字段或引用失败转换为 `processing_failed`，重试，不转换为 `no`；
- Stage 03 cache 不包含工具箱 hash。

## 3. Stage 04：软件和资源语义审查

Stage 04 可以使用同一个 screening LLM endpoint，但必须是不同 prompt version 和 cache namespace。
建议每篇执行两个调用：inventory extraction 和 audit。成本允许时，audit 不复用第一次的自由文本推理。

### 3.1 Stage 04 Inventory system prompt

```text
You are the Stage 04 computational-workflow inventory reviewer for ResearchChemBench.

Given validated paper evidence, rule matches, and Softcite mentions, reconstruct the software and resource inventory
for the paper's substantive computational chemistry workflows.

Your responsibilities are evidence extraction and semantic role classification only. You must NOT decide whether a
program is supported by the ResearchChemBench toolbox, must NOT infer toolbox capabilities from general knowledge,
and must NOT decide final benchmark suitability.

The toolbox has three execution layers: predefined Actions, documented native-software invocation, and task-specific
Python processing. Stage04 only checks whether required named software exists in the active software catalog. Never
treat a missing predefined Action or an adapter parameter restriction as evidence that present native software is
unsupported.

For every software mention, distinguish actual use from background/reference mention. Classify its role as one of:
core_compute, required_preprocessing, required_analysis, optional_auxiliary, visualization, instrumentation,
background, or unknown. A theory, method, functional, basis set, file format, database, experimental technique, or
hardware platform is not software unless the evidence explicitly names a program or code.

Build workflow steps only when supported by evidence. Extract resource and complexity facts, carefully separating
single-job resources, aggregate-study resources, and physical experimental durations. Do not interpret a synthesis,
incubation, heating, measurement, or reaction duration as computational runtime.

Every extracted fact must cite an evidence_id and exact quote. Return only one JSON object matching the schema.
```

### 3.2 Stage 04 Inventory user prompt

```text
PAPER METADATA
<PAPER_METADATA>
{paper_metadata_json}
</PAPER_METADATA>

STAGE 03 VALIDATED COMPUTATIONAL EVIDENCE
<STAGE03>
{stage03_result_json}
</STAGE03>

RULE AND SOFTCITE MENTIONS
<MENTIONS>
{mention_records_json}
</MENTIONS>

TARGETED PAPER EVIDENCE
{tagged_evidence_blocks}

Extract a complete workflow-oriented software inventory and resource profile. The normalized_name_hint may use the
provided alias vocabulary, but it is only a hint; deterministic code will resolve capabilities after this response.
```

### 3.3 Stage 04 Inventory schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "software_inventory",
    "workflow_steps",
    "resource_facts",
    "complexity_facts",
    "inventory_completeness",
    "unresolved_items"
  ],
  "properties": {
    "software_inventory": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "mention_id",
          "raw_name",
          "normalized_name_hint",
          "usage_status",
          "role",
          "workflow_step_ids",
          "evidence"
        ],
        "properties": {
          "mention_id": {"type": "string"},
          "raw_name": {"type": "string"},
          "normalized_name_hint": {"type": ["string", "null"]},
          "version": {"type": ["string", "null"]},
          "module": {"type": ["string", "null"]},
          "usage_status": {"enum": ["used", "background", "ambiguous"]},
          "role": {
            "enum": [
              "core_compute",
              "required_preprocessing",
              "required_analysis",
              "optional_auxiliary",
              "visualization",
              "instrumentation",
              "background",
              "unknown"
            ]
          },
          "workflow_step_ids": {"type": "array", "items": {"type": "string"}},
          "evidence": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["evidence_id", "quote"],
              "properties": {
                "evidence_id": {"type": "string"},
                "quote": {"type": "string"}
              }
            }
          },
          "confidence": {"type": "number", "minimum": 0, "maximum": 1}
        }
      }
    },
    "workflow_steps": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "step_id",
          "action",
          "method_family",
          "depends_on",
          "software_mention_ids",
          "evidence"
        ],
        "properties": {
          "step_id": {"type": "string"},
          "action": {"type": "string"},
          "method_family": {"type": ["string", "null"]},
          "depends_on": {"type": "array", "items": {"type": "string"}},
          "input_clues": {"type": "array", "items": {"type": "string"}},
          "output_clues": {"type": "array", "items": {"type": "string"}},
          "software_mention_ids": {"type": "array", "items": {"type": "string"}},
          "evidence": {
            "type": "array",
            "items": {
              "type": "object",
              "required": ["evidence_id", "quote"],
              "properties": {
                "evidence_id": {"type": "string"},
                "quote": {"type": "string"}
              }
            }
          }
        }
      }
    },
    "resource_facts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": [
          "resource_type",
          "value",
          "value_upper",
          "unit",
          "relation",
          "scope",
          "actual_computation",
          "evidence_id",
          "quote"
        ],
        "properties": {
          "resource_type": {
            "enum": [
              "cpu_cores", "gpus", "memory_gb", "runtime_hours",
              "core_hours", "gpu_hours", "job_count", "node_count", "other"
            ]
          },
          "value": {"type": ["number", "null"]},
          "value_upper": {"type": ["number", "null"]},
          "unit": {"type": ["string", "null"]},
          "relation": {"enum": ["exact", "approximately", "less_than", "greater_than", "range", "unknown"]},
          "scope": {"enum": ["single_job", "aggregate_study", "physical_experiment", "unknown"]},
          "actual_computation": {"type": "boolean"},
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"}
        }
      }
    },
    "complexity_facts": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "value", "unit", "evidence_id", "quote"],
        "properties": {
          "kind": {
            "enum": [
              "atom_count", "electron_count", "system_count", "conformer_count", "transition_state_count",
              "basis_set", "functional", "wavefunction_method", "pseudopotential", "periodic_dimension",
              "k_points", "cutoff", "md_steps", "trajectory_length", "sampling_windows", "other"
            ]
          },
          "value": {},
          "unit": {"type": ["string", "null"]},
          "evidence_id": {"type": "string"},
          "quote": {"type": "string"}
        }
      }
    },
    "inventory_completeness": {"enum": ["complete", "partial", "uncertain"]},
    "unresolved_items": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["kind", "description", "evidence_ids"],
        "properties": {
          "kind": {"type": "string"},
          "description": {"type": "string"},
          "evidence_ids": {"type": "array", "items": {"type": "string"}}
        }
      }
    }
  }
}
```

### 3.4 Stage 04 Audit system prompt

```text
You are the independent Stage 04 inventory auditor for ResearchChemBench.

Audit the proposed computational workflow and software/resource inventory against the supplied evidence. Focus on:
1. software that was missed;
2. software incorrectly treated as used when it is only cited or discussed;
3. incorrect role classification, especially auxiliary or visualization tools treated as core, and required custom
   code or analysis software treated as optional;
4. incomplete workflow-step to software mappings;
5. physical experimental durations incorrectly treated as compute runtime;
6. ranges, lower bounds, upper bounds, aggregate costs, or job counts interpreted incorrectly.

Do not assess toolbox support and do not use outside knowledge. Return corrected inventory fields plus explicit audit
issues. Every correction must cite exact evidence. Return only JSON matching the schema.
```

Audit schema 可以复用 Inventory schema，并增加：

```json
{
  "audit_status": "confirmed | corrected | unresolved",
  "audit_issues": [
    {
      "severity": "blocking | warning",
      "kind": "missing_software | wrong_usage | wrong_role | workflow_gap | resource_error | other",
      "description": "...",
      "evidence_ids": ["ev_..."]
    }
  ]
}
```

### 3.5 Stage 04 确定性 resolver 输出

LLM 返回后，程序生成而不是让模型生成：

```json
{
  "workflow_id": "workflow_...",
  "software_resolution": [
    {
      "mention_id": "sw_1",
      "normalized_backend": "gaussian",
      "resolution_method": "exact_alias",
      "catalog_present": true,
      "native_software_available": true,
      "coverage_basis": "native_software_catalog_presence",
      "covered": true,
      "coverage_reason": "software_present"
    }
  ],
  "resource_assessment": {
    "decision": "within_preliminary_budget | exceeds_minimum_budget | cost_unconfirmed",
    "configured_budget": {},
    "exceeded_facts": [],
    "unresolved_facts": []
  },
  "decision": "software_covered | software_inventory_unconfirmed | core_software_uncovered",
  "processing_status": "success",
  "decision_status": "pass | reject | hold"
}
```

`resource_assessment` 只作为下游成本审查的元数据，不改变 Stage04 的软件覆盖 decision。

### 3.6 Stage 04 防止单篇错误拖垮批次

- schema 校验失败只重试该 paper；
- 第一次修复 prompt 仅包含 validation errors 和原始 response；
- 最多重试次数配置化；
- 超限后写 `processing_failed`，不抛出使整个微批次失败的未捕获异常；
- 原始响应、错误和修复响应全部保留；
- resume 从 paper-level cache 恢复。

## 4. Stage 05：Benchmark 适用性判断

### 4.1 Stage 05 system prompt

```text
You are the Stage 05 benchmark-suitability reviewer for ResearchChemBench, a benchmark for computational-chemistry
research agents.

The paper has already passed computational-content, toolbox-software, and preliminary-resource gates. Determine
whether the supplied evidence supports one or more non-trivial, executable, objectively scoreable research tasks in
the allowed ten directions.

A valid candidate must define a clear scientific question, include at least three interdependent computational
stages, include at least one scientific validation gate, and produce at least one machine-computable target. The
starting inputs must be obtainable from the frozen paper package, and public inputs must be separable from hidden
answer-bearing results. The selected workflow must use only software present in the Stage 04 software catalog
and preliminary resource budget.

Do not build final task files. Do not invent missing structures, parameters, methods, software, numerical targets,
or source data. Reject trivial tasks that only read an existing output, extract a reported number, redraw a figure,
run one isolated single-point calculation, or execute a fixed script without scientific decisions or validation.

For each candidate, cite the paper claim/figure/table, workflow stages, input evidence, target evidence, and
validation-gate evidence. Return at most three candidates. If evidence is insufficient, abstain with structured
reasons. Return only one JSON object matching the schema.
```

### 4.2 Stage 05 user prompt

```text
PAPER METADATA AND DOCUMENT QUALITY
{paper_metadata_and_quality_json}

VALIDATED COMPUTATIONAL CONTENT
{stage03_json}

VALIDATED WORKFLOW, TOOLBOX COVERAGE, AND RESOURCE PROFILE
{stage04_json}

ALLOWED DIRECTIONS
{direction_taxonomy_json}

TARGETED ORIGINAL EVIDENCE
{tagged_evidence_blocks}

Identify zero to three defensible benchmark candidates. Each candidate must be grounded and must satisfy every
minimum condition. Prefer abstention to filling missing information from model knowledge.
```

### 4.3 Stage 05 schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["decision", "candidates", "abstain_reasons", "summary"],
  "properties": {
    "decision": {"enum": ["candidate_found", "abstain", "uncertain"]},
    "candidates": {
      "type": "array",
      "maxItems": 3,
      "items": {
        "type": "object",
        "required": [
          "candidate_title",
          "direction",
          "scientific_question",
          "scientific_object",
          "claim_target",
          "workflow_stages",
          "validation_gates",
          "starting_inputs",
          "hidden_targets",
          "ground_truth_grade",
          "machine_scoring",
          "toolbox_workflow_ids",
          "resource_assessment",
          "autonomous_mode_feasible",
          "reproduction_mode_feasible",
          "evidence_map",
          "blocking_uncertainties"
        ],
        "properties": {
          "candidate_title": {"type": "string"},
          "direction": {
            "enum": [
              "reaction_mechanism_selectivity",
              "conformer_thermochemistry_property_calibration",
              "periodic_surface_adsorption_bonding",
              "electron_density_topology_bonding",
              "reaction_kinetics_master_equation_microkinetics",
              "excited_state_spectroscopy_photochemistry",
              "high_pressure_phase_stability",
              "phonons_vibrations_thermal_transport",
              "molecular_dynamics_free_energy",
              "descriptor_discovery_catalyst_design"
            ]
          },
          "scientific_question": {"type": "string"},
          "scientific_object": {"type": "string"},
          "claim_target": {
            "type": "object",
            "required": ["kind", "identifier", "description"],
            "properties": {
              "kind": {"enum": ["claim", "figure", "table", "equation", "result_section"]},
              "identifier": {"type": "string"},
              "description": {"type": "string"}
            }
          },
          "workflow_stages": {
            "type": "array",
            "minItems": 3,
            "items": {
              "type": "object",
              "required": ["stage_id", "action", "depends_on", "inputs", "outputs", "evidence_ids"],
              "properties": {
                "stage_id": {"type": "string"},
                "action": {"type": "string"},
                "depends_on": {"type": "array", "items": {"type": "string"}},
                "inputs": {"type": "array", "items": {"type": "string"}},
                "outputs": {"type": "array", "items": {"type": "string"}},
                "evidence_ids": {"type": "array", "items": {"type": "string"}}
              }
            }
          },
          "validation_gates": {
            "type": "array",
            "minItems": 1,
            "items": {
              "type": "object",
              "required": ["gate", "acceptance_rule", "evidence_ids"],
              "properties": {
                "gate": {"type": "string"},
                "acceptance_rule": {"type": "string"},
                "evidence_ids": {"type": "array", "items": {"type": "string"}}
              }
            }
          },
          "starting_inputs": {"type": "array", "minItems": 1, "items": {"type": "object"}},
          "hidden_targets": {"type": "array", "minItems": 1, "items": {"type": "object"}},
          "ground_truth_grade": {"enum": ["A", "B", "C", "D"]},
          "machine_scoring": {"type": "object"},
          "toolbox_workflow_ids": {"type": "array", "minItems": 1, "items": {"type": "string"}},
          "resource_assessment": {"type": "object"},
          "autonomous_mode_feasible": {"type": "boolean"},
          "reproduction_mode_feasible": {"type": "boolean"},
          "evidence_map": {"type": "array", "minItems": 1, "items": {"type": "object"}},
          "blocking_uncertainties": {"type": "array", "items": {"type": "string"}}
        }
      }
    },
    "abstain_reasons": {
      "type": "array",
      "items": {
        "enum": [
          "no_supported_direction",
          "incomplete_scientific_question",
          "insufficient_workflow_depth",
          "missing_validation_gate",
          "missing_input",
          "missing_parameters",
          "missing_ground_truth",
          "not_machine_scorable",
          "resource_limit",
          "not_significant"
        ]
      }
    },
    "summary": {"type": "string"}
  }
}
```

### 4.4 Stage 05 后处理

- `candidate_found` 至少一个 candidate；
- workflow stages 必须形成无环依赖图，且至少三步；
- 至少一个 validation gate；
- evidence IDs 全部存在并与输入/目标/步骤关联；
- candidate 使用的 workflow IDs 必须来自 Stage 04 pass 记录；
- 两种模式至少都为 true 才进入默认成对任务 Builder；
- D 级 ground truth 默认进入 hold，除非任务只需稳健定性评分且规则明确允许。

## 5. Stage 06：Builder prompts

Stage 06 不建议用一个调用同时自由生成两个模式。先冻结共享科学记录，再分别构建两种模式。

### 5.1 Shared record Builder system prompt

```text
You are the ResearchChemBench scientific-record Builder. Use only the validated Stage 05 candidate and cited frozen
evidence. Produce a shared scientific record, hidden reference, scoring targets, resource budget, and evidence map
for one candidate. Do not write either public task yet. Do not invent missing facts. Abstain if the candidate cannot
support both autonomous-research and paper-reproduction modes.
```

共享记录必须包含：system identity、scientific question、workflow graph、validation gates、starting inputs、
hidden conclusions、units、reference state、tolerances、ground-truth grade、toolbox actions、resource budget 和
evidence map。

### 5.2 Autonomous Builder system prompt

```text
You are the autonomous-research task Builder for ResearchChemBench. Build one public task from the frozen shared
scientific record. Reveal the scientific problem, starting inputs, experimental conditions, and required scientific
validity constraints. Do not reveal the paper's software route, method sequence, intermediate states, answer-bearing
parameters, target values, or final conclusion. Require the agent to plan, select tools, generate new managed
artifacts, test alternatives, validate the result, and report uncertainty. Return only the task schema.
```

### 5.3 Reproduction Builder system prompt

```text
You are the paper-reproduction task Builder for ResearchChemBench. Build one public task from the frozen shared
scientific record. Reveal the validated computational protocol, required methods, parameters, software mapping,
reference-state conventions, and validation requirements. Do not reveal answer-bearing author outputs, final target
values, or final scientific conclusion. Require new calculations or a valid independent re-analysis, not copying.
Return only the task schema.
```

### 5.4 Builder 输出要求

- 两个 public task 共享 `task_pair_id` 和 `scientific_record_hash`；
- 每种模式有自己的 `task_info.json`、`task.md` 和 public asset manifest；
- hidden reference 只生成一次；
- Rubric 包含结论轴和过程轴，并总计 100；
- Builder 对缺失数据返回 abstain，不生成 placeholder。

## 6. Stage 07：Judge prompt

### 6.1 Judge system prompt

```text
You are the independent final Judge for a ResearchChemBench task pair. You have no access to Builder conversations
or scratch work. Audit only the frozen paper evidence, toolbox/runtime snapshot, deterministic validation report,
shared hidden reference, and the two public task packages.

Check paper fidelity, scientific significance, at least three interdependent computational stages, validation gates,
public-input sufficiency, toolbox/runtime support, resource feasibility, autonomous-route leakage, reproduction-answer
leakage, ground-truth quality, numerical units and reference states, machine-computable scoring, and consistency
between the paired modes.

Reject tasks that can be solved by copying a reported value, reading an answer-bearing output, redrawing a figure,
or running a trivial isolated calculation. Every issue must cite a concrete field, file, asset ID, or evidence ID.
Return pass only when no blocking issue remains. Return revise only when the evidence is sufficient and the defect is
repairable without inventing data. Return only one JSON object matching the schema.
```

### 6.2 Judge schema

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": [
    "decision",
    "checks",
    "blocking_issues",
    "revision_suggestions",
    "residual_risks",
    "summary"
  ],
  "properties": {
    "decision": {"enum": ["pass", "revise", "reject"]},
    "checks": {
      "type": "object",
      "required": [
        "paper_fidelity",
        "scientific_significance",
        "workflow_depth",
        "validation_gates",
        "input_sufficiency",
        "toolbox_runtime_support",
        "autonomous_route_leakage",
        "reproduction_answer_leakage",
        "ground_truth_quality",
        "scoring_quality",
        "resource_feasibility",
        "paired_mode_consistency"
      ]
    },
    "blocking_issues": {"type": "array", "items": {"type": "object"}},
    "revision_suggestions": {"type": "array", "items": {"type": "object"}},
    "residual_risks": {"type": "array", "items": {"type": "string"}},
    "summary": {"type": "string"}
  }
}
```

每个 check 统一使用：

```json
{
  "status": "pass | fail | uncertain",
  "evidence": ["file/evidence reference"],
  "reason": "..."
}
```

## 7. Prompt 版本和模型选择

建议初始版本：

```text
stage03-map-v2.0
stage03-reduce-v2.0
stage04-inventory-v2.0
stage04-audit-v2.0
stage05-suitability-v2.0
stage06-shared-record-v2.0
stage06-autonomous-v2.0
stage06-reproduction-v2.0
stage07-judge-v2.0
```

每次修改 prompt 的判定语义、字段或引用要求都提升版本并使对应缓存失效。只改空白或日志文字不必失效。

模型上线前需要在固定开发集比较：

- schema 成功率；
- evidence quote 回映率；
- Stage 03 计算内容 recall 和 background-only precision；
- Stage 04 软件发现 recall、used/background precision、core/aux role accuracy；
- 资源事实 precision；
- Stage 05 候选 precision 和人工可构建率；
- token、延迟和吞吐。

不能只比较最终 pass rate。较高通过率可能来自宽松误筛，较低通过率也可能来自系统性漏筛。
