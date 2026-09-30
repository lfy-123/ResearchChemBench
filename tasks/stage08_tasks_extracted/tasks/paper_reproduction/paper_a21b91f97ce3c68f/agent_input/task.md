# Scientific objective

Independently determine a defensible value for the average signed one-bond ^1J(^119Sn–^13C_Bu) coupling of the fixed neutral-singlet axial galactose-derived tributyltin molecule in `data/inputs/compound_1a_axial.xyz`. Explain what the computed observable says about the electronic structure and identify limitations of using one calculation to interpret a heavy-atom NMR coupling. Generate and test your own electronic-structure explanations from the supplied system and your calculations.

## Author-provided scientific guidance

**Author hypothesis or claim.**
The authors propose that antiperiplanar donor→σ*(C–Sn) hyperconjugation modulates one-bond tin–carbon coupling: stronger donation is expected to weaken and lengthen C–Sn and reduce the coupling magnitude.

**Candidate route or mechanism.**
Consider donation from oxygen lone pairs or σ(C–H) bonds aligned antiperiplanar to the anomeric C–Sn bond. Such delocalization could alter the s-character at carbon and tin and thereby the Fermi-contact contribution to the coupling. This supplies a candidate electronic explanation for interpreting the Sn–C_Bu observable, distinct from the optional anomeric Sn–C coupling.

**Discriminating evidence.**
The authors used DFT geometries and frequency checks, NBO second-order donor–acceptor stabilization energies, and heteronuclear spin–spin coupling calculations to connect donation with bond lengths, hybridization, and coupling. Relating these electronic and geometric diagnostics to the computed couplings can assess the proposed explanation within the supplied structure.

# Public inputs and scientific boundaries

The sole molecular input is the 43-atom XYZ file, whose first line gives atom count and whose comment identifies a neutral singlet (charge 0, multiplicity 1). Atom order is fixed. The Sn atom is atom 1; in the supplied geometry the three directly bonded butyl carbons are the three closest carbon atoms to Sn (atoms 2, 3, and 7, approximately 2.18–2.20 Å initially). Reconfirm that assignment from the final geometry and report atom indices and distances explicitly. The system boundary is the isolated molecule; solvent may be added only as a separately labelled sensitivity test. The measured quantities are optimized-geometry minimum evidence, signed ^1J(^119Sn–^13C) for each identified Sn–butyl carbon pair, their arithmetic mean in Hz, and optionally the anomeric Sn–C coupling if the corresponding carbon is identified unambiguously. Use the supplied molecular input and your own calculations as the evidence for the result; do not consult the paper, SI, or general web.

# Required scientific validation/investigation

Choose and justify the electronic-structure and relativistic/NMR method. Optimize the supplied structure and perform a vibrational or equivalent stationarity check; report whether the final structure is a minimum and give the evidence (for example, imaginary-frequency count). Compute the three individual one-bond Sn–C_Bu couplings and the mean, stating sign convention, isotope treatment, units, geometry, and software. Validate atom-pair assignment from the final geometry rather than silently assuming labels. If the preferred calculation fails, submit a bounded-failure report with logs and the last valid geometry/results. Completion requires either a converged, validated calculation with all three couplings and mean, or a scientifically honest bounded failure with reproducibility details. Stop after the validated result or after documenting the specific software/resource/SCF limitation and one reasonable recovery attempt; do not claim universal accuracy from one molecule. Explain any mechanistic/electronic interpretation as an inference from your own evidence.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`, plus supporting files under `report/` as needed (input-to-output atom mapping, optimization/frequency and NMR logs, and method details). The JSON must include status, method, minimum validation, explicit pair identities, individual couplings when available, mean coupling when available, uncertainty/limitations, and a concise scientific conclusion.
