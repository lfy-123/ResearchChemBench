# Private paper route

## 1. Scientific objective and author claim

The paper studies how methyl substitution on an aromatic π-acceptor changes the O–H stretching response of a weak TFE···aromatic hydrogen-bond complex.  The authors claim that their one-dimensional anharmonic local-mode treatment reproduces the observed O–H band positions and that methyl substitution increases the π-electron density and interaction, producing larger O–H redshifts in the gas-phase series.  They also use the calculated transition intensity in their equilibrium-constant analysis.

## 2. System and model boundary

The systems are TFE (2,2,2-trifluoroethanol) and its complexes with benzene, toluene, o-xylene, m-xylene, and p-xylene.  The reported lowest-energy complexes use gauche TFE; the O–H donor points toward the aromatic π system.  The scored calculated observables are the fundamental O–H local-mode transition frequency and oscillator strength.  Geometry and harmonic-frequency calculations use electronic structure theory; the anharmonic observable is obtained from a one-dimensional O–H coordinate model.  Experimental gas and matrix spectra are contextual validation, not substitutes for the calculated observable.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Generate stationary complex structures and identify minima | TFE···aromatic starting structures, with gauche TFE | Gaussian 16; DFT geometry optimization and harmonic frequencies | B3LYP-D3 with Grimme GD3 damping; aug-cc-pVTZ; frequencies used to verify no imaginary modes | Optimized geometries, harmonic frequencies, binding-energy/conformer information | `ev_doc_d897c3f9770a_000043_cf5de9d14867`; `ev_doc_403500397c02_000280_d0cd7b82f7f5` |
| 2 | Compute the anharmonic O–H local-mode transition | Optimized geometry; PES and dipole-moment data along O–H displacement | Python 3 implementation of the 1D anharmonic local-mode model; electronic surfaces at B3LYP-D3/aug-cc-pVTZ | q = −0.5 to +1.5 Å relative to equilibrium, 0.05 Å samples; cubic-spline interpolation to Δq = 0.00002 Å; Simpson integration; first 50 associated Legendre polynomials, m=1 | Fundamental O–H frequency and oscillator strength; overtone quantities also tabulated in SI | `ev_doc_d897c3f9770a_000046_050c960191e2`; `ev_doc_d897c3f9770a_000047_f2b28a9bebcd`; `ev_doc_d897c3f9770a_000048_413c05eb2e8a`; `ev_doc_d897c3f9770a_000050_49e333d432b8`; `ev_doc_d897c3f9770a_000051_151169f99332` |
| 3 | Compare model with spectroscopy and analyze substitution trend | Calculated frequencies/intensities and observed band positions | Tabulation and trend comparison | Fundamental transition; gas-phase observations for Benz/Tol/m-Xyl and matrix observations for xylenes; authors note method/model and thermal limitations | Agreement assessment, methyl-substitution trend, intensity interpretation | `ev_doc_d897c3f9770a_000329_d7cdd53d342f`; `ev_doc_d897c3f9770a_000335_96483660ede0`; `ev_doc_403500397c02_000298_e66d3bab7f3f` |

## 4. Validation and analysis protocol

The authors require optimized structures to be true minima by harmonic-frequency analysis.  They compare 1D-LM frequencies with observed O–H maxima and discuss the maximum discrepancy and the sources of discrepancy (thermal population, the one-dimensional model, and electronic-structure limitations).  The SI supplies multiple conformers for substituted systems and tabulates their energies and 1D-LM observables; the main comparison uses the lowest-energy conformers for the gas-phase series.  Reduced-dimensional VPT2 checks are used to show that oscillator strengths are comparatively insensitive to inclusion of additional intermolecular modes.  The authors interpret methyl substitution through ESP/NBO/NCI analyses, while warning that equilibrium stability includes secondary interactions and is not determined by O–H redshift alone.

## 5. Private reference results

For the lowest-energy/main-comparison complexes, the paper reports 1D-LM fundamental O–H frequencies and oscillator strengths of approximately: TFE···Benz 3573 cm⁻¹ and 4.9×10⁻⁵; TFE···Tol 3570 cm⁻¹ and 5.1×10⁻⁵; TFE···m-Xyl 3558 cm⁻¹ and 5.3×10⁻⁵.  The SI additionally reports conformer-resolved values for Tol and the xylenes, including o-Xyl, m-Xyl, and p-Xyl.  The paper reports observed gas-phase frequencies of 3608, 3600, and 3592 cm⁻¹ for Benz, Tol, and m-Xyl, respectively, and discusses matrix-isolation assignments for the xylenes.  These values are hidden from the evaluated Agent and are used only by the evaluator.

## 6. Limitations and interpretation boundaries

The one-dimensional local-mode model omits coupling to other vibrations; the electronic method and finite PES sampling introduce method dependence.  Gas and matrix measurements have different environments, and thermal population affects gas-phase band positions.  Conformer multiplicity is important for substituted aromatics, so an agent must state whether it reports a selected conformer or an ensemble and must preserve identity.  A frequency trend is not, by itself, a binding-energy or equilibrium-constant ranking.
