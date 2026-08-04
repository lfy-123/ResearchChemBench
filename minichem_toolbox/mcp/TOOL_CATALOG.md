# MiniChem Atomic Tool Catalog

Catalog hash: `e959ee31836e00f0603d26282f106b4485f14ab34719f7733271bb53679b377a`

These predefined Actions are the validated common-operation layer. They are exposed to every task but are not mandatory; the MCP server also exposes native-software and programmable-analysis layers. Provider selection follows each Action's policy.

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
| enumerate_coordination_isomers | structure_and_system | CoordinationIsomerAssignments | internal_deterministic | internal_reaction_analysis | structure, coordination_center_index, ligand_anchor_indices | Enumerate symmetry-distinct ligand-to-site assignments for an explicitly selected coordination geometry without inventing coordinates or ranking their energies. |
| assign_protonation_states | structure_and_system | AtomicStructure | agent_backend_required | rdkit | structure | Assign explicit protonation states using the agent-selected backend and pH/rule settings. |
| assign_partial_charges | structure_and_system | ChargedStructure | agent_backend_required | rdkit_gasteiger | structure | Assign named force-field or docking partial charges without parameterizing or solvating the system. |
| search_local_substructures | cheminformatics | SubstructureMatchResult | agent_backend_required | rdkit | molecule, query | Find atom-index matches for an explicit SMARTS or SMILES query in one supplied molecule. |
| enumerate_tautomers | cheminformatics | MoleculeCollection | agent_backend_required | rdkit | molecule | Enumerate bounded tautomeric forms without selecting a preferred tautomer for the agent. |
| enumerate_stereoisomers | cheminformatics | MoleculeCollection | agent_backend_required | rdkit | molecule | Enumerate bounded stereoisomers under explicit uniqueness and assignment rules. |
| calculate_energy | molecular_electronic | EnergyResult | agent_backend_required | xtb, gaussian | structure | Calculate one molecular or non-periodic scalar energy with the exact software and method selected by the agent. |
| calculate_forces | molecular_electronic | ForceResult | agent_backend_required | xtb | structure | Calculate atomic forces for one non-periodic structure or an aligned batch. |
| calculate_hessian | molecular_electronic | Hessian | agent_backend_required | xtb, gaussian | structure | Calculate one molecular Hessian without deriving modes, spectra, or thermochemistry. |
| optimize_geometry | molecular_electronic | AtomicStructure | agent_backend_required | xtb, gaussian, sella | structure | Optimize one non-periodic geometry and return the optimized structure only as the primary result. |
| calculate_dipole_moment | molecular_electronic | DipoleResult | agent_backend_required | xtb, gaussian | structure | Calculate one molecular dipole moment with an explicitly chosen electronic method. |
| calculate_atomic_charges | molecular_electronic | AtomicChargeResult | agent_backend_required | xtb, multiwfn | structure | Calculate electronic-structure population-analysis charges without attaching force-field parameters. |
| calculate_electron_isodensity_surface | molecular_electronic | ElectronIsodensitySurfaceResult | agent_backend_required | multiwfn | density_file | Calculate molecular electron-isodensity surface area and enclosed volume for an explicit list of density cutoffs using one supplied wavefunction or electron-density grid. |
| calculate_bond_orders | molecular_electronic | BondOrderResult | agent_backend_required | xtb, multiwfn | structure | Calculate atom-pair electronic bond-order indices using one explicitly selected population-analysis backend. |
| derive_vibrational_modes | molecular_electronic | FrequencyResult | internal_deterministic | internal_vibrations | hessian, structure | Derive frequencies and normal modes from an existing Hessian and structure. |
| derive_ir_spectrum | molecular_electronic | SpectrumResult | internal_deterministic | internal_spectroscopy | vibrations | Construct an IR spectrum from vibration results that already contain intensities. |
| derive_thermochemistry | molecular_electronic | ThermochemistryResult | agent_backend_required | internal_thermochemistry, goodvibes | backend-specific: internal_thermochemistry(energy,frequencies); goodvibes(output_file) | Derive thermochemical quantities from supplied electronic energy and frequencies; no optimization or Hessian is hidden. |
| scan_thermochemistry_temperature | molecular_electronic | ThermochemistryTemperatureSeries | agent_backend_required | goodvibes | output_files, temperatures_kelvin | Evaluate thermochemical quantities for supplied quantum outputs at each explicitly listed temperature without rerunning electronic-structure calculations. |
| analyze_thermochemical_ensemble | molecular_electronic | ThermochemicalEnsembleResult | agent_backend_required | goodvibes | output_files | Calculate per-structure thermochemistry and Boltzmann populations for an explicitly supplied conformer or structure ensemble. |
| validate_thermochemistry_inputs | molecular_electronic | ThermochemistryValidationReport | agent_backend_required | goodvibes | output_files | Check supplied quantum outputs for thermochemistry compatibility, calculation consistency, frequency issues, and possible duplicate structures. |
| locate_transition_state | reaction_and_kinetics | AtomicStructure | agent_backend_required | pysisyphus, sella | initial_guess | Locate one candidate transition-state structure without automatically running frequencies or IRC. |
| search_reaction_path | reaction_and_kinetics | ReactionPath | agent_backend_required | pysisyphus | reactant, product | Run an explicitly selected double-ended chain-of-states search between supplied reactant and product structures without asserting that the highest image is a validated transition state. |
| scan_reaction_coordinates | reaction_and_kinetics | ReactionCoordinateScan | agent_backend_required | pysisyphus | structure | Run one relaxed one-dimensional internal-coordinate scan from a supplied structure using explicit coordinate, range, optimizer, and calculator settings. |
| validate_reaction_path | reaction_and_kinetics | ReactionPathValidationResult | internal_deterministic | internal_reaction_analysis | path, reactant, product | Check atom/state consistency, endpoint agreement, image continuity, and optional bond-change progress for an already calculated reaction path. |
| analyze_reaction_coordinate | reaction_and_kinetics | ReactionCoordinateAnalysisResult | internal_deterministic | internal_reaction_analysis | path, energies | Convert supplied path images and aligned electronic energies into a normalized reaction-coordinate profile with relative energies and highest-image candidates. |
| trace_intrinsic_reaction_coordinate | reaction_and_kinetics | ReactionPath | agent_backend_required | pysisyphus | transition_state | Trace an IRC from an already supplied transition-state structure. |
| analyze_thermochemical_selectivity | reaction_and_kinetics | ThermochemicalSelectivityResult | agent_backend_required | goodvibes | output_files, label_groups | Calculate N-way thermodynamic selectivity from explicitly labeled structure ensembles, including two-label excess and delta-delta-G when applicable. |
| analyze_reaction_free_energy_profile | reaction_and_kinetics | ReactionFreeEnergyProfileResult | agent_backend_required | goodvibes | output_files, profile_definition_file | Calculate relative electronic and thermochemical energies along explicitly defined reaction pathways, including stoichiometric sums and conformer ensembles. |

## Registered scientific resources

| Resource | Kind | Backends | Version | Format | Status | Explicit selection syntax | Coverage |
|---|---|---|---|---|---|---|---|

## Backend installation and health

| Backend | Runtime | Status | Conda packages | Pip packages | Executables | External scientific data | License |
|---|---|---|---|---|---|---|---|
| qcelemental | workflows | not_probed | qcelemental=0.50.4 |  |  |  | open_source |
| cclib | workflows | not_probed | cclib=1.8.1 |  |  |  | open_source |
| rdkit | core | not_probed | rdkit |  |  |  | open_source |
| openbabel | quantum | not_probed | openbabel |  | obabel |  | open_source |
| rdkit_etkdg | core | not_probed | rdkit |  |  |  | open_source |
| crest | reaction | not_probed | crest, xtb |  | crest |  | open_source |
| internal_statistics | core | not_probed |  |  |  |  | open_source |
| internal_reaction_analysis | core | not_probed |  |  |  |  | open_source |
| rdkit_gasteiger | core | not_probed | rdkit |  |  |  | open_source |
| xtb | quantum | not_probed | xtb |  | xtb |  | open_source |
| multiwfn | multiwfn | not_probed |  |  | Multiwfn_noGUI | Agent-supplied fch/fchk/wfn/wfx/mwfn/Molden/47 wavefunction file; both required Multiwfn citations are returned in provenance | custom_open_source_citation_required |
| gaussian | gaussian | not_probed |  |  | g16, formchk |  | commercial_license |
| internal_vibrations | core | not_probed |  | ase, numpy |  |  | open_source |
| internal_spectroscopy | core | not_probed |  | numpy |  |  | open_source |
| internal_thermochemistry | core | not_probed |  | ase, numpy |  |  | open_source |
| goodvibes | goodvibes | not_probed |  | goodvibes[full]==4.3.0 | goodvibes |  | open_source |
| sella | sella | not_probed |  | sella==2.5.0 |  |  | open_source |
| pysisyphus | reaction | not_probed |  | pysisyphus==1.0.0 | pysis |  | open_source |
