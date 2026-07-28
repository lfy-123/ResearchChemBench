# Live Action/Backend Catalog Audit

Generated at `2026-07-28T17:31:50.528249+00:00` from the live catalog.

- Actions: 114
- Backends: 77
- Action/Backend pairs: 249

## Actions

| Action | Category | Backends |
|---|---|---|
| `align_molecular_structures` | Structure, conformers, charges, and system construction | `rdkit` |
| `analyze_crystal_symmetry` | Structure, conformers, charges, and system construction | `spglib`, `pymatgen` |
| `analyze_electron_density_topology` | Molecular electronic structure and derived properties | `critic2` |
| `analyze_free_energy_convergence` | Molecular dynamics propagation and trajectory analysis | `pymbar` |
| `analyze_periodic_bonding` | Periodic electronic structure and lattice dynamics | `lobster` |
| `analyze_reaction_coordinate` | Reaction paths, equilibrium, and kinetics | `internal_reaction_analysis` |
| `analyze_reaction_free_energy_profile` | Reaction paths, equilibrium, and kinetics | `goodvibes` |
| `analyze_thermochemical_ensemble` | Molecular electronic structure and derived properties | `goodvibes` |
| `analyze_thermochemical_selectivity` | Reaction paths, equilibrium, and kinetics | `goodvibes` |
| `assemble_force_constants` | Periodic electronic structure and lattice dynamics | `phonopy`, `phono3py` |
| `assign_force_field_parameters` | Structure, conformers, charges, and system construction | `openff`, `openmm_builder` |
| `assign_partial_charges` | Structure, conformers, charges, and system construction | `rdkit_gasteiger`, `openff_am1bcc` |
| `assign_protonation_states` | Structure, conformers, charges, and system construction | `rdkit`, `pdbfixer` |
| `assign_secondary_structure` | Molecular dynamics propagation and trajectory analysis | `mdtraj` |
| `build_supercell` | Structure, conformers, charges, and system construction | `pymatgen` |
| `calculate_atomic_basin_properties` | Molecular electronic structure and derived properties | `critic2` |
| `calculate_atomic_charges` | Molecular electronic structure and derived properties | `xtb`, `pyscf`, `psi4`, `nwchem`, `openmolcas`, `multiwfn`, `orca` |
| `calculate_bader_charges` | Molecular electronic structure and derived properties | `critic2` |
| `calculate_bond_orders` | Molecular electronic structure and derived properties | `xtb`, `multiwfn`, `orca` |
| `calculate_charge_spilling` | Periodic electronic structure and lattice dynamics | `lobster` |
| `calculate_chemical_equilibrium` | Reaction paths, equilibrium, and kinetics | `cantera` |
| `calculate_contacts` | Molecular dynamics propagation and trajectory analysis | `mdtraj` |
| `calculate_correlated_electron_density` | Molecular electronic structure and derived properties | `orca` |
| `calculate_density_of_states` | Periodic electronic structure and lattice dynamics | `gpaw` |
| `calculate_dihedral_distribution` | Molecular dynamics propagation and trajectory analysis | `mdtraj`, `mdanalysis` |
| `calculate_dipole_moment` | Molecular electronic structure and derived properties | `xtb`, `tblite`, `pyscf`, `psi4`, `nwchem`, `openmolcas`, `orca`, `gaussian`, `gamess` |
| `calculate_dynamic_cross_correlation` | Molecular dynamics propagation and trajectory analysis | `mdanalysis` |
| `calculate_electron_isodensity_surface` | Molecular electronic structure and derived properties | `multiwfn` |
| `calculate_electronic_band_structure` | Periodic electronic structure and lattice dynamics | `gpaw` |
| `calculate_energy` | Molecular electronic structure and derived properties | `xtb`, `pyscf`, `psi4`, `tblite`, `gpaw`, `nwchem`, `openmolcas`, `mace`, `chgnet`, `deepmd`, `orca`, `gaussian`, `gamess`, `ase_emt` |
| `calculate_excited_states` | Molecular electronic structure and derived properties | `pyscf`, `orca` |
| `calculate_force_field_energy` | Molecular dynamics propagation and trajectory analysis | `openmm`, `hoomd` |
| `calculate_force_field_forces` | Molecular dynamics propagation and trajectory analysis | `openmm`, `hoomd` |
| `calculate_forces` | Molecular electronic structure and derived properties | `xtb`, `pyscf`, `tblite`, `gpaw`, `nwchem`, `orca`, `mace`, `chgnet`, `deepmd`, `ase_emt` |
| `calculate_harmonic_thermodynamics` | Periodic electronic structure and lattice dynamics | `phonopy`, `phono3py` |
| `calculate_hessian` | Molecular electronic structure and derived properties | `xtb`, `pyscf`, `psi4`, `tblite`, `nwchem`, `orca`, `gaussian`, `mace`, `chgnet`, `deepmd`, `ase_emt` |
| `calculate_hydrogen_bonds` | Molecular dynamics propagation and trajectory analysis | `mdanalysis` |
| `calculate_lattice_thermal_conductivity` | Periodic electronic structure and lattice dynamics | `phono3py`, `shengbte` |
| `calculate_mean_squared_displacement` | Molecular dynamics propagation and trajectory analysis | `mdanalysis` |
| `calculate_molecular_descriptors` | Molecular descriptors, fingerprints, identifiers, and graph operations | `rdkit` |
| `calculate_molecular_fingerprint` | Molecular descriptors, fingerprints, identifiers, and graph operations | `rdkit` |
| `calculate_molecular_similarity` | Molecular descriptors, fingerprints, identifiers, and graph operations | `rdkit` |
| `calculate_orbitals` | Molecular electronic structure and derived properties | `pyscf`, `psi4`, `openmolcas`, `orca` |
| `calculate_periodic_energy` | Periodic electronic structure and lattice dynamics | `quantum_espresso`, `cp2k`, `siesta`, `dftbplus`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` |
| `calculate_periodic_forces` | Periodic electronic structure and lattice dynamics | `quantum_espresso`, `cp2k`, `siesta`, `dftbplus`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` |
| `calculate_periodic_stress` | Periodic electronic structure and lattice dynamics | `quantum_espresso`, `cp2k`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` |
| `calculate_phonon_density_of_states` | Periodic electronic structure and lattice dynamics | `phonopy`, `phono3py` |
| `calculate_phonon_dispersion` | Periodic electronic structure and lattice dynamics | `phonopy`, `phono3py` |
| `calculate_phonon_group_velocities` | Periodic electronic structure and lattice dynamics | `phonopy`, `phono3py` |
| `calculate_potential_of_mean_force` | Molecular dynamics propagation and trajectory analysis | `pymbar` |
| `calculate_principal_components` | Molecular dynamics propagation and trajectory analysis | `mdanalysis` |
| `calculate_projected_density_of_states` | Periodic electronic structure and lattice dynamics | `gpaw`, `lobster` |
| `calculate_radial_distribution` | Molecular dynamics propagation and trajectory analysis | `mdanalysis` |
| `calculate_radius_of_gyration` | Molecular dynamics propagation and trajectory analysis | `mdanalysis`, `mdtraj` |
| `calculate_rate_constants` | Reaction paths, equilibrium, and kinetics | `rmg` |
| `calculate_solvent_accessible_surface` | Molecular dynamics propagation and trajectory analysis | `mdtraj` |
| `calculate_trajectory_rmsd` | Molecular dynamics propagation and trajectory analysis | `mdanalysis`, `mdtraj` |
| `calculate_tunneling_correction` | Reaction paths, equilibrium, and kinetics | `rmg` |
| `cluster_conformers` | Structure, conformers, charges, and system construction | `rdkit` |
| `cluster_trajectory` | Molecular dynamics propagation and trajectory analysis | `mdtraj` |
| `decompose_force_field_energy` | Molecular dynamics propagation and trajectory analysis | `openmm` |
| `derive_ir_spectrum` | Molecular electronic structure and derived properties | `internal_spectroscopy` |
| `derive_thermochemistry` | Molecular electronic structure and derived properties | `internal_thermochemistry`, `goodvibes` |
| `derive_uv_vis_spectrum` | Molecular electronic structure and derived properties | `internal_spectroscopy` |
| `derive_vibrational_modes` | Molecular electronic structure and derived properties | `internal_vibrations` |
| `dock_ligand` | Molecular docking | `vina`, `gnina` |
| `enumerate_coordination_isomers` | Structure, conformers, charges, and system construction | `internal_reaction_analysis` |
| `enumerate_stereoisomers` | Molecular descriptors, fingerprints, identifiers, and graph operations | `rdkit` |
| `enumerate_surface_slabs` | Structure, conformers, charges, and system construction | `pymatgen` |
| `enumerate_tautomers` | Molecular descriptors, fingerprints, identifiers, and graph operations | `rdkit` |
| `estimate_free_energy_difference` | Molecular dynamics propagation and trajectory analysis | `pymbar` |
| `estimate_thermodynamic_expectations` | Molecular dynamics propagation and trajectory analysis | `pymbar` |
| `evaluate_collective_variables` | Molecular dynamics propagation and trajectory analysis | `plumed` |
| `export_electron_density_grid` | Molecular electronic structure and derived properties | `orca` |
| `generate_3d_structure` | Structure, conformers, charges, and system construction | `rdkit`, `openbabel` |
| `generate_conformer_ensemble` | Structure, conformers, charges, and system construction | `rdkit_etkdg`, `crest` |
| `generate_displaced_supercells` | Periodic electronic structure and lattice dynamics | `phonopy`, `phono3py` |
| `integrate_reaction_network` | Reaction paths, equilibrium, and kinetics | `scipy`, `cantera` |
| `locate_transition_state` | Reaction paths, equilibrium, and kinetics | `pysisyphus`, `sella` |
| `lookup_nist_webbook_species` | External chemistry data sources | `nist_webbook` |
| `minimize_system_energy` | Molecular dynamics propagation and trajectory analysis | `openmm`, `gromacs`, `lammps`, `hoomd`, `namd`, `amber_pmemd`, `charmm` |
| `normalize_pdb_records` | Structure, conformers, charges, and system construction | `pdb_tools` |
| `normalize_qcschema_molecule` | Scientific records, schemas, and output parsing | `qcelemental` |
| `optimize_geometry` | Molecular electronic structure and derived properties | `xtb`, `tblite`, `gpaw`, `mace`, `chgnet`, `deepmd`, `orca`, `gaussian`, `gamess`, `ase_emt`, `geometric`, `sella` |
| `parse_alchemical_energy_data` | Molecular dynamics propagation and trajectory analysis | `alchemlyb` |
| `parse_quantum_chemistry_output` | Scientific records, schemas, and output parsing | `cclib` |
| `propagate_dynamics` | Molecular dynamics propagation and trajectory analysis | `openmm`, `gromacs`, `lammps`, `hoomd`, `namd`, `amber_pmemd`, `charmm` |
| `rank_conformers_from_results` | Structure, conformers, charges, and system construction | `internal_statistics` |
| `relax_periodic_structure` | Periodic electronic structure and lattice dynamics | `quantum_espresso`, `cp2k`, `siesta`, `dftbplus`, `abinit`, `vasp`, `gpaw`, `nequip`, `allegro`, `deepmd` |
| `renumber_biomolecular_structure` | Structure, conformers, charges, and system construction | `pdb_tools` |
| `repair_biomolecular_structure` | Structure, conformers, charges, and system construction | `pdbfixer` |
| `resolve_chemical_identity` | External chemistry data sources | `pubchem` |
| `retrieve_compound_properties` | External chemistry data sources | `pubchem` |
| `retrieve_compound_structure` | External chemistry data sources | `pubchem` |
| `scan_reaction_coordinates` | Reaction paths, equilibrium, and kinetics | `pysisyphus` |
| `scan_thermochemistry_temperature` | Molecular electronic structure and derived properties | `goodvibes` |
| `search_catalysis_records` | External chemistry data sources | `catalysis_hub` |
| `search_compounds` | External chemistry data sources | `pubchem` |
| `search_local_substructures` | Molecular descriptors, fingerprints, identifiers, and graph operations | `rdkit` |
| `search_materials` | External chemistry data sources | `materials_project` |
| `search_protein_structures` | External chemistry data sources | `rcsb_pdb` |
| `search_reaction_path` | Reaction paths, equilibrium, and kinetics | `pysisyphus` |
| `search_similar_compounds` | External chemistry data sources | `pubchem` |
| `search_substructures` | External chemistry data sources | `pubchem` |
| `select_structure_subset` | Structure, conformers, charges, and system construction | `pdb_tools` |
| `solvate_molecular_system` | Structure, conformers, charges, and system construction | `openmm_builder`, `packmol` |
| `solve_master_equation` | Reaction paths, equilibrium, and kinetics | `mess`, `mesmer` |
| `solve_microkinetic_model` | Reaction paths, equilibrium, and kinetics | `catmap` |
| `standardize_crystal_structure` | Structure, conformers, charges, and system construction | `spglib`, `pymatgen` |
| `standardize_structure` | Structure, conformers, charges, and system construction | `rdkit` |
| `trace_intrinsic_reaction_coordinate` | Reaction paths, equilibrium, and kinetics | `pysisyphus` |
| `validate_qcschema_record` | Scientific records, schemas, and output parsing | `qcelemental` |
| `validate_reaction_path` | Reaction paths, equilibrium, and kinetics | `internal_reaction_analysis` |
| `validate_thermochemistry_inputs` | Molecular electronic structure and derived properties | `goodvibes` |

## Backends

| Backend | Action count |
|---|---:|
| `abinit` | 4 |
| `alchemlyb` | 1 |
| `allegro` | 4 |
| `amber_pmemd` | 2 |
| `ase_emt` | 4 |
| `cantera` | 2 |
| `catalysis_hub` | 1 |
| `catmap` | 1 |
| `cclib` | 1 |
| `charmm` | 2 |
| `chgnet` | 4 |
| `cp2k` | 4 |
| `crest` | 1 |
| `critic2` | 3 |
| `deepmd` | 8 |
| `dftbplus` | 3 |
| `gamess` | 3 |
| `gaussian` | 4 |
| `geometric` | 1 |
| `gnina` | 1 |
| `goodvibes` | 6 |
| `gpaw` | 10 |
| `gromacs` | 2 |
| `hoomd` | 4 |
| `internal_reaction_analysis` | 3 |
| `internal_spectroscopy` | 2 |
| `internal_statistics` | 1 |
| `internal_thermochemistry` | 1 |
| `internal_vibrations` | 1 |
| `lammps` | 2 |
| `lobster` | 3 |
| `mace` | 4 |
| `materials_project` | 1 |
| `mdanalysis` | 8 |
| `mdtraj` | 7 |
| `mesmer` | 1 |
| `mess` | 1 |
| `multiwfn` | 3 |
| `namd` | 2 |
| `nequip` | 4 |
| `nist_webbook` | 1 |
| `nwchem` | 5 |
| `openbabel` | 1 |
| `openff` | 1 |
| `openff_am1bcc` | 1 |
| `openmm` | 5 |
| `openmm_builder` | 2 |
| `openmolcas` | 4 |
| `orca` | 11 |
| `packmol` | 1 |
| `pdb_tools` | 3 |
| `pdbfixer` | 2 |
| `phono3py` | 7 |
| `phonopy` | 6 |
| `plumed` | 1 |
| `psi4` | 5 |
| `pubchem` | 6 |
| `pymatgen` | 4 |
| `pymbar` | 4 |
| `pyscf` | 7 |
| `pysisyphus` | 4 |
| `qcelemental` | 2 |
| `quantum_espresso` | 4 |
| `rcsb_pdb` | 1 |
| `rdkit` | 11 |
| `rdkit_etkdg` | 1 |
| `rdkit_gasteiger` | 1 |
| `rmg` | 2 |
| `scipy` | 1 |
| `sella` | 2 |
| `shengbte` | 1 |
| `siesta` | 3 |
| `spglib` | 2 |
| `tblite` | 5 |
| `vasp` | 4 |
| `vina` | 1 |
| `xtb` | 7 |

## Validation

This report is generated from the same immutable catalog used by MCP discovery. The test suite verifies that every Action id and provider Backend id appears here.
