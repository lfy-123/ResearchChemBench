# Scientific objective

Determine, by an independently planned computational study, the low-energy vertical singlet excitation behavior of the isolated neutral singlet BN-AkFlu (5a) molecule supplied in `data/inputs/bn_akflu_s0.xyz`. Report S1–S6 excitation energies and wavelengths, oscillator strengths, dominant orbital contributions, and S1–S4 hole–electron descriptors (D, Sr, H, t, HDI, EDI). Use the computed evidence to state what it supports about low-energy absorption and excited-state character, without relying on an external paper.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that internal BN incorporation changes the low-energy absorption and excited-state character of BN-AkFlu, including attenuation of low-energy absorption relative to stronger higher-energy absorption and altered frontier-orbital behavior. Treat this as a claim to test with the requested isolated-molecule calculations.

**Candidate route or mechanism.**
The authors associate the strong absorption near the higher-energy portion of the spectrum with an Sn transition (reported qualitatively as around S4) and propose that the lowest singlet transition is weak, with low-energy states shaped by BN-induced changes in π-electron structure and σ–π mixing. Examine S1–S6 and the orbital contributions to assess these proposed assignments without assuming them as results.

**Discriminating evidence.**
Use the calculated excitation energies, wavelengths, oscillator strengths, dominant orbital contributions, and S1–S4 hole–electron descriptors to distinguish weak low-energy transitions from stronger higher-energy transitions and to assess whether the excited-state density is localized or involves charge-transfer-like separation. Compare the computed pattern with the authors’ qualitative proposal while keeping the analysis within the isolated gas-phase system.

# Public inputs and scientific boundaries

The only molecular input is the 40-atom XYZ file: atom order, Cartesian coordinates in Å, neutral charge (0), singlet multiplicity (1), and the isolated molecule are fixed by the file and its comment line. The target states are vertical singlet states S1 through S6 from the S0 geometry. The target descriptors are the hole–electron separation D (Å), overlap Sr (dimensionless), hole centroid distance H (Å), charge-transfer index t (Å), hole delocalization index HDI, and electron delocalization index EDI for S1–S4. Gas phase and single-molecule boundaries apply; do not substitute crystal, solvent, vibronic, thermal, or experimental-emission quantities for the requested electronic observables. Choose and disclose a reproducible electronic-structure and excited-state-analysis protocol.

# Required scientific validation/investigation

Plan and execute a ground-state preparation and vertical excited-state calculation that addresses S1–S6, then perform the requested hole–electron analysis for S1–S4. Validate atom count, charge, multiplicity, absence of imaginary modes if an optimization is performed, state ordering, energy–wavelength consistency, and the identity of each orbital transition. Record software, method, basis, environment, state count, convergence settings, and analysis implementation. Compare independent checks (for example, wavelength reconstructed from energy and a second electronic-structure or analysis check when available). Completion requires all requested fields plus an evidence-based interpretation and limitations; stop when S1–S6 and S1–S4 are computed and validated, or report a failed calculation with the exact missing artifact and diagnostic rather than inventing values. No candidate search is required; the stopping rule is exhaustion of the fixed state list.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the calculation protocol, per-state results, per-state hole–electron results, validation evidence, a conclusion about the computed absorption/electronic character, and limitations. The report must distinguish calculated vertical absorption observables from any contextual experimental statement.
