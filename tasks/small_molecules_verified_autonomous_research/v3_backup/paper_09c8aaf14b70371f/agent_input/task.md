# Scientific question

Using computational chemistry evidence, estimate the relative reduction tendency and cathodic peak-potential ordering of the five supplied E-chalcones, compare it with the measured ordering, and explain agreements or departures in terms of molecular structural differences and solvent effects. This is an explanation task: the measured peak potentials are given; the computational relationship and its physical interpretation are to be established.

# Input files

`data/inputs/chalcone_series.json` supplies mapped identities for compounds 1–5, neutral singlet starting-state labels, solvent identities, cyclic-voltammetry conditions and measured Epc values. ACN and DMSO measurements cover all five compounds; the DCM comparison concerns compound 3 only. Atom-map labels are local to each molecule. Null experimental conditions are unknown.

# Scope

Investigate the five supplied molecular structures under comparable solution models. Choose and justify conformers, electronic descriptors, states and computational methods. Distinguish orbital energies from electrochemical peak potentials and an identified conformer from a conformational ensemble. The scope is a bounded structure–property explanation; absolute redox-potential calibration, electron-transfer kinetics, synthesis, photodynamics and a complete electrochemical mechanism are not required.

# Required results

1. Report calculated electron-acceptance descriptors for all five compounds and the peak-potential ordering they would suggest, including unresolved ties. Compare with the measured ordering, and establish the supported structure–reduction relationship within compounds 3–5. A descriptor-based ordering may disagree with experiment; explain its supported domain rather than forcing agreement.
2. Determine whether that relationship also describes compounds 1 and 2; include an explicit computational model of each member and identify any counterexample.
3. Assess the magnitude of ACN/DMSO changes across all five compounds and the direction of the additional DCM/ACN/DMSO comparison for compound 3. State what the calculation can resolve about these solvent effects.
4. Propose an explanation based on molecular structural differences for the potential differences tied to your actual calculations, with the supported domain and unresolved causes made explicit.

Report molecular/state identities, calculated quantities, units, conditions and comparable references. Evidence should support each final inference and preserve access to the native calculations.

# Submission and permitted resources

Submit `report/results.json` and `report/report.md` using `submission_schema.json` and `submission_guide.md`. Use the supplied inputs and available computational tools; choose your own hypotheses and methods.
