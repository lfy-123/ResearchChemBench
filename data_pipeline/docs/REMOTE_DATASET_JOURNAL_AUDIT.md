# 远端论文数据集期刊与补充材料审计

> 审计日期：2026-08-06
>
> 审计方式：通过现有 Xinghe/Petrel 只读凭证流式列举对象和解析远端 JSONL 元数据；
> 未下载完整元数据文件或批量 PDF。

## 1. 授权数据集

当前凭证允许读取：

```text
s3://crawl-data/www_acs_org/gz_file/1734329655/
s3://private-cooperate-data/en-paper-hzzj/
s3://private-cooperate-data/en-pdf-core-chemistry/KPS/20260603_bu/
s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-06-18/
s3://private-cooperate-data/en-pdf-core-chemistry/KPS/dt=2026-05-07/
```

ACS 前缀包含 9 个网页抓取 `jsonl.gz` 分片，不是直接供当前 PDF 管线处理的正文集合。
其余数据集包含 PDF、元数据或补充材料。

## 2. `en-paper-hzzj` 完整远端集合

本地 `data_pipeline/datasets/en-paper-hzzj` 的 100 篇只是远端对象按名称排序后的第一批，
因此恰好全部是 Wiley Angew，不能代表完整远端集合。

完整远端 `pdf/` 前缀共有 21,836 篇：

| DOI 注册前缀 | 主要出版商 | PDF 数 | 比例 |
| --- | --- | ---: | ---: |
| `10.1021` | ACS | 10,048 | 46.02% |
| `10.1002` | Wiley | 6,095 | 27.91% |
| `10.1039` | RSC | 4,300 | 19.69% |
| `10.1016` | Elsevier | 930 | 4.26% |
| `10.1038` | Nature Portfolio | 463 | 2.12% |

将远端文件名与 KPS 20260603 元数据按 `pdf_filename` 大小写无关匹配后，21,121 篇成功
关联，715 篇主要是元数据快照之后新增的 2024-2025 论文。成功关联部分包含 11 种期刊：

| 期刊 | 已匹配论文数 |
| --- | ---: |
| Journal of the American Chemical Society | 6,247 |
| Angewandte Chemie International Edition | 5,845 |
| Chemical Science | 3,085 |
| ACS Catalysis | 2,515 |
| Green Chemistry | 1,189 |
| Chem | 542 |
| Accounts of Chemical Research | 439 |
| ACS Central Science | 414 |
| Chem Catalysis | 382 |
| Nature Chemistry | 302 |
| Nature Catalysis | 161 |

未匹配的 715 篇 DOI/文件名模式仍落在相同五个出版商和上述目标期刊范围内，包括
`anie`、`acscatal`、`jacs`、`acs.accounts`、RSC `GC` 及 Cell Press `chempr/checat`。

成功关联的 21,121 篇中，18,634 篇元数据含非空 `support_path`，但该字段来自 KPS
快照，不能直接作为 `en-paper-hzzj` 中的对象路径。对实际对象清单的二次审计结果为：

| 项目 | 结果 |
| --- | ---: |
| `en-paper-hzzj/pdf/` 正文对象 | 21,836 |
| `en-paper-hzzj/support/` SI 对象 | 19,110 |
| SI 所属唯一论文 | 18,498 |
| 能按正文名去掉 `.pdf`、SI 名去掉 `_sup_N.pdf` 映射的论文 | 18,498 |
| 孤立 SI 或不符合命名规则的对象 | 0 |

18,498 个论文组中 612 个含两个或更多 SI。Stage 00 必须列举这个真实 `support/`
前缀并按 DOI 文件名匹配，不能把 KPS 元数据相对路径拼到 KPS 20260603 根目录。

## 3. KPS 20260603 主元数据

远端元数据文件：

```text
en-pdf-core-chemistry/KPS/20260603_bu/
  物质科学类化学核心期刊_935168_0602.jsonl
```

流式扫描结果：

| 项目 | 结果 |
| --- | ---: |
| 成功解析记录 | 935,148 |
| 损坏 JSONL 行 | 20 |
| 原始 `journal_name` 取值 | 107 |
| 带 `support_path` 的论文 | 431,475（46.14%） |
| `support_path` 附件总数 | 496,624 |
| 元数据引用的 SI 文件类型 | 全部为 PDF |

这里的 496,624 是 JSONL 中的路径引用数，不是该快照目录的实际对象数。只读对象清点
显示 `KPS/20260603_bu/support/` 实际只有 265 个 Nature SI，预期的 `pdf/` 前缀为
0 个正文。因此这个目录可作为元数据来源，不能单独作为 Stage 00 正文语料库，也不能
假定所有 `support_path` 都能在该根目录下载。

### 3.1 出版商/DOI 前缀分布

| DOI 前缀 | 主要出版商 | 论文数 | 比例 | 带 SI 论文数 |
| --- | --- | ---: | ---: | ---: |
| `10.1021` | ACS | 292,579 | 31.29% | 129,338 |
| `10.1039` | RSC | 221,497 | 23.69% | 162,688 |
| `10.1016` | Elsevier | 166,383 | 17.79% | 16,345 |
| `10.1002` | Wiley | 148,832 | 15.92% | 69,415 |
| `10.1038` | Nature Portfolio | 53,191 | 5.69% | 48,904 |
| `10.3390` | MDPI | 25,428 | 2.72% | 0 |
| `10.1246` | Chemical Society of Japan | 13,325 | 1.42% | 0 |
| `10.6023` | Chinese Journal of Organic Chemistry | 5,247 | 0.56% | 2,619 |
| `10.2174` | Bentham | 2,111 | 0.23% | 0 |
| `10.1055` | Thieme | 1,929 | 0.21% | 912 |
| `10.1007` | Springer | 1,776 | 0.19% | 263 |
| `10.1080` | Taylor & Francis | 1,454 | 0.16% | 95 |
| `10.3762` | Beilstein | 1,102 | 0.12% | 876 |
| `10.1093` | Oxford University Press | 294 | 0.03% | 20 |

ACS、RSC、Elsevier、Wiley、Nature Portfolio 和 MDPI 六类合计覆盖 97.09% 的记录。
Stage 04 第一批出版商适配器应优先覆盖这六类，而不是只实现 Wiley。

### 3.2 原始期刊名称完整清单

以下为元数据中的原始名称和计数，尚未合并历史刊名、标点或连字符变体：

| 数量 | 期刊名称 |
| ---: | --- |
| 98,143 | Journal of the American Chemical Society |
| 67,953 | Chemical Engineering Journal |
| 54,671 | RSC Advances |
| 49,964 | Nature Communications |
| 35,285 | The Journal of Organic Chemistry |
| 33,893 | Analytical Chemistry |
| 33,500 | ACS Applied Materials & Interfaces |
| 29,008 | Chemical Communications |
| 27,202 | Physical Chemistry Chemical Physics |
| 25,446 | Molecules |
| 21,522 | Inorganic Chemistry |
| 18,699 | Angewandte Chemie International Edition |
| 18,566 | Dalton Transactions |
| 15,838 | New Journal of Chemistry |
| 15,544 | Journal für Praktische Chemie |
| 15,470 | Journal of Molecular Structure |
| 14,948 | Small |
| 14,917 | Chemistry - A European Journal |
| 14,817 | Organic & Biomolecular Chemistry |
| 12,739 | Talanta |
| 12,680 | Advanced Materials |
| 12,674 | The Journal of Physical Chemistry C |
| 12,669 | Bulletin of the Chemical Society of Japan |
| 12,370 | Bioorganic & Medicinal Chemistry |
| 11,636 | Tetrahedron |
| 11,468 | Chemical Science |
| 11,213 | Journal of Organometallic Chemistry |
| 11,093 | Advanced Science |
| 10,837 | ChemistrySelect |
| 10,710 | ACS Nano |
| 9,596 | Nanoscale |
| 9,156 | Journal of Medicinal Chemistry |
| 8,305 | Organic Letters |
| 7,882 | Justus Liebigs Annalen der Chemie |
| 7,623 | Journal of Materials Chemistry B |
| 7,267 | Green Chemistry |
| 6,881 | Macromolecules |
| 6,627 | ACS Catalysis |
| 6,418 | Catalysis Science & Technology |
| 6,325 | Advanced Synthesis & Catalysis |
| 5,842 | Angewandte Chemie International Edition in English |
| 5,790 | Polymer Chemistry |
| 5,247 | Chinese Journal of Organic Chemistry |
| 5,080 | European Journal of Organic Chemistry |
| 4,974 | Chinese Chemical Letters |
| 4,930 | Inorganica Chimica Acta |
| 4,659 | Energy & Environmental Science |
| 4,483 | Chemistry - An Asian Journal |
| 4,468 | Organic Chemistry Frontiers |
| 4,351 | European Journal of Medicinal Chemistry |
| 4,293 | Bioorganic Chemistry |
| 4,024 | Advanced Healthcare Materials |
| 3,746 | Dyes and Pigments |
| 3,226 | Liebigs Annalen der Chemie |
| 3,221 | Chemical Communications (London) |
| 3,181 | ChemCatChem |
| 2,771 | ACS Applied Bio Materials |
| 2,750 | Biomaterials |
| 2,591 | Angewandte Chemie |
| 2,591 | Industrial & Engineering Chemistry Analytical Edition |
| 2,235 | Journal of the Indian Chemical Society |
| 2,217 | Nature Chemistry |
| 2,111 | Current Organic Chemistry |
| 2,026 | Accounts of Chemical Research |
| 2,021 | Polyhedron |
| 1,957 | Organic Process Research & Development |
| 1,929 | Synthesis |
| 1,748 | Asian Journal of Organic Chemistry |
| 1,746 | JACS Au |
| 1,661 | Organometallics |
| 1,608 | Photochemical & Photobiological Sciences |
| 1,509 | Chinese Journal of Chemistry |
| 1,492 | Journal of Natural Products |
| 1,454 | Synthetic Communications |
| 1,428 | Chem |
| 1,188 | ChemMedChem |
| 1,142 | Chinese Journal of Catalysis |
| 1,101 | Beilstein Journal of Organic Chemistry |
| 1,090 | Chem Catalysis |
| 1,072 | Synthetic Metals |
| 1,062 | ACS Central Science |
| 1,032 | Molecular Diversity |
| 1,010 | Nature Catalysis |
| 950 | Bulletin of the Chemical Society of Japan. |
| 889 | Liebigs Annalen |
| 759 | Journal für Praktische Chemie/Chemiker-Zeitung |
| 583 | Catalysis Communications |
| 562 | Chirality |
| 555 | Chemistry – A European Journal |
| 323 | Green Synthesis and Catalysis |
| 310 | Journal of Organic Chemistry |
| 270 | Chemistry – An Asian Journal |
| 266 | ACS Organic & Inorganic Au |
| 33 | Journal of Molecular Structure: THEOCHEM |
| 14 | The Chemical Engineering Journal and the Biochemical Engineering Journal |
| 9 | Biomedicine & Pharmacotherapy |
| 3 | Molecules Online |
| 1 | Beilstein Journal of Nanotechnology |
| 1 | Ceramics International |
| 1 | Computational Biology and Chemistry |
| 1 | Digital Signal Processing |
| 1 | Journal of Magnetism and Magnetic Materials |
| 1 | Marine Genomics |
| 1 | Organic Process Research and Development |
| 1 | Separation and Purification Technology |
| 1 | Theriogenology |
| 1 | Urology |

低频非核心化学期刊可能是元数据噪声或边界样本，Stage 01 应保留来源，不能仅按期刊名
静默删除。期刊名称在统计时应按 ISSN 和规范刊名归一化，但原始值必须保留。

## 4. KPS 其他版本

- `dt=2026-05-07` 含 935,168 个正文对象和 496,360 个实际 SI，对应 431,240 篇
  唯一论文；SI 文件名全部符合 `_sup_N.pdf`。100 个分层随机 SI owner 以大小写归一化
  正文名核验后全部存在。该目录较大，Stage 00 对本批元数据候选逐个 `HEAD` 验证，
  避免每批扫描 49 万对象。
- `dt=2026-06-18` 有 99 个正文对象和 23 个实际 SI，对应 10 篇论文；23 个 SI 均能
  映射到这 99 篇正文，零孤立对象。元数据期刊构成为 Advanced Materials 88、Nature
  Communications 10、Advanced Science 1。
- `KPS/20260603_bu` 只有元数据及 265 个 SI，没有可由当前配置读取的正文对象。

## 5. 对数据管线的直接要求

1. Stage 00 按数据集配置的真实 `supplementary_prefix` 列举对象，并用规范化 DOI 文件名
   将正文与 SI 分组；大目录可验证本批元数据候选，但必须先确认对象存在。
2. `support_path` 只作为审计提示，未经列举或 `HEAD` 验证不能直接拼接和下载。
3. Stage 04 仅重试 Stage 00 已验证但复制失败的 URI；本地仍缺 SI 时才调用官网适配器。
4. 第一批适配器覆盖 ACS、RSC、Elsevier、Wiley、Nature Portfolio 和 MDPI。
5. 适配器只枚举和下载出版商标记为该论文 Supplementary Information 的附件。
6. 不跟随论文正文或 SI 中的 GitHub、Zenodo、Figshare、作者主页、数据库和数据集链接。
7. 官网适配器必须显式校验媒体类型和下载预算；403 记录为 `access_blocked`，不能解释
   为论文无 SI。
8. Stage 04 只负责取得文件；补充材料文本解析放到通过 Stage 05 的 Stage 06。
