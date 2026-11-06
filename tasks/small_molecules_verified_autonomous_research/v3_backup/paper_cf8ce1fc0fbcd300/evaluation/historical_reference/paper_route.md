# Private source-grounded construction route

Paper: Modular synthesis of fluoroalkyl-substituted cyclopropenes with fluoroalkylacylsilanes as carbynyl cation equivalents; 10.1016/j.chempr.2025.102721.
The Stage05 research_contract is preserved exactly as the immutable reference and
provenance record. This file, evaluation files and task_info are not solver inputs.

## Actual computational investigation

The main computational discussion (ev_doc_66884e111ce4_000074_4cac510a97c9; duplicate supplied version
ev_doc_4faff3167966_000073_4cac510a97c9) explicitly reports two connected computations: comparing
methanol-addition transition states to explain site selectivity, and comparing the
Gibbs energies of the three resulting methoxy regioisomers to assess product
stability and its relationship to redistribution. Author attribution is explicit
in ev_doc_66884e111ce4_000104_d5cc19b38911. The actual computational methods (ev_doc_31695a0a949d_000359_9cb5c1cb8968) state
Gaussian 16, M06-2X/6-311+G(d,p), SMD dichloromethane during optimization, and
frequency characterization (zero imaginary frequencies for minima, one for TSs).

The reported reaction computations do not cover an entire photochemical/acid
network. The proposed upstream energy-transfer/silyl-transfer diagram, silicon
byproduct measurements, substrate/nucleophile scope, crystallography and downstream
synthetic reactions are not additional computed reaction outcomes. They are not
silently converted into barrier references or extra task goals.

## Original figures actually viewed

All three originals were listed with document_query. Main PDF page 8 and SI PDF
pages 5, 43 and 44 were rendered from source.pdf and viewed as private images.
Page-marker evidence text is preserved exactly as a location marker; the following
scientific observations come from viewing the corresponding original, not from
interpreting marker text as chemistry.

- pdf-page-doc_31695a0a949d-p5: the preparation scheme shows terminal phenylacetylene,
  HCF2-C(=O)-SiMe2Ph and the isolated siloxy cyclopropene. The saturated ring carbon
  bears CF2H and OSiMe2Ph; phenyl is attached to an alkene carbon. The printed name
  (ev_doc_31695a0a949d_000035_a566188741cd) has that same connectivity. The 82% isolated preparation
  is reported in ev_doc_31695a0a949d_000036_68355f8b412b.
- pdf-page-doc_66884e111ce4-p8: Figure 4A shows the isolated siloxy substrate, the proposed
  cyclopropenium working model, three methanol-attack sites, and the three neutral
  products. Displayed TS relative ΔΔG‡ values are 0.0, 1.3 and 7.1 kcal/mol;
  product ΔΔG values are 0.0, 3.2 and 7.2 kcal/mol. The minor-starting-material
  experiment uses MeOH 3.0 equivalents/TMSCl 5 mol%, DCM 0.1 M, room temperature,
  five minutes, with 91% major, 1% remaining minor, and no third product observed.
  Figure 4B is the separate gram-scale 82% major/2% minor experiment.
- pdf-page-doc_31695a0a949d-p43: the top interconversion drawing agrees with main Figure 4.
  Figure S8 proposes the wider acid-exchange/photochemical sequence and displays
  product differences of 0.0/3.2/7.2 kcal/mol. These displayed proposal arrows are
  not a calculated full network. The computational methods begin immediately below.
- pdf-page-doc_31695a0a949d-p44: Figure S9 depicts optimized methanol/cyclopropenium TS
  models and corresponding two-dimensional attack-site sketches. The first site
  is the CF2H-bearing ring carbon, the second is the remaining initially H-bearing
  carbon, and the third is the phenyl-bearing carbon. These attachment sites
  correspond to the three supplied product graphs. The TS-1 O-H···F contact is
  labelled 2.39 Å; forming C-O distances are 1.91/1.94/1.82 Å. The figure repeats
  the 0.0/1.3/7.1 relative Gibbs activation-energy differences and the stated DFT
  level (ev_doc_31695a0a949d_000362_246313387c27). No figure or optimized geometry is released.

The supplied computational section has schematic/ball-and-stick optimized
depictions, not Cartesian coordinate tables or original calculation decks. A
targeted coordinate search was made in both supplemental document texts, and the
actual computational-method/results pages were inspected. No unavailable Cartesian
record is claimed to have been inspected or inferred. Unambiguous two-dimensional
graphs, independently cross-checked with the depicted optimized attachment sites,
suffice for startable chemical identities. No molecular optimization, barrier
recalculation or author-reference reproduction was performed by this Builder.

## Identity mapping and neutral assets

Source A maps to public `siloxy_start`; source 3a to `methoxy_major`; source 3a′
to `methoxy_minor`; source 3a″ to `methoxy_comparator`. Those source labels never
appear in the autonomous public files. The silyl precursor and major product share
the same ring graph: CF2H and the O-substituent are geminal on the saturated carbon,
and phenyl is on the alkene. In the minor, CF2H and phenyl are on different alkene
carbons and methoxy/H on the saturated carbon. In the third comparator, methoxy
and phenyl are geminal on the saturated carbon and CF2H is on an alkene carbon.
This is graph verification, not merely acceptance of a printed product name.

SMILES in system.json are manually graph-encoded from those inspected depictions;
no optimized coordinates or author calculation recipe is encoded. Stereo is left
unspecified because this task concerns regioisomer connectivity/stability, not an
unreported absolute stereochemical assignment. The JSON file's per-file public
asset provenance binds its hash and inspected source evidence. No public image
or original source asset is distributed.

## Private definition correction

The frozen question names the author's charged intermediate and foregrounds one
addition step. The final question uses the ordinary experimentally isolated
substrate, withholds that hypothesis, and unites the formation-selectivity and
product-stability/redistribution investigations. The ledger has exactly one row
per changed question/input, preserving PI1-PI5, their kinds and order. No source
reference value or Stage05 record is modified. Source-supported identity and
observation details make the same system startable; they do not introduce a new
reaction or task variant.

PI4's 83% yield/>20:1 ratio is the small-scale observation from
ev_doc_31695a0a949d_000040_6424f07e658a. PI5's 82%/2% context is the separate gram-scale
observation. The redistribution endpoint is a shared neutral observation needed
for the connected stability question, not a reproduction-only input.

## Source limitations and ambiguity retained

The SI prose in ev_doc_31695a0a949d_000354_8b82efb49116 says 3a rather than 3a′ as the starting
material, calls 0.6 mmol MeOH 0.6 equivalents for a 0.2 mmol substrate, and omits
TMSCl. The adjacent original drawing, main Figure 4 and main discussion all
identify 3a′ as the substrate and 3.0-equivalent MeOH/5-mol% TMSCl. The public
endpoint and its conditions are grounded in these mutually consistent explicit
depictions and main text. The conflicting prose is preserved here and in
workflow_review; it is not used to invent a different experiment. It does not
contradict the source product graphs or reported computed differences.

No complete time course, detection limit, equilibrium constant, full interconversion
barriers, absolute activation barriers, numerical uncertainty, thermochemical
temperature, standard-state convention or explicit acid/counterion recipe is
reported in the inspected computation. The relative TS labels explicitly use G;
they are not relabelled electronic energies or interpreted as absolute barriers.
Frequency counts are reported, but an IRC procedure is not. The reference does
not make an unreported validation step a universal public requirement; validation
depends on the solver's actual claims.

## One core, two public views, one evaluation

The autonomous task contains only the problem and neutral starting facts. The
private source-bound reproduction_protocol provides the complete guidance block
for deterministic insertion immediately before the Public inputs heading. The
program changes no other task text, inputs, schema, guide, references, scoring or
deliverables. Guidance quotes use exact source text; figure transcriptions and
reporting-limit assessments are explicitly identified and bound to viewed pages.
Every material guidance statement is reproduced verbatim in its protocol ledger.

Shared evaluation awards 60 research-quality and 40 scientific-outcome points.
Formation selectivity, three-product relative stability and their integrated
relationship are core outcomes. The CR2/CR3 product energy/ranking reference stays
in the explicitly requested stability outcome; it is not demoted to an optional
descriptor. The author-selected model, TS differences, geometric/interaction
descriptors, conjugation/EWG interpretation and equilibrium interpretation are
unweighted conditional context. No separate rule rewards them. CR1-CR3 are all
covered. Fidelity is considered only when the protocol is disclosed; a blind
solver never loses credit for choosing another valid approach. Alternative
supported conclusions can resolve the question; honest unresolved work can earn
process credit without automatically solving it. Scoring binds only required
shared-schema fields and actually submitted artifacts, with no hidden numeric
tolerance or author-agreement shortcut.
