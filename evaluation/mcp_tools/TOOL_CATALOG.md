# ResearchChem Atomic Tool Catalog

Catalog hash: `04f81e0f2ead56d3e2e8b57e69462eaad309d53ea43f2bd9f8b3939ca7585d0d`

The benchmark exposes every action below for every task. Backends are selected by the agent.

| Action | Category | Primary output | Backends | Required inputs | Description |
|---|---|---|---|---|---|
| standardize_structure | structure_and_system | AtomicStructure | rdkit | structure | Standardize one molecular representation without generating 3D coordinates or optimizing geometry. |
| generate_3d_structure | structure_and_system | AtomicStructure | rdkit, openbabel | molecule | Generate one explicit three-dimensional structure from a two-dimensional molecular representation. |
| generate_conformer_ensemble | structure_and_system | ConformerEnsemble | rdkit_etkdg, crest | molecule | Generate a conformer ensemble; it does not perform the later quantum refinement or final ranking workflow. |
| rank_conformers_from_results | structure_and_system | ConformerEnsemble | internal_statistics | ensemble, scores | Rank and weight conformers only from aligned energies or free energies already supplied by the agent. |
| repair_biomolecular_structure | structure_and_system | AtomicStructure | pdbfixer | structure | Repair missing biomolecular residues or atoms without choosing protonation, force field, solvent, or dynamics settings. |
| assign_protonation_states | structure_and_system | AtomicStructure | rdkit, pdbfixer | structure | Assign explicit protonation states using the agent-selected backend and pH/rule settings. |
| assign_partial_charges | structure_and_system | ChargedStructure | rdkit_gasteiger, openff_am1bcc | structure | Assign named force-field or docking partial charges without parameterizing or solvating the system. |
| assign_force_field_parameters | structure_and_system | ParameterizedSystem | openff, openmm_builder | structure | Assign an explicitly selected force field to an already prepared molecular system. |
| solvate_molecular_system | structure_and_system | ParameterizedSystem | openmm_builder, packmol | system | Build the explicitly requested solvent/ion environment without minimizing or propagating dynamics. |
| calculate_energy | molecular_electronic | EnergyResult | xtb, pyscf, psi4, tblite, mace, chgnet, deepmd, orca, gaussian, gamess, ase_emt | structure | Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. |
| calculate_forces | molecular_electronic | ForceResult | tblite, mace, chgnet, deepmd, ase_emt | structure | Calculate atomic forces for one non-periodic structure or an aligned batch. |
| calculate_hessian | molecular_electronic | Hessian | xtb, psi4, tblite, orca, gaussian, ase_emt | structure | Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. |
| optimize_geometry | molecular_electronic | AtomicStructure | xtb, tblite, mace, chgnet, deepmd, orca, gaussian, gamess, ase_emt | structure | Optimize one non-periodic geometry and return the optimized structure only as the primary result. |
| calculate_dipole_moment | molecular_electronic | DipoleResult | tblite, pyscf, psi4, orca, gaussian, gamess | structure | Calculate one molecular dipole moment with an explicitly chosen electronic method. |
| calculate_atomic_charges | molecular_electronic | AtomicChargeResult | pyscf, psi4 | structure | Calculate electronic-structure population-analysis charges without attaching force-field parameters. |
| calculate_orbitals | molecular_electronic | OrbitalResult | pyscf, psi4 | structure | Calculate orbital energies, occupations, and optional coefficient artifacts. |
| derive_vibrational_modes | molecular_electronic | FrequencyResult | internal_vibrations | hessian, structure | Derive frequencies and normal modes from an existing Hessian and structure. |
| derive_ir_spectrum | molecular_electronic | SpectrumResult | internal_spectroscopy | vibrations | Construct an IR spectrum from vibration results that already contain intensities. |
| derive_thermochemistry | molecular_electronic | ThermochemistryResult | internal_thermochemistry, goodvibes | energy, frequencies | Derive thermochemical quantities from supplied electronic energy and frequencies; no optimization or Hessian is hidden. |
| locate_transition_state | reaction_and_kinetics | AtomicStructure | pysisyphus | initial_guess | Locate one candidate transition-state structure without automatically running frequencies or IRC. |
| trace_intrinsic_reaction_coordinate | reaction_and_kinetics | ReactionPath | pysisyphus | transition_state | Trace an IRC from an already supplied transition-state structure. |
| calculate_chemical_equilibrium | reaction_and_kinetics | EquilibriumResult | cantera | composition | Calculate an equilibrium composition/state for an explicitly supplied mechanism and thermodynamic condition. |
| integrate_reaction_network | reaction_and_kinetics | KineticsTrajectory | scipy, cantera | network, initial_state | Integrate one explicitly specified reaction network over time. |
| solve_microkinetic_model | reaction_and_kinetics | MicrokineticResult | catmap | model | Solve one explicitly supplied microkinetic model without constructing the reaction model for the agent. |
| minimize_system_energy | molecular_dynamics | ParameterizedSystem | openmm, gromacs, lammps, namd, amber_pmemd, charmm | system | Minimize an already parameterized system without automatically equilibrating or propagating dynamics. |
| propagate_dynamics | molecular_dynamics | Trajectory | openmm, gromacs, lammps, namd, amber_pmemd, charmm | system | Propagate exactly one agent-defined dynamics segment and return its trajectory and final state. |
| calculate_trajectory_rmsd | molecular_dynamics | TimeSeries | mdanalysis | trajectory, topology | Calculate an RMSD time series for an explicitly selected trajectory atom group and reference. |
| calculate_radius_of_gyration | molecular_dynamics | TimeSeries | mdanalysis | trajectory, topology | Calculate the radius-of-gyration time series for an explicitly selected atom group. |
| calculate_radial_distribution | molecular_dynamics | DistributionResult | mdanalysis | trajectory, topology | Calculate one radial distribution function for two explicitly selected atom groups. |
| calculate_mean_squared_displacement | molecular_dynamics | TimeSeries | mdanalysis | trajectory, topology | Calculate one mean-squared-displacement time series for an explicitly selected atom group. |
| evaluate_collective_variables | molecular_dynamics | TimeSeries | plumed | trajectory, topology, collective_variables | Evaluate explicitly defined collective variables on an existing trajectory. |
| calculate_periodic_energy | periodic_and_phonons | EnergyResult | quantum_espresso, cp2k, siesta, dftbplus, abinit, vasp, nequip, allegro, deepmd | structure | Calculate one periodic-system energy with the explicitly selected electronic-structure backend. |
| calculate_periodic_forces | periodic_and_phonons | ForceResult | quantum_espresso, cp2k, siesta, dftbplus, abinit, vasp, nequip, allegro, deepmd | structure | Calculate periodic atomic forces for one structure or aligned displaced-structure batch. |
| calculate_periodic_stress | periodic_and_phonons | StressResult | quantum_espresso, cp2k, abinit, vasp, nequip, allegro, deepmd | structure | Calculate one periodic stress tensor without relaxing the structure. |
| relax_periodic_structure | periodic_and_phonons | AtomicStructure | quantum_espresso, cp2k, siesta, dftbplus, abinit, vasp, nequip, allegro, deepmd | structure | Relax a periodic structure under explicit atomic/cell constraints. |
| generate_displaced_supercells | periodic_and_phonons | DisplacementSet | phonopy, phono3py | structure | Generate a displacement set from an explicit supercell matrix and displacement amplitude. |
| assemble_force_constants | periodic_and_phonons | ForceConstants | phonopy, phono3py | displacement_set, force_set | Assemble force constants only from a supplied displacement set and aligned forces. |
| calculate_phonon_dispersion | periodic_and_phonons | PhononDispersion | phonopy, phono3py | force_constants, structure | Calculate a phonon dispersion from existing force constants and an explicit q-point path. |
| calculate_phonon_density_of_states | periodic_and_phonons | PhononDensityOfStates | phonopy, phono3py | force_constants, structure | Calculate a phonon density of states from existing force constants and an explicit q mesh. |
| dock_ligand | docking | DockingResult | vina, gnina | receptor, ligand, search_space | Dock an already prepared ligand into an already prepared receptor using an explicit search space. |
| search_compounds | data_sources | CompoundRecords | pubchem | query | Search PubChem compound records by an explicit identifier and namespace. |
| search_protein_structures | data_sources | ProteinStructureRecords | rcsb_pdb | query | Search or retrieve RCSB PDB structure records using explicit identifiers or query terms. |
| search_materials | data_sources | MaterialRecords | materials_project | query | Search Materials Project records by material id, formula, or explicit query fields. |
| search_catalysis_records | data_sources | CatalysisRecords | catalysis_hub | query | Search Catalysis-Hub reaction records using explicit reactant/product filters. |

## Registered scientific resources

| Resource | Kind | Backends | Version | Format | Status | Explicit selection syntax | Coverage |
|---|---|---|---|---|---|---|---|
| qe_sssp_1_3_pbe_efficiency | element_file_collection | quantum_espresso | 1.3.0 | UPF | available | resource://qe_sssp_1_3_pbe_efficiency/<Element> | 103 elements |
| qe_sssp_1_3_pbe_precision | element_file_collection | quantum_espresso | 1.3.0 | UPF | available | resource://qe_sssp_1_3_pbe_precision/<Element> | 103 elements |
| siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml | element_file_collection | siesta | nc-sr-05 standard | PSML 1.1 | available | resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/<Element> | 72 elements |
| abinit_pseudo_dojo_nc_sr_pbe_standard_psp8 | element_file_collection | abinit | standard | PSP8 | available | resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/<Element> | 70 elements |
| dftb_3ob_3_1 | slater_koster_parameter_set | dftbplus | 3.1.0 | Slater-Koster SKF | available | resource://dftb_3ob_3_1 | 15 elements/225 directed pairs |
| dftb_matsci_0_3 | slater_koster_parameter_set | dftbplus | 0.3.0 | Slater-Koster SKF | available | resource://dftb_matsci_0_3 | 11 elements/87 directed pairs |
| gnina_1_3_3_cuda12_8_linux_x86_64 | backend_executable | gnina | 1.3.3 | Linux x86_64 executable | available | runtime-managed | runtime-managed executable |
| orca_6_1_1_linux_x86_64_shared_openmpi418_avx2 | backend_executable | orca | 6.1.1 | Linux x86-64 AVX2 executable bundle | available | runtime-managed | runtime-managed executable |
| openmpi_4_1_8_orca_runtime | backend_executable | orca | 4.1.8 | Linux x86-64 shared MPI runtime | available | runtime-managed | runtime-managed executable |
| nequip_oam_s_0_1 | model_checkpoint | nequip | 0.1 | NequIP compiled model archive | available | resource://nequip_oam_s_0_1 | one exact checkpoint |
| nequip_oam_m_0_1 | model_checkpoint | nequip | 0.1 | NequIP compiled model archive | available | resource://nequip_oam_m_0_1 | one exact checkpoint |
| nequip_oam_l_0_1 | model_checkpoint | nequip | 0.1 | NequIP compiled model archive | available | resource://nequip_oam_l_0_1 | one exact checkpoint |
| nequip_oam_xl_0_1 | model_checkpoint | nequip | 0.1 | NequIP compiled model archive | available | resource://nequip_oam_xl_0_1 | one exact checkpoint |
| nequip_mp_l_0_1 | model_checkpoint | nequip | 0.1 | NequIP compiled model archive | available | resource://nequip_mp_l_0_1 | one exact checkpoint |
| allegro_oam_l_0_1 | model_checkpoint | allegro | 0.1 | NequIP compiled Allegro model archive | available | resource://allegro_oam_l_0_1 | one exact checkpoint |
| allegro_mp_l_0_1 | model_checkpoint | allegro | 0.1 | NequIP compiled Allegro model archive | available | resource://allegro_mp_l_0_1 | one exact checkpoint |
| deepmd_dpa_3_1_3m | model_checkpoint | deepmd | DPA-3.1-3M | DeePMD PyTorch frozen multitask model | available | resource://deepmd_dpa_3_1_3m | one exact checkpoint/31 explicit branches |
| deepmd_dpa_3_2_5m | model_checkpoint | deepmd | DPA-3.2-5M | DeePMD PyTorch frozen multitask model | available | resource://deepmd_dpa_3_2_5m | one exact checkpoint/23 explicit branches |
| deepmd_dpa_3_3_1m | model_checkpoint | deepmd | DPA-3.3-1M | DeePMD PyTorch frozen multitask model | available | resource://deepmd_dpa_3_3_1m | one exact checkpoint/23 explicit branches |
| deepmd_dpa_2_4_7m | model_checkpoint | deepmd | DPA-2.4-7M | DeePMD PyTorch frozen multitask model | available | resource://deepmd_dpa_2_4_7m | one exact checkpoint/39 explicit branches |
| deepmd_dpa3_omol_large | model_checkpoint | deepmd | DPA3-Omol-Large | DeePMD PyTorch frozen single-task model | available | resource://deepmd_dpa3_omol_large | one exact single-task checkpoint |
| vasp_6_3_2_testsuite_si_potcar | single_file_resource | vasp | VASP 6.3.2 testsuite | VASP POTCAR | available | resource://vasp_6_3_2_testsuite_si_potcar | one exact registered file |

## Backend installation and health

| Backend | Runtime | Status | Conda packages | Pip packages | Executables | External scientific data | License |
|---|---|---|---|---|---|---|---|
| rdkit | core | available | rdkit |  |  |  | open_source |
| openbabel | quantum | available | openbabel |  | obabel |  | open_source |
| rdkit_etkdg | core | available | rdkit |  |  |  | open_source |
| crest | reaction | available | crest, xtb |  | crest |  | open_source |
| internal_statistics | core | available |  |  |  |  | open_source |
| pdbfixer | md | available | pdbfixer, openmm |  |  |  | open_source |
| rdkit_gasteiger | core | available | rdkit |  |  |  | open_source |
| openff_am1bcc | openff | available | openff-toolkit, ambertools |  | antechamber, sqm |  | open_source |
| openff | openff | available | openff-toolkit, openff-interchange |  |  |  | open_source |
| openmm_builder | md | available | openmm |  |  |  | open_source |
| packmol | md | available | packmol |  | packmol |  | open_source |
| xtb | quantum | available | xtb |  | xtb |  | open_source |
| pyscf | quantum | available |  | pyscf |  |  | open_source |
| psi4 | psi4 | available | psi4 |  | psi4 |  | open_source |
| tblite | quantum | available |  | tblite==0.4.0 |  |  | open_source |
| mace | mlip | available |  | mace-torch==0.3.16 |  |  | open_source |
| chgnet | mlip | available |  | chgnet |  |  | open_source |
| deepmd | deepmd | available |  | deepmd-kit==3.2.0b0, ase, e3nn | dp | Explicit resource:// DeePMD model checkpoint; multitask checkpoints require a named model_branch and single-task checkpoints require model_branch=single_task | open_source |
| nequip | nequip | available |  | nequip==0.19.0 | nequip-train | Explicit resource:// NequIP checkpoint or workspace model ArtifactRef | open_source |
| allegro | nequip | available |  | nequip-allegro==0.8.3, nequip==0.19.0 |  | Explicit resource:// Allegro checkpoint or workspace model ArtifactRef | open_source |
| orca | quantum | available |  |  | orca |  | manual_license |
| gaussian | gaussian | available |  |  | g16, formchk |  | commercial_license |
| gamess | gamess | available |  |  | rungms |  | registration_license |
| ase_emt | core | available |  | ase |  |  | open_source |
| internal_vibrations | core | available |  | numpy |  |  | open_source |
| internal_spectroscopy | core | available |  | numpy |  |  | open_source |
| internal_thermochemistry | core | available |  | ase, numpy |  |  | open_source |
| goodvibes | reaction | available | goodvibes |  | goodvibes |  | open_source |
| pysisyphus | reaction | available |  | pysisyphus==1.0.0 | pysis |  | open_source |
| cantera | reaction | available | cantera |  |  |  | open_source |
| scipy | reaction | available |  | scipy |  |  | open_source |
| catmap | reaction | available |  | git+https://github.com/SUNCAT-Center/catmap.git |  |  | open_source |
| openmm | md | available | openmm |  |  |  | open_source |
| gromacs | md | available | gromacs |  | gmx |  | open_source |
| lammps | md | available | lammps |  | lmp |  | open_source |
| namd | namd | available |  |  | namd3 |  | academic_registration |
| amber_pmemd | amber | available |  |  | pmemd, pmemd.MPI, mpirun |  | academic_registration |
| charmm | charmm | available |  |  | charmm |  | academic_registration |
| mdanalysis | md | available |  | MDAnalysis |  |  | open_source |
| plumed | md | available | plumed |  | plumed |  | open_source |
| quantum_espresso | qe | available | qe |  | pw.x | Explicit ResourceRefs from qe_sssp_1_3_pbe_efficiency or qe_sssp_1_3_pbe_precision, one per element; workspace ArtifactRefs remain accepted | open_source |
| cp2k | cp2k | available | cp2k |  | cp2k |  | open_source |
| siesta | periodic | available | siesta |  | siesta | Explicit ResourceRefs from siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml, one per element; workspace ArtifactRefs remain accepted | open_source |
| dftbplus | periodic | available | dftbplus |  | dftb+ | Explicit ResourceRef to dftb_3ob_3_1 or dftb_matsci_0_3 with all required directed element-pair SKF files; workspace directory ArtifactRefs remain accepted | open_source |
| abinit | abinit | available | abinit |  | abinit | Explicit ResourceRefs from abinit_pseudo_dojo_nc_sr_pbe_standard_psp8, one per element; workspace ArtifactRefs remain accepted | open_source |
| vasp | vasp | available |  |  | vasp_std | One explicit POTCAR ResourceRef or workspace ArtifactRef per element; the registered Si POTCAR is testsuite-only and no production PAW family is selected automatically | commercial_license |
| phonopy | phonons | available | phonopy |  | phonopy |  | open_source |
| phono3py | phonons | available | phono3py |  | phono3py |  | open_source |
| vina | docking | available | vina |  | vina |  | open_source |
| gnina | docking | available |  |  | gnina |  | open_source |
| pubchem | services | available |  | pubchempy==1.0.5 |  |  | open_source |
| rcsb_pdb | services | available |  | httpx>=0.28 |  |  | open_source |
| materials_project | services | available | mp-api |  |  |  | open_source |
| catalysis_hub | services | available |  | httpx>=0.28 |  |  | open_source |
