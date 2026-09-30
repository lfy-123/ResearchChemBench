# Scientific objective

Calculate and compare frontier-orbital gaps, chemical hardness and electrophilicity for the three supplied DQCS divalent-metal complexes, using a consistent electronic-descriptor definition.

# Public inputs and scientific boundaries

Use `data/inputs/cd_complex.xyz`, `co_complex.xyz` and `ni_complex.xyz` in that directory. Each has 65 centers, listed by atomic number and Cartesian coordinates in Å, and is the complete 1:1 complex. Charge/multiplicity are Cd (+2,1), Co (+2,2), Ni (+2,1). The primary solvent boundary is implicit DMSO; controlled alternatives may be reported separately. Do not add counterions or explicit solvent. These are given-object property calculations, not discovery of the supplied molecular identities. Optimization or a justified single point is permitted. Choose and document the model and frontier definition consistently. For orbital-based descriptors, gap = LUMO − HOMO, eta = gap/2, mu = (HOMO + LUMO)/2 and omega = mu²/(2 eta), with energies in eV. For open shells report the spin channel and avoid mixing unlike definitions; a justified alternative descriptor convention must be explicit and used consistently. No paper, SI, evaluator, historical verification archive or general-web lookup is an agent input.

# Required scientific validation/investigation

Check atom count, metal, charge and spin for each object; establish electronic convergence and provide calculation evidence. Report all three descriptors per successful object. Use exactly one main row each for object_id/metal `Cd`, `Co`, `Ni`, in any order. Failed objects retain their identity and actual diagnostics; additional attempts can be recorded separately. Compare only valid, like-defined observables.

# Deliverables

Submit `report/results.json`. Each completed complex requires all three numerical observables and validation evidence. A failed complex uses `bounded_failure` and `observables.failure_reason`; this is not a completed cross-metal comparison. Describe the method and calculated ordering; no generic disclaimer or stopping statement is required.
