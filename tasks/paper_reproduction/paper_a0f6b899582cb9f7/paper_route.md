# Private paper route

## 1. Scientific objective and author claim

The paper uses electronic-structure calculations to characterize the designed solid additive M3, 2,5-di(thiophen-2-yl)pyrazine. The authors claim that its planar, internally N···S-locked, zero-net-dipole structure has a large quadrupole component along the pi-pi stacking direction and therefore can strengthen interactions with donor and acceptor materials.

## 2. System and model boundary

The computed object is an isolated neutral M3 molecule (C12H8N2S2), with the two thiophen-2-yl groups attached at the 2 and 5 positions of pyrazine. The reported tensor is expressed in the molecular principal/stacking frame; Qzz is the component assigned to the pi-pi stacking direction. This is a gas-phase molecular property calculation, not a periodic film or device simulation.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Build and optimize M3 geometry | M3 molecular structure | DFT, Gaussian | B3LYP/6-31G | optimized geometry | ev_doc_807d3d1df12c_000194_3a3167107ee8; ev_doc_807d3d1df12c_000028_db19c7557038 |
| 2 | Evaluate molecular electrostatic multipoles | optimized M3 | Gaussian multipole analysis | same electronic-structure level | quadrupole tensor components | ev_doc_b2705987463b_000041_0d9109c0bce5 |
| 3 | Interpret the stacking-axis component | Qxx, Qyy, Qzz | comparison with additive table and molecular orientation | z assigned to pi-pi stacking direction | Qzz and qualitative comparison | ev_doc_807d3d1df12c_000030_79d6a1267049; ev_doc_b2705987463b_000041_0d9109c0bce5 |

## 4. Validation and analysis protocol

The authors describe the optimized molecule as planar and report an N···S separation of 2.95 Å, shorter than the summed van der Waals radii quoted as 3.35 Å. They use the resulting quadrupole components to argue that the stacking-axis component is unusually large and that the additive can interact with both PM6 and BTP-eC9. The SI Table S1 is the source of the three M3 components.

## 5. Private reference results

For M3, Table S1 reports Qxx = -83.67 D, Qyy = -103.14 D and Qzz = -108.35 D. The main text states that the total dipole is 0 D, that the molecule is planar with an N···S lock, and that Qzz is the pi-pi stacking-direction component. The paper further reports binding-energy ranges for model fragments and device/morphology consequences, but those are outside this task's scored molecular-property endpoint.

## 6. Limitations and interpretation boundaries

Quadrupole components depend on origin, axis convention and electronic-structure model; the evaluator therefore requires the submitted frame and convention, and scores the stacking-axis assignment rather than treating arbitrary Cartesian Qzz as equivalent. An isolated-molecule calculation does not establish a solid-state interaction energy or device efficiency. The paper itself contains a software inconsistency (Gaussian 09 in the characterization paragraph and Gaussian 03 in the dedicated DFT subsection); the reproduction task exposes only the qualitative route and leaves software/model choice to the Agent.

## 2026-09-15 dimensional clarification

The SI Table S1 prints [Debye] for quadrupoles. This is dimensionally incomplete: the Gaussian raw electric quadrupole (second moment) is in Debye angstrom, whereas the dipole is in Debye. Evaluator tensor fields and unit labels now explicitly use Debye angstrom; source numeric targets and tolerances are unchanged. Use the full raw tensor rotated into the declared molecular frame, not the traceless tensor. The stacking direction is the molecular-plane normal. This is a unit-label clarification, not a conversion, rescaling or fitted shift of computed values.
