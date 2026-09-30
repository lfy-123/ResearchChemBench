# Scientific objective

Determine the neutral substitutional Ni-vacancy and Al-vacancy formation energies in ordered bulk β-NiAl (B2), and test the authors' qualitative hypothesis that unequal vacancy energetics can favor Ni defect formation and thereby be consistent with preferential Ni transport toward a surface. The scored objects are the two bulk defect energies, their difference/order, and the defensibility of the computational validation; no surface transition state or precipitate structure is scored.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that unequal formation energies for neutral substitutional vacancies in ordered β-NiAl can favor formation of Ni vacancies. They interpret that energetic asymmetry as consistent with preferential Ni transport toward a surface and associated Ni enrichment, while the bulk vacancy comparison alone does not establish the complete surface or diffusion mechanism.

**Candidate route or mechanism.**
The candidate explanation is a bulk defect-mediated route in which Ni-vacancy formation is energetically preferred to Al-vacancy formation, enabling Ni-related mass exchange toward a surface. Treat this as a proposed interpretation to test through the requested bulk calculations; surface exchange and diffusion processes are contextual comparisons rather than replacement observables.

**Discriminating evidence.**
Distinguish the claim by calculating pristine, neutral Ni-vacancy, and neutral Al-vacancy total energies under one consistent periodic model, then evaluating the formation-energy difference with an explicit elemental-reservoir convention. Test whether the ordering is numerically stable through supercell and dominant-setting sensitivity or convergence checks, and use atom-count, sublattice, charge, and relaxation validation to support the comparison.

# Public inputs and scientific boundaries

Use `data/inputs/beta_nial_b2_primitive.poscar` as the ordered B2 conventional cell: cubic lattice parameter 2.890 Å, Ni at fractional (0,0,0), Al at (0.5,0.5,0.5), one formula unit, neutral periodic solid. `system_definition.json` fixes the defect identities and requires a neutral charge state. Build a periodic supercell, remove exactly one Ni for the Ni-vacancy state and exactly one Al for the Al-vacancy state. The measurement is the 0 K electronic formation energy in eV under the Ni-rich primary reservoir convention; state whether ions and cell are relaxed, the magnetic treatment, and all model choices. Do not use the paper, SI, source-data archive or general web as inputs.

Primary benchmark reservoir convention (Ni-rich): E_f(V_X) = E_defect - E_pristine + mu_X, for one removed atom from the same supercell. Set mu_Ni = E(fcc Ni)/atom and mu_Al = E(B2 beta-NiAl)/formula_unit - mu_Ni. Compute reservoir and host energies consistently and report them with atom/formula-unit normalization. A different reservoir convention may be reported separately but does not define the primary comparison.

# Required scientific validation/investigation

Plan and execute a reproducible periodic first-principles calculation or an explicitly justified equivalent. Establish a pristine reference and both defect states with identical conventions. Demonstrate numerical convergence or sensitivity for supercell size and the dominant numerical settings, report total energies and the formation-energy equation, and show that atom counts and the removed sublattice are correct. Deduplicate repeated calculations and advance a setting only when the preceding result is internally consistent. Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result.

The Ni-rich reservoir definition above is the benchmark comparison convention. It is not a claim that the source article uniquely specified those chemical potentials. Keep the reservoir normalization and both formation energies explicit when interpreting the result.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. For a completed investigation, include method provenance, pristine/Ni-vacancy/Al-vacancy energies, formation energies with units and reservoir convention, ordering, validation evidence. If convergence cannot be achieved, use the bounded-failure branch and report the validated work, exact missing calculation or unresolved sensitivity, and its consequences without fabricating energies or an ordering. The report must distinguish computed values from interpretation and must not silently substitute a surface or diffusion calculation for the requested bulk observable.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
