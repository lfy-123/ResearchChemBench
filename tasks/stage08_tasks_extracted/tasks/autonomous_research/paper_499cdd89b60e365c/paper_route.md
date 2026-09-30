# Private paper route

## 1. Scientific objective and author claim

The authors use first-principles thermodynamics to test whether reduction of Ga2O3 and incorporation of Ga into Cu is feasible as a bulk alloy or as a Cu(111) surface alloy under methanol-synthesis conditions. Their qualitative claim is that bulk alloying is restricted to more reducing/high-temperature conditions, whereas surface alloying can begin under the lower-temperature reaction conditions, helping explain Ga promotion without a measurable bulk alloy.

## 2. System and model boundary

The computational system is Cu, β-Ga2O3, Cu-Ga bulk alloys, Cu(111) slabs with Ga substituted in the top layer, and gas-phase H2/H2O. Surface cells contain four layers and 2×2, 3×3, or 4×4 lateral repeats; the bottom two layers are fixed and 16 Å vacuum separates slabs. The thermodynamic reference is bulk β-Ga2O3 plus gas-phase H2/H2O; solid-phase entropy is omitted.

## 3. Authors' implemented computational route

| Step | Purpose | Input | Method/software | Key parameters | Output | Source evidence |
|---|---|---|---|---|---|---|
| 1 | Relax elemental, oxide, gas, bulk-alloy, and surface-alloy structures | Materials Project bulk structures; SI coordinate blocks; H2/H2O molecules | VASP 5.4.1 with ASE | PAW, BEEF-vdW, 500 eV cutoff; forces <0.01 eV/Å; stated Monkhorst-Pack meshes; gas vibrational finite differences at 0.01 Å | Relaxed geometries and total energies | ev_doc_adb4b9c183b5_000205_1dfae24c0cc9; ev_doc_3ede3706ba09_000117_a319f09b00a3 |
| 2 | Construct composition-dependent bulk and surface alloy free-energy diagrams | Relaxed energies, β-Ga2O3, H2, H2O | ASE thermodynamic post-processing | H2O/H2 pressure ratio and temperature; no solid entropy; alloy formation balanced against oxide reduction | Stable phase/coverage as a function of T and H2O/H2 | ev_doc_adb4b9c183b5_000211_008096d47b88; ev_doc_adb4b9c183b5_000212_d322fd50d182; ev_doc_adb4b9c183b5_000217_219361fbab9d |
| 3 | Compare the diagram with reaction conditions | Phase diagrams and estimated experimental point | Point-in-region interpretation | Reaction at 230 °C; H2/CO2=3; estimated H2O/H2 ≈3×10^-3 for roughly 2% conversion | Surface-onset interpretation and bulk/surface contrast | ev_doc_adb4b9c183b5_000590_0cafd8d0f4b4; ev_doc_adb4b9c183b5_000624_d322fd50d182; ev_doc_adb4b9c183b5_000625_1ba9979dc1bd |

## 4. Validation and analysis protocol

The authors compare the bulk and Cu(111) diagrams at the experimental point and use the qualitative contrast as validation against operando observations: no measurable bulk alloying near 230 °C, onset of bulk alloying at high temperature, and possible surface alloy formation at reaction-relevant conditions. The plotted experimental point has deviations, so interpretation is made over the stated point/error-bar region rather than at an artificially exact coordinate.

## 5. Private reference results

The paper reports that bulk alloying is associated with high-temperature conditions (around 480 °C feed / 530 °C TPR), while comparison of the surface diagram indicates onset of surface alloy formation under methanol-synthesis conditions. Figure 8b contains the hidden coverage/phase value at the experimental point. The SI also reports explicit stable Cu(111) surface-alloy compositions and energies in Table S16.

## 6. Limitations and interpretation boundaries

The β-Ga2O3 reference is described as an upper-limit reference for mostly amorphous Ga2O3. Solid entropy is neglected, finite slab sizes and selected substitution patterns do not exhaust configurational space, and the phase diagram is a thermodynamic model rather than a kinetic prediction. Surface alloying inferred from the diagram should not be treated as proof of a unique microscopic arrangement.
