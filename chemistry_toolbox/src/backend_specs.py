"""Static BackendSpec declarations for all executable providers."""

from __future__ import annotations

from .models import BackendSpec
from .parameter_specs import (
    fixed_parameter_specs_for_backend,
    parameter_specs_for_backend,
)


def _backend(
    backend_id: str,
    display_name: str,
    runtime: str,
    capabilities: tuple[str, ...],
    description: str,
    *,
    modules: tuple[str, ...] = (),
    executables: tuple[str, ...] = (),
    environment: tuple[str, ...] = (),
    conda: tuple[str, ...] = (),
    pip: tuple[str, ...] = (),
    data_resources: tuple[str, ...] = (),
    license_class: str = "open_source",
    install_notes: str = "",
    resource_constraints: dict[str, object] | None = None,
    method_schema: dict[str, str] | None = None,
    required_inputs: dict[str, tuple[str, ...]] | None = None,
    required_methods: dict[str, tuple[str, ...]] | None = None,
    required_settings: dict[str, tuple[str, ...]] | None = None,
    allowed_methods: dict[str, dict[str, tuple[str, ...]]] | None = None,
    allowed_settings: dict[str, dict[str, tuple[str, ...]]] | None = None,
    required_components: dict[str, tuple[str, ...]] | None = None,
    component_options: dict[str, dict[str, tuple[str, ...]]] | None = None,
    supported_system_types: dict[str, tuple[str, ...]] | None = None,
    validation_levels: dict[str, str] | None = None,
) -> BackendSpec:
    return BackendSpec(
        id=backend_id,
        display_name=display_name,
        runtime=runtime,
        capabilities=capabilities,
        description=description,
        python_modules=modules,
        executables=executables,
        environment_variables=environment,
        conda_packages=conda,
        pip_packages=pip,
        required_data_resources=data_resources,
        license_class=license_class,
        install_notes=install_notes,
        resource_constraints=resource_constraints or {},
        method_schema=method_schema or {},
        required_input_fields=required_inputs or {},
        required_method_fields=required_methods or {},
        required_setting_fields=required_settings or {},
        allowed_method_values=allowed_methods or {},
        allowed_setting_values=allowed_settings or {},
        required_component_roles=required_components or {},
        component_backend_options=component_options or {},
        supported_system_types=supported_system_types or {},
        validation_levels=validation_levels or {},
        parameter_specs=parameter_specs_for_backend(backend_id),
        fixed_parameter_specs=fixed_parameter_specs_for_backend(backend_id),
    )


_PERIODIC_RELAX = {
    "relax_periodic_structure": (
        "force_threshold_ev_per_angstrom",
        "max_steps",
        "relax_cell",
    )
}


_DFTB_SETTINGS = {
    "calculate_periodic_energy": ("scc_tolerance", "max_scc_iterations"),
    "calculate_periodic_forces": ("scc_tolerance", "max_scc_iterations"),
    "relax_periodic_structure": (
        "scc_tolerance",
        "max_scc_iterations",
        "force_threshold_ev_per_angstrom",
        "max_steps",
        "relax_cell",
    ),
}


_MLIP_PERIODIC_RELAX = {
    "relax_periodic_structure": (
        "force_threshold_ev_per_angstrom",
        "max_steps",
        "relax_cell",
        "optimizer",
    )
}


_ASE_OPTIMIZER_CHOICES = ("bfgs", "lbfgs", "fire")


_VASP_SETTINGS = {
    "calculate_periodic_energy": ("scf_convergence_ev", "max_scf_cycles"),
    "calculate_periodic_forces": ("scf_convergence_ev", "max_scf_cycles"),
    "calculate_periodic_stress": ("scf_convergence_ev", "max_scf_cycles"),
    "relax_periodic_structure": (
        "scf_convergence_ev",
        "max_scf_cycles",
        "force_threshold_ev_per_angstrom",
        "max_steps",
        "relax_cell",
    ),
}


BACKEND_SPECS: tuple[BackendSpec, ...] = (
    _backend(
        "qcelemental", "QCElemental", "workflows",
        ("normalize_qcschema_molecule", "validate_qcschema_record"),
        "QCElemental 0.50.4 schema models and physical-data normalization without calculation execution.",
        modules=("qcelemental",), conda=("qcelemental=0.50.4",),
        required_settings={
            "normalize_qcschema_molecule": ("fix_center_of_mass", "fix_orientation"),
            "validate_qcschema_record": ("record_type",),
        },
    ),
    _backend(
        "cclib", "cclib", "workflows",
        ("parse_quantum_chemistry_output",),
        "cclib 1.8.1 parser for extracting selected properties from existing quantum-chemistry output files.",
        modules=("cclib",), conda=("cclib=1.8.1",),
        method_schema={
            "properties": (
                "action_settings.properties must be a non-empty list chosen from metadata, "
                "atom_coordinates, energies, gradients, hessian, vibrational_frequencies, "
                "vibrational_intensities, molecular_orbitals, charges, multipoles, and "
                "excited_states"
            ),
            "coordinate_frames": "action_settings.coordinate_frames is last or all",
            "include_orbital_coefficients": (
                "explicit action_settings boolean controlling large MO coefficient arrays"
            ),
            "include_excited_state_configurations": (
                "explicit action_settings boolean controlling excited-state configuration arrays"
            ),
            "max_array_elements": (
                "explicit action_settings integer limit between 1 and 100000000"
            ),
        },
        required_settings={
            "parse_quantum_chemistry_output": (
                "properties", "coordinate_frames", "include_orbital_coefficients",
                "include_excited_state_configurations", "max_array_elements",
            ),
        },
    ),
    _backend(
        "rdkit", "RDKit", "core",
        (
            "standardize_structure", "generate_3d_structure", "assign_protonation_states",
            "cluster_conformers", "align_molecular_structures",
            "calculate_molecular_descriptors", "calculate_molecular_fingerprint",
            "calculate_molecular_similarity", "search_local_substructures",
            "enumerate_tautomers", "enumerate_stereoisomers",
        ),
        "Cheminformatics structure standardization, hydrogen handling, and 3D embedding.",
        modules=("rdkit",), conda=("rdkit",),
        required_settings={
            "standardize_structure": ("largest_fragment", "neutralize", "canonical_tautomer"),
            "generate_3d_structure": ("random_seed",),
            "cluster_conformers": (
                "rmsd_cutoff_angstrom", "atom_selection", "prealign_conformers",
                "reorder_cluster_centers",
            ),
            "align_molecular_structures": ("reflect", "max_iterations"),
            "assign_protonation_states": ("ph", "rule"),
            "enumerate_tautomers": ("max_tautomers",),
            "enumerate_stereoisomers": ("max_isomers", "only_unassigned", "unique"),
        },
        required_methods={
            "calculate_molecular_fingerprint": ("fingerprint_type",),
            "calculate_molecular_similarity": ("fingerprint_type", "similarity_metric"),
            "search_local_substructures": ("query_format",),
        },
    ),
    _backend(
        "sisso", "SISSO", "sisso",
        (
            "discover_sparse_symbolic_descriptor",
            "evaluate_sparse_symbolic_descriptor",
            "summarize_sparse_symbolic_descriptor_results",
        ),
        "SISSO 3.5 sparse symbolic regression with explicit data splits and official out-of-sample prediction.",
        executables=("SISSO", "SISSO_predict"),
        environment=("CHEMGRAPH_SISSO_COMMAND", "CHEMGRAPH_SISSO_PREDICT_COMMAND"),
        conda=("bc=1.07.1",),
        install_notes="SISSO 3.5 is compiled with the official Intel Fortran Classic 2021.2 and Intel MPI 2021.15 toolchain cached under .software_cache.",
        required_methods={
            "discover_sparse_symbolic_descriptor": (
                "sample_id_column", "target_column", "feature_columns",
                "training_sample_ids", "validation_sample_ids", "feature_unit_groups",
                "operators", "descriptor_dimension", "feature_complexity",
                "sis_subspace_size", "sparsification_method", "fit_intercept",
                "selection_metric",
            ),
            "evaluate_sparse_symbolic_descriptor": (
                "sample_id_column", "target_column", "feature_columns", "descriptor_dimension",
            ),
        },
        required_settings={
            "discover_sparse_symbolic_descriptor": (
                "feature_storage_mode", "feature_minimum_absolute_max",
                "feature_maximum_absolute_max", "number_of_models", "mpi_processes",
                "maximum_prediction_records",
            ),
            "evaluate_sparse_symbolic_descriptor": ("maximum_prediction_records",),
            "summarize_sparse_symbolic_descriptor_results": ("maximum_prediction_records",),
        },
        supported_system_types={
            "discover_sparse_symbolic_descriptor": ("tabular_regression_dataset",),
            "evaluate_sparse_symbolic_descriptor": ("sisso_regression_model",),
            "summarize_sparse_symbolic_descriptor_results": ("sisso_output",),
        },
        validation_levels={
            "discover_sparse_symbolic_descriptor": "real_smoke",
            "evaluate_sparse_symbolic_descriptor": "real_smoke",
            "summarize_sparse_symbolic_descriptor_results": "real_smoke",
        },
    ),
    _backend(
        "gplearn", "gplearn", "gplearn",
        (
            "fit_symbolic_regression_baseline",
            "assess_symbolic_regression_seed_stability",
            "summarize_symbolic_regression_results",
        ),
        "gplearn 0.4.3 genetic-programming symbolic regression with explicit held-out splits and seed stability analysis.",
        modules=("gplearn", "sklearn", "numpy"),
        pip=("gplearn==0.4.3",),
        install_notes="BSD-3-Clause gplearn 0.4.3 is installed from its pinned PyPI wheel; upstream tests are cached with the source checkout.",
        required_methods={
            "fit_symbolic_regression_baseline": (
                "sample_id_column", "target_column", "feature_columns",
                "training_sample_ids", "validation_sample_ids", "function_set", "metric",
            ),
            "assess_symbolic_regression_seed_stability": (
                "sample_id_column", "target_column", "feature_columns",
                "training_sample_ids", "validation_sample_ids", "function_set", "metric",
            ),
        },
        required_settings={
            "fit_symbolic_regression_baseline": (
                "population_size", "generations", "tournament_size", "stopping_criteria",
                "const_range", "init_depth", "init_method", "parsimony_coefficient",
                "p_crossover", "p_subtree_mutation", "p_hoist_mutation", "p_point_mutation",
                "p_point_replace", "max_samples", "low_memory", "n_jobs", "random_seed",
                "maximum_prediction_records",
            ),
            "assess_symbolic_regression_seed_stability": (
                "population_size", "generations", "tournament_size", "stopping_criteria",
                "const_range", "init_depth", "init_method", "parsimony_coefficient",
                "p_crossover", "p_subtree_mutation", "p_hoist_mutation", "p_point_mutation",
                "p_point_replace", "max_samples", "low_memory", "n_jobs", "random_seeds",
                "maximum_prediction_records",
            ),
            "summarize_symbolic_regression_results": ("maximum_prediction_records",),
        },
        supported_system_types={
            "fit_symbolic_regression_baseline": ("tabular_regression_dataset",),
            "assess_symbolic_regression_seed_stability": ("tabular_regression_dataset",),
            "summarize_symbolic_regression_results": ("gplearn_action_json",),
        },
        validation_levels={
            "fit_symbolic_regression_baseline": "real_smoke",
            "assess_symbolic_regression_seed_stability": "real_smoke",
            "summarize_symbolic_regression_results": "real_smoke",
        },
    ),
    _backend(
        "openbabel", "Open Babel", "quantum", ("generate_3d_structure",),
        "Open Babel 3D coordinate generation.", modules=("openbabel",), executables=("obabel",),
        conda=("openbabel",),
        required_methods={"generate_3d_structure": ("force_field",)},
    ),
    _backend(
        "acpype", "ACPYPE", "acpype",
        ("generate_small_molecule_topology", "convert_amber_topology_to_gromacs"),
        "ACPYPE 2023.10.27 GAFF-family small-molecule topology generation and explicit AMBER-to-GROMACS conversion.",
        modules=("acpype", "openbabel"), executables=("acpype",),
        environment=("CHEMGRAPH_ACPYPE_COMMAND",),
        conda=("openbabel=3.1.1", "ambertools=26.0"), pip=("acpype==2023.10.27",),
        required_methods={
            "generate_small_molecule_topology": (
                "atom_type", "charge_method", "net_charge", "multiplicity", "charge_program",
            ),
        },
        required_settings={
            "generate_small_molecule_topology": (
                "output_topologies", "maximum_charge_time_seconds",
                "merge_atom_types", "sort_atoms",
            ),
            "convert_amber_topology_to_gromacs": ("direct_conversion", "sort_atoms"),
        },
        allowed_methods={
            "generate_small_molecule_topology": {
                "atom_type": ("gaff", "gaff2", "amber", "amber2"),
                "charge_method": ("gas", "bcc", "user"),
                "charge_program": ("sqm", "mopac", "divcon"),
            },
        },
        allowed_settings={
            "generate_small_molecule_topology": {
                "output_topologies": ("all", "gmx", "cns", "charmm"),
            },
        },
        supported_system_types={
            "generate_small_molecule_topology": ("small_molecule",),
            "convert_amber_topology_to_gromacs": ("small_molecule", "biomolecule", "molecular_system"),
        },
        validation_levels={
            "generate_small_molecule_topology": "real_smoke",
            "convert_amber_topology_to_gromacs": "real_smoke",
        },
    ),
    _backend(
        "pmx", "pmx", "pmx",
        (
            "mutate_biomolecular_residues_for_alchemy",
            "generate_alchemical_hybrid_topology",
            "map_alchemical_ligand_atoms",
        ),
        "Fixed pmx develop commit for explicit biomolecular mutations, B-state hybrid topology generation, and ligand atom mapping.",
        modules=("pmx", "rdkit"), executables=("pmx",),
        environment=("CHEMGRAPH_PMX_COMMAND", "GMXLIB"),
        pip=("pmx @ git+https://github.com/deGrootLab/pmx@0dd5f0a9cdf26109eff98bdfeb4ac4e55353aa76",),
        install_notes="The upstream Python 3 branch is documented as development software; this runtime is pinned to commit 0dd5f0a and must not float to branch HEAD.",
        required_methods={
            "mutate_biomolecular_residues_for_alchemy": ("force_field",),
            "generate_alchemical_hybrid_topology": ("force_field",),
        },
        required_settings={
            "mutate_biomolecular_residues_for_alchemy": ("keep_residue_ids",),
            "generate_alchemical_hybrid_topology": (
                "recursive", "split_transformations", "dummy_mass_scale", "dummy_dihedral_scale",
            ),
            "map_alchemical_ligand_atoms": (
                "use_alignment", "use_mcs", "map_nonpolar_hydrogens",
                "map_polar_hydrogens", "allow_hydrogen_to_heavy",
                "rings_only", "apply_distance_to_mcs", "cross_check_swapped_order",
                "check_chirality", "distance_cutoff_nm", "mcs_timeout_seconds",
            ),
        },
        allowed_methods={
            "mutate_biomolecular_residues_for_alchemy": {
                "force_field": (
                    "amber99sb-star-ildn-mut", "amber99sb-star-ildn-dna-mut",
                    "amber99sb-star-ildn-bsc1-mut", "amber14sbmut", "charmm36m-mut",
                    "charmm22star-mut",
                ),
            },
            "generate_alchemical_hybrid_topology": {
                "force_field": (
                    "amber99sb-star-ildn-mut", "amber99sb-star-ildn-dna-mut",
                    "amber99sb-star-ildn-bsc1-mut", "amber14sbmut", "charmm36m-mut",
                    "charmm22star-mut",
                ),
            },
        },
        supported_system_types={
            "mutate_biomolecular_residues_for_alchemy": ("protein", "dna", "rna"),
            "generate_alchemical_hybrid_topology": ("biomolecule", "molecular_system"),
            "map_alchemical_ligand_atoms": ("small_molecule_pair",),
        },
        validation_levels={
            "mutate_biomolecular_residues_for_alchemy": "real_smoke",
            "generate_alchemical_hybrid_topology": "real_smoke",
            "map_alchemical_ligand_atoms": "real_smoke",
        },
    ),
    _backend(
        "rdkit_etkdg", "RDKit ETKDG", "core", ("generate_conformer_ensemble",),
        "RDKit ETKDG conformer generation with agent-selected sampling settings.",
        modules=("rdkit",), conda=("rdkit",),
        required_settings={"generate_conformer_ensemble": ("num_conformers", "random_seed")},
    ),
    _backend(
        "crest", "CREST", "reaction", ("generate_conformer_ensemble",),
        "CREST conformer search from an explicit starting geometry.", executables=("crest",),
        environment=("CHEMGRAPH_CREST_COMMAND",), conda=("crest", "xtb"),
        resource_constraints={
            "maximum_cpu_cores": 48,
            "reason": "CREST/xTB threads are set from the Agent-selected resource limits and capped on this server.",
        },
        method_schema={
            "method": "GFN1-xTB, GFN2-xTB, or GFN-FF; compact gfn1/gfn2/gfnff spellings are equivalent",
            "charge": "optional explicit integer molecular charge; otherwise taken from the starting structure",
            "multiplicity": "optional explicit positive spin multiplicity; otherwise taken from the starting structure",
            "solvation_model": "optional alpb or gbsa",
            "solvent": "required solvent name when solvation_model is supplied",
        },
        required_methods={"generate_conformer_ensemble": ("method",)},
    ),
    _backend(
        "internal_statistics", "ResearchChem deterministic statistics", "core",
        ("rank_conformers_from_results",),
        "Deterministic sorting, degeneracy handling, and Boltzmann weighting of supplied scores.",
        required_settings={"rank_conformers_from_results": ("temperature_kelvin", "score_unit")},
    ),
    _backend(
        "internal_reaction_analysis", "ResearchChem reaction/coordination analysis", "core",
        (
            "enumerate_coordination_isomers", "validate_reaction_path",
            "analyze_reaction_coordinate", "analyze_post_transition_state_trajectory_ensemble",
        ),
        (
            "Deterministic coordination-site enumeration and reaction-path analysis from "
            "explicitly supplied structures, paths, bond changes, and energies. It does not "
            "run electronic-structure calculations or infer a mechanism."
        ),
        required_settings={
            "enumerate_coordination_isomers": ("coordination_geometry", "max_isomers"),
            "validate_reaction_path": (
                "endpoint_rmsd_tolerance_angstrom",
                "maximum_image_step_rmsd_angstrom",
                "bond_distance_tolerance_angstrom",
            ),
            "analyze_reaction_coordinate": ("energy_unit",),
            "analyze_post_transition_state_trajectory_ensemble": (
                "confidence_level", "failure_policy", "minimum_successful_trajectories",
            ),
        },
        allowed_settings={
            "enumerate_coordination_isomers": {
                "coordination_geometry": (
                    "trigonal_bipyramidal", "square_pyramidal", "octahedral"
                ),
            },
            "analyze_reaction_coordinate": {
                "energy_unit": ("hartree", "kj/mol", "kcal/mol", "ev")
            },
            "analyze_post_transition_state_trajectory_ensemble": {
                "failure_policy": ("exclude", "include_as_unassigned"),
            },
        },
    ),
    _backend(
        "internal_periodic_analysis", "ResearchChem periodic evidence analysis", "core",
        (
            "calculate_adsorption_energy", "construct_pressure_enthalpy_phase_diagram",
            "assess_phonon_stability",
        ),
        (
            "Deterministic adsorption-energy bookkeeping, pressure-enthalpy phase selection, "
            "and phonon-stability assessment from explicitly supplied calculation results."
        ),
        required_settings={
            "calculate_adsorption_energy": ("energy_unit", "adsorbate_count"),
            "construct_pressure_enthalpy_phase_diagram": (
                "enthalpy_unit", "energy_tolerance_ev_per_formula_unit",
                "maximum_reported_transitions",
            ),
            "assess_phonon_stability": (
                "frequency_unit", "imaginary_tolerance", "gamma_q_tolerance",
                "acoustic_gamma_tolerance", "maximum_returned_imaginary_modes",
            ),
        },
        allowed_settings={
            "calculate_adsorption_energy": {
                "energy_unit": ("hartree", "ev", "kj/mol", "kcal/mol"),
            },
            "construct_pressure_enthalpy_phase_diagram": {
                "enthalpy_unit": ("ev_per_formula_unit", "hartree_per_formula_unit", "kj/mol"),
            },
            "assess_phonon_stability": {
                "frequency_unit": ("thz", "cm-1", "mev"),
            },
        },
    ),
    _backend(
        "internal_trajectory_analysis", "ResearchChem trajectory-ensemble analysis", "core",
        ("analyze_nonadiabatic_trajectory_ensemble",),
        (
            "Deterministic state-population, hopping, survival, and uncertainty analysis from "
            "explicit normalized nonadiabatic trajectory records."
        ),
        required_settings={
            "analyze_nonadiabatic_trajectory_ensemble": (
                "state_count", "initial_state_index", "time_grid_fs",
                "confidence_level", "failure_policy",
            ),
        },
        allowed_settings={
            "analyze_nonadiabatic_trajectory_ensemble": {
                "failure_policy": ("exclude", "include_until_failure"),
            },
        },
    ),
    _backend(
        "pdbfixer", "PDBFixer", "md",
        ("repair_biomolecular_structure", "assign_protonation_states"),
        "Biomolecular structure repair and explicit pH-based hydrogen addition.",
        modules=("pdbfixer", "openmm"), conda=("pdbfixer", "openmm"),
        required_settings={
            "repair_biomolecular_structure": ("add_missing_residues", "replace_nonstandard_residues", "keep_water"),
            "assign_protonation_states": ("ph",),
        },
    ),
    _backend(
        "pdb_tools", "pdb-tools", "core",
        (
            "select_structure_subset", "renumber_biomolecular_structure",
            "normalize_pdb_records",
        ),
        "Composable pdb-tools 2.7.0 record transformations exposed as bounded typed structure actions.",
        modules=("pdbtools",), executables=("pdb_selchain", "pdb_reres", "pdb_tidy"),
        pip=("pdb-tools==2.7.0",),
        required_settings={
            "select_structure_subset": ("chains", "models", "keep_heteroatoms"),
            "renumber_biomolecular_structure": (
                "starting_atom_serial", "starting_residue_number", "hybrid36",
            ),
            "normalize_pdb_records": ("sort_by", "strict_chain_breaks", "hybrid36"),
        },
    ),
    _backend(
        "rdkit_gasteiger", "RDKit Gasteiger charges", "core", ("assign_partial_charges",),
        "Gasteiger partial-charge assignment on a fixed molecular graph.", modules=("rdkit",),
        conda=("rdkit",), required_methods={"assign_partial_charges": ("charge_model",)},
    ),
    _backend(
        "openff_am1bcc", "OpenFF AM1-BCC", "openff", ("assign_partial_charges",),
        "OpenFF AM1-BCC partial-charge assignment through the AmberTools toolkit wrapper.",
        modules=("openff.toolkit",), executables=("antechamber", "sqm"),
        conda=("openff-toolkit", "ambertools"),
        required_methods={"assign_partial_charges": ("charge_model",)},
    ),
    _backend(
        "openff", "OpenFF Toolkit/Interchange", "openff", ("assign_force_field_parameters",),
        "OpenFF force-field parameter assignment and interchange serialization.",
        modules=("openff.toolkit", "openff.interchange"),
        conda=("openff-toolkit", "openff-interchange"),
        required_methods={"assign_force_field_parameters": ("force_field",)},
    ),
    _backend(
        "openmm_builder", "OpenMM system builder", "md",
        ("assign_force_field_parameters", "solvate_molecular_system"),
        "OpenMM force-field assignment and explicit solvent/ion construction.",
        modules=("openmm",), conda=("openmm",),
        required_methods={"assign_force_field_parameters": ("force_field",)},
        required_settings={
            "solvate_molecular_system": ("box_shape", "padding_angstrom", "solvent_model"),
        },
    ),
    _backend(
        "packmol", "Packmol", "md", ("solvate_molecular_system",),
        "Packmol construction of an explicitly specified molecular environment.",
        executables=("packmol",), conda=("packmol",),
        required_settings={
            "solvate_molecular_system": (
                "box_shape",
                "box_size_angstrom",
                "solvent_model",
                "solvent_path",
                "molecule_counts",
            ),
        },
    ),
    _backend(
        "spglib", "spglib", "workflows",
        ("analyze_crystal_symmetry", "standardize_crystal_structure"),
        "Crystallographic symmetry detection and cell standardization using explicit numerical tolerances.",
        modules=("spglib", "numpy"), conda=("spglib", "numpy"),
        required_settings={
            "analyze_crystal_symmetry": ("symmetry_tolerance_angstrom", "angle_tolerance_degrees"),
            "standardize_crystal_structure": (
                "convention", "symmetry_tolerance_angstrom",
                "angle_tolerance_degrees", "idealize",
            ),
        },
    ),
    _backend(
        "pymatgen", "pymatgen", "workflows",
        (
            "analyze_crystal_symmetry", "standardize_crystal_structure",
            "build_supercell", "enumerate_surface_slabs",
        ),
        "Materials structure, symmetry, supercell, and surface-slab operations with all structural choices supplied by the Agent.",
        modules=("pymatgen", "numpy"), conda=("pymatgen", "numpy"),
        required_settings={
            "analyze_crystal_symmetry": ("symmetry_tolerance_angstrom", "angle_tolerance_degrees"),
            "standardize_crystal_structure": (
                "convention", "symmetry_tolerance_angstrom", "angle_tolerance_degrees",
            ),
            "build_supercell": ("scaling_matrix",),
            "enumerate_surface_slabs": (
                "miller_index", "minimum_slab_thickness_angstrom",
                "minimum_vacuum_thickness_angstrom", "center_slab",
                "primitive", "max_terminations",
            ),
        },
    ),
    _backend(
        "vaspkit", "VASPKIT", "vaspkit",
        ("analyze_crystal_symmetry", "generate_vasp_kpoint_mesh", "extract_vasp_band_gap"),
        "VASPKIT 1.5.1 noncommercial binary for explicit VASP structure, reciprocal-mesh, and electronic-result post-processing.",
        executables=("vaspkit",),
        environment=("CHEMGRAPH_VASPKIT_COMMAND", "CHEMGRAPH_VASPKIT_CONFIG"),
        license_class="noncommercial_no_redistribution",
        install_notes="Download the official 1.5.1 Linux binary separately. Its license prohibits redistribution without written permission.",
        required_settings={
            "analyze_crystal_symmetry": ("symmetry_tolerance_angstrom", "angle_tolerance_degrees"),
            "generate_vasp_kpoint_mesh": ("reciprocal_space_resolution_inverse_angstrom", "centering_scheme"),
            "extract_vasp_band_gap": ("set_fermi_energy_zero",),
        },
        supported_system_types={
            "analyze_crystal_symmetry": ("periodic_atomic_structure",),
            "generate_vasp_kpoint_mesh": ("vasp_structure_file",),
            "extract_vasp_band_gap": ("vasp_electronic_output_set",),
        },
        validation_levels={
            "analyze_crystal_symmetry": "real_smoke",
            "generate_vasp_kpoint_mesh": "real_smoke",
            "extract_vasp_band_gap": "real_smoke",
        },
    ),
    _backend(
        "xtb", "xTB", "quantum",
        (
            "calculate_energy", "calculate_forces", "calculate_hessian",
            "optimize_geometry", "calculate_dipole_moment", "calculate_atomic_charges",
            "calculate_bond_orders",
        ),
        "Standalone xTB GFN energy, derivative, optimization, dipole, and population-analysis calculations.", executables=("xtb",),
        environment=("CHEMGRAPH_XTB_COMMAND",), conda=("xtb",),
        method_schema={
            "method": "gfn1, gfn1-xtb, gfn2, or gfn2-xtb",
            "charge": "optional explicit integer molecular charge",
            "unpaired_electrons": "optional explicit nonnegative integer number of unpaired electrons",
            "optimization_level": "crude, sloppy, loose, normal, tight, verytight, or extreme",
        },
        required_methods={
            action: ("method",) for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "optimize_geometry", "calculate_dipole_moment", "calculate_atomic_charges",
                "calculate_bond_orders",
            )
        }, required_settings={
            "optimize_geometry": ("optimization_level",),
            "calculate_bond_orders": ("minimum_bond_order",),
        },
        allowed_methods={
            action: {"method": ("gfn1", "gfn1-xtb", "gfn2", "gfn2-xtb")}
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "optimize_geometry", "calculate_dipole_moment", "calculate_atomic_charges",
                "calculate_bond_orders",
            )
        },
        allowed_settings={
            "optimize_geometry": {
                "optimization_level": (
                    "crude", "sloppy", "loose", "normal", "tight", "verytight", "extreme",
                )
            }
        },
    ),
    _backend(
        "pyscf", "PySCF", "quantum",
        (
            "calculate_energy", "calculate_forces", "calculate_hessian",
            "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals",
            "calculate_excited_states",
        ),
        "PySCF molecular Hartree-Fock and density-functional energies, analytic derivatives, and electronic properties.", modules=("pyscf",),
        pip=("pyscf",), method_schema={"method": "rhf|uhf|rks|uks", "basis": "PySCF basis name"},
        required_methods={
            action: ("method", "basis") for action in
            (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals",
            )
        } | {"calculate_excited_states": ("method", "basis", "excited_state_method")},
        required_settings={
            "calculate_excited_states": ("number_of_states", "spin_symmetry"),
        },
    ),
    _backend(
        "gpaw", "GPAW", "gpaw",
        (
            "calculate_energy", "calculate_forces", "optimize_geometry",
            "calculate_periodic_energy", "calculate_periodic_forces",
            "calculate_periodic_stress", "relax_periodic_structure",
            "calculate_electronic_band_structure", "calculate_density_of_states",
            "calculate_projected_density_of_states",
        ),
        "GPAW real-space, LCAO, or plane-wave DFT with explicit representation, PAW setup, k-point, spin, and convergence choices.",
        modules=("gpaw", "ase", "numpy"), executables=("gpaw",),
        conda=("gpaw=25.7.0", "ase", "numpy"),
        data_resources=("GPAW PAW setup datasets under .software_cache/shared/scientific-data/gpaw-setups",),
        method_schema={
            "mode": "fd or lcao for molecules; pw, fd, or lcao for periodic structures",
            "xc": "explicit GPAW exchange-correlation functional",
            "ecut_ev": "required for pw mode",
            "grid_spacing_angstrom": "required for fd mode",
            "basis": "required for lcao mode",
            "k_points": "required periodic three-integer grid or {grid,gamma}",
            "spin_polarized": "explicit boolean; true requires initial_magnetic_moments",
        },
        required_inputs={
            "calculate_projected_density_of_states": ("ground_state",),
        },
        required_methods={
            action: ("mode", "xc", "spin_polarized")
            for action in ("calculate_energy", "calculate_forces", "optimize_geometry")
        } | {
            action: ("mode", "xc", "spin_polarized", "k_points")
            for action in (
                "calculate_periodic_energy", "calculate_periodic_forces",
                "calculate_periodic_stress", "relax_periodic_structure",
            )
        },
        required_settings={
            "calculate_energy": ("vacuum_angstrom", "scf_energy_convergence_ev", "max_scf_cycles"),
            "calculate_forces": ("vacuum_angstrom", "scf_energy_convergence_ev", "max_scf_cycles"),
            "optimize_geometry": (
                "vacuum_angstrom", "scf_energy_convergence_ev", "max_scf_cycles",
                "force_threshold_ev_per_angstrom", "max_steps", "optimizer",
            ),
            "calculate_periodic_energy": ("scf_energy_convergence_ev", "max_scf_cycles"),
            "calculate_periodic_forces": ("scf_energy_convergence_ev", "max_scf_cycles"),
            "calculate_periodic_stress": ("scf_energy_convergence_ev", "max_scf_cycles"),
            "relax_periodic_structure": (
                "scf_energy_convergence_ev", "max_scf_cycles",
                "force_threshold_ev_per_angstrom", "max_steps", "optimizer", "relax_cell",
            ),
            "calculate_electronic_band_structure": (
                "band_path", "number_of_points", "number_of_bands",
                "converged_bands", "energy_reference",
            ),
            "calculate_density_of_states": (
                "minimum_energy_ev", "maximum_energy_ev", "grid_points",
                "broadening_ev", "spin", "energy_reference",
            ),
            "calculate_projected_density_of_states": (
                "minimum_energy_ev", "maximum_energy_ev", "grid_points",
                "broadening_ev", "spin", "energy_reference",
            ),
        },
    ),
    _backend(
        "lobster", "LOBSTER", "lobster",
        (
            "analyze_periodic_bonding", "calculate_projected_density_of_states",
            "calculate_charge_spilling",
        ),
        "LOBSTER 5.1.0 periodic bonding, projected-DOS, and projection-quality postprocessing from explicit existing output Artifacts.",
        modules=("pymatgen", "numpy"), executables=("lobster-5.1.0",),
        environment=("CHEMGRAPH_LOBSTER_COMMAND",), conda=("pymatgen",),
        license_class="academic_license",
        install_notes=(
            "Operator-supplied LOBSTER 5.1.0 is cached locally with its User Guide and FAQ. "
            "These public actions parse bounded existing outputs and do not expose arbitrary lobsterin execution."
        ),
        required_inputs={
            "analyze_periodic_bonding": ("integrated_bond_list",),
            "calculate_projected_density_of_states": ("dos_file", "structure_file"),
            "calculate_charge_spilling": ("lobster_output",),
        },
        required_settings={
            "analyze_periodic_bonding": (
                "bonding_metric", "spin", "minimum_absolute_integrated_value_ev",
                "max_bonds", "include_curve_data", "minimum_energy_ev",
                "maximum_energy_ev", "curve_stride", "max_curve_points",
            ),
            "calculate_projected_density_of_states": (
                "minimum_energy_ev", "maximum_energy_ev", "spin", "curve_stride",
            ),
            "calculate_charge_spilling": (
                "maximum_charge_spilling_percent",
                "maximum_total_spilling_percent", "require_finished",
            ),
        },
        supported_system_types={
            action: ("periodic_crystal",)
            for action in (
                "analyze_periodic_bonding", "calculate_projected_density_of_states",
                "calculate_charge_spilling",
            )
        },
        validation_levels={
            action: "validated"
            for action in (
                "analyze_periodic_bonding", "calculate_projected_density_of_states",
                "calculate_charge_spilling",
            )
        },
    ),
    _backend(
        "nwchem", "NWChem", "nwchem",
        (
            "calculate_energy", "calculate_forces", "calculate_hessian",
            "calculate_dipole_moment", "calculate_atomic_charges",
        ),
        "NWChem single-geometry QCSchema calculations through QCEngine with explicit method, basis, convergence, and population/property requests.",
        modules=("qcengine", "qcelemental", "numpy"), executables=("nwchem",),
        environment=("NWCHEM_BASIS_LIBRARY",),
        conda=("nwchem=7.3.1", "qcengine=0.50.0", "qcelemental=0.50.4", "cclib"),
        data_resources=("NWChem basis libraries under .software_cache/sources/nwchem/source/src/basis/libraries",),
        method_schema={
            "method": "NWChem/QCEngine method such as hf, dft, mp2, or ccsd",
            "basis": "NWChem basis-library name",
            "functional": "required explicit XC functional when method=dft",
            "reference": "optional rhf, uhf, or rohf reference selection",
            "charge/multiplicity": "optional values overriding the supplied structure metadata",
        },
        required_methods={
            action: ("method", "basis")
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "calculate_dipole_moment", "calculate_atomic_charges",
            )
        },
        required_settings={
            action: ("scf_convergence", "max_scf_cycles")
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "calculate_dipole_moment", "calculate_atomic_charges",
            )
        },
    ),
    _backend(
        "openmolcas", "OpenMolcas", "openmolcas",
        (
            "calculate_energy", "calculate_dipole_moment",
            "calculate_atomic_charges", "calculate_orbitals",
        ),
        "OpenMolcas v25.10 molecular HF/Kohn-Sham SCF energy, dipole, Mulliken-charge, and orbital-property calculations from typed structures and explicit SCF controls.",
        executables=("pymolcas",), environment=("CHEMGRAPH_OPENMOLCAS_COMMAND",),
        data_resources=("OpenMolcas v25.10 basis_library managed under .software_cache/installations/openmolcas/25.10",),
        install_notes="Locally compiled OpenMolcas v25.10 serial/OpenMP build with built-in Libxc.",
        method_schema={
            "method": "hf or dft",
            "basis": "explicit OpenMolcas basis-library label",
            "functional": "required explicit OpenMolcas/Libxc functional when method=dft",
            "charge/multiplicity": "optional explicit overrides of structure metadata",
        },
        required_methods={
            action: ("method", "basis")
            for action in (
                "calculate_energy", "calculate_dipole_moment",
                "calculate_atomic_charges", "calculate_orbitals",
            )
        },
        required_settings={
            action: (
                "use_symmetry", "use_uhf", "use_cholesky", "initial_guess",
                "max_scf_iterations", "scf_thresholds",
            )
            for action in (
                "calculate_energy", "calculate_dipole_moment",
                "calculate_atomic_charges", "calculate_orbitals",
            )
        },
        supported_system_types={
            action: ("molecule", "cluster")
            for action in (
                "calculate_energy", "calculate_dipole_moment",
                "calculate_atomic_charges", "calculate_orbitals",
            )
        },
        validation_levels={
            action: "real_smoke"
            for action in (
                "calculate_energy", "calculate_dipole_moment",
                "calculate_atomic_charges", "calculate_orbitals",
            )
        },
    ),
    _backend(
        "multiwfn", "Multiwfn", "multiwfn",
        (
            "calculate_atomic_charges", "calculate_bond_orders",
            "calculate_electron_isodensity_surface",
        ),
        "Multiwfn 2026.7.15 noGUI wavefunction post-processing for explicit population analysis, bond orders, and batch molecular electron-isodensity surface areas/volumes.",
        executables=("Multiwfn_noGUI",), environment=("CHEMGRAPH_MULTIWFN_COMMAND",),
        license_class="custom_open_source_citation_required",
        data_resources=(
            "Agent-supplied fch/fchk/wfn/wfx/mwfn/Molden/47 wavefunction file; both required Multiwfn citations are returned in provenance",
        ),
        install_notes=(
            "Official 2026.7.15 Linux noGUI binary is managed under .software_cache/installations/multiwfn; "
            "the adapter uses fixed version-specific menu sequences and accepts no arbitrary menu script."
        ),
        method_schema={
            "population_analysis": "mulliken or lowdin",
            "bond_order_definition": "mayer, wiberg_lowdin, or mulliken",
            "surface_input": "wavefunction electron density or an external cube grid, inferred from the supplied file extension",
        },
        required_methods={
            "calculate_atomic_charges": ("population_analysis",),
            "calculate_bond_orders": ("bond_order_definition",),
        },
        required_settings={
            "calculate_bond_orders": ("minimum_bond_order",),
            "calculate_electron_isodensity_surface": (
                "cutoffs_au", "grid_spacing_bohr",
            ),
        },
        supported_system_types={
            "calculate_atomic_charges": ("molecular_wavefunction",),
            "calculate_bond_orders": ("molecular_wavefunction",),
            "calculate_electron_isodensity_surface": (
                "molecular_wavefunction", "molecular_density_grid",
            ),
        },
        validation_levels={
            "calculate_atomic_charges": "real_smoke",
            "calculate_bond_orders": "real_smoke",
            "calculate_electron_isodensity_surface": "real_smoke",
        },
    ),
    _backend(
        "critic2", "Critic2", "critic2",
        (
            "analyze_electron_density_topology", "calculate_atomic_basin_properties",
            "calculate_bader_charges",
        ),
        "Critic2 1.2.1081 QTAIM critical-point search and typed grid-basin integration over Agent-supplied fields.",
        executables=("critic2",), environment=("CHEMGRAPH_CRITIC2_COMMAND",),
        data_resources=(
            "Agent-supplied electron-density grid or compatible wavefunction file; an explicit separate structure file is required when the density file does not contain geometry",
        ),
        install_notes=(
            "The locally compiled GPL-3.0 development build is managed under "
            ".software_cache/installations/critic2/install-conda. The adapter exposes typed AUTO/CPREPORT "
            "controls and never accepts an arbitrary Critic2 command script."
        ),
        required_settings={
            "analyze_electron_density_topology": (
                "system_type", "density_format", "interpolation",
                "critical_point_types", "gradient_tolerance",
                "seed_strategy", "report_detail",
                "max_reported_critical_points",
            ),
            "calculate_atomic_basin_properties": (
                "system_type", "density_format", "interpolation",
                "partition_method", "non_nuclear_maxima",
                "all_maxima_non_atomic", "write_weight_cubes",
                "max_reported_basins", "laplacian_sum_tolerance",
            ),
            "calculate_bader_charges": (
                "system_type", "density_format", "interpolation",
                "partition_method", "non_nuclear_maxima",
                "all_maxima_non_atomic", "write_weight_cubes",
                "max_reported_basins", "laplacian_sum_tolerance",
            ),
        },
    ),
    _backend(
        "psi4", "Psi4", "psi4",
        ("calculate_energy", "calculate_hessian", "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals"),
        "Psi4 molecular electronic-structure calculations.", modules=("psi4",), executables=("psi4",),
        conda=("psi4",), required_methods={
            action: ("method", "basis") for action in
            ("calculate_energy", "calculate_hessian", "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals")
        },
    ),
    _backend(
        "tblite", "TBLite", "quantum",
        ("calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry", "calculate_dipole_moment"),
        "TBLite GFN calculator through its Python/ASE interface.", modules=("tblite", "ase"),
        pip=("tblite==0.4.0",), required_methods={
            action: ("method",) for action in
            ("calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry", "calculate_dipole_moment")
        }, required_settings={
            "calculate_hessian": ("displacement_angstrom",),
            "optimize_geometry": ("fmax_ev_per_angstrom", "optimizer", "max_steps"),
        },
        method_schema={
            "method": "gfn1, gfn1-xtb, gfn2, or gfn2-xtb",
            "optimizer": "bfgs, lbfgs, or fire for optimize_geometry",
        },
        allowed_methods={
            action: {"method": ("gfn1", "gfn1-xtb", "gfn2", "gfn2-xtb")}
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "optimize_geometry", "calculate_dipole_moment",
            )
        },
        allowed_settings={"optimize_geometry": {"optimizer": _ASE_OPTIMIZER_CHOICES}},
    ),
    _backend(
        "mace", "MACE", "mlip",
        ("calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry"),
        "MACE machine-learned interatomic potential with explicit model/device selection.",
        modules=("mace.calculators", "ase"), pip=("mace-torch==0.3.16",),
        method_schema={
            "model": (
                "one exact installed cache alias: 'medium-mpa-0', "
                "'MACE-MPA-0-medium', 'medium', or 'MACE-MP-0-medium'; "
                "alternatively an explicit local model path, "
                "or a pinned MACE 0.3.16 foundation-model name/HTTPS URL when allow_model_download=true"
            ),
            "device": "explicit MACE device such as cpu, cuda, or cuda:<index>",
            "allow_model_download": "explicit boolean; false still permits an installed cache alias/local path",
            "default_dtype": "optional float32 or float64",
            "optimizer": "bfgs, lbfgs, or fire for optimize_geometry",
        },
        required_methods={
            action: ("model", "device", "allow_model_download")
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
            )
        },
        required_settings={
            "calculate_hessian": ("displacement_angstrom",),
            "optimize_geometry": ("fmax_ev_per_angstrom", "optimizer", "max_steps"),
        },
        allowed_settings={"optimize_geometry": {"optimizer": _ASE_OPTIMIZER_CHOICES}},
    ),
    _backend(
        "chgnet", "CHGNet", "mlip",
        ("calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry"),
        "CHGNet machine-learned interatomic potential with explicit model/device selection.",
        modules=("chgnet", "ase"), pip=("chgnet",),
        required_methods={
            action: ("model", "device", "allow_model_download")
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
            )
        },
        required_settings={
            "calculate_hessian": ("displacement_angstrom",),
            "optimize_geometry": ("fmax_ev_per_angstrom", "optimizer", "max_steps"),
        },
        allowed_settings={"optimize_geometry": {"optimizer": _ASE_OPTIMIZER_CHOICES}},
    ),
    _backend(
        "deepmd", "DeePMD-kit", "deepmd",
        (
            "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
            "calculate_periodic_energy", "calculate_periodic_forces",
            "calculate_periodic_stress", "relax_periodic_structure",
        ),
        "DeePMD inference from an exact registered checkpoint and an explicit multitask branch; the adapter never chooses or downloads a model.",
        modules=("deepmd", "ase"), executables=("dp",),
        pip=("deepmd-kit==3.2.0b0", "ase", "e3nn"),
        data_resources=(
            "Explicit resource:// DeePMD model checkpoint; multitask checkpoints require a named model_branch and single-task checkpoints require model_branch=single_task",
        ),
        method_schema={
            "model": "resource://<registered_deepmd_checkpoint> or an explicit workspace file ArtifactRef",
            "device": "cpu (the configured inference runtime is CPU-only)",
            "model_branch": "exact registered multitask branch, or the literal single_task",
            "charge": "explicit total charge supplied as a DeePMD frame parameter",
            "spin": "explicit spin value supplied as a DeePMD frame parameter",
            "frame_parameters": "optional additional explicit per-frame parameters",
        },
        required_methods={
            action: ("model", "device", "model_branch", "charge", "spin")
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
                "calculate_periodic_energy", "calculate_periodic_forces",
                "calculate_periodic_stress", "relax_periodic_structure",
            )
        },
        required_settings={
            "calculate_hessian": ("displacement_angstrom",),
            "optimize_geometry": ("fmax_ev_per_angstrom", "optimizer", "max_steps"),
            **_MLIP_PERIODIC_RELAX,
        },
        allowed_settings={
            "optimize_geometry": {"optimizer": _ASE_OPTIMIZER_CHOICES},
            "relax_periodic_structure": {"optimizer": _ASE_OPTIMIZER_CHOICES},
        },
    ),
    _backend(
        "nequip", "NequIP", "nequip",
        (
            "calculate_periodic_energy", "calculate_periodic_forces",
            "calculate_periodic_stress", "relax_periodic_structure",
        ),
        "NequIP inference from the exact checkpoint and species mapping selected by the Agent.",
        modules=("nequip", "torch", "e3nn", "ase"),
        executables=("nequip-train",), pip=("nequip==0.19.0",),
        data_resources=("Explicit resource:// NequIP checkpoint or workspace model ArtifactRef",),
        method_schema={
            "model": "resource://<registered_nequip_checkpoint> or an explicit workspace file ArtifactRef",
            "device": "cpu, cuda, or cuda:<index>",
            "chemical_species_mapping": "identity or an explicit element-to-model-type mapping",
            "allow_tf32": "explicit boolean controlling CUDA TF32 use",
            "neighborlist_backend": "optional NequIP neighbor-list backend; default matscipy",
        },
        required_methods={
            action: ("model", "device", "chemical_species_mapping", "allow_tf32")
            for action in (
                "calculate_periodic_energy", "calculate_periodic_forces",
                "calculate_periodic_stress", "relax_periodic_structure",
            )
        },
        required_settings=_MLIP_PERIODIC_RELAX,
        allowed_settings={
            "relax_periodic_structure": {"optimizer": _ASE_OPTIMIZER_CHOICES}
        },
    ),
    _backend(
        "allegro", "Allegro", "nequip",
        (
            "calculate_periodic_energy", "calculate_periodic_forces",
            "calculate_periodic_stress", "relax_periodic_structure",
        ),
        "Allegro inference through the NequIP integration using the exact checkpoint and species mapping selected by the Agent.",
        modules=("allegro", "nequip", "torch", "e3nn", "ase"),
        pip=("nequip-allegro==0.8.3", "nequip==0.19.0"),
        data_resources=("Explicit resource:// Allegro checkpoint or workspace model ArtifactRef",),
        method_schema={
            "model": "resource://<registered_allegro_checkpoint> or an explicit workspace file ArtifactRef",
            "device": "cpu, cuda, or cuda:<index>",
            "chemical_species_mapping": "identity or an explicit element-to-model-type mapping",
            "allow_tf32": "explicit boolean controlling CUDA TF32 use",
            "neighborlist_backend": "optional NequIP neighbor-list backend; default matscipy",
        },
        required_methods={
            action: ("model", "device", "chemical_species_mapping", "allow_tf32")
            for action in (
                "calculate_periodic_energy", "calculate_periodic_forces",
                "calculate_periodic_stress", "relax_periodic_structure",
            )
        },
        required_settings=_MLIP_PERIODIC_RELAX,
        allowed_settings={
            "relax_periodic_structure": {"optimizer": _ASE_OPTIMIZER_CHOICES}
        },
    ),
    _backend(
        "orca", "ORCA", "quantum",
        (
            "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
            "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals",
            "calculate_bond_orders", "calculate_excited_states",
            "calculate_correlated_electron_density", "export_electron_density_grid",
        ),
        (
            "Operator-provided ORCA 6.1.1 electronic-structure executable with an isolated "
            "OpenMPI 4.1.8 runtime. The Agent explicitly selects method, basis, solvation, "
            "and resources. This server's validated execution contract permits up to 48 "
            "CPU cores; the evaluator supplies the common compute timeout."
        ),
        executables=("orca",), environment=("CHEMGRAPH_ORCA_COMMAND",),
        license_class="manual_license",
        install_notes=(
            "Configured from the operator-downloaded ORCA 6.1.1 installer under "
            ".software_cache/installations/orca/6.1.1 with the exact OpenMPI 4.1.8 runtime required by this "
            "ORCA build. Parallel Actions retain the Agent-selected PAL process count without "
            "automatic fallback or resource substitution."
        ),
        resource_constraints={
            "maximum_cpu_cores": 48,
            "reason": (
                "The current 64-online-CPU server reserves capacity for the service and exposes "
                "at most 48 ORCA MPI processes per synchronous Action."
            ),
        },
        method_schema={
            "method": "ORCA method/functional keyword",
            "basis": "ORCA orbital basis keyword or method_default/auto for a built-in 3c composite method",
            "basis_conditional": (
                "Non-composite ORCA methods require a concrete method_spec.basis. "
                "HF-3c, B97-3c, r2SCAN-3c, PBEh-3c, B3LYP-3c, and wB97X-3c "
                "include their orbital basis and require basis to be omitted or set to "
                "method_default/auto; the sentinel is never emitted as an ORCA keyword."
            ),
            "dispersion": "optional ORCA dispersion keyword",
            "solvation_model": "optional cpcm or smd implicit-solvation model",
            "solvent": "required solvent name when solvation_model is supplied",
            "charge": "optional explicit molecular charge",
            "multiplicity": "optional explicit spin multiplicity",
            "density_type": "scf, relaxed_mp2, or unrelaxed_ccsd; unavailable combinations are rejected rather than silently substituted",
            "auxiliary_basis": "optional ORCA auxiliary/C basis keyword for MP2 and double-hybrid methods",
            "frozen_core": "optional explicit boolean; false emits NoFrozenCore",
            "pmodel": "optional explicit boolean enabling ORCA PModel for the density calculation",
        },
        required_methods={
            action: ("method",) for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
                "calculate_dipole_moment", "calculate_orbitals", "calculate_bond_orders",
            )
        } | {
            "calculate_atomic_charges": ("method", "population_analysis"),
            "calculate_excited_states": ("method", "excited_state_method"),
            "calculate_correlated_electron_density": (
                "method", "density_type",
            ),
        },
        required_settings={
            "optimize_geometry": ("optimization_convergence", "max_steps"),
            "calculate_bond_orders": ("minimum_bond_order",),
            "calculate_excited_states": (
                "number_of_states", "spin_symmetry",
                "excited_energy_tolerance_hartree", "residual_tolerance",
            ),
            "calculate_correlated_electron_density": (
                "scf_convergence", "max_scf_cycles", "stability_analysis",
            ),
            "export_electron_density_grid": ("density_source", "output_format"),
        },
        allowed_methods={
            action: {"solvation_model": ("cpcm", "smd")}
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "optimize_geometry", "calculate_dipole_moment",
                "calculate_atomic_charges", "calculate_orbitals",
                "calculate_bond_orders", "calculate_excited_states",
            )
        } | {
            "calculate_correlated_electron_density": {
                "density_type": ("scf", "relaxed_mp2", "unrelaxed_ccsd"),
            }
        },
        allowed_settings={
            "optimize_geometry": {
                "optimization_convergence": ("Loose", "Normal", "Tight", "VeryTight")
            },
            "calculate_correlated_electron_density": {
                "scf_convergence": ("LooseSCF", "TightSCF", "VeryTightSCF"),
            },
            "export_electron_density_grid": {
                "density_source": ("scf", "relaxed_mp2", "mdci"),
                "output_format": ("wfn", "wfx", "cube"),
            },
        },
    ),
    _backend(
        "gaussian", "Gaussian 16", "gaussian",
        ("calculate_energy", "calculate_hessian", "optimize_geometry", "calculate_dipole_moment"),
        "Operator-provided Gaussian 16 C.01 SCF/DFT jobs rendered from typed molecular structures and explicit method settings.",
        executables=("g16", "formchk"),
        environment=("CHEMGRAPH_GAUSSIAN_COMMAND", "CHEMGRAPH_GAUSSIAN_FORMCHK_COMMAND"),
        license_class="commercial_license",
        install_notes=(
            "Configured from the operator-provided Gaussian 16 C.01 distribution under "
            ".software_cache/installations/gaussian/g16; the adapter accepts no arbitrary route deck."
        ),
        resource_constraints={
            "maximum_cpu_cores": 48,
            "reason": (
                "The current 64-online-CPU server reserves capacity for the service and "
                "exposes at most 48 Gaussian shared-memory cores per synchronous Action."
            ),
        },
        method_schema={
            "method": "Gaussian SCF or DFT method keyword",
            "basis": "Gaussian built-in basis-set keyword",
            "dispersion": "optional single Gaussian dispersion route keyword",
            "solvation_model": "optional pcm, cpcm, or smd implicit-solvation model",
            "solvent": "required Gaussian solvent name when solvation_model is supplied",
            "charge": "optional explicit molecular charge",
            "multiplicity": "optional explicit spin multiplicity",
        },
        required_methods={
            action: ("method", "basis")
            for action in ("calculate_energy", "calculate_hessian", "optimize_geometry", "calculate_dipole_moment")
        },
        required_settings={
            "calculate_energy": ("scf_convergence",),
            "calculate_hessian": ("scf_convergence",),
            "calculate_dipole_moment": ("scf_convergence",),
            "optimize_geometry": ("scf_convergence", "optimization_convergence", "max_steps"),
        },
        allowed_methods={
            action: {"solvation_model": ("pcm", "cpcm", "smd")}
            for action in (
                "calculate_energy", "calculate_hessian", "optimize_geometry",
                "calculate_dipole_moment",
            )
        },
        allowed_settings={
            "optimize_geometry": {
                "scf_convergence": ("Loose", "Tight", "VeryTight"),
                "optimization_convergence": ("Loose", "Tight", "VeryTight"),
            }
        },
    ),
    _backend(
        "gamess", "GAMESS", "gamess",
        ("calculate_energy", "optimize_geometry", "calculate_dipole_moment"),
        "Operator-registered GAMESS 15 Jul 2024 R2 Patch 1 molecular SCF/DFT calculations through a typed input renderer.",
        executables=("rungms",), environment=("CHEMGRAPH_GAMESS_COMMAND",),
        license_class="registration_license",
        install_notes=(
            "The registered source distribution is compiled under .software_cache/installations/gamess/2024-r2-p1 "
            "with a sockets DDI build and isolated compiler/runtime libraries."
        ),
        method_schema={
            "scftyp": "RHF, UHF, ROHF, or another explicit GAMESS SCFTYP",
            "gbasis": "GAMESS GBASIS family such as STO, N31, or N311",
            "ngauss": "explicit Gaussian primitive count for GBASIS",
            "dfttyp": "optional GAMESS DFTTYP keyword",
            "ndfunc/npfunc/nffunc": "optional explicit polarization counts",
            "diffsp/diffs": "optional explicit diffuse-function booleans",
            "charge/multiplicity": "optional explicit molecular charge and multiplicity",
        },
        required_methods={
            action: ("scftyp", "gbasis", "ngauss")
            for action in ("calculate_energy", "optimize_geometry", "calculate_dipole_moment")
        },
        required_settings={
            "calculate_energy": ("scf_convergence",),
            "calculate_dipole_moment": ("scf_convergence",),
            "optimize_geometry": ("scf_convergence", "gradient_tolerance_hartree_per_bohr", "max_steps"),
        },
    ),
    _backend(
        "ase_emt", "ASE EMT", "core", ("calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry"),
        "ASE bundled EMT reference calculator, mainly for validation and small supported element sets.",
        modules=("ase.calculators.emt",), pip=("ase",), required_settings={
            "calculate_hessian": ("displacement_angstrom",),
            "optimize_geometry": ("fmax_ev_per_angstrom", "optimizer", "max_steps"),
        },
        allowed_settings={"optimize_geometry": {"optimizer": _ASE_OPTIMIZER_CHOICES}},
    ),
    _backend(
        "internal_vibrations", "ResearchChem vibrational analysis", "core", ("derive_vibrational_modes",),
        "Mass-weighted Hessian diagonalization with explicit units and linearity handling.", modules=("ase", "numpy"), pip=("ase", "numpy"),
        method_schema={
            "hessian": "full Hessian object, full ArtifactRef, compact {artifact_id}, or artifact-id string",
            "structure": "matching AtomicStructure or its ArtifactRef",
            "linearity": "linear, nonlinear, or explicitly selected auto metadata",
        },
        required_settings={"derive_vibrational_modes": ("linearity",)},
        allowed_settings={
            "derive_vibrational_modes": {"linearity": ("linear", "nonlinear", "auto")}
        },
    ),
    _backend(
        "internal_spectroscopy", "ResearchChem spectrum builder", "core",
        ("derive_ir_spectrum", "derive_uv_vis_spectrum"),
        "Deterministic line/broadened spectrum construction from supplied frequencies and intensities.", modules=("numpy",), pip=("numpy",),
        required_settings={
            "derive_ir_spectrum": ("broadening", "fwhm_cm1"),
            "derive_uv_vis_spectrum": (
                "broadening", "fwhm_ev", "minimum_energy_ev",
                "maximum_energy_ev", "grid_points",
            ),
        },
    ),
    _backend(
        "internal_thermochemistry", "ResearchChem statistical thermochemistry", "core", ("derive_thermochemistry",),
        "Ideal-gas rigid-rotor/harmonic-oscillator thermochemistry from supplied results.", modules=("ase", "numpy"), pip=("ase", "numpy"),
        method_schema={
            "energy": "EnergyResult with an explicit eV/hartree unit, including ArtifactRef forms",
            "frequencies": "FrequencyResult including its matching structure, or supply inputs.structure separately",
            "geometry": "monatomic, linear, or nonlinear",
            "symmetry_number": "explicit positive rotational symmetry number",
            "spin": "explicit total electronic spin used by ASE IdealGasThermo",
            "ignore_imaginary_modes": "explicit boolean controlling imaginary-mode handling",
        },
        required_inputs={"derive_thermochemistry": ("energy", "frequencies")},
        required_settings={
            "derive_thermochemistry": (
                "temperature_kelvin", "pressure_pa", "geometry", "symmetry_number", "spin",
                "ignore_imaginary_modes",
            )
        },
        allowed_settings={
            "derive_thermochemistry": {"geometry": ("monatomic", "linear", "nonlinear")}
        },
    ),
    _backend(
        "goodvibes",
        "GoodVibes",
        "goodvibes",
        (
            "derive_thermochemistry",
            "scan_thermochemistry_temperature",
            "analyze_thermochemical_ensemble",
            "validate_thermochemistry_inputs",
            "analyze_thermochemical_selectivity",
            "analyze_reaction_free_energy_profile",
        ),
        (
            "GoodVibes 4.3.0 post-processing for explicit Gaussian, ORCA, NWChem, Q-Chem, "
            "xTB, or ASE-extxyz outputs: RRHO/quasi-harmonic thermochemistry, temperature "
            "analysis, conformer populations, selectivity, consistency checks, and reaction "
            "free-energy profiles. It never runs or chooses the upstream quantum calculation."
        ),
        modules=("goodvibes",),
        executables=("goodvibes",),
        pip=("goodvibes[full]==4.3.0",),
        install_notes=(
            "Pinned GoodVibes 4.3.0 with full JSON/CSV/Parquet/plot dependencies; official "
            "v4.3.0 source and examples are cached under .software_cache/sources/goodvibes/4.3.0/source. "
            "The supported Python surface includes goodvibes.api.compute_thermo/compute_batch; "
            "goodvibes.gaussian and goodvibes.orca are not public modules. Prefer the preset "
            "Action or CLI unless a documented public API is explicitly required."
        ),
        method_schema={
            "single_point_correction_suffix": (
                "optional explicit GoodVibes --spc suffix; derive_thermochemistry accepts the "
                "matching high-level calculation as inputs.single_point_output_file and stages "
                "a safe frequency/SPC filename pair. A legacy matching file beside the frequency "
                "output remains accepted when the explicit input is omitted"
            ),
            "custom_file_extensions": (
                "optional list of additional accepted extensions such as .qfi or .gaussian"
            ),
            "exclude_pattern": "optional explicit filename glob excluded by GoodVibes",
            "free_space_solvent": (
                "optional GoodVibes free-space solvent correction name; supported names are "
                "version-specific and must be selected by the Agent"
            ),
            "media_solvent": (
                "optional GoodVibes --media solution solvent; supported names are "
                "version-specific and must be selected by the Agent"
            ),
            "frequency_scale_factor": (
                "action_settings positive number or explicit 'auto'; mapped to --vscal, "
                "never to --fs"
            ),
            "zpe_scale_factor": (
                "action_settings positive number, 'auto', or 'same_as_frequency'; combinations "
                "that the GoodVibes CLI cannot represent faithfully are rejected"
            ),
            "quasi_harmonic_conditionals": (
                "grimme/truhlar entropy requires entropy_frequency_cutoff_cm1; grimme also "
                "requires free_rotor_inertia_model; Head-Gordon enthalpy requires "
                "enthalpy_frequency_cutoff_cm1"
            ),
            "population_basis_conditionals": (
                "population_basis=quasi_harmonic_gibbs requires entropy_model=grimme or "
                "truhlar; provide entropy_frequency_cutoff_cm1, and for grimme also provide "
                "free_rotor_inertia_model"
            ),
            "standard_state_conditionals": (
                "custom_concentration requires action_settings.concentration_mol_l"
            ),
            "imaginary_frequency_conditionals": (
                "invert_below_threshold requires action_settings.imaginary_frequency_threshold_cm1"
            ),
            "duplicate_conditionals": (
                "deduplicate_structures=true requires explicit energy, rotational, and nullable "
                "RMSD duplicate cutoffs"
            ),
        },
        required_inputs={
            "derive_thermochemistry": ("output_file",),
            "scan_thermochemistry_temperature": ("output_files", "temperatures_kelvin"),
            "analyze_thermochemical_ensemble": ("output_files",),
            "validate_thermochemistry_inputs": ("output_files",),
            "analyze_thermochemical_selectivity": ("output_files", "label_groups"),
            "analyze_reaction_free_energy_profile": (
                "output_files", "profile_definition_file",
            ),
        },
        required_settings={
            "derive_thermochemistry": (
                "temperature_kelvin", "standard_state", "entropy_model",
                "enthalpy_model", "frequency_scale_factor", "zpe_scale_factor",
                "symmetry_correction", "imaginary_frequency_policy",
            ),
            "scan_thermochemistry_temperature": (
                "standard_state", "entropy_model", "enthalpy_model",
                "frequency_scale_factor", "zpe_scale_factor", "symmetry_correction",
                "imaginary_frequency_policy",
            ),
            "analyze_thermochemical_ensemble": (
                "temperature_kelvin", "standard_state", "entropy_model",
                "enthalpy_model", "frequency_scale_factor", "zpe_scale_factor",
                "symmetry_correction", "imaginary_frequency_policy", "population_basis",
                "deduplicate_structures",
            ),
            "validate_thermochemistry_inputs": (
                "temperature_kelvin", "standard_state", "entropy_model",
                "enthalpy_model", "frequency_scale_factor", "zpe_scale_factor",
                "symmetry_correction", "imaginary_frequency_policy",
                "duplicate_energy_cutoff_kcal_mol",
                "duplicate_rotational_cutoff_fraction", "duplicate_rmsd_cutoff_angstrom",
            ),
            "analyze_thermochemical_selectivity": (
                "temperature_kelvin", "standard_state", "entropy_model",
                "enthalpy_model", "frequency_scale_factor", "zpe_scale_factor",
                "symmetry_correction", "imaginary_frequency_policy", "population_basis",
                "deduplicate_structures",
            ),
            "analyze_reaction_free_energy_profile": (
                "temperature_kelvin", "standard_state", "entropy_model",
                "enthalpy_model", "frequency_scale_factor", "zpe_scale_factor",
                "symmetry_correction", "imaginary_frequency_policy",
                "profile_ensemble_mode",
            ),
        },
        allowed_settings={
            action_id: {
                "standard_state": ("gas_1atm", "solution_1mol_l", "custom_concentration"),
                "entropy_model": ("rrho", "grimme", "truhlar"),
                "enthalpy_model": ("rrho", "head_gordon"),
                "imaginary_frequency_policy": ("retain", "invert_below_threshold"),
                "free_rotor_inertia_model": ("global", "per_conformer"),
                **(
                    {"population_basis": ("electronic_energy", "quasi_harmonic_gibbs")}
                    if action_id in {
                        "analyze_thermochemical_ensemble",
                        "analyze_thermochemical_selectivity",
                    }
                    else {}
                ),
                **(
                    {
                        "profile_ensemble_mode": (
                            "gconf", "lowest_conformer", "boltzmann_without_gconf",
                        )
                    }
                    if action_id == "analyze_reaction_free_energy_profile"
                    else {}
                ),
            }
            for action_id in (
                "derive_thermochemistry",
                "scan_thermochemistry_temperature",
                "analyze_thermochemical_ensemble",
                "validate_thermochemistry_inputs",
                "analyze_thermochemical_selectivity",
                "analyze_reaction_free_energy_profile",
            )
        },
        validation_levels={
            "derive_thermochemistry": "validated",
            "scan_thermochemistry_temperature": "validated",
            "analyze_thermochemical_ensemble": "validated",
            "validate_thermochemistry_inputs": "validated",
            "analyze_thermochemical_selectivity": "validated",
            "analyze_reaction_free_energy_profile": "validated",
        },
    ),
    _backend(
        "geometric", "geomeTRIC", "nwchem", ("optimize_geometry",),
        "geomeTRIC 1.1.1 molecular geometry optimization driven by the exact energy/force backend and settings selected in component_backends.calculator.",
        modules=("geometric", "numpy"), pip=("geometric==1.1.1",),
        method_schema={
            "calculator_method": "complete method_spec mapping passed unchanged to the Agent-selected calculator backend",
            "calculator_action_settings": (
                "action-keyed mapping with both calculate_energy and calculate_forces objects; "
                "each object must contain the settings required by the exact Agent-selected "
                "component_backends.calculator"
            ),
        },
        required_methods={"optimize_geometry": ("calculator_method",)},
        required_settings={
            "optimize_geometry": (
                "calculator_action_settings", "coordinate_system", "max_iterations",
                "trust_radius_angstrom", "minimum_trust_radius_angstrom",
                "maximum_trust_radius_angstrom", "hessian_strategy",
                "project_rigid_force_torque", "convergence_energy_hartree",
                "convergence_grms_hartree_per_bohr",
                "convergence_gmax_hartree_per_bohr", "convergence_drms_angstrom",
                "convergence_dmax_angstrom", "rigid_fragments",
                "constraint_algorithm", "constraint_enforcement_tolerance",
            ),
        },
        required_components={"optimize_geometry": ("calculator",)},
        component_options={
            "optimize_geometry": {
                "calculator": (
                    "xtb", "pyscf", "tblite", "gpaw", "nwchem", "orca",
                    "mace", "chgnet", "deepmd", "ase_emt",
                ),
            },
        },
        supported_system_types={"optimize_geometry": ("molecule", "cluster")},
        validation_levels={"optimize_geometry": "validated"},
    ),
    _backend(
        "sella", "Sella", "sella", ("optimize_geometry", "locate_transition_state"),
        "Sella 2.5.0 order-0 minimum optimization and order-1 transition-state search driven by the exact energy/force backend and settings selected in component_backends.calculator.",
        modules=("sella", "ase", "numpy"), pip=("sella==2.5.0",),
        method_schema={
            "calculator_method": "complete method_spec mapping passed unchanged to the Agent-selected calculator backend",
            "calculator_action_settings": (
                "action-keyed mapping with both calculate_energy and calculate_forces objects, "
                "for example {'calculate_energy': {}, 'calculate_forces': {}} when the selected "
                "calculator declares no nested settings"
            ),
        },
        required_methods={
            action: ("calculator_method",)
            for action in ("optimize_geometry", "locate_transition_state")
        },
        required_settings={
            action: (
                "calculator_action_settings", "force_threshold_ev_per_angstrom",
                "max_steps", "internal_coordinates", "initial_trust_radius",
                "minimum_model_quality", "finite_difference_step",
                "three_point_differences", "steps_per_diagonalization",
                "diagonalization_interval", "allow_fragments",
                "refine_initial_hessian_iterations",
            )
            for action in ("optimize_geometry", "locate_transition_state")
        },
        required_components={
            action: ("calculator",)
            for action in ("optimize_geometry", "locate_transition_state")
        },
        component_options={
            action: {
                "calculator": (
                    "xtb", "pyscf", "tblite", "gpaw", "nwchem", "orca",
                    "mace", "chgnet", "deepmd", "ase_emt",
                ),
            }
            for action in ("optimize_geometry", "locate_transition_state")
        },
        supported_system_types={
            action: ("molecule", "cluster")
            for action in ("optimize_geometry", "locate_transition_state")
        },
        validation_levels={
            action: "validated"
            for action in ("optimize_geometry", "locate_transition_state")
        },
    ),
    _backend(
        "pysisyphus", "pysisyphus", "reaction",
        (
            "locate_transition_state", "search_reaction_path",
            "scan_reaction_coordinates", "trace_intrinsic_reaction_coordinate",
        ),
        (
            "pysisyphus transition-state, double-ended chain-of-states, relaxed coordinate "
            "scan, and IRC algorithms using explicit structures and calculator settings."
        ),
        modules=("pysisyphus",), executables=("pysis",), pip=("pysisyphus==1.0.0",),
        resource_constraints={
            "maximum_cpu_cores": 48,
            "reason": "Calculator processes/threads remain exactly Agent-selected, capped at 48 on this server.",
        },
        method_schema={
            "calculator_backend": "exact native pysisyphus calculator type: xtb, pyscf, or orca",
            "method": (
                "method interpreted by the explicitly selected calculator_backend; for xtb use "
                "GFN0-xTB, GFN1-xTB, GFN2-xTB, or GFN-FF (compact gfn0/gfn1/gfn2/gfnff "
                "spellings are equivalent)"
            ),
            "basis": "basis-set label used by calculator_backend=pyscf and optionally by orca",
            "functional": "DFT functional used when calculator_backend=pyscf and method denotes DFT",
            "charge": "explicit integer molecular charge; otherwise taken from the supplied structure",
            "multiplicity": "explicit positive spin multiplicity; otherwise taken from the supplied structure",
            "solvation_model": "optional alpb/gbsa for xTB or cpcm/smd for ORCA",
            "solvent": (
                "required solvent name when solvation_model is supplied; xTB 6.7 validates "
                "its exact built-in ALPB/GBSA parameter set and does not provide ethanol"
            ),
            "pyscf_basis_conditional": "calculator_backend=pyscf requires method_spec.basis",
            "hessian_init": (
                "explicit pysisyphus initial-Hessian strategy; calc requests an exact Hessian, "
                "whereas unit/fischer/lindh/simple/swart/xtb/xtb1/xtbff select the named model"
            ),
        },
        required_methods={
            action: ("calculator_backend", "method")
            for action in (
                "locate_transition_state", "search_reaction_path",
                "scan_reaction_coordinates", "trace_intrinsic_reaction_coordinate",
            )
        },
        required_settings={
            "locate_transition_state": ("optimizer", "convergence", "max_cycles", "hessian_init"),
            "search_reaction_path": (
                "path_method", "interpolation", "images", "optimizer",
                "convergence", "max_cycles", "climb",
            ),
            "scan_reaction_coordinates": (
                "coordinate_type", "atom_indices", "start_value", "end_value",
                "value_unit", "steps", "optimizer", "convergence", "max_cycles",
                "hessian_init",
            ),
            "trace_intrinsic_reaction_coordinate": ("integrator", "step_length", "max_cycles", "forward", "backward", "hessian_init"),
        },
        allowed_methods={
            action: {
                "calculator_backend": ("xtb", "pyscf", "orca"),
                "solvation_model": ("alpb", "gbsa", "cpcm", "smd"),
            }
            for action in (
                "locate_transition_state", "search_reaction_path",
                "scan_reaction_coordinates", "trace_intrinsic_reaction_coordinate",
            )
        },
        allowed_settings={
            "locate_transition_state": {
                "optimizer": ("rsprfo", "prfo", "trim", "rsirfo", "irfo"),
                "convergence": ("nwchem_loose", "gau_loose", "gau", "gau_tight", "gau_vtight", "baker", "never"),
                "hessian_init": ("calc", "unit", "fischer", "lindh", "simple", "swart", "xtb", "xtb1", "xtbff"),
            },
            "search_reaction_path": {
                "path_method": ("neb", "growing_string", "freezing_string"),
                "interpolation": ("linear", "idpp", "redund"),
                "optimizer": ("qm", "fire", "lbfgs", "string", "sd"),
                "convergence": ("nwchem_loose", "gau_loose", "gau", "gau_tight", "gau_vtight", "baker", "never"),
            },
            "scan_reaction_coordinates": {
                "coordinate_type": ("bond", "angle", "dihedral"),
                "value_unit": ("angstrom", "degree", "radian"),
                "optimizer": ("rfo", "lbfgs", "fire"),
                "convergence": ("nwchem_loose", "gau_loose", "gau", "gau_tight", "gau_vtight", "baker", "never"),
                "hessian_init": ("calc", "unit", "fischer", "lindh", "simple", "swart", "xtb", "xtb1", "xtbff"),
            },
            "trace_intrinsic_reaction_coordinate": {
                "integrator": ("dvv", "euler", "eulerpc", "gs", "imk", "lqa", "modekill", "rk4"),
                "hessian_init": ("calc", "unit", "fischer", "lindh", "simple", "swart", "xtb", "xtb1", "xtbff"),
            },
        },
    ),
    _backend(
        "cantera", "Cantera", "reaction", ("calculate_chemical_equilibrium", "integrate_reaction_network"),
        "Cantera equilibrium and mechanism-based kinetic integration.", modules=("cantera",), conda=("cantera",),
        required_settings={
            "calculate_chemical_equilibrium": ("temperature_kelvin", "pressure_pa", "equilibrium_mode"),
            "integrate_reaction_network": ("time_end_seconds", "num_points"),
        },
    ),
    _backend(
        "scipy", "SciPy", "reaction", ("integrate_reaction_network",),
        "SciPy integration of an explicitly supplied mass-action network.", modules=("scipy",), pip=("scipy",),
        required_settings={"integrate_reaction_network": ("time_end_seconds", "num_points")},
    ),
    _backend(
        "rmg", "RMG-Py", "rmg",
        ("calculate_rate_constants", "calculate_tunneling_correction"),
        "RMG-Py 4.0.0 typed kinetics-model evaluation and Wigner/Eckart tunneling factors without mechanism generation or hidden database selection.",
        modules=("rmgpy",), executables=("rmg.py",), conda=("rmg=4.0.0",),
        required_methods={
            "calculate_tunneling_correction": ("tunneling_model",),
        },
        required_settings={
            "calculate_rate_constants": ("allow_extrapolation",),
        },
    ),
    _backend(
        "mess", "MESS", "mess", ("solve_master_equation",),
        "MESS 2020.1.24 multi-well gas-phase master-equation solution from an Agent-supplied native model, with structured finite/high-pressure rate-table extraction.",
        executables=("mess",), environment=("CHEMGRAPH_MESS_COMMAND",),
        install_notes="Locally compiled PAPR MESS 2020.1.24 runtime and official manual/examples.",
        required_settings={"solve_master_equation": ("maximum_rate_records",)},
        supported_system_types={"solve_master_equation": ("gas_phase_reaction_network",)},
        validation_levels={"solve_master_equation": "real_smoke"},
    ),
    _backend(
        "mesmer", "MESMER", "mesmer", ("solve_master_equation",),
        "MESMER 7.1 energy-grained master-equation solution from an Agent-supplied XML model, with structured first- and second-order phenomenological rate extraction.",
        executables=("mesmer",), environment=("CHEMGRAPH_MESMER_COMMAND",),
        install_notes="Locally compiled official MESMER 7.1 SourceForge release and manual/examples.",
        required_settings={"solve_master_equation": ("maximum_rate_records",)},
        supported_system_types={"solve_master_equation": ("gas_phase_reaction_network",)},
        validation_levels={"solve_master_equation": "real_smoke"},
    ),
    _backend(
        "pyfrag", "PyFrag", "reaction",
        (
            "analyze_activation_strain_profile",
            "summarize_activation_strain_profile",
            "validate_activation_strain_profile",
        ),
        "PyFrag 2019.02 activation-strain analysis using serial ORCA single points along an Agent-supplied reaction path.",
        executables=("pyfrag-orca",),
        environment=("CHEMGRAPH_PYFRAG_COMMAND",),
        install_notes=(
            "Pinned LGPL-3.0 v1.0.0 source with the tracked Python 3 tokenization and ORCA 6 "
            "final-energy compatibility patch. ORCA itself requires separate registration/download."
        ),
        required_methods={
            "analyze_activation_strain_profile": ("orca_keywords", "charge", "multiplicity"),
        },
        required_settings={
            "analyze_activation_strain_profile": (
                "path_format", "path_type", "fragment_1_name", "fragment_2_name",
                "fragment_1_atom_indices", "fragment_2_atom_indices",
                "fragment_1_reference_energy_kcal_mol",
                "fragment_2_reference_energy_kcal_mol",
                "reaction_coordinate_atom_indices", "maximum_path_points",
            ),
            "summarize_activation_strain_profile": ("maximum_records",),
            "validate_activation_strain_profile": (
                "energy_closure_tolerance_kcal_mol", "expected_path_point_count",
            ),
        },
        allowed_settings={
            "analyze_activation_strain_profile": {
                "path_format": ("amv", "xyz"),
                "path_type": ("irc", "lt"),
            },
        },
        supported_system_types={
            "analyze_activation_strain_profile": ("molecular_reaction_path",),
            "summarize_activation_strain_profile": ("pyfrag_activation_strain_table",),
            "validate_activation_strain_profile": ("pyfrag_activation_strain_table",),
        },
        validation_levels={
            "analyze_activation_strain_profile": "real_smoke",
            "summarize_activation_strain_profile": "real_smoke",
            "validate_activation_strain_profile": "real_smoke",
        },
    ),
    _backend(
        "catmap", "CatMAP", "catmap", ("solve_microkinetic_model",),
        "CatMAP 0.3.x microkinetic solver through an allow-listed typed model adapter that generates a controlled setup file and returns structured descriptor maps.",
        modules=("catmap",),
        pip=("git+https://github.com/SUNCAT-Center/catmap.git",),
        required_settings={"solve_microkinetic_model": ("temperature_kelvin", "pressure_bar")},
        supported_system_types={"solve_microkinetic_model": ("heterogeneous_catalytic_network",)},
        validation_levels={"solve_microkinetic_model": "real_smoke"},
    ),
    _backend(
        "bagel", "BAGEL", "bagel",
        (
            "calculate_multireference_state_energies",
            "calculate_multireference_nuclear_gradient",
            "calculate_nonadiabatic_coupling_vector",
        ),
        "BAGEL 1.2.2 state-averaged CASSCF and XMS-CASPT2 energies, analytical gradients, and nonadiabatic couplings with explicit active spaces.",
        executables=("BAGEL",),
        environment=(
            "CHEMGRAPH_BAGEL_COMMAND", "CHEMGRAPH_BAGEL_MPIRUN_COMMAND",
            "CHEMGRAPH_BAGEL_RAW_COMMAND", "CHEMGRAPH_BAGEL_BASIS_DIRECTORY",
        ),
        install_notes=(
            "GPL-3.0+ v1.2.2 source and Ubuntu 22.04 1.2.2-3ubuntu1 MPICH binary plus "
            "its redistribution-compatible runtime libraries are cached locally."
        ),
        method_schema={
            "multireference_method": "casscf or xms-caspt2; state-energy Action accepts casscf only",
            "basis": "exact bundled BAGEL orbital-basis name",
            "density_fitting_basis": "exact bundled BAGEL JK-fitting basis name",
            "active_orbitals": "positive CASSCF active-orbital count",
            "closed_orbitals": "nonnegative doubly occupied closed-orbital count",
            "active_orbital_indices": "optional explicit one-based orbital list whose length equals active_orbitals",
            "caspt2_options": "required mapping for xms-caspt2: imaginary_shift_hartree, freeze_core, and sssr",
        },
        required_methods={
            action: (
                "multireference_method", "basis", "density_fitting_basis", "charge",
                "multiplicity", "active_orbitals", "closed_orbitals", "state_count",
                "casscf_convergence", "fci_convergence", "casscf_max_iterations",
            )
            for action in (
                "calculate_multireference_state_energies",
                "calculate_multireference_nuclear_gradient",
                "calculate_nonadiabatic_coupling_vector",
            )
        },
        required_settings={
            "calculate_multireference_state_energies": (
                "maximum_returned_states", "mpi_ranks", "threads_per_rank",
            ),
            "calculate_multireference_nuclear_gradient": (
                "state_index", "max_zvector_iterations", "mpi_ranks", "threads_per_rank",
            ),
            "calculate_nonadiabatic_coupling_vector": (
                "state_index_1", "state_index_2", "coupling_type",
                "max_zvector_iterations", "mpi_ranks", "threads_per_rank",
            ),
        },
        allowed_methods={
            "calculate_multireference_state_energies": {
                "multireference_method": ("casscf",),
            },
            "calculate_multireference_nuclear_gradient": {
                "multireference_method": ("casscf", "xms-caspt2"),
            },
            "calculate_nonadiabatic_coupling_vector": {
                "multireference_method": ("casscf", "xms-caspt2"),
            },
        },
        allowed_settings={
            "calculate_nonadiabatic_coupling_vector": {
                "coupling_type": ("full", "interstate", "etf", "noweight"),
            },
        },
        supported_system_types={
            action: ("molecular_atomic_structure",)
            for action in (
                "calculate_multireference_state_energies",
                "calculate_multireference_nuclear_gradient",
                "calculate_nonadiabatic_coupling_vector",
            )
        },
        validation_levels={
            action: "real_smoke"
            for action in (
                "calculate_multireference_state_energies",
                "calculate_multireference_nuclear_gradient",
                "calculate_nonadiabatic_coupling_vector",
            )
        },
    ),
    _backend(
        "openmm", "OpenMM", "md",
        (
            "minimize_system_energy", "propagate_dynamics",
            "calculate_force_field_energy", "calculate_force_field_forces",
            "decompose_force_field_energy",
        ),
        "OpenMM force/energy evaluation, force-object decomposition, minimization, and one-segment dynamics propagation.", modules=("openmm",), conda=("openmm",),
        required_settings={
            "minimize_system_energy": ("force_tolerance_kj_mol_nm", "max_iterations"),
            "propagate_dynamics": ("ensemble", "temperature_kelvin", "timestep_fs", "steps", "report_interval"),
            "calculate_force_field_energy": ("use_saved_state", "enforce_periodic_box"),
            "calculate_force_field_forces": ("use_saved_state", "enforce_periodic_box"),
            "decompose_force_field_energy": (
                "use_saved_state", "enforce_periodic_box", "include_zero_terms",
            ),
        },
    ),
    _backend(
        "gromacs", "GROMACS", "md", ("minimize_system_energy", "propagate_dynamics"),
        "GROMACS execution from typed ParameterizedSystem artifacts and explicit segment settings.",
        executables=("gmx",), environment=("CHEMGRAPH_GROMACS_COMMAND",), conda=("gromacs",),
        required_settings={
            "minimize_system_energy": ("force_tolerance_kj_mol_nm", "max_iterations"),
            "propagate_dynamics": (
                "ensemble", "temperature_kelvin", "timestep_fs", "steps", "report_interval",
                "generate_velocities",
            ),
        },
        install_notes=(
            "For propagate_dynamics, generate_velocities=true also requires an explicit random_seed. "
            "NVT/NPT additionally require explicit temperature_coupling_groups; no coupling group is chosen implicitly."
        ),
    ),
    _backend(
        "gmx_mmpbsa", "gmx_MMPBSA", "gmx_mmpbsa",
        (
            "calculate_end_state_binding_free_energy",
            "calculate_end_state_energy_decomposition",
            "summarize_end_state_free_energy_results",
        ),
        "gmx_MMPBSA 1.6.5 end-state binding energy, residue decomposition, and bounded result parsing from explicit native inputs.",
        modules=("GMXMMPBSA",), executables=("gmx_MMPBSA",),
        environment=("CHEMGRAPH_GMX_MMPBSA_COMMAND", "AMBERHOME"),
        conda=(
            "python=3.11", "ambertools=23.6", "gromacs=2025.4", "mpi4py=4.0.1",
            "numpy=1.26.4", "pandas=1.5.3", "matplotlib=3.7.3",
            "seaborn=0.11.2", "scipy=1.14.1", "parmed=4.3.1",
        ),
        pip=("gmx_MMPBSA==1.6.5",),
        install_notes="Isolated in .envs/gmx-mmpbsa because gmx_MMPBSA 1.6.5 requires Python 3.11 and AmberTools 23.6, incompatible with the shared Python 3.12/AmberTools 26 runtime.",
        required_methods={
            "calculate_end_state_binding_free_energy": ("receptor_group_index", "ligand_group_index"),
            "calculate_end_state_energy_decomposition": ("receptor_group_index", "ligand_group_index"),
        },
        required_settings={
            "calculate_end_state_binding_free_energy": ("overwrite",),
            "calculate_end_state_energy_decomposition": ("overwrite", "maximum_decomposition_records"),
            "summarize_end_state_free_energy_results": ("maximum_decomposition_records",),
        },
        supported_system_types={
            "calculate_end_state_binding_free_energy": ("molecular_complex",),
            "calculate_end_state_energy_decomposition": ("molecular_complex",),
            "summarize_end_state_free_energy_results": ("end_state_free_energy_output",),
        },
        validation_levels={
            "calculate_end_state_binding_free_energy": "real_smoke",
            "calculate_end_state_energy_decomposition": "real_smoke",
            "summarize_end_state_free_energy_results": "real_smoke",
        },
    ),
    _backend(
        "lammps", "LAMMPS", "lammps", ("minimize_system_energy", "propagate_dynamics"),
        "LAMMPS execution from typed ParameterizedSystem artifacts and explicit segment settings.",
        modules=("lammps",), executables=("lmp",), environment=("CHEMGRAPH_LAMMPS_COMMAND",), conda=("lammps",),
        required_settings={
            "minimize_system_energy": ("energy_tolerance", "force_tolerance", "max_iterations"),
            "propagate_dynamics": ("ensemble", "temperature_kelvin", "timestep_fs", "steps", "report_interval"),
        },
    ),
    _backend(
        "hoomd", "HOOMD-blue", "free_energy",
        (
            "minimize_system_energy", "propagate_dynamics",
            "calculate_force_field_energy", "calculate_force_field_forces",
        ),
        "HOOMD-blue typed particle simulations with explicit device, reduced-unit force field, integration method, and segment controls.",
        modules=("hoomd", "numpy"), conda=("hoomd=7.1.0", "numpy"),
        method_schema={
            "device": "cpu or gpu; no automatic device selection",
            "unit_system": "explicit unit label, currently reduced_lj",
            "pair_potential": "currently lj",
            "pair_parameters": "type-pair mapping to epsilon, sigma, and r_cut",
            "bond_potential/bond_parameters": "optional harmonic typed bond parameters",
        },
        required_methods={
            action: ("device", "unit_system", "pair_potential", "pair_parameters", "neighbor_buffer")
            for action in (
                "minimize_system_energy", "propagate_dynamics",
                "calculate_force_field_energy", "calculate_force_field_forces",
            )
        },
        required_settings={
            "minimize_system_energy": (
                "integration_timestep", "force_tolerance", "energy_tolerance", "max_iterations",
            ),
            "propagate_dynamics": (
                "ensemble", "temperature_energy", "timestep", "steps",
                "report_interval", "random_seed", "initialize_velocities",
            ),
        },
    ),
    _backend(
        "namd", "NAMD 3", "namd", ("minimize_system_energy", "propagate_dynamics"),
        "NAMD 3.0.2 execution of exactly one minimization or dynamics segment from an explicitly supplied CHARMM-format system.",
        executables=("namd3",), environment=("CHEMGRAPH_NAMD_COMMAND",),
        license_class="academic_registration",
        install_notes=(
            "The AVX-512 multicore and CUDA bundles are cached under .software_cache/installations/namd/3.0.2. "
            "The public backend selects the validated CPU AVX-512 binary only; CUDA is never chosen implicitly."
        ),
        method_schema={
            "force_field_family": "currently the literal charmm",
            "exclude/one_four_scaling": "explicit NAMD nonbonded exclusions and 1-4 scaling",
            "cutoff_angstrom/switch_distance_angstrom/pairlist_distance_angstrom": "explicit nonbonded distances",
            "switching/pme": "explicit booleans; PME requires periodic cell metadata",
            "rigid_bonds": "NAMD rigidBonds choice such as none, water, or all",
            "system": "namd_psf_path, coordinate_path or namd_binary_coordinates_path, and namd_parameter_paths",
        },
        required_methods={
            action: (
                "force_field_family", "exclude", "one_four_scaling", "cutoff_angstrom",
                "switching", "switch_distance_angstrom", "pairlist_distance_angstrom", "pme", "rigid_bonds",
            )
            for action in ("minimize_system_energy", "propagate_dynamics")
        },
        required_settings={
            "minimize_system_energy": ("max_iterations", "report_interval"),
            "propagate_dynamics": (
                "ensemble", "temperature_kelvin", "timestep_fs", "steps", "report_interval", "random_seed",
            ),
        },
    ),
    _backend(
        "amber_pmemd", "Amber 26 PMEMD", "amber", ("minimize_system_energy", "propagate_dynamics"),
        "Amber 26 PMEMD CPU serial or Agent-sized MPI execution of one typed minimization/dynamics segment.",
        executables=("pmemd", "pmemd.MPI", "mpirun"),
        environment=(
            "CHEMGRAPH_AMBER_COMMAND", "CHEMGRAPH_AMBER_MPI_COMMAND",
            "CHEMGRAPH_AMBER_MPIRUN_COMMAND", "CHEMGRAPH_AMBER_MPI_EXECUTABLE",
        ),
        license_class="academic_registration",
        install_notes=(
            "Licensed PMEMD26 CPU serial and MPI binaries are built under .software_cache/installations/amber/26. "
            "AmberTools 26 remains independently available in the OpenFF runtime."
        ),
        method_schema={
            "boundary": "vacuum, implicit, or periodic",
            "cutoff_angstrom": "explicit nonbonded cutoff",
            "constraints": "none, h_bonds, or all_bonds",
            "igb/saltcon_molar": "explicit implicit-solvent model and optional salt concentration",
            "system": "amber_topology_path/prmtop_path plus amber_coordinate_path/coordinate_path",
        },
        required_methods={
            action: ("boundary", "cutoff_angstrom", "constraints")
            for action in ("minimize_system_energy", "propagate_dynamics")
        },
        required_settings={
            "minimize_system_energy": (
                "max_iterations", "steepest_descent_steps",
                "gradient_tolerance_kcal_mol_angstrom", "report_interval",
            ),
            "propagate_dynamics": (
                "ensemble", "temperature_kelvin", "timestep_fs", "steps",
                "report_interval", "random_seed", "restart",
            ),
        },
    ),
    _backend(
        "charmm", "CHARMM c50b2", "charmm", ("minimize_system_energy", "propagate_dynamics"),
        "CHARMM c50b2 execution of one typed minimization or NVE/NVT dynamics segment from a pre-parameterized PSF/coordinate system.",
        executables=("charmm",), environment=("CHEMGRAPH_CHARMM_COMMAND",),
        license_class="academic_registration",
        install_notes=(
            "The operator-provided CHARMM c50b2 source is compiled as a serial/OpenMP GNU build under "
            ".software_cache/installations/charmm/50b2; arbitrary CHARMM input scripts are not accepted."
        ),
        method_schema={
            "force_field_family": "the literal charmm",
            "coordinate_format": "card or pdb",
            "flexible_parameters": "explicit boolean selecting CHARMM flexible parameter parsing",
            "electrostatics/electrostatic_switch/dielectric": "explicit CHARMM nonbonded electrostatics",
            "vdw_switch/cutoff_angstrom/switch_on_angstrom/pairlist_distance_angstrom": "explicit van der Waals switching distances",
            "constraints": "none or h_bonds",
            "nonbond_update_interval": "explicit CHARMM INBFRQ value for dynamics",
            "system": "charmm_topology_paths, charmm_parameter_paths, charmm_psf_path, and charmm_coordinate_path",
        },
        required_methods={
            "minimize_system_energy": (
                "force_field_family", "coordinate_format", "flexible_parameters", "electrostatics", "electrostatic_switch",
                "dielectric", "vdw_switch", "cutoff_angstrom", "switch_on_angstrom",
                "pairlist_distance_angstrom", "constraints",
            ),
            "propagate_dynamics": (
                "force_field_family", "coordinate_format", "flexible_parameters", "electrostatics", "electrostatic_switch",
                "dielectric", "vdw_switch", "cutoff_angstrom", "switch_on_angstrom",
                "pairlist_distance_angstrom", "constraints", "nonbond_update_interval",
            ),
        },
        required_settings={
            "minimize_system_energy": (
                "algorithm", "max_iterations", "gradient_tolerance_kcal_mol_angstrom", "report_interval",
            ),
            "propagate_dynamics": (
                "ensemble", "temperature_kelvin", "timestep_fs", "steps",
                "report_interval", "random_seed", "restart",
            ),
        },
    ),
    _backend(
        "mdanalysis", "MDAnalysis", "md",
        (
            "calculate_trajectory_rmsd", "calculate_radius_of_gyration",
            "calculate_radial_distribution", "calculate_mean_squared_displacement",
            "calculate_dihedral_distribution", "calculate_hydrogen_bonds",
            "calculate_principal_components", "calculate_dynamic_cross_correlation",
        ),
        "Trajectory analysis with explicit atom selections and analysis parameters.", modules=("MDAnalysis",), pip=("MDAnalysis",),
        required_settings={
            "calculate_trajectory_rmsd": ("selection",),
            "calculate_radius_of_gyration": ("selection",),
            "calculate_radial_distribution": ("selection_a", "selection_b", "range_angstrom", "bins"),
            "calculate_mean_squared_displacement": ("selection", "dimensions"),
            "calculate_dihedral_distribution": ("periodic",),
            "calculate_hydrogen_bonds": (
                "donor_selection", "hydrogen_selection", "acceptor_selection",
                "donor_hydrogen_cutoff_angstrom", "donor_acceptor_cutoff_angstrom",
                "angle_cutoff_degrees", "update_selections", "start_frame",
                "stop_frame", "frame_stride", "max_events",
            ),
            "calculate_principal_components": (
                "selection", "align", "n_components", "start_frame",
                "stop_frame", "frame_stride", "include_eigenvectors", "max_atoms",
            ),
            "calculate_dynamic_cross_correlation": (
                "selection", "align", "alignment_selection", "reference_frame",
                "start_frame", "stop_frame", "frame_stride", "max_atoms",
            ),
        },
    ),
    _backend(
        "mdtraj", "MDTraj", "workflows",
        (
            "calculate_trajectory_rmsd", "calculate_radius_of_gyration",
            "calculate_contacts", "calculate_solvent_accessible_surface",
            "calculate_dihedral_distribution", "assign_secondary_structure",
            "cluster_trajectory",
        ),
        "Trajectory I/O and explicit geometric analyses using atom/residue indices supplied by the Agent.",
        modules=("mdtraj", "numpy"), conda=("mdtraj", "numpy"),
        required_settings={
            "calculate_trajectory_rmsd": ("atom_indices", "reference_frame"),
            "calculate_radius_of_gyration": ("atom_indices",),
            "calculate_contacts": ("scheme", "periodic", "soft_min"),
            "calculate_solvent_accessible_surface": ("mode", "probe_radius_nm", "sphere_points"),
            "calculate_dihedral_distribution": ("periodic",),
            "assign_secondary_structure": ("simplified",),
            "cluster_trajectory": (
                "atom_indices", "frame_stride", "rmsd_cutoff_angstrom", "max_clusters",
            ),
        },
    ),
    _backend(
        "plumed", "PLUMED", "md", ("evaluate_collective_variables",),
        "PLUMED driver evaluation of supplied collective-variable definitions; optional action_settings box_angstrom, timestep_ps, and trajectory_stride provide explicit metadata when the trajectory does not contain it.",
        executables=("plumed",),
        environment=("CHEMGRAPH_PLUMED_COMMAND",), conda=("plumed",),
    ),
    _backend(
        "pymbar", "PyMBAR", "free_energy",
        (
            "estimate_free_energy_difference", "estimate_thermodynamic_expectations",
            "calculate_potential_of_mean_force", "analyze_free_energy_convergence",
        ),
        "Multistate Bennett estimation, observable reweighting, and explicit-prefix convergence analysis from supplied reduced potentials; no simulation or state selection is hidden.",
        modules=("pymbar", "numpy"), conda=("pymbar", "numpy"),
        required_settings={
            "estimate_free_energy_difference": (
                "uncertainty_method", "maximum_iterations", "relative_tolerance",
            ),
            "estimate_thermodynamic_expectations": (
                "output", "observable_unit", "maximum_iterations", "relative_tolerance",
            ),
            "calculate_potential_of_mean_force": (
                "bin_edges", "reference", "uncertainty_method",
                "maximum_iterations", "relative_tolerance",
            ),
            "analyze_free_energy_convergence": (
                "fractions", "state_pair", "uncertainty_method",
                "maximum_iterations", "relative_tolerance",
            ),
        },
    ),
    _backend(
        "alchemlyb", "alchemlyb", "free_energy", ("parse_alchemical_energy_data",),
        "Engine-aware parsing and normalization of alchemical energy outputs without choosing an estimator or discarding samples implicitly.",
        modules=("alchemlyb", "pandas", "numpy"), conda=("alchemlyb=2.5.0", "pandas", "numpy"),
        required_settings={
            "parse_alchemical_energy_data": (
                "engine", "observable", "temperature_kelvin", "filter_invalid_rows",
            ),
        },
    ),
    _backend(
        "yambo", "Yambo", "yambo",
        ("calculate_quasiparticle_corrections", "calculate_bse_optical_spectrum"),
        "Yambo 5.3 execution and bounded parsing for explicit GW quasiparticle and BSE optical calculations from existing compatible databases.",
        executables=("yambo",),
        environment=("CHEMGRAPH_YAMBO_COMMAND",),
        conda=("yambo=5.3.0",),
        required_settings={
            "calculate_quasiparticle_corrections": (
                "job_name", "maximum_returned_records", "require_normal_exit",
            ),
            "calculate_bse_optical_spectrum": (
                "job_name", "maximum_returned_records", "require_normal_exit",
            ),
        },
        supported_system_types={
            "calculate_quasiparticle_corrections": ("periodic_crystal",),
            "calculate_bse_optical_spectrum": ("periodic_crystal",),
        },
        validation_levels={
            "calculate_quasiparticle_corrections": "real_smoke",
            "calculate_bse_optical_spectrum": "real_smoke",
        },
    ),
    _backend(
        "sharc", "SHARC", "sharc",
        ("propagate_nonadiabatic_trajectory",),
        "SHARC trajectory propagation from complete Agent-supplied dynamics and QM-interface inputs with final-time and state-history validation.",
        executables=("sharc.x",),
        environment=("CHEMGRAPH_SHARC_COMMAND", "SHARC", "PYTHONPATH"),
        required_methods={"propagate_nonadiabatic_trajectory": ("interface",)},
        required_settings={
            "propagate_nonadiabatic_trajectory": (
                "input_filename", "expected_final_time_fs", "final_time_tolerance_fs",
                "maximum_returned_steps",
            ),
        },
        allowed_methods={
            "propagate_nonadiabatic_trajectory": {
                "interface": ("lvc", "orca", "openmolcas", "analytical", "other"),
            },
        },
        validation_levels={"propagate_nonadiabatic_trajectory": "real_ensemble_smoke"},
    ),
    _backend(
        "kinbot", "KinBot", "kinbot",
        ("explore_reaction_network",),
        "KinBot 2.2.2 full-PES orchestration from one explicit JSON protocol, including patched local asynchronous execution and current ASE/NWChem compatibility.",
        modules=("kinbot", "sella"), executables=("pes",),
        environment=("CHEMGRAPH_KINBOT_PES_COMMAND", "CHEMGRAPH_NWCHEM_COMMAND"),
        pip=("kinbot=2.2.2", "sella=2.5.0"),
        install_notes="Apply chemistry_toolbox/patches/kinbot-v2.2.2-local-nwchem.patch to official tag 2.2.2 before installation.",
        required_settings={
            "explore_reaction_network": (
                "maximum_returned_reactions", "require_pes_done",
                "sella_force_threshold_ev_per_angstrom", "sella_max_steps",
                "imaginary_frequency_threshold_cm1",
            ),
        },
        validation_levels={"explore_reaction_network": "real_pes_smoke"},
    ),
    _backend(
        "airss", "AIRSS", "airss",
        ("generate_crystal_structure_candidates", "convert_crystal_structure_format"),
        "AIRSS 0.9.3 random crystal generation and explicit cabal format conversion without hidden relaxation or ranking.",
        executables=("buildcell", "cabal"),
        environment=("CHEMGRAPH_AIRSS_BUILDCELL_COMMAND", "CHEMGRAPH_AIRSS_CABAL_COMMAND"),
        conda=("airss-with-default-names=0.9.3",),
        required_settings={
            "generate_crystal_structure_candidates": ("candidate_count",),
            "convert_crystal_structure_format": ("input_format", "output_format"),
        },
        allowed_settings={
            "convert_crystal_structure_format": {
                "input_format": ("cell", "res", "shx", "cif", "xtl", "xyz"),
                "output_format": ("cell", "res", "shx", "cif", "xtl", "xyz"),
            },
        },
        supported_system_types={
            "generate_crystal_structure_candidates": ("periodic_crystal",),
            "convert_crystal_structure_format": ("periodic_crystal",),
        },
        validation_levels={
            "generate_crystal_structure_candidates": "real_smoke",
            "convert_crystal_structure_format": "real_smoke",
        },
    ),
    _backend(
        "tdep", "TDEP", "tdep",
        (
            "fit_effective_force_constants",
            "generate_thermal_displacement_configurations",
            "calculate_temperature_dependent_phonon_dispersion",
        ),
        "TDEP 25.03 effective-force-constant fitting, canonical thermal configuration sampling, and phonon dispersion from explicit native model files.",
        executables=(
            "extract_forceconstants", "canonical_configuration",
            "phonon_dispersion_relations",
        ),
        environment=(
            "CHEMGRAPH_TDEP_EXTRACT_FORCECONSTANTS_COMMAND",
            "CHEMGRAPH_TDEP_CANONICAL_CONFIGURATION_COMMAND",
            "CHEMGRAPH_TDEP_PHONON_DISPERSION_COMMAND",
        ),
        install_notes="Official tag 25.03 compiled with MPICH and gfortran at -O0; the upstream extract_forceconstants test segfaults with this toolchain at -O2.",
        required_settings={
            "fit_effective_force_constants": (
                "second_order_cutoff_angstrom", "third_order_cutoff_angstrom",
                "fourth_order_cutoff_angstrom", "polar", "configuration_stride",
                "include_first_order", "self_consistent_temperature_kelvin",
                "enforce_rotational_invariance", "enforce_huang_invariance",
                "enforce_hermitian_symmetry",
            ),
            "generate_thermal_displacement_configurations": (
                "temperature_kelvin", "configuration_count", "statistics",
                "output_format", "initialization_source",
                "debye_temperature_kelvin", "maximum_frequency_thz",
                "minimum_distance_ratio",
            ),
            "calculate_temperature_dependent_phonon_dispersion": (
                "frequency_unit", "points_per_segment", "calculate_gruneisen",
            ),
        },
        allowed_settings={
            "generate_thermal_displacement_configurations": {
                "statistics": ("classical", "quantum"),
                "output_format": ("vasp", "abinit", "fhi_aims", "siesta"),
                "initialization_source": (
                    "force_constants", "debye_temperature", "maximum_frequency",
                ),
            },
            "calculate_temperature_dependent_phonon_dispersion": {
                "frequency_unit": ("thz", "mev", "icm"),
            },
        },
        supported_system_types={
            "fit_effective_force_constants": ("periodic_crystal",),
            "generate_thermal_displacement_configurations": ("periodic_crystal",),
            "calculate_temperature_dependent_phonon_dispersion": ("periodic_crystal",),
        },
        validation_levels={
            "fit_effective_force_constants": "real_smoke",
            "generate_thermal_displacement_configurations": "real_smoke",
            "calculate_temperature_dependent_phonon_dispersion": "real_smoke",
        },
    ),
    _backend(
        "quantum_espresso", "Quantum ESPRESSO", "qe",
        ("calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress", "relax_periodic_structure"),
        "Quantum ESPRESSO pw.x periodic calculations rendered from typed structures/settings.",
        executables=("pw.x",), environment=("CHEMGRAPH_QE_COMMAND",), conda=("qe",),
        data_resources=(
            "Explicit ResourceRefs from qe_sssp_1_3_pbe_efficiency or qe_sssp_1_3_pbe_precision, one per element; workspace ArtifactRefs remain accepted",
        ),
        method_schema={
            "pseudopotentials": "element -> resource://<SSSP resource id>/<Element> or workspace ArtifactRef",
            "input_dft": "explicit Quantum ESPRESSO XC identifier compatible with the selected resources",
            "ecutwfc_ry": "explicit wavefunction cutoff in Ry; SSSP per-element recommendations are exposed in the resource catalog",
            "ecutrho_ry": "optional explicit charge-density cutoff in Ry",
            "k_points": "{grid:[nx,ny,nz], shift:[sx,sy,sz]}",
        },
        required_methods={action: ("input_dft", "pseudopotentials", "ecutwfc_ry", "k_points") for action in ("calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress", "relax_periodic_structure")},
        required_settings=_PERIODIC_RELAX,
    ),
    _backend(
        "cp2k", "CP2K", "cp2k",
        ("calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress", "relax_periodic_structure"),
        "CP2K periodic calculations rendered from typed structures/settings.", executables=("cp2k",),
        environment=("CHEMGRAPH_CP2K_COMMAND",), conda=("cp2k",),
        required_methods={action: ("method", "basis_set", "potential", "cutoff_ry", "k_points", "scf_algorithm") for action in ("calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress", "relax_periodic_structure")},
        required_settings=_PERIODIC_RELAX,
    ),
    _backend(
        "siesta", "SIESTA", "periodic",
        ("calculate_periodic_energy", "calculate_periodic_forces", "relax_periodic_structure"),
        "SIESTA calculations rendered from typed structures/settings.", executables=("siesta",),
        environment=("CHEMGRAPH_SIESTA_COMMAND",), conda=("siesta",),
        data_resources=(
            "Explicit ResourceRefs from siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml, one per element; workspace ArtifactRefs remain accepted",
        ),
        method_schema={
            "pseudopotentials": "element -> resource://siesta_pseudo_dojo_nc_sr_05_pbe_standard_psml/<Element>",
            "xc_functional": "explicit SIESTA XC family compatible with selected PSML files",
            "xc_authors": "explicit SIESTA XC parametrization",
            "basis_size": "explicit PAO basis size",
            "mesh_cutoff_ry": "explicit real-space mesh cutoff in Ry",
            "k_points": "{grid:[nx,ny,nz], shift:[sx,sy,sz]}",
        },
        required_methods={action: ("xc_functional", "xc_authors", "pseudopotentials", "basis_size", "mesh_cutoff_ry", "k_points") for action in ("calculate_periodic_energy", "calculate_periodic_forces", "relax_periodic_structure")},
        required_settings=_PERIODIC_RELAX,
    ),
    _backend(
        "dftbplus", "DFTB+", "periodic",
        ("calculate_periodic_energy", "calculate_periodic_forces", "relax_periodic_structure"),
        "DFTB+ calculations rendered from typed structures/settings.", executables=("dftb+",),
        environment=("CHEMGRAPH_DFTBPLUS_COMMAND",), conda=("dftbplus",),
        data_resources=(
            "Explicit ResourceRef to dftb_3ob_3_1 or dftb_matsci_0_3 with all required directed element-pair SKF files; workspace directory ArtifactRefs remain accepted",
        ),
        method_schema={
            "parameter_set": "resource://dftb_3ob_3_1 or resource://dftb_matsci_0_3",
            "k_points": "{grid:[nx,ny,nz], shift:[sx,sy,sz]}",
            "scc": "explicit boolean selecting SCC or non-SCC DFTB",
            "max_angular_momenta": "element -> s|p|d|f, explicitly selected for the parameter family",
            "third_order_full": "optional explicit DFTB3 full third-order toggle",
            "hubbard_derivatives": "optional element -> atomic Hubbard derivative mapping",
            "damp_xh_exponent": "optional explicit gamma^h damping exponent (3ob commonly documents 4.0)",
            "fermi_temperature_kelvin": "optional explicit electronic filling temperature",
        },
        required_methods={action: ("parameter_set", "k_points", "scc", "max_angular_momenta") for action in ("calculate_periodic_energy", "calculate_periodic_forces", "relax_periodic_structure")},
        required_settings=_DFTB_SETTINGS,
    ),
    _backend(
        "abinit", "ABINIT", "abinit",
        ("calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress", "relax_periodic_structure"),
        "ABINIT calculations rendered from typed structures/settings.",
        modules=("numpy", "pydantic", "yaml"), executables=("abinit",),
        environment=("CHEMGRAPH_ABINIT_COMMAND",), conda=("abinit",),
        data_resources=(
            "Explicit ResourceRefs from abinit_pseudo_dojo_nc_sr_pbe_standard_psp8, one per element; workspace ArtifactRefs remain accepted",
        ),
        method_schema={
            "pseudopotentials": "element -> resource://abinit_pseudo_dojo_nc_sr_pbe_standard_psp8/<Element>",
            "ixc": "explicit ABINIT XC code compatible with the selected PSP8 files",
            "ecut_hartree": "explicit plane-wave cutoff in Hartree",
            "k_points": "{grid:[nx,ny,nz], shift:[sx,sy,sz]}",
        },
        required_methods={action: ("ixc", "pseudopotentials", "ecut_hartree", "k_points") for action in ("calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress", "relax_periodic_structure")},
        required_settings=_PERIODIC_RELAX,
    ),
    _backend(
        "vasp", "VASP", "vasp",
        (
            "calculate_periodic_energy", "calculate_periodic_forces",
            "calculate_periodic_stress", "relax_periodic_structure",
        ),
        "Locally licensed VASP 6.3.2 periodic calculations with explicit POTCAR ResourceRefs, INCAR controls, k-point mesh, and convergence settings.",
        executables=("vasp_std",), environment=("CHEMGRAPH_VASP_COMMAND",),
        license_class="commercial_license",
        data_resources=(
            "One explicit POTCAR ResourceRef or workspace ArtifactRef per element; five operator-supplied production families expose exact directory-name variants and no family or variant is selected automatically",
        ),
        install_notes=(
            "VASP 6.3.2 was built locally from the operator-provided source. "
            "The operator-supplied local POTCAR archive is registered as five explicit variant collections; treat it as licensed, non-redistributable data."
        ),
        method_schema={
            "pseudopotentials": "element -> resource://<VASP family id>/<exact variant directory> or workspace ArtifactRef",
            "encut_ev": "explicit plane-wave cutoff in eV",
            "k_points": "{grid:[nx,ny,nz], shift:[sx,sy,sz]}",
            "kpoint_scheme": "gamma or monkhorst-pack",
            "precision": "explicit VASP PREC value",
            "algorithm": "explicit VASP ALGO value",
            "ismear": "explicit integer ISMEAR",
            "sigma_ev": "explicit SIGMA in eV",
            "spin_polarized": "explicit boolean selecting ISPIN=1/2",
            "real_space_projection": "explicit LREAL boolean or Auto",
            "xc_family": "lda, pbe, pbesol, scan, or r2scan",
            "initial_magnetic_moments": "optional one value per atom",
            "electron_count": "optional explicit NELECT",
            "additional_incar": "optional explicit extra INCAR mapping; relaxation-semantic keys are protected",
        },
        required_methods={
            action: (
                "pseudopotentials", "encut_ev", "k_points", "kpoint_scheme",
                "precision", "algorithm", "ismear", "sigma_ev",
                "spin_polarized", "real_space_projection", "xc_family",
            )
            for action in (
                "calculate_periodic_energy", "calculate_periodic_forces",
                "calculate_periodic_stress", "relax_periodic_structure",
            )
        },
        required_settings=_VASP_SETTINGS,
    ),
    _backend(
        "phonopy", "Phonopy", "phonons",
        (
            "generate_displaced_supercells", "assemble_force_constants",
            "calculate_phonon_dispersion", "calculate_phonon_density_of_states",
            "calculate_harmonic_thermodynamics", "calculate_phonon_group_velocities",
        ),
        "Second-order lattice-dynamics operations on explicit displacement/force artifacts.", modules=("phonopy",),
        executables=("phonopy",), conda=("phonopy",),
        required_settings={
            "generate_displaced_supercells": ("supercell_matrix", "displacement_distance_angstrom"),
            "calculate_phonon_dispersion": ("q_path",),
            "calculate_phonon_density_of_states": ("q_mesh",),
            "calculate_harmonic_thermodynamics": ("q_mesh", "temperatures_kelvin"),
            "calculate_phonon_group_velocities": ("q_path",),
        },
    ),
    _backend(
        "phono3py", "Phono3py", "phonons",
        (
            "generate_displaced_supercells", "assemble_force_constants",
            "calculate_phonon_dispersion", "calculate_phonon_density_of_states",
            "calculate_harmonic_thermodynamics", "calculate_phonon_group_velocities",
            "calculate_lattice_thermal_conductivity",
        ),
        "Third-order-capable lattice-dynamics operations on explicit displacement/force artifacts.", modules=("phono3py",),
        executables=("phono3py",), conda=("phono3py",),
        required_inputs={
            "calculate_lattice_thermal_conductivity": (
                "second_order_force_constants", "third_order_force_constants", "structure",
            ),
        },
        required_settings={
            "generate_displaced_supercells": ("supercell_matrix", "displacement_distance_angstrom", "order"),
            "calculate_phonon_dispersion": ("q_path",),
            "calculate_phonon_density_of_states": ("q_mesh",),
            "calculate_harmonic_thermodynamics": ("q_mesh", "temperatures_kelvin"),
            "calculate_phonon_group_velocities": ("q_path",),
            "calculate_lattice_thermal_conductivity": (
                "q_mesh", "temperatures_kelvin", "solution_method",
                "include_isotope_scattering", "boundary_mean_free_path_micrometer",
                "primitive_matrix",
            ),
        },
    ),
    _backend(
        "shengbte", "ShengBTE", "shengbte", ("calculate_lattice_thermal_conductivity",),
        "ShengBTE source revision b0d2090 solution of an explicitly supplied native phonon-BTE model, with structured RTA or iterative conductivity-tensor extraction.",
        executables=("ShengBTE",), environment=("CHEMGRAPH_SHENGBTE_COMMAND",),
        install_notes="Locally compiled official ShengBTE source; the bundled Test-RTA calculation passed.",
        required_inputs={
            "calculate_lattice_thermal_conductivity": (
                "control_file", "second_order_force_constants_file",
                "third_order_force_constants_file",
            ),
        },
        required_settings={
            "calculate_lattice_thermal_conductivity": (
                "solution_method", "maximum_temperature_records", "require_normal_exit",
            ),
        },
        supported_system_types={
            "calculate_lattice_thermal_conductivity": ("periodic_crystal",),
        },
        validation_levels={"calculate_lattice_thermal_conductivity": "real_smoke"},
    ),
    _backend(
        "vina", "AutoDock Vina", "docking", ("dock_ligand",),
        "AutoDock Vina docking using prepared structures and an explicit search box.", modules=("vina",),
        executables=("vina",), environment=("CHEMGRAPH_VINA_COMMAND",), conda=("vina",),
        required_settings={"dock_ligand": ("exhaustiveness", "num_modes", "energy_range_kcal_mol")},
    ),
    _backend(
        "gnina", "GNINA", "docking", ("dock_ligand",),
        "GNINA docking using prepared structures and an explicit search box/model.", executables=("gnina",),
        environment=("CHEMGRAPH_GNINA_COMMAND",),
        install_notes="Configured from registered GNINA 1.3.3 CUDA 12.8 binary; rerun chemistry_toolbox/scripts/configure_toolbox_resources.py to verify/relink.",
        method_schema={
            "cnn_model": "builtin_default or an explicit GNINA built-in --cnn model name",
            "cnn_scoring": "optional GNINA mode: none|rescore|refinement|metrorescore|metrorefine|all",
            "scoring_function": "optional explicit empirical scoring function",
        },
        required_methods={"dock_ligand": ("cnn_model",)},
        required_settings={"dock_ligand": ("exhaustiveness", "num_modes", "use_gpu")},
    ),
    _backend(
        "pubchem", "PubChem PUG REST", "services",
        (
            "search_compounds", "resolve_chemical_identity",
            "retrieve_compound_properties", "retrieve_compound_structure", "search_similar_compounds",
            "search_substructures",
        ),
        "PubChem compound lookup through PubChemPy/PUG REST.", modules=("pubchempy",), pip=("pubchempy==1.0.5",),
        required_settings={
            "resolve_chemical_identity": ("require_unique",),
            "retrieve_compound_properties": ("properties", "max_records"),
            "retrieve_compound_structure": (
                "record_type", "hydrogen_policy", "max_records", "require_unique",
            ),
            "search_similar_compounds": ("threshold", "max_records"),
            "search_substructures": ("max_records", "match_stereo"),
        },
        install_notes=(
            "Live PUG REST access uses cross-worker rate limiting and bounded retries. Optional mechanical "
            "controls are max_retries, retry_backoff_seconds, minimum_request_interval_seconds, "
            "max_poll_attempts, and poll_interval_seconds. Request timeout is evaluator-controlled. "
            "Existing proxy variables take priority; "
            "otherwise PubChem loads proxy-only values from the ignored config.local.env file. No alternate data "
            "source is selected implicitly."
        ),
    ),
    _backend(
        "rcsb_pdb", "RCSB PDB Data API", "services", ("search_protein_structures",),
        "RCSB PDB entry/search APIs.", modules=("httpx",), pip=("httpx>=0.28",),
    ),
    _backend(
        "materials_project", "Materials Project", "services", ("search_materials",),
        "Materials Project summary REST API requiring an MP_API_KEY for live access; bounded transient-failure retries protect against temporary service or network interruptions.", modules=("httpx", "mp_api"),
        environment=("MP_API_KEY",), conda=("mp-api",),
    ),
    _backend(
        "catalysis_hub", "Catalysis-Hub GraphQL", "services", ("search_catalysis_records",),
        "Authenticated Catalysis-Hub GraphQL reaction lookup.", modules=("httpx",), pip=("httpx>=0.28",),
        environment=("CATALYSIS_HUB_API_KEY",),
        install_notes=(
            "Live GraphQL calls send CATALYSIS_HUB_API_KEY through X-API-Key and use bounded "
            "retry/backoff controls (max_retries, retry_backoff_seconds) "
            "and return retryable remote-service errors without hidden fallback."
        ),
    ),
    _backend(
        "nist_webbook", "NIST Chemistry WebBook SRD 69 CGI", "services",
        ("lookup_nist_webbook_species",),
        "Bounded single-species lookup through the official parameterized WebBook CGI; this is not represented as a REST/JSON API and does not perform bulk crawling.",
        modules=("httpx",), pip=("httpx>=0.28",),
        data_resources=(
            "NIST Chemistry WebBook SRD 69 official CGI and its SRD copyright/licensing terms",
        ),
        license_class="nist_srd_terms",
        install_notes=(
            "No local dataset is mirrored. Name/formula wildcards and responses over 2 MiB "
            "are rejected; formula isotope/ion choices remain explicit Agent settings."
        ),
        required_settings={"lookup_nist_webbook_species": ("units",)},
    ),
)
