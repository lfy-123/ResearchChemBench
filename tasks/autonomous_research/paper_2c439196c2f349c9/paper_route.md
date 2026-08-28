# Private paper route

## 1. Scientific objective and author claim

The paper uses a molecular DFT calculation to characterize the frontier electronic
structure of the azo-Schiff-base dye INP, 2-((E)-(isobutylimino)methyl)-4-((E)-(4-nitrophenyl)diazenyl)phenol.
The authors claim that its calculated frontier-orbital separation supports a stable,
insulator-like/wide-band-gap electronic structure and helps explain why the observed
CW nonlinear-optical response is substantially thermal rather than purely electronic.

## 2. System and model boundary

The calculated object is one isolated, neutral, closed-shell INP molecule in the gas
phase (charge 0, singlet multiplicity 1). The connectivity is the azo-linked,
nitro-substituted salicylaldehyde Schiff base with an isobutyl substituent on imine
nitrogen. The paper does not report a crystal, solvent, counterion, or explicit
excited-state model for this calculation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build the target molecule | INP constitution from synthesis/Scheme 1 | Gaussian 09 input construction | neutral closed shell | molecular geometry | ev_doc_9159d1046798_000040_67d4103bb924; ev_doc_9159d1046798_000065_d26c9a9dc2ae |
| 2 | Find an equilibrium geometry | initial INP geometry | DFT geometry optimization | B3LYP/6-31G(d,p) | optimized structure | ev_doc_9159d1046798_000065_d26c9a9dc2ae |
| 3 | Validate the stationary point | optimized geometry | harmonic frequency calculation | same stated level | no negative/imaginary frequencies | ev_doc_9159d1046798_000065_d26c9a9dc2ae |
| 4 | Obtain frontier orbital energies | validated optimized geometry | electronic single point/frontier-orbital analysis | same stated level | HOMO and LUMO energies | ev_doc_9159d1046798_000147_fb5434a55d33 |
| 5 | Form the gap and interpret it | HOMO/LUMO energies | arithmetic conversion | 1 a.u. = 27.2114 eV | ΔE = E(LUMO) − E(HOMO), in eV | ev_doc_9159d1046798_000147_fb5434a55d33; ev_doc_9159d1046798_000148_f8f337c8368e; ev_doc_9159d1046798_000150_ec73f9beae3d |

## 4. Validation and analysis protocol

The stationary point is accepted only after a frequency calculation shows no
negative frequencies. The frontier gap is computed from the orbital energies with
the LUMO-minus-HOMO convention and atomic-unit-to-eV conversion. Interpretation is
limited to the isolated-molecule orbital descriptor: the paper relates the large gap
to low electronic polarizability/insulator-like behavior, while attributing the large
CW NLO response mainly to thermal lensing. The paper does not establish that a single
optimization is the global minimum in the rigorous global-search sense.

## 5. Private reference results

The paper reports HOMO = −0.23029 a.u., LUMO = −0.10866 a.u., ΔE = 0.12163 a.u.
(3.31 eV after conversion). It describes the gap as consistent with an
insulator-like or wide-band-gap-semiconductor character and limited polarizability,
and says the strong CW NLO response is predominantly thermal.

## 6. Limitations and interpretation boundaries

Frontier-orbital gaps are method- and geometry-dependent descriptors, not measured
band gaps. The source gives no Cartesian starting geometry or exhaustive conformer
search. Comparisons should therefore evaluate a defensible converged calculation and
its validation, with numerical agreement interpreted within ordinary reproducibility
uncertainty rather than as a universal experimental constant.
