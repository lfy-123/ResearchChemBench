# ResearchChem Atomic Tool Catalog

Catalog hash: `640b6353d0995b81b52cd11f49a8d639501eb7c8836a9c7fcec0c1fa7254e1be`

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
| calculate_energy | molecular_electronic | EnergyResult | xtb, pyscf, psi4, tblite, mace, chgnet, orca, ase_emt | structure | Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. |
| calculate_forces | molecular_electronic | ForceResult | tblite, mace, chgnet, ase_emt | structure | Calculate atomic forces for one non-periodic structure or an aligned batch. |
| calculate_hessian | molecular_electronic | Hessian | xtb, psi4, tblite, orca, ase_emt | structure | Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. |
| optimize_geometry | molecular_electronic | AtomicStructure | xtb, tblite, mace, chgnet, orca, ase_emt | structure | Optimize one non-periodic geometry and return the optimized structure only as the primary result. |
| calculate_dipole_moment | molecular_electronic | DipoleResult | tblite, pyscf, psi4, orca | structure | Calculate one molecular dipole moment with an explicitly chosen electronic method. |
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
| minimize_system_energy | molecular_dynamics | ParameterizedSystem | openmm, gromacs, lammps | system | Minimize an already parameterized system without automatically equilibrating or propagating dynamics. |
| propagate_dynamics | molecular_dynamics | Trajectory | openmm, gromacs, lammps | system | Propagate exactly one agent-defined dynamics segment and return its trajectory and final state. |
| calculate_trajectory_rmsd | molecular_dynamics | TimeSeries | mdanalysis | trajectory, topology | Calculate an RMSD time series for an explicitly selected trajectory atom group and reference. |
| calculate_radius_of_gyration | molecular_dynamics | TimeSeries | mdanalysis | trajectory, topology | Calculate the radius-of-gyration time series for an explicitly selected atom group. |
| calculate_radial_distribution | molecular_dynamics | DistributionResult | mdanalysis | trajectory, topology | Calculate one radial distribution function for two explicitly selected atom groups. |
| calculate_mean_squared_displacement | molecular_dynamics | TimeSeries | mdanalysis | trajectory, topology | Calculate one mean-squared-displacement time series for an explicitly selected atom group. |
| evaluate_collective_variables | molecular_dynamics | TimeSeries | plumed | trajectory, topology, collective_variables | Evaluate explicitly defined collective variables on an existing trajectory. |
| calculate_periodic_energy | periodic_and_phonons | EnergyResult | quantum_espresso, cp2k, siesta, dftbplus, abinit | structure | Calculate one periodic-system energy with the explicitly selected electronic-structure backend. |
| calculate_periodic_forces | periodic_and_phonons | ForceResult | quantum_espresso, cp2k, siesta, dftbplus, abinit | structure | Calculate periodic atomic forces for one structure or aligned displaced-structure batch. |
| calculate_periodic_stress | periodic_and_phonons | StressResult | quantum_espresso, cp2k, abinit | structure | Calculate one periodic stress tensor without relaxing the structure. |
| relax_periodic_structure | periodic_and_phonons | AtomicStructure | quantum_espresso, cp2k, siesta, dftbplus, abinit | structure | Relax a periodic structure under explicit atomic/cell constraints. |
| generate_displaced_supercells | periodic_and_phonons | DisplacementSet | phonopy, phono3py | structure | Generate a displacement set from an explicit supercell matrix and displacement amplitude. |
| assemble_force_constants | periodic_and_phonons | ForceConstants | phonopy, phono3py | displacement_set, force_set | Assemble force constants only from a supplied displacement set and aligned forces. |
| calculate_phonon_dispersion | periodic_and_phonons | PhononDispersion | phonopy, phono3py | force_constants, structure | Calculate a phonon dispersion from existing force constants and an explicit q-point path. |
| calculate_phonon_density_of_states | periodic_and_phonons | PhononDensityOfStates | phonopy, phono3py | force_constants, structure | Calculate a phonon density of states from existing force constants and an explicit q mesh. |
| dock_ligand | docking | DockingResult | vina, gnina | receptor, ligand, search_space | Dock an already prepared ligand into an already prepared receptor using an explicit search space. |
| search_compounds | data_sources | CompoundRecords | pubchem | query | Search PubChem compound records by an explicit identifier and namespace. |
| search_protein_structures | data_sources | ProteinStructureRecords | rcsb_pdb | query | Search or retrieve RCSB PDB structure records using explicit identifiers or query terms. |
| search_materials | data_sources | MaterialRecords | materials_project | query | Search Materials Project records by material id, formula, or explicit query fields. |
| search_catalysis_records | data_sources | CatalysisRecords | catalysis_hub | query | Search Catalysis-Hub reaction records using explicit reactant/product filters. |

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
| openff_am1bcc | md | unavailable | openff-toolkit |  |  |  | open_source |
| openff | md | unavailable | openff-toolkit, openff-interchange |  |  |  | open_source |
| openmm_builder | md | available | openmm |  |  |  | open_source |
| packmol | md | unavailable | packmol |  | packmol |  | open_source |
| xtb | quantum | available | xtb |  | xtb |  | open_source |
| pyscf | quantum | available |  | pyscf |  |  | open_source |
| psi4 | psi4 | available | psi4 |  | psi4 |  | open_source |
| tblite | quantum | available |  | tblite==0.4.0 |  |  | open_source |
| mace | mlip | available |  | mace-torch==0.3.16 |  |  | open_source |
| chgnet | mlip | available |  | chgnet |  |  | open_source |
| orca | quantum | unavailable |  |  | orca |  | manual_license |
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
| mdanalysis | md | available |  | MDAnalysis |  |  | open_source |
| plumed | md | available | plumed |  | plumed |  | open_source |
| quantum_espresso | qe | available | qe |  | pw.x | UPF pseudopotentials covering every element in the calculation (for example SSSP or PseudoDojo), supplied as workspace Artifacts | open_source |
| cp2k | cp2k | available | cp2k |  | cp2k |  | open_source |
| siesta | periodic | available | siesta |  | siesta | SIESTA PSF or compatible pseudopotentials covering every element, supplied as workspace Artifacts | open_source |
| dftbplus | periodic | available | dftbplus |  | dftb+ | A DFTB+ Slater-Koster parameter-set directory containing every required element-pair .skf file (for example 3ob or matsci), supplied as a workspace Artifact | open_source |
| abinit | abinit | available | abinit |  | abinit | ABINIT-compatible pseudopotentials covering every element, supplied as workspace Artifacts | open_source |
| phonopy | phonons | available | phonopy |  | phonopy |  | open_source |
| phono3py | phonons | available | phono3py |  | phono3py |  | open_source |
| vina | docking | available | vina |  | vina |  | open_source |
| gnina | docking | unavailable |  |  | gnina |  | open_source |
| pubchem | services | available |  | pubchempy==1.0.5 |  |  | open_source |
| rcsb_pdb | services | available |  | httpx>=0.28 |  |  | open_source |
| materials_project | services | unavailable | mp-api |  |  |  | open_source |
| catalysis_hub | services | available |  | httpx>=0.28 |  |  | open_source |
