# Scientific objective

Determine, by an independently planned computational study, the low-energy vertical singlet excitation behavior of the isolated neutral singlet BN-AkFlu (5a) molecule supplied in `data/inputs/bn_akflu_s0.xyz`. Report S1–S6 excitation energies and wavelengths, oscillator strengths, dominant orbital contributions, and S1–S4 hole–electron descriptors (D, Sr, H, t, HDI, EDI). Use the computed evidence to state what it supports about low-energy absorption and excited-state character, without relying on an external paper.

# Public inputs and scientific boundaries

The only molecular input is the 40-atom XYZ file: atom order, Cartesian coordinates in Å, neutral charge (0), singlet multiplicity (1), and the isolated molecule are fixed by the file and its comment line. The target states are vertical singlet states S1 through S6 from the S0 geometry. The target descriptors are the hole–electron separation D (Å), overlap Sr (dimensionless), hole centroid distance H (Å), charge-transfer index t (Å), hole delocalization index HDI, and electron delocalization index EDI for S1–S4. Gas phase and single-molecule boundaries apply; do not substitute crystal, solvent, vibronic, thermal, or experimental-emission quantities for the requested electronic observables. Choose and disclose a reproducible electronic-structure and excited-state-analysis protocol.

# Required scientific validation/investigation

Plan and execute a ground-state preparation and vertical excited-state calculation that addresses S1–S6, then perform the requested hole–electron analysis for S1–S4. Validate atom count, charge, multiplicity, absence of imaginary modes if an optimization is performed, state ordering, energy–wavelength consistency, and the identity of each orbital transition. Record software, method, basis, environment, state count, convergence settings, and analysis implementation. Compare independent checks (for example, wavelength reconstructed from energy and a second electronic-structure or analysis check when available). Completion requires all requested fields plus an evidence-based interpretation and limitations; stop when S1–S6 and S1–S4 are computed and validated, or report a failed calculation with the exact missing artifact and diagnostic rather than inventing values. No candidate search is required; the stopping rule is exhaustion of the fixed state list.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the calculation protocol, per-state results, per-state hole–electron results, validation evidence, a conclusion about the computed absorption/electronic character, and limitations. The report must distinguish calculated vertical absorption observables from any contextual experimental statement.
