# Scientific objective

What molecular explanation of the absorption differences among complexes1a–1d in toluene is supported by the supplied observations and an independent investigation? Establish defensible state/band assignments and the limits of any proposed structure–spectrum relationship.

# Author-provided scientific guidance

Main pp2–3 and SI p2 report Gaussian16 B3LYP/6-31+G(d,p) DFT/TD-DFT and confirmation of minima by real vibrational frequencies. The source writes the basis as6-31G+(d,p) in one SI line; disclose the intended diffuse-basis convention. The authors associate the red shift relative to1a with expanded aromatic conjugation and attribute the weak lower-energy1c band to a low-intensity S0–S1 HOMO–LUMO transition; higher S2/S3 transitions carry more intensity. Treat these as source assignments to reproduce/test, not ground truth independent of method. SI pp57 onward contains optimized answer coordinates/energies, distinct from public topology. Toluene is the measured medium; the retrieved method paragraph does not specify a complete solvent implementation, so state any chosen solvent model as an explicit modeling decision. Earlier common-geometry interventions were builder extensions, not an author protocol.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

# Public inputs and scientific boundaries

Complete graphs define1a C11H8BF2NO and1b–1d C15H10BF2NO, all neutral singlet starting molecules. The three larger compounds have distinct fused-ring connectivity, despite sharing a formula. The public table contains measured toluene absorption features: the lower-energy bands for all four compounds and the stronger higher-energy band of1c. These observations are public retrospective evidence. Geometry, electronic states and spectral interpretation are to be investigated; no common-geometry model or root count is prescribed.

Read `data/inputs/objects.json` for atom-indexed chemical identity and the other supplied input files for known facts. Generate and justify the models needed for your investigation.

Conclusions cover solution absorption of these four molecules. A frontier gap, vertical transition or inferred geometric effect does not establish emission efficiency, crystal polymorphism, white-light generation or OLED performance. Distinguish observed band maxima from computed vertical energies and from a chosen broadening model.

# Required scientific validation/investigation

Develop and execute a scientifically justified investigation that answers the question within these boundaries. You choose the explanations or models to examine, their number, the methods, searches, comparisons and evidence needed, and how the investigation changes in response to findings. Justify the adequacy and limits of the evidence for your claims. AR chooses its route independently. PR must reproduce the disclosed author baseline or justify scientifically grounded substitutions; additional investigations are independently designed. Neither mode is required to recover an author outcome or follow a fixed candidate/control grid.

A spectral assignment must compare the same kind of observable and show relevant state character/intensity or other sufficient evidence. Explain model-dependent shifts and uncertainty rather than selecting whichever computed root is closest after the fact. Validate the adequacy of structures, methods and analysis for the claims using a defensible route of your choice.

A well-supported negative or unresolved answer is eligible for scientific credit. Explain what the evidence establishes and what it leaves open. Nonconvergence, missing calculations or a self-declared uncertainty flag do not establish non-identifiability. Report genuine model/basin collapse with the corresponding evidence.

# Deliverables

Submit `report/results.json` under the structured submission contract and a readable `report/report.md`. Preserve actual inputs, native outputs, identity/state mappings, analysis code and execution records. Quantitative evidence must be recoverable from linked artifacts. Record concise decisions, failures, revisions, resource use and limitations; consult `submission_guide.md` and `resources.md`.
