# Scientific objective

Determine, by an independently planned computational study, the low-energy vertical singlet excitation behavior of the isolated neutral singlet BN-AkFlu (5a) molecule supplied in `data/inputs/bn_akflu_s0.xyz`. Report S1–S6 excitation energies and wavelengths, oscillator strengths, dominant orbital contributions, and S1–S4 hole–electron descriptors (D, Sr, H, t, HDI, EDI). In the interpretation, test the authors' qualitative proposal that internal BN incorporation changes the low-energy absorption and excited-state character; do not assume that proposal is correct.

# Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that internal BN incorporation changes the low-energy absorption and excited-state character of BN-AkFlu, including attenuation of low-energy absorption relative to stronger higher-energy absorption and altered frontier-orbital behavior. Treat this as a claim to test with the requested isolated-molecule calculations.

**Candidate route or mechanism.**
The authors associate the strong absorption near the higher-energy portion of the spectrum with an Sn transition (reported qualitatively as around S4) and propose that the lowest singlet transition is weak, with low-energy states shaped by BN-induced changes in π-electron structure and σ–π mixing. Examine S1–S6 and the orbital contributions to assess these proposed assignments without assuming them as results.

**Discriminating evidence.**
Use the calculated excitation energies, wavelengths, oscillator strengths, dominant orbital contributions, and S1–S4 hole–electron descriptors to distinguish weak low-energy transitions from stronger higher-energy transitions and to assess whether the excited-state density is localized or involves charge-transfer-like separation. Compare the computed pattern with the authors’ qualitative proposal while keeping the analysis within the isolated gas-phase system.

# Public inputs and scientific boundaries

The only molecular input is the 40-atom XYZ file: atom order, Cartesian coordinates in Å, neutral charge (0), singlet multiplicity (1), and the isolated molecule are fixed by the file and its comment line. The target states are vertical singlet states S1 through S6 from the S0 geometry. The target descriptors are the hole–electron separation D (Å), overlap Sr (dimensionless), mean hole/electron spatial extent H (Å), charge-transfer index t (Å), hole delocalization index HDI, and electron delocalization index EDI for S1–S4. Gas phase and single-molecule boundaries apply; do not substitute crystal, solvent, vibronic, thermal, or experimental-emission quantities for the requested electronic observables. Choose and disclose a reproducible electronic-structure and excited-state-analysis protocol; the paper's software and exact keyword route are not prescribed.

This is a fixed-structure property track: the supplied coordinates are public inputs for the named property comparison, not a scored structure discovery answer. Do not claim that the input geometry itself was rediscovered; report any optimization or conformer search separately.

Descriptor definitions follow the normalized hole/electron densities of each identified excitation: D is the Euclidean distance between their centroids; H = (|sigma_hole| + |sigma_electron|)/2 is the average overall RMS spatial extent. Componentwise H_lambda = (sigma_hole,lambda + sigma_electron,lambda)/2, H_CT = |H_vector dot u_CT|, and t = D - H_CT, where u_CT is the centroid-to-centroid unit vector. D, H and t are in angstrom. Sr is the dimensionless hole-electron overlap; HDI and EDI use the declared normalized-density analysis convention. H is not a centroid distance, and t is not D/H. Retain the state IDs S1-S4 and the same S0 geometry used for the vertical excitation table.

Define Sr as the whole-space integral of sqrt(rho_hole * rho_electron), with normalized hole and electron densities. Check grid/coefficient convergence rather than relying on default truncated TD output. For reproduction guidance, the author-level B3LYP/6-311G(d,p) gas-phase S0 optimization followed by full TDDFT provides a documented route; retain all requested observables if using another justified protocol.

Submit the six `states` entries ordered S1–S6 and the four `hole_electron` entries ordered S1–S4, with explicit matching state IDs and energies. Report S2–S4 Sr separately; these values are evaluated against benchmark-computed references using an absolute numerical tolerance of 0.08. Do not relabel states to force agreement. Report D/H/t/HDI/EDI as before; no new hard numerical thresholds for those descriptors are introduced.

# Required scientific validation/investigation

Plan and execute a ground-state preparation and vertical excited-state calculation that addresses S1–S6, then perform the requested hole–electron analysis for S1–S4. Validate atom count, charge, multiplicity, absence of imaginary modes if an optimization is performed, state ordering, energy–wavelength consistency, and the identity of each orbital transition. Record software, method, basis, environment, state count, convergence settings, and analysis implementation. Compare independent checks (for example, wavelength reconstructed from energy and a second electronic-structure or analysis check when available). Scientific completion requires all requested primary observables, the specified validation evidence and the resulting scientific comparison. A partial or failed calculation may be submitted with its actual results and diagnostics, but does not satisfy an uncomputed scientific result. The primary comparison covers the specified state list.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include the calculation protocol, per-state results, per-state hole–electron results, validation evidence, qualitative hypothesis assessment. The report must distinguish calculated vertical absorption observables from experimental emission context.

Additional starting structures or investigations may be used to obtain the required results. Report auxiliary results separately; they do not replace the primary observables or their specified definitions. Optional analyses may be omitted without explanation or penalty.
