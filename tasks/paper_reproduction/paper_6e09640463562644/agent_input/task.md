## Scientific objective

Investigate neutral open-shell BaOH(H2O)n clusters for n=1–5 and independently test the authors' qualitative hypothesis that sequential hydration preserves a contact Ba–OH ion-pair arrangement at the smallest sizes but can reorganize the BaOH unit into a solvent-shared arrangement as the water network grows. Generate and validate candidate structures, then determine structural descriptors, relative stability, and OH-stretching signatures. Do not assume that any named candidate is the global minimum.

## Public inputs and scientific boundaries

The system is BaOH(H2O)n with n ∈ {1,2,3,4,5}, total charge 0 and spin multiplicity 2. BaOH oxygen is O(1); each water oxygen is O(2) or higher according to the explicit atom map supplied by the Agent. Public experimental band positions and assignments are in `data/inputs/experimental_band_assignments.json`. The physical boundary is isolated neutral clusters in the stated electronic state; do not infer bulk-solution behavior. The measured quantities are candidate relative energies/free energies, harmonic or anharmonic OH frequencies and intensities, Ba···O(1) distance, water coordination/hydrogen-bond topology, and optional charge or interaction descriptors. You may choose software and model chemistry, but state them and do not present them as the authors' protocol.

## Required scientific validation/investigation

For each n, define a finite candidate-generation strategy covering both intact-contact and separated/network-organized possibilities, retain a stable candidate ID and atom mapping, and deduplicate by a stated structural criterion. Optimize candidates and validate stationary points with a frequency or equivalent minimum test; report failures rather than silently discarding them. Advance candidates using an explicitly stated stability/spectral criterion. Assign computed modes to the public experimental bands with mode identity and uncertainty. Compare at least the n=1–5 structural trend and the n=3 alternatives. Completion requires either (a) validated candidates supporting a conclusion, or (b) a bounded-failure report identifying which calculations could not be completed and why. Stop when additional candidate generations no longer produce a distinct validated low-energy structure or materially change the structural/spectral conclusion, or when resources prevent that test; report coverage, stopping rule, and limitations.

## Deliverables

Submit `report/results.json` containing the candidate table, validation records, per-size observables, spectral assignments, conclusion, limitations, and provenance. Include enough coordinates or structure identifiers to reproduce every scored candidate. State whether the evidence supports the qualitative author hypothesis and distinguish computed evidence from interpretation.
