# Scientific objective

Investigate neutral open-shell BaOH(H2O)n clusters for n=1–5 and independently test the authors' qualitative hypothesis that sequential hydration preserves a contact Ba–OH ion-pair arrangement at the smallest sizes but can reorganize the BaOH unit into a solvent-shared arrangement as the water network grows. Generate and validate candidate structures, then determine structural descriptors, relative stability, and OH-stretching signatures. Do not assume that any named candidate is the global minimum.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that growth of the hydration network can reorganize a contact Ba–OH ion-pair arrangement toward a solvent-shared arrangement. Test this candidate mechanism across the full hydration series and determine whether and where a transition is supported.

**Candidate route or mechanism.**
Compare intact-contact structures across n=1–5 with water-network-organized, solvent-shared alternatives, including competing nondissociated and Ba···OH-separated arrangements at each size where chemically meaningful. Treat these as candidate explanations to test, not as predetermined rankings.

**Discriminating evidence.**
Use validated stationary-point energetics and structures together with calculated OH-stretching frequencies/intensities and their assignments to the public bands. Ba···O(1) distances, water coordination and hydrogen-bond topology, charge or interaction descriptors, and finite-temperature spectral or distance checks can provide complementary evidence for distinguishing the alternatives.

# Public inputs and scientific boundaries

The system is BaOH(H2O)n with n ∈ {1,2,3,4,5}, total charge 0 and spin multiplicity 2. BaOH oxygen is O(1); each water oxygen is O(2) or higher according to the explicit atom map supplied by the Agent. Public experimental band positions, units and neutral band labels are in `data/inputs/experimental_band_assignments.json`. The physical boundary is isolated neutral clusters in the stated electronic state; do not infer bulk-solution behavior. The measured quantities are candidate relative energies/free energies, harmonic or anharmonic OH frequencies and intensities, Ba···O(1) distance, water coordination/hydrogen-bond topology, and optional charge or interaction descriptors. You may choose software and model chemistry, but state them and do not present them as the authors' protocol.

The band labels a-f are identifiers only, not assignments to an atomic group or shell. The input file retains its legacy filename but contains measured peak positions only. Determine mode identities from computed displacements and spectra; determine any change in ion-pair arrangement by comparing the full n=1-5 series, without assuming its onset.

# Required scientific validation/investigation

For each n, define a finite candidate-generation strategy covering both intact-contact and separated/network-organized possibilities, retain a stable candidate ID and atom mapping, and deduplicate by a stated structural criterion. Optimize candidates and validate stationary points with a frequency or equivalent minimum test; report failures rather than silently discarding them. Advance candidates using an explicitly stated stability/spectral criterion. Assign computed modes to the public experimental bands with mode identity and uncertainty. Compare the n=1–5 structural trend and the competing arrangements at each size. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

# Deliverables

Submit `report/results.json` containing the candidate table, validation records, per-size observables, spectral assignments, conclusion, and provenance. Include enough coordinates or structure identifiers to reproduce every scored candidate. State whether the evidence supports the qualitative author hypothesis and distinguish computed evidence from interpretation.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
