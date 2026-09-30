# Private paper route

## 1. Scientific objective and author claim

The paper tests how oxide-film thickness and noble-metal identity alter CO oxidation on supported cobalt oxide through interfacial electronic interaction. The computational claim is that electron transfer from the outermost CoO layer to the metal support polarizes surface Co–O bonds, making lattice-oxygen removal by CO more favorable; the effect is strongest for a one-layer film and follows Pt > Pd > Au > Ag in reactivity.

## 2. System and model boundary

The relevant models are epitaxial CoO films on fcc(111) noble-metal slabs. For the thickness study the substrate is a 2×2 Pt(111) slab with six metal layers and CoO lattice/substrate spacing strained to 3.18 Å; substrate atoms and two interfacial Co atoms are constrained to z-only relaxation. The support-comparison models use the analogous epitaxial construction at 3.15 Å for Pt, Pd, Au and Ag. The reaction is CO(g) + O(surface) → CO2(g) + an oxygen vacancy. Bader charge is summed for the outermost CoO layer relative to the noble-metal substrate.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Construct supported oxide films | fcc(111) noble-metal slabs and epitaxial CoO | VASP structural models | 2×2 cell; six metal layers for CoO thickness series; 3.18 Å spacing (3.15 Å for support comparison); bottom/registry constraints as above | Initial 1–3-layer interface geometries | ev_doc_128c24e48945_000077_9f0f56445474; ev_doc_128c24e48945_000080_859817874ceb |
| 2 | Relax electronic and ionic structures | interface geometries | VASP 5.4.1, PBE/PAW, Dudarev DFT+U | Ueff(Co)=3.5 eV; 500 eV plane-wave cutoff; SCF 10^-6 eV; unconstrained forces 0.02 eV Å^-1; 6×6×1 mesh for CoO thickness models | Optimized slabs and total energies | ev_doc_e3929a45aa3a_000816_f7a7a61feb47; ev_doc_e3929a45aa3a_000817_3fe4ca4b325a; ev_doc_128c24e48945_000080_859817874ceb |
| 3 | Find CO/lattice-O reaction pathway | relaxed slab, CO and CO2 references | NEB, CI-NEB, dimer and quasi-Newton searches | transition-state search across reactant/product endpoints | barriers, TS geometries and reaction energies | ev_doc_e3929a45aa3a_000722_08c0ba6de218; ev_doc_e3929a45aa3a_000816_f7a7a61feb47 |
| 4 | Quantify interfacial charge transfer | relaxed pristine interfaces and charge densities | Bader partitioning | charge assigned to outermost CoO layer versus metal slab | charge-transfer values for each support/thickness | ev_doc_e3929a45aa3a_000745_afd9c5dac396; ev_doc_e3929a45aa3a_000747_a83a4b02a13b |
| 5 | Relate electronic structure to reactivity | reaction energies, barriers and Bader charges | correlation/trend analysis | compare 1 and 2 ML films and Pt/Pd/Au/Ag supports | substrate trend and charge-transfer interpretation | ev_doc_e3929a45aa3a_000745_afd9c5dac396; ev_doc_e3929a45aa3a_000747_a83a4b02a13b |

## 4. Validation and analysis protocol

The authors checked SCF and force convergence, searched transition states with more than one algorithm, and compared film thickness and support identity. The reaction-energy convention is formation of gas-phase CO2 while leaving an O vacancy. Free-energy profiles use translational/rotational gas corrections at 100 °C, 100 mTorr CO and 0.1 mTorr CO2. The paper reports a 1.44 eV CO+lattice-O barrier and −1.66 eV net reaction energy for 1-ML CoO/Pt(111), and reports the qualitative support order Pt > Pd > Au > Ag for 1-ML reactivity; charge transfer from oxide to metal increases with reactivity.

## 5. Private reference results

The hidden reference includes the reported −1.66 eV net reaction energy and 1.44 eV barrier for 1-ML CoO/Pt(111), the 1-ML support reactivity order Pt > Pd > Au > Ag, stronger charge-transfer/reactivity variation for 1 ML than 2 ML, and the interpretation that oxide-to-metal transfer polarizes and weakens outermost Co–O bonds. Figure 9a supplies the plotted charge-transfer points but does not tabulate exact values; it is therefore used for qualitative/ordering evaluation rather than invented point estimates.

## 6. Limitations and interpretation boundaries

These are periodic slab DFT results, not a calibrated kinetic model. The paper notes uneven Stranski–Krastanov growth experimentally and does not establish a universal mechanism for every CoOx phase. Comparisons should preserve the stated reaction and charge-partition definitions; alternative reasonable electronic-structure choices must be reported as sensitivity/limitation evidence rather than silently mixed with the primary result.
