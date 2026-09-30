# Scientific objective

Determine the ground-state frontier-orbital energy gaps of two supplied neutral molecules—CSO-CY and the CSO-CY + NH2OH product—and determine whether conversion changes the gap in a way that can support the reported fluorescence blue-shift interpretation. Determine from the supplied structures whether hydroxylamine-derived conversion changes the electronic gap and whether that change can support the stated optical interpretation. Do not assume a mechanism or direction in advance.

# Public inputs and scientific boundaries

Use `data/inputs/cso.xyz` (51 atoms) as CSO-CY and `data/inputs/product.xyz` (38 atoms) as the hydroxylamine-derived product. Each XYZ file gives element identities and Cartesian coordinates in Å for a neutral singlet S0 structure. No atom remapping, protonation change, fragmentation, or guessed connectivity is permitted. The calculation concerns isolated-molecule electronic orbital energies; an implicit solvent may be used only if fully disclosed. The measured quantity is ΔE_HL = E_LUMO − E_HOMO in eV, not an optical excitation energy or emission wavelength.

# Required scientific validation/investigation

Plan and execute one consistent, independently justified electronic-structure protocol for both named structures. State software, functional/correlation treatment, basis, dispersion, solvent treatment, charge and multiplicity, convergence settings, and how the starting geometries were handled. Verify that each calculation used the correct atom count and elements, reached a valid stationary/converged ground state, and produced identifiable HOMO and LUMO orbitals. If optimizing, report optimization convergence and a frequency/stationarity check or a scientifically justified alternative. Compute each gap, the product-minus-probe difference, and its direction using the same unit convention. A complete investigation requires both structures or an explicit, evidence-backed bounded failure for a named structure; do not silently substitute a different structure. Stop when both calculations have passed the stated identity/convergence checks and the paired comparison plus sensitivity/limitation discussion is complete. If a calculation cannot be completed, report the exact failed stage, diagnostics, and any valid partial result.

# Deliverables

Write `report/results.json` conforming to the submission schema. Include calculation provenance, per-structure identity and validation, HOMO/LUMO energies and gaps when available, paired difference/direction when available, conclusion, and limitations. Include enough command/input/output references for another researcher to reproduce the actual investigation. A bounded-failure branch is allowed only with truthful diagnostics and no fabricated numeric result.