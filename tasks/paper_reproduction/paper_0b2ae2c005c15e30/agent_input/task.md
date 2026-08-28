# Scientific objective

Test the authors' qualitative proposal that the experimentally observed centrosymmetric dinuclear Zn(II) dithiocarbamate can be represented by a geometry-optimized molecular model. Independently plan and execute calculations for the neutral, closed-shell dimer identified in `data/inputs/structure_record.json`; quantify agreement between your optimized geometry and the selected SC-XRD observables from the deposited record, preserving the crystallographic atom labels. Do not assume the authors' software, functional, basis, or protocol.

# Public inputs and scientific boundaries

The sole scientific identity input is the controlled CCDC record 2361759 (DOI 10.5517/ccdc.csd.cc2k8ls7), the 1-(4-methylphenyl)piperazinyl dithiocarbamato-S,S′ Zn(II) centrosymmetric dimer. Retrieve the CIF through that pinned record, extract one complete molecular dimer, convert to Cartesian coordinates, and use charge 0 and multiplicity 1. Preserve labels/connectivity and report any symmetry expansion or hydrogen treatment. The measured quantities are the selected Zn/S/C/N bond lengths and S–Zn–S, Zn–S–C and C–N angle entries defined by the atom labels in the record and your supplied mapping table. Crystal packing and thermal motion are outside the molecular calculation; do not claim catalytic or nanoparticle properties.

# Required scientific validation/investigation

Propose a defensible optimization and analysis route, including model chemistry, environment, convergence, software, and any conformer or symmetry decisions. Generate and deduplicate any alternative starting geometries you actually investigate; retain their identities and explain advancement or rejection. A candidate is validated only when the optimization converges, the final structure retains chemically plausible Zn–S coordination and the required dimer identity, and the reported atom mapping permits independent recomputation of every selected distance and angle. Independently recompute absolute and squared absolute errors and their means from the per-observable table. The calculation is complete when one validated final geometry (or a clearly documented bounded failure with all attempted candidates and diagnostics) and all selected observables are reported. Stop when the validated route is complete and additional candidates no longer change the selected conclusion, or when a stated resource/technical limit is reached; report coverage and limitations in either case.

# Deliverables

Submit `report/results.json` containing status, input provenance, route, candidate/validation records, atom mapping, per-observable computed values and errors, aggregate metrics, conclusion, and limitations. Numeric values must include units. A bounded failure branch must still include attempted candidates, diagnostics, and the reason completion was not reached.
