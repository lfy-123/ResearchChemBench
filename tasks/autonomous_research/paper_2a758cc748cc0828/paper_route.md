# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to support a metal-free visible-light aminocarbonylation of an unactivated alkyl iodide.  The modeled claim is that a cyclohexyl radical adds CO, undergoes iodine-atom transfer to regenerate the radical, and that amine attack on the resulting acyl iodide controls amine selectivity.  The published profile reports barriers for the radical carbonylation/chain sequence and compares tetrahedral-intermediate stability for aniline, N-ethylaniline, N-methylaniline, and morpholine.

## 2. System and model boundary

The mechanistic system is cyclohexyl radical + CO + iodocyclohexane, followed by acyl iodide reaction with one of four amines, in an acetonitrile continuum.  Radical-pathway calculations use the doublet surface; closed-shell amine-attack calculations use the singlet surface.  The reported labels 1a–1e and TS1–TS4 are paper-local labels only; the public task replaces them with explicit chemical identities.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize radical-pathway stationary points and locate TS1–TS3 | Cyclohexyl radical, CO, iodocyclohexane-derived species, acyl iodide and amide pathway structures | Gaussian 16 QST3/DFT | UM06-2X/6-311+G(d,p), PCM(MeCN), doublet | Optimized minima and transition structures | ev_doc_ab161734106e_000680_804b36ebd9d1; ev_doc_ab161734106e_000681_ccc59bc433ef; ev_doc_ab161734106e_000689_2caf767aa0a1 |
| 2 | Confirm stationary-point character and obtain thermochemistry | Optimized structures | Gaussian 16 frequency calculations | Same electronic structure and solvent model | Gibbs energies and imaginary-frequency counts | ev_doc_ab161734106e_000680_804b36ebd9d1; ev_doc_ab161734106e_000683_d6fc1e82ce45 |
| 3 | Model amine attack on acyl iodide and locate TS4 for each amine | Acyl iodide plus aniline, N-ethylaniline, N-methylaniline or morpholine | Gaussian 16 QST3/DFT | UM06-2X/6-311+G(d,p), PCM(MeCN), singlet | TS and tetrahedral-intermediate structures | ev_doc_ab161734106e_000680_804b36ebd9d1; ev_doc_ab161734106e_000681_ccc59bc433ef |
| 4 | Compare relative barriers and reaction free energies | Frequency-corrected Gibbs energies | Relative-energy analysis | Reference state is the corresponding separated reactant state for each step | ΔG‡ and ΔG values and mechanistic interpretation | ev_doc_229c23be21b8_000158_6b33124d0d0c; ev_doc_229c23be21b8_000174_4de3fcaa601f; ev_doc_229c23be21b8_000175_ba06a9d8f309 |

## 4. Validation and analysis protocol

Minima were expected to have no imaginary frequencies and transition structures exactly one.  The radical sequence was interpreted through CO addition, iodine-atom transfer and morpholine attack; the amine comparison was interpreted by separating activation free energy from tetrahedral-intermediate free energy.  The main paper's Fig. 3 caption specifies M06-2X/6-311++G** with PCM(MeCN), while the SI mechanistic-method text specifies UM06-2X/6-311+G(d,p); the SI is treated as the definitive implemented protocol for the route table.

## 5. Private reference results

The hidden reference contains the published radical-pathway barriers/free energies and the four amine barrier/intermediate pairs.  Radical values are TS1 11.9, TS2 16.4, TS3 11.3 kcal/mol; relative energies for the acyl radical, acyl iodide and final amide are −0.8, +3.2 and −7.7 kcal/mol.  Amine attack pairs (barrier, tetrahedral-intermediate ΔG) are aniline (12.9, +8.9), N-ethylaniline (13.2, +4.0), N-methylaniline (14.1, +6.9), and morpholine (11.3, −1.0), all in kcal/mol.

## 6. Limitations and interpretation boundaries

These are single-level continuum-solvent calculations and do not establish photophysical electron-transfer kinetics, explicit-solvent effects, conformational completeness, or experimental yields.  The calculation supports thermodynamic/kinetic plausibility and a selectivity rationale; it does not by itself prove the full ConPET photochemical cycle.
