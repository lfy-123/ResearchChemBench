# Scientific question

What electronic and structural features explain the short Ir–Ir bond in the supplied iminoxolene dimer, and what can a reduced molecular model establish about that observation?

# Input files

- `data/inputs/problem_context.json` gives the observed Ir–Ir distance, diamagnetism and molecular scope.
- `data/inputs/Egan_identity.json` and `dimer_identity.json` define the experimental neutral (A,C)-(Egan)2Ir2 dimer, C88H104Ir2N4O12.
- `data/inputs/Hap_core_identity.json` defines neutral Ir2(Hap)4, C24H20Ir2N4O4 (54 atoms), with two Ir centers and four iminoxolene N/O donor units. The connectivity does not assign localized oxidation states or a metal–metal bond order.

# Scope

Use the neutral singlet Hap model to compare S4 and C2h relative orientations of the two coordination units in the gas phase. These are candidate geometrical comparisons; determine their stationary character and relative energies. Generate the structures from the supplied identities. Compare Gibbs energies at 298.15 K with a consistent molecular standard state and declared thermal/low-frequency treatment. Keep atom correspondence, composition and electronic state consistent.

The experimental Egan dimer has an observed Ir–Ir distance of 2.5584(4) Å and is diamagnetic. These are supplied facts to explain. Hap omits the Egan straps and substituents; a Hap result is not a full-Egan result. Full-molecule calculations, optical spectra, electrochemical mechanisms and a relativistic response survey are outside the required scope.

# Required results

1. Determine the Ir–Ir distance in Å for each candidate orientation and ΔG = G(C2h) − G(S4) in kcal/mol. Establish the physical structures and stationary character underlying this comparison; distinguish electronic energy from Gibbs energy.
2. Explain how metal–ligand electronic interactions and orbital occupations affect net Ir–Ir bonding. Use electronic evidence to establish any proposed bonding and antibonding contributions; a short distance or formal oxidation-state label alone is insufficient.
3. Explain how the relative orientation changes the available intermetal interactions and relates to the structural and energetic comparison. Distinguish support for an orientation-dependent mechanism from a uniquely isolated causal energy decomposition.
4. State what the calculated stationary character permits one to infer about equilibrium conformers, and which parts of the bonding explanation can be carried from Hap to the experimental Egan dimer. Distinguish a model-dependent bonding index from a uniquely determined experimental bond order.

Choose and justify the computational methods and analyses. No fixed orbital-label list, bond partition, deformation grid or calculation sequence is required. Link each claim to evidence appropriate to its physical meaning.

# Submission

Submit `report/results.json` and `report/report.md` under the supplied schema and guide, with native inputs/outputs, mapped structures and reproducible electronic analyses. Only final scientific propositions are scored. Use supplied inputs and general scientific/software documentation; private references and prior verification archives are not inputs.
