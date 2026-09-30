# Private paper route

## 1. Scientific objective and author claim

The paper uses DFT to test a boron-mediated C1 hydroxylation mechanism for N-benzoyl carbazole (1a). The authors claim that coordination to BBr3, bromide transfer to a second BBr3 unit, intramolecular electrophilic substitution at C1, and deprotonation form the borylated intermediate; the C–H borylation event is the rate-limiting chemical step and the computed profile is consistent with the kinetic isotope effect.

## 2. System and model boundary

The modeled substrate is N-benzoyl carbazole (1a), with BBr3 as Lewis acid/reagent and dichloroethane as solvent. The modeled species are 1a, adduct A, borenium species B, Wheland intermediate C, borylation intermediate D, TS A–B and TS B–C, plus BBr3 and HBr reference species. The later oxidation/deprotection chemistry is outside the DFT profile.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize stationary points | 1a, BBr3 and proposed intermediates | Gaussian 16 DFT | M06-2X; 6-31G(d,p) for non-Br; SDD for Br; SMD DCE | optimized geometries and thermal data | ev_doc_79a5a57845fc_000558_20ba990e5306; ev_doc_79a5a57845fc_000560_0cd17c6fd8f6; ev_doc_79a5a57845fc_000564_703253fcedb4 |
| 2 | Classify stationary points | optimized structures | Gaussian 16 frequency calculations | same level; minima all real frequencies, TS one imaginary frequency | validated minima/TS | ev_doc_79a5a57845fc_000558_20ba990e5306; ev_doc_79a5a57845fc_000564_703253fcedb4 |
| 3 | Verify TS connectivity | TS A–B and TS B–C | Gaussian 16 IRC | forward/reverse IRC to adjacent minima | connectivity assignments | ev_doc_79a5a57845fc_000560_0cd17c6fd8f6; ev_doc_79a5a57845fc_000564_703253fcedb4 |
| 4 | Refine energies | validated optimized structures | Gaussian 16 single points | M06-2X/6-311+G(d,p) for non-Br with SDD for Br; SMD DCE | refined electronic energies | ev_doc_79a5a57845fc_000561_1a11171e547b; ev_doc_79a5a57845fc_000584_233b2989d5cc |
| 5 | Assemble profile | thermal corrections and refined energies | free-energy analysis | Gibbs free energies in DCE; relative to separated 1a + 2 BBr3 as defined by profile | step barriers, overall barrier, rate-determining step | ev_doc_333ef975639c_000123_7327214cd7d2; ev_doc_333ef975639c_000183_4ad97f53c6f3 |

## 4. Validation and analysis protocol

Every reported minimum was checked for zero imaginary frequencies and every reported transition state for exactly one. IRC calculations were used to establish that each TS joins the intended neighboring states. The free-energy profile was interpreted by comparing each transition-state free energy with its preceding minimum and by identifying the largest barrier from the initial separated reactants.

## 5. Private reference results

The paper reports a 10.2 kcal/mol free-energy release on complexation, an 11.3 kcal/mol barrier for TS A–B, an 11.5 kcal/mol barrier for TS B–C, a 20.9 kcal/mol free-energy release on deprotonation, and an overall barrier of 21.6 kcal/mol. The C–H borylation/electrophilic-substitution step is identified as rate-determining.

## 6. Limitations and interpretation boundaries

These are single-model-chemistry gas/continuum-solvent DFT results, not experimental activation free energies. The profile tests the proposed elementary sequence within the species boundary and does not establish all alternative aggregation, solvent, spin, or oxidation pathways.
