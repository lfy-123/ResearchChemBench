# Methoxy substitution and epoxy-fragment polarity

## Scientific question

How does ortho-methoxy substitution change the permanent polarity of the supplied EPI1/EPI2 fragments, what molecular features explain that change, and what does it imply for interpreting the supplied resin dielectric observations?

## Input files

- `data/inputs/systems.json`: full neutral-singlet molecular graphs and a common representative stereochemistry; these do not prescribe a three-dimensional conformation.
- `data/inputs/observations.json`: qualitative dielectric and temperature-dependent FTIR observations for cured materials. These are given context, not isolated-molecule dipole measurements.

## Scope

Study these full fragments under explicitly matched conditions. Distinguish a local conformation, a sampled population and a cured material. State environment and, for population averages, temperature and weighting. Quantitative polymer-network dielectric constants, water uptake and mechanical properties are outside scope.

## Author baseline for reproduction

The authors attribute lower polarity in one EPI2 conformation to an intramolecular interaction between the curing-generated OH and the ortho-methoxy group (main pp6–7, Figure 4D–E). The reproduction baseline is the gas-phase permanent dipole at a relaxed local geometry. The reported permanent dipoles are 2.2223 D for EPI1 and 1.9036 D for EPI2. Reconstruct the full models from the supplied identities and reproduce this single-conformation comparison; distinguish it from any optional population extension.

Main p4 specifies Gaussian16 A.03, B3LYP-D3(BJ)/6-31G* geometry and frequency calculations, ma-def2-TZVPP dipole calculations and Multiwfn ESP analysis. The Figure 4 caption instead names CAM-B3LYP/6-311G(d,p). Declare which protocol is reproduced and report the conflict. SI pp23–26 contains the source structures. The resin FTIR observation is not an isolated-molecule spectrum.

Assess the computed comparison and its physical interpretation using actual evidence. State any justified method substitutions and distinguish optional extensions from the disclosed author baseline. Copying the target values does not establish reproduction.

## Required results

1. Compute the full permanent-dipole magnitude of each source-compatible fragment (D) and report their difference with a consistent sign convention. Distinguish the disclosed baseline from any optional population extension.
2. Explain the computed effect using molecular and electronic evidence, and state how configuration affects the reach of that explanation.
3. Determine what the molecular result supports about the supplied dielectric trend, using the appropriate response statistic and distinguishing molecular evidence from bulk behavior.

## Submission

Submit `report/results.json` and `report/report.md` following the supplied schema and guide, with linked native calculations and analyses. Only final scientific conclusions receive points. Choose methods independently within the mode's scope. Use public inputs and available runtime tools; do not access private evaluator files, verification archives or the other mode's guidance. General scientific/software documentation is allowed.
