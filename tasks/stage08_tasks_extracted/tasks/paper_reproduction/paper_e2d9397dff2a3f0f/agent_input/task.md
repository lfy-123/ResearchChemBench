# Scientific objective

Calculate and validate the Gibbs free-energy barrier associated with N–O cleavage in the explicitly supplied neutral singlet Ru-bda-Py model, using the two public stationary-point starting geometries. Report the barrier in kcal/mol and the evidence that the target structure is a transition state. This is a direct computational investigation: independently choose the route, validate it, and state the conclusion without relying on an author mechanism.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors interpret catalyst-organized N–O cleavage in the bda model as the kinetically controlling event before ammonia attack.

**Candidate route or mechanism.**
The proposed event is cleavage of the N–O interaction in the singlet bda intermediate, proceeding through the supplied singlet target saddle, before a subsequent NH3 attack step. Treat this as the candidate explanation to test with the fixed structures.

**Discriminating evidence.**
Use stationary-point optimization and harmonic frequencies to distinguish a minimum from a first-order saddle, and inspect the imaginary-mode displacements and N–O bond metrics for cleavage character. Assemble the Gibbs barrier from the optimized structures, thermal terms, solvent treatment, and any stated electrochemical reference convention.

# Public inputs and scientific boundaries

The only molecular inputs are `data/inputs/reference.xyz` and `data/inputs/target.xyz`, explicit XYZ files with element identities and Cartesian coordinates. Both are neutral singlets. The system is Ru-bda-Py (bda = 2,2′-bipyridine-6,6′-dicarboxylate; Py = pyridine) in acetonitrile at 298.15 K. State whether and how you apply the electrochemical reference conditions 0.5 V vs Fc+/0 and pH 15.1. The endpoint is the free-energy difference between the optimized target saddle and optimized supplied reference state. Do not infer additional structures, products, pathways or literature facts; no result values are public.

# Required scientific validation/investigation

Plan a reproducible calculation for the fixed pair, optimize and frequency-test both structures, and report convergence. Show that the reference is a minimum and that the target is a first-order saddle with one imaginary frequency. Test the physical character of that mode by reporting the atoms/bond distances or displacement analysis used to associate it with N–O cleavage. Define the barrier equation and all corrections. Completion requires either a documented barrier with all checks or a bounded-failure report containing diagnostics and limitations. Stop after the fixed pair and these validation checks; no open candidate search is authorized.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, with route, charge/multiplicity, structure validation, frequency evidence, barrier and limitations. The failure branch must be used honestly if the endpoint cannot be obtained.
