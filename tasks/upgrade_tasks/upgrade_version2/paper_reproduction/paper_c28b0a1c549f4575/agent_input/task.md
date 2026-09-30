# Scientific objective

What molecular account of propylene-carbonate association with the TEA/DED/BF4 components is supported in the stated mixed-electrolyte context? Determine whether and under which model assumptions the change of cation composition can alter the local PC environment, and what cannot be inferred from that evidence.

# Author-provided scientific guidance

The authors propose that DED2+ binds PC more strongly and changes TEA+ solvation, with concentration-dependent behavior and an optimum near0.2 M addition in the broader experiments. This interpretation must be tested within the bounded molecular question. SI pp5–6 reports Gaussian16 B3LYP-D3BJ/def2-SVP optimization and frequencies, B3LYP/6-311+G(2d,p) ion/solvent binding energies, separate B3LYP-D3BJ/def2-TZVP electrode adsorption, and B3LYP/6-311G** optimized frontier levels. These are distinct protocols; do not silently mix their reference energies. Separate GROMACS/GAFF/RESP bulk simulations are outside the required molecular baseline. The SI time-step text says2 nm, a dimensional error, not a validated simulation parameter. Old fixed PC-loading and exchange panels were builder additions. Reproduce or justify substitutions for the relevant molecular baseline, leaving new validation choices explicit.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

# Public inputs and scientific boundaries

Components are tetraethylammonium TEA+, C8H20N+; 1,4-diethyl-1,4-diazabicyclo[2.2.2]octane dication DED2+, C10H22N2(2+); BF4−; and propylene carbonate PC, C4H6O3. All supplied starting species are closed-shell singlets. The source uses PC with 1 M TEA-BF4 and DEDABCO-(BF4)2 additions up to0.3 M; DED requires two BF4 per neutral salt unit. Source NMR/Raman observations vary with composition. Investigate local molecular association, with independently chosen composition and configurations of any model. The source does not establish a single PC stereoisomer; disclose any stereochemical choice.

Read `data/inputs/objects.json` for atom-indexed chemical identity and the other supplied input files for known facts. Generate and justify the models needed for your investigation.

A local finite model does not determine a bulk concentration optimum, electrode adsorption, electrochemical window, charge storage or device energy density. Do not infer those properties from a frontier gap, one optimized cluster or a raw energy difference between unequally charged salts.

# Required scientific validation/investigation

Develop and execute a scientifically justified investigation that answers the question within these boundaries. You choose the explanations or models to examine, their number, the methods, searches, comparisons and evidence needed, and how the investigation changes in response to findings. Justify the adequacy and limits of the evidence for your claims. AR chooses its route independently. PR must reproduce the disclosed author baseline or justify scientifically grounded substitutions; additional investigations are independently designed. Neither mode is required to recover an author outcome or follow a fixed candidate/control grid.

Support each association inference with a chemically matched reference and appropriate structure/state/numerical evidence. Distinguish electronic interaction, thermodynamics and bulk speciation; justify the model and any comparison to concentration-dependent spectroscopy. If results depend on composition, solvent treatment or configurations, bound the conclusion accordingly rather than prespecifying one grid.

A well-supported negative or unresolved answer is eligible for scientific credit. Explain what the evidence establishes and what it leaves open. Nonconvergence, missing calculations or a self-declared uncertainty flag do not establish non-identifiability. Report genuine model/basin collapse with the corresponding evidence.

# Deliverables

Submit `report/results.json` under the structured submission contract and a readable `report/report.md`. Preserve actual inputs, native outputs, identity/state mappings, analysis code and execution records. Quantitative evidence must be recoverable from linked artifacts. Record concise decisions, failures, revisions, resource use and limitations; consult `submission_guide.md` and `resources.md`.
