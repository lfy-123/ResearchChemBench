# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to quantify the interaction of Li+ with asymmetric ether solvents, supporting a solvent-screening rationale for low-temperature lithium-metal electrolytes. For TFPM (3,3,3-trifluoropropyl-1-methyl ether), the authors claim that complementary Li–O and Li–F coordination produces a stable chelating complex.

## 2. System and model boundary

The focal system is one isolated Li+ ion and one neutral TFPM molecule. The reported binding energy is defined from the electronic energy of the optimized complex minus the energies of the isolated Li+ and solvent fragments. The paper's theory section specifies ground-state geometry optimization and frequency analysis; no solvent continuum, counterion, periodic cell, or thermal free-energy correction is part of this focal observable.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize isolated solvent and Li+ complexes | TFPM and Li+ starting geometries; analogous PM/BM/TFEM/TFBM systems | Gaussian 16 DFT | B3LYP/6-311+G(d,p), ground state; charge/multiplicity appropriate to each species | optimized stationary points | ev_doc_5a271b4ca1ac_000409_965238d8538c; ev_doc_eeee11483b22_000009_161c153feb10 |
| 2 | Verify stationary points | optimized geometries | Gaussian 16 frequency analysis | same B3LYP/6-311+G(d,p) level | frequencies and minimum validation | ev_doc_5a271b4ca1ac_000409_965238d8538c |
| 3 | Compute fragment energies | isolated Li+ and isolated solvent | Gaussian 16 | same level and species charge/multiplicity | E(Li+) and E(solvent) | ev_doc_5a271b4ca1ac_000412_9060a44b5c6d |
| 4 | Form binding energy | complex and fragment electronic energies | arithmetic from DFT energies | Eb = Etotal − (ELi+ + Esolvent) | Li+–solvent binding energy | ev_doc_5a271b4ca1ac_000412_9060a44b5c6d |
| 5 | Interpret TFPM geometry | optimized Li+–TFPM structure | geometric analysis of DFT output | compare Li–O and Li–F contacts and ring topology | chelation interpretation | ev_doc_5a271b4ca1ac_000102_35a16c1113a0 |

## 4. Validation and analysis protocol

The optimized complex must be a true minimum by harmonic frequency analysis. Fragment calculations must use the same electronic-structure definition as the complex and the binding-energy sign convention must be stated. The authors report a Li–O contact of 1.853 Å, a Li–F contact of 1.845 Å, and describe a six-membered chelate for TFPM; these are private reference checks, not required public targets. The supplementary description identifies Supplementary Data 9 as the optimized Li+–TFPM coordinate source, but the supplied snapshot contains the description rather than the coordinate file itself.

## 5. Private reference results

The paper reports TFPM as having the most negative Li+–solvent binding energy in the compared set, with Eb = −2.16 eV. It reports Li–O = 1.853 Å, Li–F = 1.845 Å, and a stable six-membered chelating structure. The main-paper theory section defines Eb and attributes calculations to Gaussian 16 at B3LYP/6-311+G(d,p).

## 6. Limitations and interpretation boundaries

This benchmark evaluates a gas-phase electronic binding-energy protocol, not bulk-electrolyte solvation, LiFSI coordination, electrochemical performance, or a thermodynamic free energy. The public structure is a connectivity-level SMILES because the snapshot lacks the downloadable Supplementary Data 9 coordinates; conformer generation and orientation are therefore part of the Agent's investigation. Numerical agreement is method-, conformer-, and implementation-sensitive, so the evaluator also scores process validation and honest limitations.
