# Private upgraded paper route

Status: pending scientific validation, development package; A → proposed B.

The paper proposes that donor–acceptor electronic asymmetry and bridge conjugation influence field response and rectification. It uses phenyl donors, pyrimidinyl acceptors and sulfur anchors; Group B doubles the aromatic units. Its isolated route uses Gaussian 16 B3LYP/6-31+G(d) geometries with terminal S constraints, followed by B3LYP/6-311++G(d,p) properties. The actual junction route is QuantumATK W-2024.09 DFT–NEGF/PBE, Au(111), SZP for Au and DZP for other atoms, a 4x4x130 k grid and 75 Hartree mesh cutoff, with four central-region Au layers at each side and a 0.05 eV/angstrom relaxation criterion. These are source settings, not evidence that SIESTA is equivalent or that those cutoffs are converged here. QuantumATK is not asserted to be available. The proposed allowed alternative SIESTA/TranSIESTA/TBtrans chain requires its own validated entry points and lead calculation. Matched reversal and unilateral 0.2-angstrom contact perturbation below are new benchmark interventions, not author-validated controls. The manuscript prints a malformed Fermi difference; use the physical f_L-f_R expression in the public definitions.

## Expanded scientific scope

Test whether isolated molecular polarity predicts rectification across the no-bridge, ethene-bridge and ethane-bridge Group A donor–acceptor molecules. Separate bridge-dependent transmission from orientation and Au-contact effects using genuine self-consistent positive/negative-bias transport.

First validate the allowed native NEGF chain for one mapped AD_base junction at zero and both nonzero biases, with explicit lead/electrode inputs, Hamiltonian/self-energy dependencies and TBtrans current/transmission artifacts. Full studies wait for this gate. Then compute zero-field vector dipoles for all three isolated molecules, and T(E,V), potential drop and I(V) for all five configurations at all three biases. Reintegrate I=(2e/h) integral T(E,V)[f_L−f_R]dE for the unpolarized spin-degenerate convention and check bias/energy units. Define R=|I(+0.5)|/|I(−0.5)| without silently inverting it. If the denominator is unresolved relative to the measured current floor, report bounds and evidence, not a huge asserted ratio. Compare all three bridge types and separately quantify AD reversal and unilateral contact changes. Validate lead matching, zero-bias current and tighter k/quadrature plus screening-layer sensitivity. Support or reject a dipole proxy only within this matched Au model.

## Historical boundary

Old fixed isolated-AD dipole and force check are molecular calibration only. They contain no current, electrode self-energy, transmission or finite-bias convergence. The prior scalar target is removed. Source optimized coordinates remain private and cannot prove independent device construction.

The previous route is preserved verbatim in `evaluation/legacy_final_snapshot/paper_route.md.snapshot`; its old scope and PASS claims do not govern this task.
