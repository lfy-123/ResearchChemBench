# ResearchChem Atomic Tool Catalog

Catalog hash: `62a5234cd4946edca48ed064f0b33ad2eebb509d0f0fcb91f1f59f7c2db66674`

The benchmark exposes every action below for every task. Provider selection follows each Action's policy.

| Action | Category | Primary output | Selection policy | Providers | Required inputs | Description |
|---|---|---|---|---|---|---|
| normalize_qcschema_molecule | scientific_data_interchange | QCSchemaMolecule | internal_deterministic | qcelemental | structure | Validate and normalize one supplied molecular structure into a QCSchema Molecule record without launching a calculation. |
| validate_qcschema_record | scientific_data_interchange | QCSchemaValidationResult | internal_deterministic | qcelemental | record | Validate one explicit QCSchema/QCArchive record type and return a normalized record or structured validation errors without executing it. |
| parse_quantum_chemistry_output | scientific_data_interchange | ParsedQuantumChemistryResult | internal_deterministic | cclib | output_file | Parse explicitly selected properties from one existing quantum-chemistry output file without rerunning the calculation. |
| standardize_structure | structure_and_system | AtomicStructure | agent_backend_required | rdkit | structure | Standardize one molecular representation without generating 3D coordinates or optimizing geometry. |
| generate_3d_structure | structure_and_system | AtomicStructure | agent_backend_required | rdkit, openbabel | molecule | Generate one explicit three-dimensional structure from a two-dimensional molecular representation. |
| generate_conformer_ensemble | structure_and_system | ConformerEnsemble | agent_backend_required | rdkit_etkdg, crest | molecule | Generate a conformer ensemble; it does not perform the later quantum refinement or final ranking workflow. |
| cluster_conformers | structure_and_system | ConformerClusterResult | agent_backend_required | rdkit | ensemble | Cluster an already supplied conformer ensemble by an explicit heavy/all-atom RMSD cutoff without generating or ranking conformers. |
| align_molecular_structures | structure_and_system | StructureAlignmentResult | agent_backend_required | rdkit | reference, probe, atom_map | Rigidly align one supplied 3D probe structure to a reference using an explicit atom-to-atom map. |
| rank_conformers_from_results | structure_and_system | ConformerEnsemble | internal_deterministic | internal_statistics | ensemble, scores | Rank and weight conformers only from aligned energies or free energies already supplied by the agent. |
| repair_biomolecular_structure | structure_and_system | AtomicStructure | agent_backend_required | pdbfixer | structure | Repair missing biomolecular residues or atoms without choosing protonation, force field, solvent, or dynamics settings. |
| select_structure_subset | structure_and_system | AtomicStructure | internal_deterministic | pdb_tools | structure | Select explicit chains and/or models from one PDB structure, with an explicit choice about retaining heteroatom records. |
| renumber_biomolecular_structure | structure_and_system | AtomicStructure | internal_deterministic | pdb_tools | structure | Renumber PDB atom serials and residue identifiers from explicit starting values without changing coordinates or chemistry. |
| normalize_pdb_records | structure_and_system | AtomicStructure | internal_deterministic | pdb_tools | structure | Sort and format one PDB record stream under explicit ordering, chain-break, and hybrid-36 choices. |
| assign_protonation_states | structure_and_system | AtomicStructure | agent_backend_required | rdkit, pdbfixer | structure | Assign explicit protonation states using the agent-selected backend and pH/rule settings. |
| assign_partial_charges | structure_and_system | ChargedStructure | agent_backend_required | rdkit_gasteiger, openff_am1bcc | structure | Assign named force-field or docking partial charges without parameterizing or solvating the system. |
| assign_force_field_parameters | structure_and_system | ParameterizedSystem | agent_backend_required | openff, openmm_builder | structure | Assign an explicitly selected force field to an already prepared molecular system. |
| solvate_molecular_system | structure_and_system | ParameterizedSystem | agent_backend_required | openmm_builder, packmol | system | Build the explicitly requested solvent/ion environment without minimizing or propagating dynamics. |
| analyze_crystal_symmetry | structure_and_system | CrystalSymmetryResult | agent_backend_required | spglib, pymatgen | structure | Determine the crystallographic space group and symmetry-equivalent sites for one supplied periodic structure. |
| standardize_crystal_structure | structure_and_system | AtomicStructure | agent_backend_required | spglib, pymatgen | structure | Standardize one periodic structure in an explicitly selected primitive or conventional crystallographic setting. |
| build_supercell | structure_and_system | AtomicStructure | agent_backend_required | pymatgen | structure | Apply one explicit integer supercell transformation to a periodic structure. |
| enumerate_surface_slabs | structure_and_system | StructureCollection | agent_backend_required | pymatgen | structure | Enumerate a bounded set of symmetry-distinct slabs for one explicit Miller index and slab/vacuum geometry. |
| calculate_molecular_descriptors | cheminformatics | MolecularDescriptorResult | agent_backend_required | rdkit | molecule | Calculate an explicitly selected set of graph-based molecular descriptors without generating coordinates or running electronic structure. |
| calculate_molecular_fingerprint | cheminformatics | MolecularFingerprint | agent_backend_required | rdkit | molecule | Calculate one explicitly selected molecular fingerprint representation. |
| calculate_molecular_similarity | cheminformatics | MolecularSimilarityResult | agent_backend_required | rdkit | molecule_a, molecule_b | Calculate one similarity value between two molecules using an explicit fingerprint and metric. |
| search_local_substructures | cheminformatics | SubstructureMatchResult | agent_backend_required | rdkit | molecule, query | Find atom-index matches for an explicit SMARTS or SMILES query in one supplied molecule. |
| enumerate_tautomers | cheminformatics | MoleculeCollection | agent_backend_required | rdkit | molecule | Enumerate bounded tautomeric forms without selecting a preferred tautomer for the agent. |
| enumerate_stereoisomers | cheminformatics | MoleculeCollection | agent_backend_required | rdkit | molecule | Enumerate bounded stereoisomers under explicit uniqueness and assignment rules. |
| calculate_energy | molecular_electronic | EnergyResult | agent_backend_required | xtb, pyscf, psi4, tblite, gpaw, nwchem, openmolcas, mace, chgnet, deepmd, orca, gaussian, gamess, ase_emt | structure | Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. |
| calculate_forces | molecular_electronic | ForceResult | agent_backend_required | xtb, pyscf, tblite, gpaw, nwchem, orca, mace, chgnet, deepmd, ase_emt | structure | Calculate atomic forces for one non-periodic structure or an aligned batch. |
| calculate_hessian | molecular_electronic | Hessian | agent_backend_required | xtb, pyscf, psi4, tblite, nwchem, orca, gaussian, mace, chgnet, deepmd, ase_emt | structure | Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. |
| optimize_geometry | molecular_electronic | AtomicStructure | agent_backend_required | xtb, tblite, gpaw, mace, chgnet, deepmd, orca, gaussian, gamess, ase_emt, geometric, sella | structure | Optimize one non-periodic geometry and return the optimized structure only as the primary result. |
| calculate_dipole_moment | molecular_electronic | DipoleResult | agent_backend_required | xtb, tblite, pyscf, psi4, nwchem, openmolcas, orca, gaussian, gamess | structure | Calculate one molecular dipole moment with an explicitly chosen electronic method. |
| calculate_atomic_charges | molecular_electronic | AtomicChargeResult | agent_backend_required | xtb, pyscf, psi4, nwchem, openmolcas, multiwfn, orca | structure | Calculate electronic-structure population-analysis charges without attaching force-field parameters. |
| calculate_orbitals | molecular_electronic | OrbitalResult | agent_backend_required | pyscf, psi4, openmolcas, orca | structure | Calculate orbital energies, occupations, and optional coefficient artifacts. |
| calculate_bond_orders | molecular_electronic | BondOrderResult | agent_backend_required | xtb, multiwfn, orca | structure | Calculate atom-pair electronic bond-order indices using one explicitly selected population-analysis backend. |
| calculate_excited_states | molecular_electronic | ExcitedStateResult | agent_backend_required | pyscf, orca | structure | Calculate a bounded set of vertical electronic excited states without constructing a broadened spectrum or propagating dynamics. |
| analyze_electron_density_topology | molecular_electronic | ElectronDensityTopologyResult | agent_backend_required | critic2 | density_file | Locate and characterize critical points in one supplied molecular or periodic electron-density field without generating that field or integrating atomic basins. |
| calculate_atomic_basin_properties | molecular_electronic | AtomicBasinPropertyResult | agent_backend_required | critic2 | density_file | Integrate population, Laplacian, and available volume properties over atomic or attractor basins in one supplied scalar-field grid using an explicitly selected partition algorithm. |
| calculate_bader_charges | molecular_electronic | AtomicChargeResult | agent_backend_required | critic2 | density_file | Calculate atomic Bader charges from one supplied electron-density grid using an explicitly selected Yu-Trinkle or Henkelman grid partition. |
| derive_vibrational_modes | molecular_electronic | FrequencyResult | internal_deterministic | internal_vibrations | hessian, structure | Derive frequencies and normal modes from an existing Hessian and structure. |
| derive_ir_spectrum | molecular_electronic | SpectrumResult | internal_deterministic | internal_spectroscopy | vibrations | Construct an IR spectrum from vibration results that already contain intensities. |
| derive_uv_vis_spectrum | molecular_electronic | SpectrumResult | internal_deterministic | internal_spectroscopy | excited_states | Construct a deterministic broadened UV/visible spectrum from supplied transition energies and oscillator strengths. |
| derive_thermochemistry | molecular_electronic | ThermochemistryResult | agent_backend_required | internal_thermochemistry, goodvibes | backend-specific: internal_thermochemistry(energy,frequencies); goodvibes(output_file) | Derive thermochemical quantities from supplied electronic energy and frequencies; no optimization or Hessian is hidden. |
| locate_transition_state | reaction_and_kinetics | AtomicStructure | agent_backend_required | pysisyphus, sella | initial_guess | Locate one candidate transition-state structure without automatically running frequencies or IRC. |
| trace_intrinsic_reaction_coordinate | reaction_and_kinetics | ReactionPath | agent_backend_required | pysisyphus | transition_state | Trace an IRC from an already supplied transition-state structure. |
| calculate_chemical_equilibrium | reaction_and_kinetics | EquilibriumResult | agent_backend_required | cantera | composition | Calculate an equilibrium composition/state for an explicitly supplied mechanism and thermodynamic condition. |
| integrate_reaction_network | reaction_and_kinetics | KineticsTrajectory | agent_backend_required | scipy, cantera | network, initial_state | Integrate one explicitly specified reaction network over time. |
| calculate_rate_constants | reaction_and_kinetics | RateConstantResult | agent_backend_required | rmg | kinetics_model, temperatures_kelvin | Evaluate an explicitly supplied Arrhenius, multi-Arrhenius, pressure-dependent Arrhenius, or Chebyshev kinetics model on explicit temperature/pressure points. |
| calculate_tunneling_correction | reaction_and_kinetics | TunnelingCorrectionResult | agent_backend_required | rmg | temperatures_kelvin, imaginary_frequency_cm1 | Calculate Wigner or Eckart transition-state tunneling correction factors at explicit temperatures. |
| solve_master_equation | reaction_and_kinetics | MasterEquationResult | agent_backend_required | mess, mesmer | model_file | Solve an explicitly supplied gas-phase chemical master-equation model and extract pressure/temperature-dependent phenomenological rate coefficients without constructing or modifying the reaction model. |
| solve_microkinetic_model | reaction_and_kinetics | MicrokineticResult | agent_backend_required | catmap | model | Solve one explicitly supplied microkinetic model without constructing the reaction model for the agent. |
| minimize_system_energy | molecular_dynamics | ParameterizedSystem | agent_backend_required | openmm, gromacs, lammps, hoomd, namd, amber_pmemd, charmm | system | Minimize an already parameterized system without automatically equilibrating or propagating dynamics. |
| calculate_force_field_energy | molecular_dynamics | ForceFieldEnergyResult | agent_backend_required | openmm, hoomd | system | Evaluate the total potential energy of an already parameterized system at explicitly selected stored coordinates/state without minimizing or propagating it. |
| calculate_force_field_forces | molecular_dynamics | ForceResult | agent_backend_required | openmm, hoomd | system | Evaluate atomic force-field forces for an already parameterized system at explicitly selected stored coordinates/state. |
| decompose_force_field_energy | molecular_dynamics | ForceFieldEnergyDecompositionResult | agent_backend_required | openmm | system | Decompose one OpenMM potential energy evaluation by the explicitly present Force objects without changing parameters or running dynamics. |
| propagate_dynamics | molecular_dynamics | Trajectory | agent_backend_required | openmm, gromacs, lammps, hoomd, namd, amber_pmemd, charmm | system | Propagate exactly one agent-defined dynamics segment and return its trajectory and final state. |
| calculate_trajectory_rmsd | molecular_dynamics | TimeSeries | agent_backend_required | mdanalysis, mdtraj | trajectory, topology | Calculate an RMSD time series for an explicitly selected trajectory atom group and reference. |
| calculate_radius_of_gyration | molecular_dynamics | TimeSeries | agent_backend_required | mdanalysis, mdtraj | trajectory, topology | Calculate the radius-of-gyration time series for an explicitly selected atom group. |
| calculate_radial_distribution | molecular_dynamics | DistributionResult | agent_backend_required | mdanalysis | trajectory, topology | Calculate one radial distribution function for two explicitly selected atom groups. |
| calculate_mean_squared_displacement | molecular_dynamics | TimeSeries | agent_backend_required | mdanalysis | trajectory, topology | Calculate one mean-squared-displacement time series for an explicitly selected atom group. |
| calculate_contacts | molecular_dynamics | ContactTimeSeries | agent_backend_required | mdtraj | trajectory, topology, residue_pairs | Calculate inter-residue contact distances for an explicitly supplied residue-pair set and contact definition. |
| calculate_solvent_accessible_surface | molecular_dynamics | SurfaceAreaTimeSeries | agent_backend_required | mdtraj | trajectory, topology | Calculate solvent-accessible surface area per atom or residue for an existing trajectory. |
| calculate_dihedral_distribution | molecular_dynamics | DihedralTimeSeries | agent_backend_required | mdtraj, mdanalysis | trajectory, topology, atom_quartets | Calculate dihedral-angle time series for explicitly supplied atom-index quartets. |
| calculate_hydrogen_bonds | molecular_dynamics | HydrogenBondResult | agent_backend_required | mdanalysis | trajectory, topology | Identify hydrogen-bond events in an existing trajectory using explicit donor, hydrogen, acceptor, distance, and angle definitions. |
| calculate_principal_components | molecular_dynamics | PrincipalComponentResult | agent_backend_required | mdanalysis | trajectory, topology | Calculate coordinate principal components and frame projections for an explicitly selected trajectory atom group. |
| calculate_dynamic_cross_correlation | molecular_dynamics | DynamicCrossCorrelationResult | agent_backend_required | mdanalysis | trajectory, topology | Calculate an atom-wise dynamic cross-correlation matrix from explicitly selected and optionally aligned trajectory coordinates. |
| assign_secondary_structure | molecular_dynamics | SecondaryStructureTimeSeries | agent_backend_required | mdtraj | trajectory, topology | Assign per-residue secondary-structure labels for every frame of an existing protein trajectory. |
| cluster_trajectory | molecular_dynamics | TrajectoryClusterResult | agent_backend_required | mdtraj | trajectory, topology | Cluster explicitly selected trajectory frames by RMSD using a deterministic cutoff-based leader assignment. |
| evaluate_collective_variables | molecular_dynamics | TimeSeries | agent_backend_required | plumed | trajectory, topology, collective_variables | Evaluate explicitly defined collective variables on an existing trajectory. |
| estimate_free_energy_difference | molecular_dynamics | FreeEnergyDifferenceResult | agent_backend_required | pymbar | reduced_potentials, samples_per_state | Estimate dimensionless pairwise free-energy differences from an explicitly supplied reduced-potential matrix and sample counts. |
| estimate_thermodynamic_expectations | molecular_dynamics | ThermodynamicExpectationResult | agent_backend_required | pymbar | reduced_potentials, samples_per_state, observables | Estimate state-resolved observable expectations from explicitly supplied samples and a reduced-potential matrix. |
| calculate_potential_of_mean_force | molecular_dynamics | FreeEnergyProfileResult | agent_backend_required | pymbar | reduced_potentials, samples_per_state, target_reduced_potential, collective_variable | Estimate a one-dimensional histogram free-energy profile from supplied uncorrelated samples; this does not integrate a mean-force trajectory or choose bins for the agent. |
| analyze_free_energy_convergence | molecular_dynamics | FreeEnergyConvergenceResult | agent_backend_required | pymbar | reduced_potentials, samples_per_state | Re-estimate one explicitly selected pairwise free-energy difference over supplied sample fractions without generating or decorrelating samples. |
| parse_alchemical_energy_data | molecular_dynamics | AlchemicalEnergyData | agent_backend_required | alchemlyb | files | Parse one or more explicitly identified engine output files into a normalized alchemical reduced-potential or derivative table. |
| calculate_periodic_energy | periodic_and_phonons | EnergyResult | agent_backend_required | quantum_espresso, cp2k, siesta, dftbplus, abinit, vasp, gpaw, nequip, allegro, deepmd | structure | Calculate one periodic-system energy with the explicitly selected electronic-structure backend. |
| calculate_periodic_forces | periodic_and_phonons | ForceResult | agent_backend_required | quantum_espresso, cp2k, siesta, dftbplus, abinit, vasp, gpaw, nequip, allegro, deepmd | structure | Calculate periodic atomic forces for one structure or aligned displaced-structure batch. |
| calculate_periodic_stress | periodic_and_phonons | StressResult | agent_backend_required | quantum_espresso, cp2k, abinit, vasp, gpaw, nequip, allegro, deepmd | structure | Calculate one periodic stress tensor without relaxing the structure. |
| relax_periodic_structure | periodic_and_phonons | AtomicStructure | agent_backend_required | quantum_espresso, cp2k, siesta, dftbplus, abinit, vasp, gpaw, nequip, allegro, deepmd | structure | Relax a periodic structure under explicit atomic/cell constraints. |
| calculate_electronic_band_structure | periodic_and_phonons | ElectronicBandStructureResult | agent_backend_required | gpaw | ground_state | Calculate electronic eigenvalue bands along one explicit reciprocal-space path from an existing converged periodic ground-state restart. |
| calculate_density_of_states | periodic_and_phonons | DensityOfStatesResult | agent_backend_required | gpaw | ground_state | Calculate a total electronic density of states on an explicit energy grid from an existing converged periodic ground-state restart. |
| calculate_projected_density_of_states | periodic_and_phonons | ProjectedDensityOfStatesResult | agent_backend_required | gpaw, lobster | projections | Calculate or extract explicitly requested atom/orbital projected electronic densities of states from an existing compatible periodic electronic-state artifact. |
| analyze_periodic_bonding | periodic_and_phonons | PeriodicBondingResult | agent_backend_required | lobster | integrated_bond_list | Extract explicitly selected integrated and optional energy-resolved COHP, COOP, or COBI bonding information from existing LOBSTER outputs. |
| calculate_charge_spilling | periodic_and_phonons | ProjectionQualityResult | agent_backend_required | lobster | lobster_output | Assess LOBSTER wavefunction-projection charge/total spilling against explicit acceptance thresholds from an existing lobsterout file. |
| generate_displaced_supercells | periodic_and_phonons | DisplacementSet | agent_backend_required | phonopy, phono3py | structure | Generate a displacement set from an explicit supercell matrix and displacement amplitude. |
| assemble_force_constants | periodic_and_phonons | ForceConstants | agent_backend_required | phonopy, phono3py | displacement_set, force_set | Assemble force constants only from a supplied displacement set and aligned forces. |
| calculate_phonon_dispersion | periodic_and_phonons | PhononDispersion | agent_backend_required | phonopy, phono3py | force_constants, structure | Calculate a phonon dispersion from existing force constants and an explicit q-point path. |
| calculate_phonon_density_of_states | periodic_and_phonons | PhononDensityOfStates | agent_backend_required | phonopy, phono3py | force_constants, structure | Calculate a phonon density of states from existing force constants and an explicit q mesh. |
| calculate_harmonic_thermodynamics | periodic_and_phonons | HarmonicThermodynamicsResult | agent_backend_required | phonopy, phono3py | force_constants, structure | Calculate harmonic free energy, entropy, and constant-volume heat capacity at explicitly supplied temperatures. |
| calculate_phonon_group_velocities | periodic_and_phonons | PhononGroupVelocityResult | agent_backend_required | phonopy, phono3py | force_constants, structure | Calculate mode-resolved phonon group-velocity vectors along an explicitly supplied q-point path. |
| calculate_lattice_thermal_conductivity | periodic_and_phonons | LatticeThermalConductivityResult | agent_backend_required | phono3py, shengbte | backend-specific: phono3py(second_order_force_constants,third_order_force_constants,structure); shengbte(control_file,second_order_force_constants_file,third_order_force_constants_file) | Calculate the lattice thermal-conductivity tensor from explicit second-/third-order force constants or a complete native BTE model under Agent-selected solution and scattering settings. |
| dock_ligand | docking | DockingResult | agent_backend_required | vina, gnina | receptor, ligand, search_space | Dock an already prepared ligand into an already prepared receptor using an explicit search space. |
| search_compounds | data_sources | CompoundRecords | fixed_source | pubchem | query | Search PubChem compound records by an explicit identifier and namespace. |
| resolve_chemical_identity | data_sources | ChemicalIdentity | fixed_source | pubchem | query | Resolve one explicit compound identifier to a bounded ChemicalIdentity record through PubChem. |
| retrieve_compound_properties | data_sources | CompoundPropertyRecords | fixed_source | pubchem | query | Retrieve an explicitly selected bounded property set for matching PubChem compounds. |
| retrieve_compound_structure | data_sources | StructureCollection | fixed_source | pubchem | query | Retrieve bounded PubChem 2D or 3D coordinate records while leaving coordinate dimensionality and explicit-hydrogen handling to the agent. |
| search_similar_compounds | data_sources | CompoundRecords | fixed_source | pubchem | query | Run one bounded PubChem 2D similarity search from an explicit structure identifier. |
| search_substructures | data_sources | CompoundRecords | fixed_source | pubchem | query | Run one bounded PubChem substructure search from an explicit SMILES, SMARTS, InChI, or CID query. |
| search_protein_structures | data_sources | ProteinStructureRecords | fixed_source | rcsb_pdb | query | Search or retrieve RCSB PDB structure records using explicit identifiers or query terms. |
| search_materials | data_sources | MaterialRecords | fixed_source | materials_project | query | Search Materials Project records by material id, formula, or explicit query fields. |
| search_catalysis_records | data_sources | CatalysisRecords | fixed_source | catalysis_hub | query | Search Catalysis-Hub reaction records using explicit reactant/product filters. |
| lookup_nist_webbook_species | data_sources | NISTWebBookSpeciesRecords | fixed_source | nist_webbook | query | Look up one bounded NIST Chemistry WebBook species query by explicit CAS number, exact name, or exact formula through the official CGI interface. |

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
| vasp_uspp_lda_legacy | variant_file_collection | vasp | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / ultrasoft pseudopotential | available | resource://vasp_uspp_lda_legacy/<Variant> | 102 exact variants/66 elements |
| vasp_uspp_gga_legacy | variant_file_collection | vasp | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / ultrasoft pseudopotential | available | resource://vasp_uspp_gga_legacy/<Variant> | 8 exact variants/8 elements |
| vasp_paw_lda_54 | variant_file_collection | vasp | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / PAW | available | resource://vasp_paw_lda_54/<Variant> | 316 exact variants/81 elements |
| vasp_paw_pw91_54 | variant_file_collection | vasp | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / PAW | available | resource://vasp_paw_pw91_54/<Variant> | 5 exact variants/5 elements |
| vasp_paw_pbe_54 | variant_file_collection | vasp | potpaw54 archive label; exact upstream revision unverified | VASP POTCAR / PAW | available | resource://vasp_paw_pbe_54/<Variant> | 304 exact variants/96 elements |
| vasp_6_3_2_testsuite_si_potcar | single_file_resource | vasp | VASP 6.3.2 testsuite | VASP POTCAR | available | resource://vasp_6_3_2_testsuite_si_potcar | one exact registered file |

## Backend installation and health

| Backend | Runtime | Status | Conda packages | Pip packages | Executables | External scientific data | License |
|---|---|---|---|---|---|---|---|
| qcelemental | workflows | available | qcelemental=0.50.4 |  |  |  | open_source |
| cclib | workflows | available | cclib=1.8.1 |  |  |  | open_source |
| rdkit | core | available | rdkit |  |  |  | open_source |
| openbabel | quantum | available | openbabel |  | obabel |  | open_source |
| rdkit_etkdg | core | available | rdkit |  |  |  | open_source |
| crest | reaction | available | crest, xtb |  | crest |  | open_source |
| internal_statistics | core | available |  |  |  |  | open_source |
| pdbfixer | md | available | pdbfixer, openmm |  |  |  | open_source |
| pdb_tools | core | available |  | pdb-tools==2.7.0 | pdb_selchain, pdb_reres, pdb_tidy |  | open_source |
| rdkit_gasteiger | core | available | rdkit |  |  |  | open_source |
| openff_am1bcc | openff | available | openff-toolkit, ambertools |  | antechamber, sqm |  | open_source |
| openff | openff | available | openff-toolkit, openff-interchange |  |  |  | open_source |
| openmm_builder | md | available | openmm |  |  |  | open_source |
| packmol | md | available | packmol |  | packmol |  | open_source |
| spglib | workflows | available | spglib, numpy |  |  |  | open_source |
| pymatgen | workflows | available | pymatgen, numpy |  |  |  | open_source |
| xtb | quantum | available | xtb |  | xtb |  | open_source |
| pyscf | quantum | available |  | pyscf |  |  | open_source |
| gpaw | gpaw | available | gpaw=25.7.0, ase, numpy |  | gpaw | GPAW PAW setup datasets under .software_cache/gpaw/setups | open_source |
| lobster | lobster | available | pymatgen |  | lobster-5.1.0 |  | academic_license |
| nwchem | nwchem | available | nwchem=7.3.1, qcengine=0.50.0, qcelemental=0.50.4, cclib |  | nwchem | NWChem basis libraries under .software_cache/nwchem/source/src/basis/libraries | open_source |
| openmolcas | openmolcas | available |  |  | pymolcas | OpenMolcas v25.10 basis_library managed under .software_cache/openmolcas/25.10 | open_source |
| multiwfn | multiwfn | available |  |  | Multiwfn_noGUI | Agent-supplied fch/fchk/wfn/wfx/mwfn/Molden/47 wavefunction file; both required Multiwfn citations are returned in provenance | custom_open_source_citation_required |
| critic2 | critic2 | available |  |  | critic2 | Agent-supplied electron-density grid or compatible wavefunction file; an explicit separate structure file is required when the density file does not contain geometry | open_source |
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
| internal_vibrations | core | available |  | ase, numpy |  |  | open_source |
| internal_spectroscopy | core | available |  | numpy |  |  | open_source |
| internal_thermochemistry | core | available |  | ase, numpy |  |  | open_source |
| goodvibes | reaction | available | goodvibes |  | goodvibes |  | open_source |
| geometric | nwchem | available |  | geometric==1.1.1 |  |  | open_source |
| sella | sella | available |  | sella==2.5.0 |  |  | open_source |
| pysisyphus | reaction | available |  | pysisyphus==1.0.0 | pysis |  | open_source |
| cantera | reaction | available | cantera |  |  |  | open_source |
| scipy | reaction | available |  | scipy |  |  | open_source |
| rmg | rmg | available | rmg=4.0.0 |  | rmg.py |  | open_source |
| mess | mess | available |  |  | mess |  | open_source |
| mesmer | mesmer | available |  |  | mesmer |  | open_source |
| catmap | reaction | available |  | git+https://github.com/SUNCAT-Center/catmap.git |  |  | open_source |
| openmm | md | available | openmm |  |  |  | open_source |
| gromacs | md | available | gromacs |  | gmx |  | open_source |
| lammps | md | available | lammps |  | lmp |  | open_source |
| hoomd | free_energy | available | hoomd=7.1.0, numpy |  |  |  | open_source |
| namd | namd | available |  |  | namd3 |  | academic_registration |
| amber_pmemd | amber | available |  |  | pmemd, pmemd.MPI, mpirun |  | academic_registration |
| charmm | charmm | available |  |  | charmm |  | academic_registration |
| mdanalysis | md | available |  | MDAnalysis |  |  | open_source |
| mdtraj | workflows | available | mdtraj, numpy |  |  |  | open_source |
| plumed | md | available | plumed |  | plumed |  | open_source |
| pymbar | free_energy | available | pymbar, numpy |  |  |  | open_source |
| alchemlyb | free_energy | available | alchemlyb=2.5.0, pandas, numpy |  |  |  | open_source |
| quantum_espresso | qe | available | qe |  | pw.x | Explicit ResourceRefs from qe_sssp_1_3_pbe_efficiency or qe_sssp_1_3_pbe_precision, one per element; workspace ArtifactRefs remain accepted | open_source |
| cp2k | cp2k | available | cp2k |  | cp2k |  | open_source |
| siesta | periodic | available | siesta |  | siesta | Explicit ResourceRefs from siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml, one per element; workspace ArtifactRefs remain accepted | open_source |
| dftbplus | periodic | available | dftbplus |  | dftb+ | Explicit ResourceRef to dftb_3ob_3_1 or dftb_matsci_0_3 with all required directed element-pair SKF files; workspace directory ArtifactRefs remain accepted | open_source |
| abinit | abinit | available | abinit |  | abinit | Explicit ResourceRefs from abinit_pseudo_dojo_nc_sr_pbe_standard_psp8, one per element; workspace ArtifactRefs remain accepted | open_source |
| vasp | vasp | available |  |  | vasp_std | One explicit POTCAR ResourceRef or workspace ArtifactRef per element; five operator-supplied production families expose exact directory-name variants and no family or variant is selected automatically | commercial_license |
| phonopy | phonons | available | phonopy |  | phonopy |  | open_source |
| phono3py | phonons | available | phono3py |  | phono3py |  | open_source |
| shengbte | shengbte | available |  |  | ShengBTE |  | open_source |
| vina | docking | available | vina |  | vina |  | open_source |
| gnina | docking | available |  |  | gnina |  | open_source |
| pubchem | services | available |  | pubchempy==1.0.5 |  |  | open_source |
| rcsb_pdb | services | available |  | httpx>=0.28 |  |  | open_source |
| materials_project | services | available | mp-api |  |  |  | open_source |
| catalysis_hub | services | available |  | httpx>=0.28 |  |  | open_source |
| nist_webbook | services | available |  | httpx>=0.28 |  | NIST Chemistry WebBook SRD 69 official CGI and its SRD copyright/licensing terms | nist_srd_terms |
