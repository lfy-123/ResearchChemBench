# Submission guide

The submission contract records the present task. It records what you actually did; it does not prescribe a research matrix.

Link your explanation of the donor redox/photophysical behaviour to numerical quantities on defined scales and to the actual fluorescence observations. For computed thermodynamic, excited-state or association claims, include the inputs, raw outputs, state/composition definitions and the analysis that connects those quantities to the claim. For a plot-based statement, retain the graphical extraction or explain its qualitative limit; do not invent lifetime points or error bars. Source-data analysis alone must go beyond reciting printed potentials and must justify how far it answers the question.

Use free identifiers for your ideas, methods, models, executions, measurements and findings. Model source_system_id refers to a supplied identity; your model description may introduce physically justified states, conformers or representations within its boundary. Report composition, charge/spin, medium and every approximation. A finding may be supported, refuted, mixed, unresolved or withdrawn. There is no minimum number of ideas or required change of direction.

Each numerical measurement has observable, definition/reference, value (scalar or numeric array), unit, conditions, method/model references, uncertainty and evidence links. Use a numeric table artifact and an extraction/analysis script for spectra, tensors, ensembles or other large data. Do not hide the audit trail inside an unconstrained prose object. A missing number is not zero; omit an uncomputed measurement and explain it in incomplete_work. Uncalibrated uncertainty has kind=not_calibrated, magnitude=null and an explicit explanation; it does not excuse unwarranted precision or a unsupported complete claim.

Each evidence record identifies a workspace-relative file under outputs/, analysis/, structures/ or data/, SHA256, its kind and actual origin. Copy any public input used into the submission data/ with its original hash. Use unique IDs, resolve every link, and include raw native inputs/outputs for calculations or original data plus executable scripts for analyses. A plotted image or results.json alone is insufficient for a computed claim. Distinguish supplied observations, new calculations and external sources. Report failed attempts honestly. Record execution/tool-trace references where available; a self-authored research log is a summary, not independent proof of chronological decisions or blind prediction.

Complete submissions need relevant structured measurements and evidence-supported findings that address the question. The schema tests the presence/shape of records, not their scientific sufficiency. Partial work may establish bounded local findings; list the unresolved scope. Zero-launch blocked/failed reports may have no methods/models/calculations, but must explain the actual obstacle, attempted diagnostic and recovery condition; they cannot assert scientific completion. An evidenced inability to distinguish models can be complete only when the data and investigation actually justify that limitation. No credit is awarded merely for filling fields, listing hypotheses or matching author numbers.

The readable report must link to the same results and artifacts, explain decisions and limitations, and state what evidence could change its conclusions. Do not include internal chain-of-thought.

# Source and model correspondence

Use models.mapping_and_approximations to identify any surrogate substrate or counterion treatment. Keep electronic and Gibbs association quantities separate in measurements.definition_and_reference, and record the fragment/standard-state convention where used. Preserve both steady-state excitation annotations in measurements.conditions or findings.scope_and_limitations; the separate TCSPC setting cannot silently replace them. A documented source conflict or justified alternative receives credit only for the scientific evidence actually provided.

V3 evaluates the required final results in the task. Linked structures, calculations and analysis support those conclusions and have no independent process score.

PR also reports the two disclosed PhCl models and their balanced electronic and Gibbs association energies. These four final properties retain independent numeric scoring; reproducing an optimization alone earns no points. The proxy does not replace the measured 4-chloroanisole question.

`research_log` may be empty, including for a complete submission. It is a concise process summary, not a required scientific result. Required results, actual execution records and linked native evidence remain mandatory.
