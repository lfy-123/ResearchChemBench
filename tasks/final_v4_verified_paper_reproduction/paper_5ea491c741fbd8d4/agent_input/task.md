# Scientific question

Which intermolecular contacts organize the supplied isoxazole crystal, what are their geometrical and surface-area contributions, and what do those results establish about their roles in packing?

# Input files

- `data/inputs/source_crystal.cif` contains the measured C12H11NO3 crystal at 300 K (CCDC 2445596, P 21/c, Z=4), including cell, symmetry, fractional coordinates, occupancies, ADPs and constrained X-ray H positions. Its 27-atom asymmetric unit expands to four formula units.
- `data/inputs/system.json` defines the complete neutral singlet molecular graph. `atom_mapping.json` maps its 27 atoms to CIF labels; `crystal_source_specification.json` gives crystallographic conditions.
- `source_provenance.json` and `input_status.json` document the supplied structure and its identity. `resource_limits.json` describes available-resource boundaries. All these files are under `data/inputs/`.

# Scope

The physical object is the supplied measured packing. Preserve its Z configuration at graph bond 7=8 and declare any hydrogen normalization or model transformation. Distinguish intermolecular contacts from intramolecular proximity. Quantify molecular Hirshfeld surface contact areas using a defined stockholder construction with neutron-normalized C–H distances, or demonstrate a physically equivalent area definition. Report combined inside/outside element orientations and percentages of total surface area, not atom counts. This defines the requested observable without prescribing software or a calculation sequence.

The question concerns crystal contacts and their physical interpretation; monomer orbital energies, docking, biochemical activity and lattice free-energy prediction are outside its scope.

# Author baseline for reproduction

The source attributes packing of the measured P21/c crystal to C–H···O motifs and aromatic contacts (§3.2–3.3, Figs.2–5). It uses CrystalExplorer 17.5 Hirshfeld surfaces and fingerprints, with hydrogen distances normalized to neutron values. It reports H···H 38.7%, O···H/H···O 29.1%, C···C 13.4%, N···H/H···N 9.7% and C···H/H···C 6.2%; these are author-derived surface fractions, author-derived area reference values to assess, not stabilization energies. Section 3.2 (physical PDF p4) labels 3.3883(6) angstrom as a centroid-centroid distance for Cg(1) = C9/C10/N1/O2/C11 and Cg(2) = C2/C3/C4/C5/C6/C7, with symmetry 1-X,-1/2+Y,1/2-Z. This is the author-reported value and label, not an independently certified target. Verify the full mapping and physical quantity definition against the supplied CIF, distinguishing the centroid norm from centroid-to-plane projections; document any evidenced source discrepancy. The separate isolated-molecule route is Gaussian 09/B3LYP/6-311+G(d,p), while another method sentence says 6-31+G(d,p); document that ambiguity. Neither the isolated orbital gap nor fingerprint percentages prove an interaction-energy ranking. Reproduce and critically assess the disclosed contact interpretation where the actual source data permit it. Pair-energy calculations, any cutoff comparison and additional robustness analyses would be your investigations, not author-reported protocols. No force-field, surface package or quantum code is asserted available merely because the authors used it.

Source interpretation and ambiguities: the methods continuation on physical PDF p3 gives a d_norm display range of -0.18 to 1.4 and labels it a.u.; p4 gives -0.676 to 1.415 and labels it angstrom. d_norm is a normalized distance quantity; the two ranges and the dimensional labels are inconsistent as reported. Record the definition and display settings actually used, and do not treat either printed interval as a certified numerical target or tolerance. In section 3.2, the S(7) C6-H6...O3 motif is intramolecular, whereas the C8-H8...O3 and C12-H12B...O2 contacts form the intermolecular R2^2(9) motif. Verify source labels and symmetry operations against authenticated coordinates before using them. The red/blue triangles on the shape-index surface and flat curvedness regions (pp4-6, Figs2-5) are the authors' evidence for a pi-packing interpretation; they do not measure stabilization energies or establish an energetic ordering. These are disclosed source interpretations to test against actual calculations and geometry.

Source attachments provided for PR: data/author_sources/2445596_original.cif preserves the full user-supplied deposition, and data/author_sources/isoxazole_mmc1.zip preserves the independently supplied 1a.cif. data/author_sources/checkcif_observations.md discloses the four-page checkCIF text with source hash (the official public-package contract excludes PDFs); data/author_sources/isoxazole_mmc3.docx contains Figs S1-S5 (NMR, chromatography/mass and UV-vis material) and Tables S1-S3 (source XRD/DFT intramolecular geometry comparisons). These are author disclosures, not newly generated evidence. Their broader spectroscopy and molecular-property content does not add tasks to the crystal-packing question. Use the common minimal CIF for an auditable structure baseline; the original retains source attribution and ancillary refinement data.


# Required results

1. Determine the H···H, H···O/O···H, C···C, H···N/N···H and C···H/H···C fractions of the molecular Hirshfeld surface. Give values in percent, the hydrogen treatment and numerical uncertainty.
2. Identify the relevant directional contacts and the intermolecular network they form. Use atom labels and symmetry to distinguish network connections from intramolecular contacts.
3. Characterize the neighboring isoxazole/phenyl ring arrangement. Define and calculate centroid separation, centroid-to-plane projection, lateral displacement and ring-plane angle; explain the packing relationship supported by those quantities.
4. Explain what the calculated contact distribution and geometry show about the relative packing roles of the interactions and whether they establish any energetic ordering.

# Submission

Submit `report/results.json` and `report/report.md` under the existing schema and guide, linking numerical results and conclusions to actual analysis inputs and native outputs. You choose the methods and checks needed to support your conclusions. Reconstructing structures or completing a protocol earns no separate points.
