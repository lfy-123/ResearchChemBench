## Scientific question

For the specified five- and six-membered cyclic-enone electron-deficient [3]dendralenes reacting with methanethiolate in chloroform, determine the favored addition sites and protonated-product connectivities. Explain the competition between simple addition and cyclization for the five- and six-membered cyclic-enone pair, assess whether second thiol addition to the five-membered substrate is competitive, and establish how reliable the predictions are. This is a computational prediction and explanation task; no measured product distribution is supplied.

## Input files

`data/inputs/system.json` specifies PI1 (cyclopentenone), PI2 (cyclohexenone), PI4 (methanethiolate and methanethiol), and PI5 (chloroform, 298.15 K, 1 M standard state). `molecular_structures.json` and the corresponding SDF files supply machine-readable graphs, mapped alkene stereochemistry and candidate addition-site labels. The listed alpha, delta and beta-prime sites are unranked candidates, not a prescribed winning site or a proof that other attacks are impossible. Distinguish initial sulfur addition sites from subsequent enolate ring-closure sites. SDF coordinates are two-dimensional depictions, not minima. Retain their molecular graphs and alkene stereochemistry; choose conformations, reactive states and methods independently. `submission_schema.json` and `submission_guide.md` define the submission format.

## Scope

Compare addition-site and protonated-product preferences for PI1 and PI2. Simple-versus-cyclic competition concerns PI1 and PI2; second addition concerns PI1 only. Other substrates, nucleophiles, exact experimental yields and workup chemistry are outside this question. State charge/spin and any proton/thiol reservoir assumptions. Balance each comparison: initial anions and neutral protonated products have different reference compositions. A 1 M standard state is not an experimental concentration.

## Required results

1. Give PI1's preferred or unresolved monoaddition site/product assignment and its computed relative energies.
2. Explain PI1's simple-addition versus cyclization outcome using evidence for accessibility and structure, distinguishing a stable endpoint from an accessible route.
3. Give the incremental free energy and thermodynamic competitiveness of a second MeSH addition to a PI1 monoaddition product; distinguish this from its rate or observed fraction.
4. Give PI2's relative stability of simple and cyclic product classes, including competing cyclic connectivities.
5. Determine which PI2 simple-addition or cyclic-product connectivities are supported as accessible, and explain the contrast with PI1 using evidence that bears on competing formation routes.
6. Compare the robustness of these outcomes using quantitative sensitivity evidence from informative comparisons. Explain how the quantified changes support or limit the conclusions; relevant comparisons within the results you generate may provide this evidence, with no prescribed additional method or rerun.

Choose your hypotheses, computational models and investigations. Report actual computed quantities, units, references and conditions. Validate stationary points and connectivity as needed for the claims; no fixed number of structures, hypotheses, transition states or searches is required. Do not infer formation selectivity solely from endpoint stability without a supported thermodynamic-control argument. A finite electronic-energy scan is not an exact Gibbs barrier.

## Submission and permitted resources

Submit `report/results.json`, `report/report.md` and actual inputs, outputs, logs and analysis code under `research/`. Link final claims to indexed native evidence. Use the supplied public files and independently generated calculations with your chosen software; no external source document is needed. Report actual resource use and unresolved limitations. Honest partial or failed work must preserve attempted inputs and logs. Scientific points are awarded only to supported final outcomes, with no separate process score.
