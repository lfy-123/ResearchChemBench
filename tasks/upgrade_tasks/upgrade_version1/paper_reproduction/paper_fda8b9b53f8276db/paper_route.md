# Private development paper route

The authors compare a gas-phase cis local minimum with crystal intramolecular bonds using Gaussian03 B3LYP/6-311+G(2d,p). The crystal pyridyl orientation differs; a local minimum need not be globally lowest. The paired cis/trans solvent and torsion controls are benchmark extensions.

## Expanded first-version scope

Determine whether local bond residuals and cis/trans preference are attributable to torsional conformation or medium, keeping the original six-bond cis validation separate from thermochemistry.

Use neutral singlet 6,7-dimethyl-2-(pyridin-2-yl)quinoxaline, C15H13N3, from CCDC2433822. Cis/trans is the mapped N1-C1-C2-N2 torsion; preserve deposited labels. Primary gas phase and acetonitrile continuum at 298.15 K, consistent 1 M molecular convention for solution. Six bonds are exactly those in experimental_bonds.json; seven SI or 33 CIF bond sets must not enter this RMSE.

## Status and evidence

implemented_pending_expanded_reference. Main p4 computational structure discussion; SI Table S2 and FigsS11-S13; immutable CCDC2433822 and current final experimental_bonds.json define the six-bond scope.

Expanded reference computations and uncertainty calibration pending.

The original route and numeric anchors are archived in evaluation/legacy_final_snapshot/paper_route.md.snapshot; they do not certify the new endpoints.
