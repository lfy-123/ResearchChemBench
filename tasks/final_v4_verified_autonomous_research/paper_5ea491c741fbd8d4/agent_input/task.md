# Scientific question

Which intermolecular contacts organize the supplied isoxazole crystal, what are their geometrical and surface-area contributions, and what do those results establish about their roles in packing?

# Input files

- `data/inputs/source_crystal.cif` contains the measured C12H11NO3 crystal at 300 K (CCDC 2445596, P 21/c, Z=4), including cell, symmetry, fractional coordinates, occupancies, ADPs and constrained X-ray H positions. Its 27-atom asymmetric unit expands to four formula units.
- `data/inputs/system.json` defines the complete neutral singlet molecular graph. `atom_mapping.json` maps its 27 atoms to CIF labels; `crystal_source_specification.json` gives crystallographic conditions.
- `source_provenance.json` and `input_status.json` document the supplied structure and its identity. `resource_limits.json` describes available-resource boundaries. All these files are under `data/inputs/`.

# Scope

The physical object is the supplied measured packing. Preserve its Z configuration at graph bond 7=8 and declare any hydrogen normalization or model transformation. Distinguish intermolecular contacts from intramolecular proximity. Quantify molecular Hirshfeld surface contact areas using a defined stockholder construction with neutron-normalized C–H distances, or demonstrate a physically equivalent area definition. Report combined inside/outside element orientations and percentages of total surface area, not atom counts. This defines the requested observable without prescribing software or a calculation sequence.

The question concerns crystal contacts and their physical interpretation; monomer orbital energies, docking, biochemical activity and lattice free-energy prediction are outside its scope.

Choose your contact interpretation and computational methods independently.


# Required results

1. Determine the H···H, H···O/O···H, C···C, H···N/N···H and C···H/H···C fractions of the molecular Hirshfeld surface. Give values in percent, the hydrogen treatment and numerical uncertainty.
2. Identify the relevant directional contacts and the intermolecular network they form. Use atom labels and symmetry to distinguish network connections from intramolecular contacts.
3. Characterize the neighboring isoxazole/phenyl ring arrangement. Define and calculate centroid separation, centroid-to-plane projection, lateral displacement and ring-plane angle; explain the packing relationship supported by those quantities.
4. Explain what the calculated contact distribution and geometry show about the relative packing roles of the interactions and whether they establish any energetic ordering.

# Submission

Submit `report/results.json` and `report/report.md` under the existing schema and guide, linking numerical results and conclusions to actual analysis inputs and native outputs. You choose the methods and checks needed to support your conclusions. Reconstructing structures or completing a protocol earns no separate points.
