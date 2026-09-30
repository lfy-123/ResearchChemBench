# Scientific objective

Determine whether an independently designed computational model of the neutral, closed-shell 1-(4-methylphenyl)piperazinyl dithiocarbamato-S,S′ Zn(II) centrosymmetric dimer reproduces the selected single-crystal structural observables associated with CCDC 2361759. Choose and justify the computational route; the task scores the scientific validation and conclusion, not adherence to a hidden protocol.

# Public inputs and scientific boundaries

Use the pinned CCDC record 2361759 (DOI 10.5517/ccdc.csd.cc2k8ls7) in `data/inputs/structure_record.json` to establish the complete dimer, connectivity, atom labels and Cartesian starting geometry. Use charge 0 and multiplicity 1 and document hydrogen and symmetry handling. The measured quantities are the selected atom-labelled Zn/S/C/N bond lengths and S–Zn–S, Zn–S–C and C–N angles defined by the record and your mapping table. The molecular geometry comparison excludes crystal-packing and thermal-motion corrections; do not infer nanoparticle or photocatalytic behavior.

# Required scientific validation/investigation

Independently formulate any plausible structural model choices and, where alternatives are tested, retain unique candidate identities, deduplicate them, and explain which are advanced or rejected. Validate each reported candidate by optimization convergence, preservation of the specified dimer identity and coordination, and a reproducible atom mapping. Independently calculate per-observable absolute and squared absolute errors and their means. Completion requires a validated final model with all selected observables and a conclusion about structural agreement, or a bounded-failure report with every attempted model and diagnostic. Stop after the validated investigation supports a stable conclusion and further explicitly considered alternatives no longer alter it, or at a declared technical/resource boundary; report search coverage and limitations.

# Deliverables

Submit `report/results.json` with status, provenance, independently chosen route, candidate and validation records, atom mapping, per-observable values/errors, aggregate metrics, conclusion and limitations. Numeric values require units. The bounded-failure branch must contain attempted models and diagnostics rather than a success-only placeholder.
