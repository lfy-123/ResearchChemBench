# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to explain why chiral macrocycle (+)-C[2]BNDI is a promising circularly polarized luminescence (CPL) emitter. The central computational claim is that its rigid chiral conformation produces a comparatively large calculated CPL dissymmetry factor for the S1→S0 transition.

## 2. System and model boundary

The calculated model is neutral, singlet C[2]BNDI with every n-octyl substituent replaced by methyl. The calculations use an SMD continuum solvent model. The molecular property of interest is the dimensionless magnitude of the luminescence dissymmetry factor, |g_lum|, derived from electric and magnetic transition dipoles for S1→S0.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Optimize and verify the ground-state minimum for the CPL subproblem | Methyl-truncated C[2]BNDI | Gaussian 16 DFT | B3LYP/6-31G(d), SMD, unconstrained geometry, neutral singlet; the CPL subsection does not specify D3 | Optimized geometry and frequencies; no imaginary frequencies | SI Section G, CPL subsection, page S24; ev_doc_1c553297f9ef_000191_403785856c82 |
| 2 | Obtain excited-state properties | Ground-state geometry | Gaussian 16 TD-DFT | B3LYP/6-31G(d), SMD; first three excited states optimized; CPL assigned to S1→S0 | S1 geometry and electric/magnetic transition dipoles | SI Section G, page S24; ev_doc_1c553297f9ef_000191_403785856c82 |
| 3 | Derive CPL dissymmetry | S1 transition dipoles | Multiwfn | CPL analysis using electric and magnetic transition dipoles | Calculated |g_lum| | SI Figure S29 and main-paper Figure 2 discussion; ev_doc_b580573d77f7_000153_a4fa98b480af |

## 4. Validation and analysis protocol

A valid ground-state structure is a stationary minimum with no imaginary vibrational frequencies. The excited-state calculation identifies the S1→S0 transition and obtains electric and magnetic transition-dipole information. The CPL observable is calculated from those dipoles, with geometry and state assignments retained for audit.

## 5. Private reference results

The main paper reports that (+)-C[2]BNDI has a 74.6° electric/magnetic transition-dipole angle and a calculated |g_lum| of 7.1 × 10−3. It contrasts this with (+)-C[3]BNDI, whose angle is nearly orthogonal and calculated value is an order of magnitude smaller.

## 6. Limitations and interpretation boundaries

The reported computation is a model result for methyl-truncated molecules in an implicit solvent, not a direct prediction of every experimental conformer, full octyl-substituted species, aggregate or solid-state environment. Alternative software or equivalent wavefunction analysis is scientifically acceptable if the state, dipoles, convention and provenance are explicit.

Source-method clarification (2026-09-19): SI S23's separate ground-state/ESP subsection explicitly includes Grimme D3, whereas the S24 CPL subsection specifies B3LYP/6-31G(d)/SMD without a dispersion keyword. The S23 keyword is therefore not asserted as an author CPL setting. The SI does not identify the SMD solvent; chloroform remains the declared benchmark boundary from the solution measurement context, not a recovered verbatim author parameter. No scientific objective, numeric reference or tolerance is changed by this clarification.
