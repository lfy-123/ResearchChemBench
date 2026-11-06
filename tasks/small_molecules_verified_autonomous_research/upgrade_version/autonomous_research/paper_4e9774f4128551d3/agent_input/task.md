# Scientific question

Why does reversible epimerization of ketoester 50 behave differently from its two-stage enolization/protonolysis treatment, and, under explicit ideal separation/recycling assumptions, is the calculated three-cycle cis recovery compatible with the reported isolated yield? Explain the supplied observations using molecular calculations and quantitative analysis. The experimental outcomes are known; their explanation is the task.

# Input files

- `data/inputs/systems.json` supplies mapped stereochemical identities for 50, the tetrasubstituted O-TMS enol ether, racemic camphorsulfonic acid and solvents.
- `data/inputs/source_facts.json` supplies reagent amounts and operations.
- `data/inputs/observations.json` supplies the reversible-condition outcome, single-pass trans:cis ratio and cumulative isolated yield.

# Scope

Preserve the polycyclic skeleton and all remote stereocentres while changing only the specified local stereochemistry. No optimized conformer is supplied. Choose your models and computational methods. Two conflicting THF/MeOH volume ratios, 1:1 and 10:1 (6.0/0.60 mL), remain unresolved. The required question is local stereochemistry and recycling; full diterpenoid synthesis, acid screening and exact isolated-yield prediction are outside scope.

# Required results

1. Compute G(cis)-G(trans) for the correctly mapped epimers, using 298.15 K and a methanol continuum as a defined endpoint comparison. Identify its limits relative to the 23 °C mixed-solvent operations.
2. Explain quantitatively why reversible conditions and the separate-pot sequence can give different stereochemical outcomes. Establish what the endpoint energy difference implies, and whether it determines the observed single-pass ratio. A kinetic consistency analysis is permitted; no prescribed transition-state search is required.
3. Calculate the ideal three-cycle cumulative cis fraction under complete conversion per pass, complete cis separation, complete trans recycling and no loss. Declare the single-pass fraction and its source: the supplied experimental fraction may be used for consistency analysis; an independently calculated fraction must describe the actual two-stage process. Compare the ideal result with the reported cumulative isolated yield, then explain what incomplete conversion, recovery or loss could change without fitting unmeasured losses as an independent prediction. Do not substitute the endpoint Boltzmann equilibrium ratio for the single-pass protonolysis ratio. No new protonolysis transition-state search is required.

Retain actual molecular/computational evidence. Define identities, charge/spin, units, energy references and thermal/standard-state conventions. Distinguish equilibrium populations, formation selectivity and cumulative isolated yield. State unresolved findings, including the solvent-ratio conflict.

# Submission and permitted resources

Submit `report/results.json` and `report/report.md` under `submission_schema.json` and `submission_guide.md`, with native calculation artifacts and reproducible analysis. Supplied inputs and general scientific/software documentation are permitted; hidden evaluator references and prior run outputs are excluded.
