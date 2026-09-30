# Scientific objective

How do the molecular identities of PM, BM, TFPM and TFBM affect local lithium solvation in the presence of FSI, and what account of their differences is supported by a defensible molecular investigation? Determine the extent to which the evidence supports a common explanation across these four solvents.

# Author-provided scientific guidance

The authors propose dual RESPO/dipole descriptors and synergistic O/F lithium coordination, favoring a six-membered TFPM chelate. Source calculations use Gaussian16 B3LYP/6-311+G(d,p), geometry/frequency checks, and Eb=Ecomplex−ELi+−Esolvent; Multiwfn3.8 is named for RESP. The source RESPO axis is labeled eV, whereas RESP atomic charges are in e; reproduce the actual defined quantity or explicitly flag this ambiguity instead of treating them as interchangeable. Their separate GROMACS2018 OPLS-AA bulk simulations use30 LiFSI with145 PM/125 BM/129 TFPM/110 TFBM,8 ns NVT and40 ns NPT with final30 ns analysis. The molecular task does not require that MD protocol or the builder’s former1:1:1 FSI cluster grid. Reproduce the relevant disclosed molecular baseline or justify substitutions; any new local model is an additional investigation. Published computed chelation and populations are author interpretations/results, not required answers.

Interpret and reproduce the disclosed author approach within this task’s bounded question. Explain justified substitutions and distinguish replication, new checks and disagreement. Source agreement is not a substitute for valid evidence.

# Public inputs and scientific boundaries

The supplied graphs define PM C4H10O, BM C5H12O, TFPM C4H7F3O and TFBM C5H9F3O, Li+ and FSI−. The neutral solvents and closed-shell ions are singlet starting species. Source electrolyte formulations use 2 M LiFSI in each of the four ethers. Investigate molecular/local solvation within these components; distinguish a finite molecular model from the 2 M bulk liquid. Cluster composition, configurations, medium treatment and informative quantities are research decisions. There is no prescribed Li:FSI:solvent cluster ratio.

Read `data/inputs/objects.json` for atom-indexed chemical identity and the other supplied input files for known facts. Generate and justify the models needed for your investigation.

Limit claims to the local interactions and the actual range of sampled models. Isolated descriptors or small-cluster energies cannot prove bulk coordination fractions, ionic conductivity, SEI composition, oxidation stability, low-temperature cycling or cell lifetime. Do not treat source MD populations as experimental observations.

# Required scientific validation/investigation

Develop and execute a scientifically justified investigation that answers the question within these boundaries. You choose the explanations or models to examine, their number, the methods, searches, comparisons and evidence needed, and how the investigation changes in response to findings. Justify the adequacy and limits of the evidence for your claims. AR chooses its route independently. PR must reproduce the disclosed author baseline or justify scientifically grounded substitutions; additional investigations are independently designed. Neither mode is required to recover an author outcome or follow a fixed candidate/control grid.

Define the observable, molecular composition and reference of every comparison. Show adequate validity for any claimed structure or relative interaction, and justify transfer from selected models to the stated local question. If electrostatic or charge descriptors are used, distinguish potential units/locations from fitted atomic charges and document the calculation; an ESP extremum is not automatically a RESP charge.

A well-supported negative or unresolved answer is eligible for scientific credit. Explain what the evidence establishes and what it leaves open. Nonconvergence, missing calculations or a self-declared uncertainty flag do not establish non-identifiability. Report genuine model/basin collapse with the corresponding evidence.

# Deliverables

Submit `report/results.json` under the structured submission contract and a readable `report/report.md`. Preserve actual inputs, native outputs, identity/state mappings, analysis code and execution records. Quantitative evidence must be recoverable from linked artifacts. Record concise decisions, failures, revisions, resource use and limitations; consult `submission_guide.md` and `resources.md`.
