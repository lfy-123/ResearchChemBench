# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum-chemical calculations to rationalize photochromism of the viologen host–guest complexes, especially the [4]pseudorotaxane G2+@β-CD3. The authors claim that cyclodextrin hosts donate electron density to the electron-deficient viologen guest; the resulting host-to-guest transfer explains radical formation and the optical response.

## 2. System and model boundary

The calculated β complex is one dicationic viologen guest, N,N′-di[2-(4-fluorophenyl)-2-oxoethyl]-4,4′-(1,4-phenylene)-bipyridinium, threaded by three β-cyclodextrin molecules. The model is an isolated, closed-shell, +2 complex; counterions, solvent and periodic packing are not included in the reported quantum calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build host–guest models | G2+ and three β-CD units (and an analogous γ model) | Molecular construction guided by the reported inclusion structures | β complex is a symmetric homowheel; terminal pyridinium portions remain outside portals | Initial 3-D complexes | ev_doc_6f6701facb90_000022_3409529677cc; ev_doc_1be67e438730_000035_d553032ee66d |
| 2 | Relax structures | Initial complexes | xTB 6.7.0, GFN2-xTB | Charge +2, singlet | Optimized geometries | ev_doc_6f6701facb90_000312_1fe24ed5bfe8; ev_doc_6f6701facb90_000445_6508aa9dc28d; ev_doc_6f6701facb90_000447_ed004ac7e904 |
| 3 | Obtain orbitals | Optimized geometries | ORCA 6.0.0 single point | B3LYP-D3(BJ)/def2-SVP, +2, singlet | Wavefunction and orbital energies | ev_doc_6f6701facb90_000447_ed004ac7e904 |
| 4 | Analyze frontier orbitals | ORCA wavefunction | Multiwfn | Frontier orbital energies and distributions | HOMO/LUMO energies and plots | ev_doc_6f6701facb90_000325_cf536bf5a778; ev_doc_6f6701facb90_000447_ed004ac7e904 |
| 5 | Measure closest contact | Optimized β complex | Structure-distance analysis | Minimum β-CD hydroxyl-O···pyridinium-N distance | Contact distance | ev_doc_6f6701facb90_000325_cf536bf5a778 |

## 4. Validation and analysis protocol

The structure must be chemically sane, retain +2 charge and singlet multiplicity, and be checked for optimization convergence. Frontier-orbital localization is interpreted by fragment identity: HOMO density should be primarily on cyclodextrin host atoms and LUMO density on the pyridinium/phenylene guest. The closest contact is the minimum distance over β-CD hydroxyl oxygens and the two pyridinium nitrogens, with atom identities retained in the report. The authors report a 3.058 Å minimum for this pair.

## 5. Private reference results

The source reports 3.058 Å for the minimum β-CD oxygen–pyridinium nitrogen distance. Figure 5 shows host-localized HOMO and guest-localized LUMO for G2+@β-CD3, but the supplied machine-readable evidence does not provide numerical HOMO/LUMO values; therefore only localization and the contact value are hidden evaluator targets. The paper reports that the complex's photochromic behavior is attributed to host-to-guest electron transfer and viologen radical formation.

## 6. Limitations and interpretation boundaries

The paper does not disclose the exact starting coordinates, conformer search, optimization convergence thresholds, or numerical orbital energies in text. Reproduction is consequently an evidence-anchored structural reconstruction, not a bitwise rerun. A calculated orbital energy is method-, geometry- and implementation-dependent; orbital localization and charge-transfer direction are the defensible mechanistic observables. The reported contact is a single optimized-structure value and should not be treated as an experimental bond length.
