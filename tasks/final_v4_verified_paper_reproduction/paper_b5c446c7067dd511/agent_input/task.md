# Electronic relaxation in four substituted emitters

## Scientific question

Which molecular electronic relaxation pathways are supported for Ph-mP, Na-mP, An-mP and Py-mP, and how does extending their aromatic substituent affect that assessment?

## Input files

- `data/inputs/Ph-mP_identity.json`, `Na-mP_identity.json`, `An-mP_identity.json` and `Py-mP_identity.json` give complete atom-mapped graphs for C34H24N2, C38H26N2, C42H28N2 and C44H28N2, respectively.
- `data/inputs/problem_context.json` gives molecular scope and solution-measurement context. The THF concentration is measurement context, not a prescribed computational solvent.

## Scope

Study the four neutral molecules in the isolated-molecule limit for the vertical spectroscopic comparison, defining their reference geometry and electronic state. Relate other environments only where supported. Distinguish vertical excitation energies at a common S0 geometry from relaxed energies and measurements in solution or a solid. For the isolated-molecule comparison at a common neutral S0 equilibrium geometry, use S1 and T1 for the lowest singlet and triplet excitations. Define T_edge as the upper boundary of the triplet manifold below S1: the highest-energy triplet below S1, excluding T1. Establish that boundary from the neighboring response states, without assuming a root index or a local/charge-transfer assignment. If no such state exists, or state crossing changes its identity, report that result explicitly. This is a spectroscopic comparison state; its definition does not establish a relaxation pathway. When comparing geometries or methods, distinguish a change of energy ordering from physical state correspondence using transition-density/NTO or equivalent response evidence. Do not replace a tracked state with a different state just because its energy is closer. This question concerns molecular electronic evidence; numerical RISC rates, kinetic dominance and device efficiencies require evidence beyond energy proximity or state mixing and are not required outputs.

## Required results

For each molecule:

1. Give S1 and T1 vertical excitation energies and the vertical energy of T_edge, in eV relative to the same neutral S0 reference. Identify the state and report the dimensionless S0→S1 oscillator strength.
2. Determine the spatial local/charge-transfer character of S1 and T_edge using an explicitly defined, normalized analysis of the actual response. Report what moves between molecular regions and what remains localized.
3. Evaluate the molecular relaxation candidate using the S1/T1/T_edge energy relationships together with the state character and any other evidence needed for your specific claim. You may support or reject a route involving T_edge, or justify a different candidate; identify any different route state separately from the spectroscopic comparison state. Separate an electronic candidate from a demonstrated rate or dominant kinetic route.

Across all four molecules, explain how aromatic substitution changes the electronic character and the resulting assessment. Determine whether a common substituent trend is supported and identify the limits set by the calculated model. Neither a fixed state count nor a fixed control matrix is prescribed.

## Author baseline for reproduction

The authors used Gaussian09W gas-phase B3LYP/6-31G(d,p) geometry optimization and TD response, followed by Multiwfn NTO/IFCT analysis. Their fragments are the phenanthroimidazole core, methylphenyl group, and appended aromatic/benzene-bridge region. Main p3 and Fig3 on p4 discuss mixed local/CT S1 states and a high-triplet RISC candidate: T4 for Ph/Na and T3 for An/Py. These source triplets are T_edge under the neutral energy-order definition above; their root labels do not prescribe correspondence after a model change. Reported S1−T1 gaps are 0.88, 0.89, 1.34 and 1.11 eV. Reproduce that baseline or justify a physically comparable substitution; the same final quantities are required in both modes.

SI pp2–6 gives the ten-singlet/ten-triplet calculation table; full-table replication is not required here. Main text/Fig3 gives Py-S1 CT/LE 57.23/45.77 and An-T3 50.09/49.01 in the prose, which do not sum to 100%; SI provides 54.23/45.77 and 50.99/49.01. Preserve these source inconsistencies rather than force an exact percentage match. Source pathway proposals are not measured rates. Subsequent SOC, constrained-geometry and alternative-functional controls are optional extensions, not author-protocol requirements.

## Submission

Submit `report/results.json` and `report/report.md` following `submission_guide.md` and `submission_schema.json`. Support final answers with inspectable native calculations and reproducible analyses. Final scientific results total 100 points; research-process completion carries no independent points. Use supplied inputs and available tools; general scientific/software documentation is allowed. Private evaluator files, prior verification archives and undisclosed target-paper answers are not public resources.
