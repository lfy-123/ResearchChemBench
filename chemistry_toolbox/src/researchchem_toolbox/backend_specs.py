"""Static BackendSpec declarations for all executable providers."""

from __future__ import annotations

from .models import BackendSpec


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
        "openbabel", "Open Babel", "quantum", ("generate_3d_structure",),
        "Open Babel 3D coordinate generation.", modules=("openbabel",), executables=("obabel",),
        conda=("openbabel",),
        required_methods={"generate_3d_structure": ("force_field",)},
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
            "analyze_reaction_coordinate",
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
        data_resources=("GPAW PAW setup datasets under .software_cache/gpaw/setups",),
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
        data_resources=("NWChem basis libraries under .software_cache/nwchem/source/src/basis/libraries",),
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
        data_resources=("OpenMolcas v25.10 basis_library managed under .software_cache/openmolcas/25.10",),
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
        ("calculate_atomic_charges", "calculate_bond_orders"),
        "Multiwfn 2026.7.15 noGUI wavefunction post-processing for explicit Mulliken/Lowdin atomic charges and Mayer/Wiberg-Lowdin/Mulliken bond-order definitions.",
        executables=("Multiwfn_noGUI",), environment=("CHEMGRAPH_MULTIWFN_COMMAND",),
        license_class="custom_open_source_citation_required",
        data_resources=(
            "Agent-supplied fch/fchk/wfn/wfx/mwfn/Molden/47 wavefunction file; both required Multiwfn citations are returned in provenance",
        ),
        install_notes=(
            "Official 2026.7.15 Linux noGUI binary is managed under .software_cache/multiwfn; "
            "the adapter uses fixed version-specific menu sequences and accepts no arbitrary menu script."
        ),
        method_schema={
            "population_analysis": "mulliken or lowdin",
            "bond_order_definition": "mayer, wiberg_lowdin, or mulliken",
        },
        required_methods={
            "calculate_atomic_charges": ("population_analysis",),
            "calculate_bond_orders": ("bond_order_definition",),
        },
        required_settings={"calculate_bond_orders": ("minimum_bond_order",)},
        supported_system_types={
            "calculate_atomic_charges": ("molecular_wavefunction",),
            "calculate_bond_orders": ("molecular_wavefunction",),
        },
        validation_levels={
            "calculate_atomic_charges": "real_smoke",
            "calculate_bond_orders": "real_smoke",
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
            ".software_cache/critic2/install-conda. The adapter exposes typed AUTO/CPREPORT "
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
        ),
        (
            "Operator-provided ORCA 6.1.1 electronic-structure executable with an isolated "
            "OpenMPI 4.1.8 runtime. The Agent explicitly selects method, basis, solvation, "
            "and resources. This server's validated execution contract permits up to 48 "
            "CPU cores and 7200 seconds per synchronous ORCA Action. Longer ORCA "
            "calculations remain available through the Agent-selected asynchronous native layer."
        ),
        executables=("orca",), environment=("CHEMGRAPH_ORCA_COMMAND",),
        license_class="manual_license",
        install_notes=(
            "Configured from the operator-downloaded ORCA 6.1.1 installer under "
            ".software_cache/orca/6.1.1 with the exact OpenMPI 4.1.8 runtime required by this "
            "ORCA build. Parallel Actions retain the Agent-selected PAL process count without "
            "automatic fallback or resource substitution. Use inspect_software plus "
            "submit_native_job for explicitly authored jobs beyond the synchronous limits."
        ),
        resource_constraints={
            "maximum_cpu_cores": 48,
            "maximum_walltime_seconds": 7200,
            "reason": (
                "The current 64-online-CPU server reserves capacity for the service and exposes "
                "at most 48 ORCA MPI processes per synchronous Action."
            ),
            "walltime_reason": (
                "execute_action is synchronous and must finish comfortably inside the MCP client "
                "timeout. Long ORCA jobs must be submitted explicitly through the asynchronous "
                "software-native layer so their state can be polled without blocking discovery "
                "or other Action calls."
            ),
        },
        method_schema={
            "method": "ORCA method/functional keyword",
            "basis": "ORCA basis-set keyword",
            "dispersion": "optional ORCA dispersion keyword",
            "solvation_model": "optional cpcm or smd implicit-solvation model",
            "solvent": "required solvent name when solvation_model is supplied",
            "charge": "optional explicit molecular charge",
            "multiplicity": "optional explicit spin multiplicity",
        },
        required_methods={
            action: ("method", "basis") for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
                "calculate_dipole_moment", "calculate_orbitals", "calculate_bond_orders",
            )
        } | {
            "calculate_atomic_charges": ("method", "basis", "population_analysis"),
            "calculate_excited_states": ("method", "basis", "excited_state_method"),
        },
        required_settings={
            "optimize_geometry": ("optimization_convergence", "max_steps"),
            "calculate_bond_orders": ("minimum_bond_order",),
            "calculate_excited_states": (
                "number_of_states", "spin_symmetry",
                "excited_energy_tolerance_hartree", "residual_tolerance",
            ),
        },
        allowed_methods={
            action: {"solvation_model": ("cpcm", "smd")}
            for action in (
                "calculate_energy", "calculate_forces", "calculate_hessian",
                "optimize_geometry", "calculate_dipole_moment",
                "calculate_atomic_charges", "calculate_orbitals",
                "calculate_bond_orders", "calculate_excited_states",
            )
        },
        allowed_settings={
            "optimize_geometry": {
                "optimization_convergence": ("Loose", "Normal", "Tight", "VeryTight")
            }
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
            ".software_cache/gaussian/g16; the adapter accepts no arbitrary route deck."
        ),
        resource_constraints={
            "maximum_cpu_cores": 48,
            "maximum_walltime_seconds": 1800,
            "reason": (
                "The current 64-online-CPU server reserves capacity for the service and "
                "exposes at most 48 Gaussian shared-memory cores per synchronous Action."
            ),
            "walltime_reason": (
                "execute_action is synchronous and shares the MCP service event loop. "
                "Gaussian calculations expected to exceed 1800 seconds must be submitted "
                "through inspect_software plus submit_native_job so they can be polled "
                "without blocking discovery and unrelated tool calls."
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
            "The registered source distribution is compiled under .software_cache/gamess/2024-r2-p1 "
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
            "v4.3.0 source and examples are cached under .software_cache/goodvibes/4.3.0/source."
        ),
        method_schema={
            "single_point_correction_suffix": (
                "optional explicit GoodVibes --spc suffix; matching FILE_SUFFIX output files "
                "must already exist beside each frequency output"
            ),
            "custom_file_extensions": (
                "optional list of additional accepted extensions such as .qfi or .gaussian"
            ),
            "exclude_pattern": "optional explicit filename glob excluded by GoodVibes",
            "free_space_solvent": (
                "optional GoodVibes free-space solvent correction name; supported names are "
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
            "maximum_walltime_seconds": 7200,
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
        "catmap", "CatMAP", "reaction", ("solve_microkinetic_model",),
        "CatMAP 0.3.x microkinetic solver through an allow-listed typed model adapter that generates a controlled setup file and returns structured descriptor maps.",
        modules=("catmap",),
        pip=("git+https://github.com/SUNCAT-Center/catmap.git",),
        required_settings={"solve_microkinetic_model": ("temperature_kelvin", "pressure_bar")},
        supported_system_types={"solve_microkinetic_model": ("heterogeneous_catalytic_network",)},
        validation_levels={"solve_microkinetic_model": "real_smoke"},
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
        "lammps", "LAMMPS", "md", ("minimize_system_energy", "propagate_dynamics"),
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
            "The AVX-512 multicore and CUDA bundles are cached under .software_cache/namd/3.0.2. "
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
            "Licensed PMEMD26 CPU serial and MPI binaries are built under .software_cache/amber/26. "
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
            ".software_cache/charmm/50b2; arbitrary CHARMM input scripts are not accepted."
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
            "timeout_seconds, max_poll_attempts, and poll_interval_seconds. Existing proxy variables take priority; "
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
        "Materials Project summary REST API requiring an MP_API_KEY for live access; bounded HTTP timeouts avoid unbounded client initialization.", modules=("httpx", "mp_api"),
        environment=("MP_API_KEY",), conda=("mp-api",),
    ),
    _backend(
        "catalysis_hub", "Catalysis-Hub GraphQL", "services", ("search_catalysis_records",),
        "Catalysis-Hub GraphQL reaction lookup.", modules=("httpx",), pip=("httpx>=0.28",),
        install_notes=(
            "Live GraphQL calls use bounded retry/backoff controls (max_retries, retry_backoff_seconds) "
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
