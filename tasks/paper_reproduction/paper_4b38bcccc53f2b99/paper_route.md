# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to explain why alkali-metal retention changes the accessibility of high oxidation states in homoleptic imidophosphorane complexes.  The focused benchmark is the Pr4+/Pr3+ couple of potassium-containing 1-KPr(NPC2), K[Pr(NP(tBu)2(pyrrolidinyl))4].  The authors claim that a calculation in which K+ remains associated through oxidation reproduces the experimental anodic potential and therefore supports counterion retention on the electrochemical time scale (main paper p. 6; SI Tables S16–S18).

## 2. System and model boundary

The computed species are molecular gas-phase geometries subsequently evaluated with implicit THF solvation: neutral K[Pr3+(NPC2)4] and the singly charged oxidized K[Pr4+(NPC2)4]+, together with ferrocene/ferrocenium as the electrochemical reference.  The four NPC2 ligands are [NP(tBu)2(pyrr)]−, and K+ is the intercalated counterion.  The paper's reported experimental comparison is in THF versus Fc/Fc+; explicit solvent and solid-state packing are outside the model boundary.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Obtain equilibrium structures | XRD-based starting structures, or optimized lower-oxidation-state structures for unisolated species | Gaussian 16, unconstrained gas-phase DFT optimization | TPSSh; Pr ECP28MWB/ECP28MWB_ANO; K ECP46MWB/ECP46MWB; other atoms 6-311G(d) | Optimized geometries | ev_doc_bc83b60893e5_000832_d6f5e8a97880; ev_doc_bc83b60893e5_000854_4429f58ff645; ev_doc_bc83b60893e5_000855_68bc2b58f545; ev_doc_bc83b60893e5_000858_f844db698cfd; ev_doc_bc83b60893e5_000859_570b1618f261 |
| 2 | Verify stationary point and obtain thermal terms | Optimized structures | Gaussian 16 frequency calculation | Same electronic-structure model | No imaginary frequencies; ZPE and thermal corrections | ev_doc_bc83b60893e5_000879_96d9e83ba310 |
| 3 | Evaluate solution-phase energies | Optimized structures | Gaussian 16 single points with IEFPCM | THF solvent; same TPSSh/ECP/basis model | Solvated energies | ev_doc_bc83b60893e5_000878_e9875230b4cb; ev_doc_bc83b60893e5_000879_96d9e83ba310 |
| 4 | Convert the oxidation free-energy difference to a potential | Solvated/thermal quantities for KPr(NPC2), KPr(NPC2)+, Fc and Fc+ | Revised Born–Haber/isodesmic ferrocene calibration | Fc0/+ absolute half-cell reference in THF; TPSSh/LANL08 for Fe and 6-311G(d) for C/H | Pr4+/3+ potential vs Fc/Fc+ | ev_doc_bc83b60893e5_000876_24173aec5d2e; ev_doc_bc83b60893e5_000877_4db03f45b93f; ev_doc_bc83b60893e5_000878_e9875230b4cb |

## 4. Validation and analysis protocol

The optimized structure was required to be a true minimum (frequency calculation with no imaginary modes).  The redox result was compared to the experimental anodic wave for 1-KPr(NPC2) and to the corresponding calculated value in the counterion-retention series.  The authors also compared retained-K and cation-free/cation-ejected models across the NPC family to interpret the counterion effect.  Their experimental boundary is that 1-KPr(NPC2) shows an irreversible Pr4+/3+ wave with Epa = −0.60 V and Epc = −1.47 V versus Fc/Fc+ (main paper p. 4; SI Table S1).

## 5. Private reference results

SI Table S17 reports the calculated retained-K Pr4+/3+ potential for 1-KPr(NPC2) as −0.68 V.  The same table gives −0.76 V for NPC1 and −0.65 V for NPC3 in the KPr4+/3+ column.  The cation-free NPC2 value in SI Table S16 is −1.48 V.  These are hidden evaluator references, not public task inputs.  The experimental 1-KPr(NPC2) Epa/Epc pair is −0.60/−1.47 V (SI Table S1), and the main paper explicitly states that the retained-K theoretical value closely matches Epa.

## 6. Limitations and interpretation boundaries

The reference is a model-dependent theoretical potential, not a claim that an isolated gas-phase molecule has a directly measurable absolute potential.  Implicit solvation omits explicit solvent coordination; different conformers, spin treatments, relativistic Hamiltonians, thermal conventions and redox-reference implementations can shift the number.  Agreement with Epa supports the retained-counterion interpretation within this model but does not prove a unique microscopic electrochemical pathway.  The public benchmark therefore scores reproducible process evidence and a quantitatively reported potential, while requiring uncertainty and model limitations to be disclosed.
