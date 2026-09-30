# Private paper route

## 1. Scientific objective and author claim

The paper tests how relocating a π-bridge spacer changes inverted solvatochromism in phenolate–nitroaryl push–pull dyes. For dye 3, the authors claim that the lowest-energy visible transition is an intramolecular charge-transfer (ICT) excitation from the phenolate donor toward the nitroaryl acceptor; agreement between experiment and TDDFT supports that assignment (ev_doc_3c131162617b_000112_b0151dd61ab6, ev_doc_3c131162617b_000118_6d48212257e0).

## 2. System and model boundary

The computed solute is the singly deprotonated (phenolate) form of compound 10, the E-imine made from 4-aminophenol and 4-(5-nitrothiophen-2-yl)benzaldehyde: a phenolate–imine–para-phenylene–5-nitrothiophen-2-yl π scaffold. The electronic state is closed-shell singlet, charge −1. Solvent is dichloromethane represented by a continuum model.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Locate equilibrium geometry | Dye 3 phenolate | ORCA DFT | r2SCAN-3c; RI; CPCM/CH2Cl2 | Optimized structure | ev_doc_3c131162617b_000242_4db4f21d3d11, ev_doc_3c131162617b_000243_99af383eb51c |
| 2 | Verify a minimum | Optimized structure | ORCA frequencies | Same r2SCAN-3c/CPCM model | Frequencies; no imaginary mode | ev_doc_3c131162617b_000242_4db4f21d3d11 |
| 3 | Compute Franck–Condon excitations | Validated minimum | ORCA TDDFT | ω-B97X-D4/def2-TZVP; RI and COSX; CPCM/CH2Cl2 | Excitation energies, oscillator strengths, orbital/transition character | ev_doc_3c131162617b_000243_99af383eb51c, ev_doc_3c131162617b_000244_45f88c3f22d0 |
| 4 | Compare assignment and energy | Lowest-energy visible state | Paper analysis | Compare calculated and experimental band and inspect donor/acceptor orbital localization | Quantitative and mechanistic validation | ev_doc_3c131162617b_000112_b0151dd61ab6, ev_doc_3c131162617b_000118_6d48212257e0 |

## 4. Validation and analysis protocol

The optimized structure was frequency-checked as a potential-energy-surface minimum. The authors examined the two low-lying transitions, assigning the higher-energy transition to localized π–π* character and the lower-energy transition to ICT. Frontier-orbital localization and the solvent-dependent experimental band were used together to interpret the ICT state. The reported experimental and calculated lower-band energies were compared quantitatively.

## 5. Private reference results

The paper reports 59.44 kcal mol−1 for the calculated dye-3 lower-energy ICT band and 57.18 kcal mol−1 experimentally (ev_doc_3c131162617b_000118_6d48212257e0). It reports 84.79 kcal mol−1 calculated versus 77.48 kcal mol−1 experimental for the higher-energy band (ev_doc_3c131162617b_000112_b0151dd61ab6, ev_doc_3c131162617b_000118_6d48212257e0). The lower state is phenolate-to-nitroaryl CT with HOMO on phenolate and LUMO on nitroaryl (ev_doc_3c131162617b_000112_b0151dd61ab6).

## 6. Limitations and interpretation boundaries

The continuum-solvent and finite-conformer treatment do not establish a complete condensed-phase ensemble. The benchmark therefore scores a defensible, independently documented calculation and assignment for the defined solute/model boundary, not universal experimental reproduction or proof that no other conformer/state exists.
