# Private paper route

## 1. Scientific objective and author claim

The paper uses quantum chemistry to explain why ethanolamine (MEA) is the preferred hydrogen-bond donor for taurine (Tau) in an in-situ deep eutectic solvent. It compares BSSE-corrected interaction energies for Tau complexes with imidazole (Im), glycerol (Gly), and MEA. The author claim is that MEA gives the strongest Tau interaction and therefore supports selective Tau purification.

## 2. System and model boundary

The quantum-chemistry comparison is Tau–HBD with a 1:2 Tau:HBD stoichiometry for Im, Gly, and MEA (Figure 8). The paper names Tau, MEA, Gly, EG, Im and sodium sulfate as neutral molecular structures used to generate complexes; the scored comparison is the three HBD systems. The reported observable is the electronic interaction energy with BSSE correction, in kJ mol^-1. The paper also discusses RDG weak-interaction character; its qualitative interpretation is dispersion-dominated Im–Tau versus hydrogen-bond-like attraction for Gly–Tau and MEA–Tau.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate starting monomers and combined structures and locate low-energy conformations | Tau, MEA, Gly, EG, Im, Na2SO4 and combined structures | Random generation and PM6-D3 pre-optimization in MOPAC | PM6-D3; random initial structures | Low-energy conformations | ev_doc_99d3cb8f3445_000102_3eb5402a859f; ev_doc_99d3cb8f3445_000104_97d99b12590d |
| 2 | Refine structures and check stationary points | Selected low-energy conformations | B3LYP-D3(BJ) optimization and vibrational analysis in Gaussian 16W | 6-311+G(d,p) basis | Optimized geometries and frequencies | ev_doc_99d3cb8f3445_000104_97d99b12590d; ev_doc_99d3cb8f3445_000105_56ccefc434b8 |
| 3 | Compute interaction energies | Tau–HBD complexes and monomers | Counterpoise/BSSE-corrected DFT energy calculation | ΔE = EAB − EA − EB + BSSE | Interaction energies | ev_doc_99d3cb8f3445_000106_92e88b5b40d4; ev_doc_99d3cb8f3445_000108_48392f611e63 |
| 4 | Interpret the interaction | Wavefunction files for Tau–Im, Tau–Gly, Tau–MEA | Multiwfn RDG analysis | Blue attractive, green vdW, red repulsive regions; electron-density discussion | Weak-interaction characterization | ev_doc_99d3cb8f3445_000255_5ad2d78be19a |

## 4. Validation and analysis protocol

The source route selects low-energy conformations before DFT refinement and vibrational analysis. A reproducible reconstruction should retain distinct candidate poses, optimize monomers and complexes consistently, reject non-minima with imaginary frequencies, and calculate the same counterpoise definition for each named complex. Compare all three energies on a common sign convention and report the ranking. If RDG is performed, report whether the contact region is dominated by van der Waals character or hydrogen-bond-like attraction, without treating RDG alone as proof of energetic ordering.

## 5. Private reference results

The paper reports interaction energies of −65.1 kJ mol^-1 for Tau–Im, −91.4 kJ mol^-1 for Tau–Gly, and −116.1 kJ mol^-1 for Tau–MEA (Figure 8 and Section 3.6). Thus MEA is the most stabilizing of the three, followed by Gly and Im. The paper describes Im–Tau as predominantly van der Waals, while Gly–Tau and MEA–Tau show blue RDG isosurfaces consistent with hydrogen-bonding; MEA is described as more effective than Im because of its hydroxyl group.

## 6. Limitations and interpretation boundaries

The paper does not publish Cartesian starting geometries, random seeds, full conformer populations, optimization thresholds, counterpoise input files, or an uncertainty analysis. The numerical references therefore define a reproduction target rather than a uniquely reproducible geometry. Interaction energies are electronic complexation energies, not solution free energies or direct extraction yields. The public task must permit independent conformer and method choices, require transparent coverage and validation, and distinguish failure to locate a validated minimum from a numerical scientific conclusion.
