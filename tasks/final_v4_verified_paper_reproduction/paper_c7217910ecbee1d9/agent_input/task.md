# Scientific question

How does attaching one or two B(C6F5)3 ligands change electron acceptance by isolated gas-phase PAl12, and what electronic effects account for the changes across n = 0, 1 and 2?

## Input files

- `data/inputs/system_specification.json` supplies the full PAl12 core, BC18F15 ligand graphs, atom maps, compositions and electron-count/spin-parity constraints. The n = 0, 1 and 2 species contain 13, 47 and 81 atoms. Charges 0 and −1 define electron attachment; equilibrium structures and spin states remain to be determined.
- `data/inputs/electron_acceptance_conventions.json` defines energy/state bookkeeping and the validity of the chosen comparisons.
- `data/inputs/resource_limits.json` describes the available execution interfaces and resource boundary.

## Scope

Keep the full ligand and metal-core composition. Investigate the neutral and anionic states needed for an affinity comparison across all three n values and report the state/structure domain actually covered. Do not extrapolate one composition to the entire family. Choose the relevant structural and electronic comparisons; no particular binding site, spin list, method or search order is prescribed. Graphene, other cores/ligands, synthesis and device behavior are outside scope.

Use zero-point-corrected adiabatic electron affinity in eV for the family comparison: AEA = (E + ZPE)neutral − (E + ZPE)anion, with each species evaluated at its own relaxed state and with a free electron as common zero. State selection must follow the calculated evidence. Distinguish additional vertical, electronic-only or constrained quantities from this comparison.

## Author baseline

The author gas-phase aluminum-cluster calculations use Gaussian 16, PBE0/def2-SVP, exploration of spin multiplicities and ligand binding positions, same-level frequencies and ZPE corrections (SI Computational details). Main Figs. 1–4 report approximate AEA values 1.76, 3.22 and 3.93 eV for n = 0, 1 and 2. These are disclosed theoretical references, not proof that a new calculation reproduces them. The SI gives structural figures but no complete Cartesian table; constructed starts must be identified as reconstructions.

The proposed explanation is local charge redistribution toward the Lewis-acid ligands, downward shifts of electronic levels and retained superatomic character. Hirshfeld, ESP, MO and full-fragment CDA analyses with Multiwfn/VMD support it. The source-marked unoccupied levels are approximately −2.76, −3.81 and −4.41 eV; these are not AEA. Neutral fragment binding and neutral-to-anion attachment probe different density changes. Any fragment analysis must retain full PAl12 and BC18F15 identities and declare fragment states and geometry conventions.

Reproduce the relevant disclosed baseline or justify a scientifically comparable substitution, reporting disagreements as well as agreement. Structural retention and a few orbital projections alone do not establish complete shell preservation. The separate PBE-D3/PAW stability calculations and AIMD are outside the requested gas-phase affinity/explanation scope.

## Required results

- Report the AEA and electron-binding conclusion for each n, with the neutral/anion states, energies and individual ZPE terms supporting that value.
- Quantify and interpret separately the first-ligand change AEA(1) − AEA(0) and second-ligand change AEA(2) − AEA(1), including the resolution of each comparison.
- Determine the nature and ligand-count dependence of electronic redistribution when neutral fragments bind. Distinguish it from the response to adding an electron to a ligated cluster.
- Explain the electron-acceptance changes using computed electronic-level and bonding evidence with explicit state/spin correspondence. Treat orbital eigenvalues and total-energy affinities as different quantities.
- State what the actual evidence establishes about retention or change of superatomic electronic character, and what would be needed to infer a complete shell configuration. Bound this inference to the studied PAl12 family.

## Submission

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Link actual inputs, native outputs, structures, atom maps and analysis artifacts with SHA256. Evidence of structural/state validity must be appropriate to each conclusion; structures or normal termination alone are not final scientific results. Only final conclusions receive points. Report supported partial findings and remaining uncertainty honestly without replacing missing family members by extrapolation.
