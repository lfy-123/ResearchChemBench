# Scientific objective

Characterize the lowest singlet and triplet vertical excitations of the two fixed neutral Ir(III) arylacetylide molecules `IrF2ppz/H` and `IrF2ppz/CN`, and determine from independent electronic-structure evidence whether the lowest triplet is localized on the arylacetylide ligand or instead has substantial metal/cyclometalating-ligand character. Report the energies, dominant orbital transition, and a defensible state-character conclusion for each named complex.

# Public inputs and scientific boundaries

The public inputs are `data/inputs/irf2ppz_h.xyz` and `data/inputs/irf2ppz_cn.xyz`. Each XYZ file contains 58 atoms, element symbols, and Cartesian coordinates in Å for the named complex's optimized starting geometry. No solvent molecules are included. Use neutral charge and singlet ground-state multiplicity. The observables are vertical S0→S1 and S0→T1 excitation energies in eV, the dominant S0→T1 orbital configuration and contribution, and ligand/metal localization evidence. State explicitly the reference geometry, solvent boundary for each state, and the method used. The task does not ask for emission rates, relaxed excited-state geometries, or experimental-spectrum fitting.

# Required scientific validation/investigation

Plan and execute an independent calculation suitable for these fixed molecules. Before calculating, formulate at least one plausible computational route and, when more than one defensible route is available, compare alternatives on accuracy, cost, state/boundary consistency, and ability to support localization; select and justify the route actually used. This is a fixed direct characterization, so do not invent a molecule-discovery objective. Validate the reference geometry as a stationary minimum using a frequency or equivalent curvature check. Compute both requested states for both named complexes, inspect state ordering and spin, and analyze orbital contributions and localization using a reproducible population, orbital, density-difference, or equivalent analysis. State how alternative plausible state-character interpretations were discriminated and what was not tested. Completion requires all four energy observables and both named triplet assignments with validation evidence, or a bounded-failure report that identifies exactly which observable failed and preserves all successful results. Stop after both complexes pass the validation and state-character evidence requirements, or when a reproducible limitation prevents further progress; report coverage and the limitation.

# Deliverables

Submit `report/results.json` conforming to `submission_schema.json`. Include per-complex method, geometry/minimum validation, energies, state and localization evidence, conclusion, and uncertainty. If a calculation fails, use the schema's bounded-failure branch rather than inventing a value; include logs and evidence paths where available.
