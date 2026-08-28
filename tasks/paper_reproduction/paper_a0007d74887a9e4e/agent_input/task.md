# Scientific objective

Independently plan and execute calculations testing the authors' qualitative hypothesis that Br-mediated charge transfer and molecule–surface interaction can reduce the intrinsic spin polarization of neutral NiCp2. Investigate the explicitly defined conf3 bridge state and report the converged molecular magnetic moment in μB, its sign convention and magnitude, plus Ni/Ni-3d local moments when your method provides them.

# Public inputs and scientific boundaries

Use `data/inputs/system_spec.json`. The object is neutral C10H10Ni, multiplicity 3, with two eta5-Cp rings; the surface is a 4x4 Au(111) slab with a=b=14.98 Å, gamma=60°, >10 Å vacuum, bottom two Au layers fixed, and nine Br atoms in quasi-(sqrt(3)x(sqrt(3))R30°) packing. Conf3 means the molecule is initialized over the bridge between two adjacent Br atoms; record the selected pair, height, azimuth, tilt and all atom mapping. You may choose software/model chemistry, but state it completely. Do not use paper/SI or general web information during the investigation and do not put target values in the input or report them as assumptions.

# Required scientific validation/investigation

Generate at least two distinct bridge-site starting orientations or heights, deduplicate converged structures by heavy-atom RMSD and selected Br-pair identity, and advance only calculations with a spin-polarized SCF solution and a geometry whose maximum unconstrained force is reported. A calculation is complete when the chosen electronic and ionic convergence criteria are met, the selected bridge state remains identifiable after relaxation, and the molecular/Ni moment extraction is documented. Stop after all planned starts have converged or failed with reasons; if resources prevent this, report the attempted coverage and limitation. Validate the magnetic observable by an independent restart, spin initialization, or equivalent analysis and disclose any alternative method/sensitivity test.

# Deliverables

Submit `report/results.json` conforming to the schema. Include system construction, method, candidate/start records, convergence evidence, selected candidate identity, molecular moment (signed and absolute), optional Ni and Ni-3d moments, validation evidence, conclusion and limitations. A bounded-failure submission is valid only if status is bounded_failure or partial, includes a concrete top-level failure_reason, records attempted calculations and per-start failure causes, reports coverage, and explains why no scientifically defensible moment could be reported; it must not invent a selected candidate or moment.
