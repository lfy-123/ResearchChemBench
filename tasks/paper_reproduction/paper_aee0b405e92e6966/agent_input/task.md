# Scientific objective

Assess the authors' qualitative proposal that neutral probe A can adopt two intramolecular proton-placement arrangements, OH···N and NH···O. Independently plan and perform calculations that determine which supplied arrangement is more stable and quantify the relative energy in kcal mol⁻¹. The research object is the two complete 71-atom neutral-singlet structures in the public XYZ files; the scored endpoint is their consistently defined relative electronic or thermochemical energy.

The authors' qualitative route is that proton relocation between the oxygen and nitrogen sites (an ESIPT-like intramolecular proton-transfer/conjugation picture) can distinguish these two arrangements. Treat this as a hypothesis to test; it does not specify the energetic ordering or numerical result.

The authors' qualitative route is that proton relocation between the oxygen and nitrogen sites (an ESIPT-like intramolecular proton-transfer/conjugation picture) can distinguish these two arrangements. Treat that as a hypothesis to test; it does not specify the energetic ordering or numerical result.

# Public inputs and scientific boundaries

`data/inputs/probe_A_OH_N.xyz` is the neutral-singlet probe-A geometry with the labile proton on oxygen and an OH···N contact. `data/inputs/probe_A_NH_O.xyz` is the neutral-singlet probe-A geometry with the labile proton on nitrogen and an NH···O contact. Each file has 71 atoms and Cartesian coordinates in Å; atom order is part of the input identity. No paper, SI, result value, target interval, or prescribed model chemistry is supplied. Treat the molecule as an isolated molecular system, and state any solvent model, charge, multiplicity, thermal correction, and conformer treatment used. Do not claim a population, pKa, fluorescence wavelength, or transition state from this two-state calculation.

# Required scientific validation/investigation

For each named input, perform a reproducible calculation that can compare the same physical state across both structures. Generate any needed 3-D preparation or relaxation from the supplied coordinates, preserve the two proton-placement identities, and record software, method, basis, environment, convergence, and energy convention. Validate every advanced structure as a minimum using a frequency or an equivalently justified Hessian/stationarity test; report imaginary modes if present. Deduplicate only if you generate additional conformers and retain the mapping to the named input. The investigation is complete when both named states have comparable energies and validation status, or when a bounded failure is documented with the failed calculation and the reason no comparison is scientifically defensible. Stop after both named states are validated and the energy difference and uncertainty/convention statement are reported; do not expand into other probe forms.

# Deliverables

Submit `report/results.json` plus any supporting output files referenced there. A successful result must identify each state by `state_id` (`A_OH_N` or `A_NH_O`), give its calculation and minimum-validation status, provide the signed or absolute relative energy with units and an explicit definition, and include a final conclusion, reproducibility record, and limitations. If completion fails, submit only the failure branch and explain the scientifically material cause rather than fabricating values.
