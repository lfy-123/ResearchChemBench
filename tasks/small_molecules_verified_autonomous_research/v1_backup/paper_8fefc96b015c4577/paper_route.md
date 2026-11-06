# Private paper route

## 1. Scientific objective and author claim

The paper studies why the photoredox cascade from allylamine 1a gives hydroisoquinoline 3a rather than closure onto the competing arenesulfonyl ring. The authors claim that, after radical addition gives intermediate B, the two cyclization transition states are electronically similar in topology but differ in feasibility; the benzyl-tethered aryl closure is favored, whereas the alternative closure is higher in free energy. The comparison is intended to explain product selectivity, not to model the complete photochemical reaction kinetics.

## 2. System and model boundary

The computed system is the neutral doublet radical molecular model used for the free-energy profile of the 1a pathway: intermediate B and the two cyclization transition structures TS2 and TS2′, each containing the sulfonyl group, difluoroester-derived fragment, tertiary amine framework, and two pendant aryl groups. Coordinates are reported in the SI in ångström and free energies in hartree. The paper treats the 3a pathway with an implicit DMSO environment. This boundary excludes explicit photocatalyst, zinc acetate, photons, solvent molecules, and subsequent oxidation/aromatization steps.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate stationary points for the free-energy profile | Structures A, 1a, TS1, B, TS2, C, TS2′ from the SI coordinate appendix | Gaussian 16 geometry optimization | Dispersion-corrected B3LYP-D3; def2-TZVPP; SMD; DMSO for the 3a/hydroisoquinoline pathway | Optimized geometries and Gibbs free energies | SI computational details, SI S34; coordinate blocks SI S36–S41 |
| 2 | Classify each stationary point | Optimized structures from step 1 | Gaussian 16 frequency calculation at the same level | One imaginary frequency for a transition state; zero for a minimum | Vibrational frequencies and thermochemical corrections | SI computational details, SI S34 |
| 3 | Compare the two competing cyclizations | B, TS2 and TS2′ free energies | Relative Gibbs free-energy subtraction | Common reference B; report in kcal mol−1 | Two barriers and their difference | Main paper mechanistic paragraph; SI coordinate/free-energy blocks S36–S40 |

## 4. Validation and analysis protocol

The authors use the frequency analysis to assign minima versus transition states. Intermediate B is a minimum and each of TS2 and TS2′ is a first-order saddle point. Relative barriers are obtained by subtracting the Gibbs free energy of B from each transition-state Gibbs free energy and converting hartree to kcal mol−1. The interpretation is comparative: the lower cyclization barrier is the more feasible route within this model and is used to rationalize hydroisoquinoline formation. The calculation does not establish a complete rate law or prove that the electronic-structure model captures all solution-phase dynamics.

## 5. Private reference results

The published energy heights relative to separated reactants are B = −13.13, TS2 = −0.05 and TS2′ = 6.12 kcal mol−1. Therefore the task-defined barriers relative to B are TS2 = 13.08 and TS2′ = 19.25 kcal mol−1. SI Gibbs energies independently confirm this subtraction: G(B) = −1768.468122, G(TS2) = −1768.447278 and G(TS2′) = −1768.437447 hartree. Thus the TS2′ pathway is higher by 6.17 kcal mol−1, and the paper interprets the lower TS2 pathway as the benzyl-tethered aryl cyclization leading toward intermediate C and ultimately 3a. The SI reports the relevant optimized Gibbs energies in hartree and the main text reports the converted relative values.

## 6. Limitations and interpretation boundaries

The source gives starting/optimized geometries and a single DFT protocol, but it does not establish conformer completeness, intrinsic-reaction-coordinate connectivity, anharmonic corrections, standard-state conventions beyond the authors' calculation, or method sensitivity. A reproduction may therefore compare the supplied stationary-point identities and relative barriers while reporting convergence, frequency classification, and any alternative stationary points. Numerical agreement is a validation of the published model result, not a standalone proof of experimental selectivity.

## Current public/private boundary (2026-09-26)

The original SI geometries are private author_results only. Public input is a fresh ETKDGv3/UFF radical starter generated from the chemical graph, not a perturbed author endpoint. Historical author-informed Opt/Freq and negative-mode analysis validate the same two cyclization observables; they do not constitute blind replay from the new public starter. No new IRC requirement or coordinate-RMSD scoring is introduced.
