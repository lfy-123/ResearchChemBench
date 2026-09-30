# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT energetics to test a UV-induced photocyclization explanation for the solid-state photochromism of tetraphenylethylene derivative 1. The authors propose four cyclized stereoisomers (two E and two Z), interpret the E products as lower than the Z products, and report that all cyclized products lie above the open reactant. They report high reactant-to-Z barriers.

## 2. System and model boundary

Neutral, closed-shell compound 1 (C44H31NO6) is treated as an isolated molecule in its electronic ground state. The comparison is between the open reactant and four intramolecular photocyclization products. Solvent, crystal packing, and excited-state dynamics are outside the electronic-structure calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build open reactant and four E/Z cyclization models | Compound structures/geometries | Gaussian 09 | Neutral ground-state molecules | Five structures | ev_doc_6c41f6e52df1_000214_fca80956942b |
| 2 | Relax all structures | Molecular geometries | DFT optimization | B3LYP/6-311+G(d,p) | Optimized geometries | ev_doc_6c41f6e52df1_000110_a7d28dd668ca; ev_doc_6c41f6e52df1_000111_5cd9a3d853b0; ev_doc_6c41f6e52df1_000112_8575da31557e |
| 3 | Compare electronic energies | Optimized structures | Same DFT model | Hartree energies converted to kJ mol−1 | Relative energy profile | ev_doc_79646157cc91_000163_39e32d5fa223; ev_doc_79646157cc91_000168_fff1487462ff; ev_doc_79646157cc91_000179_bba40ee760c4 |
| 4 | Interpret mechanism | Energy profile | Comparison with experiment | Reactant-to-Z barrier range | Mechanistic conclusion | ev_doc_6c41f6e52df1_000237_8bbd021486dd |

## 4. Validation and analysis protocol

The authors optimized twenty structures for compounds 1–4 and E/Z products, then used TD-DFT for UV-visible spectra. The compound-1 profile compares open and cyclized structures on a common electronic-energy scale. The paper reports a range for barriers between reactants and Z isomers; no transition-state coordinate is supplied in the cited SI energy-profile material.

## 5. Private reference results

SI energies for compound 1 are: open −2202.0670279 Hartree; 1-E1 −2202.0009561; 1-E2 −2202.0009262; 1-Z1 −2201.9904353; 1-Z2 −2201.988573. The main text reports reactant-to-Z barriers of 173.4–190.4 kJ mol−1. E products are lower than Z products, while all cyclized products are above the reactant.

## 6. Limitations and interpretation boundaries

These isolated-molecule ground-state results do not establish photochemical kinetics, crystal packing, or an excited-state activation free energy. Reports must distinguish reproduction of the electronic-energy profile from a true kinetic barrier.
