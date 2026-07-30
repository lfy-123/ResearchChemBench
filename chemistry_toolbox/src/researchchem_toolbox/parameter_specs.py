"""Agent-visible parameter metadata for Action/backend contracts.

The execution adapters intentionally accept extensible ``method_spec`` and
``action_settings`` mappings.  Every scientifically or numerically meaningful
optional value implemented by a backend must be registered here so it is
discoverable instead of surviving as a hidden implementation default.
"""

from __future__ import annotations

from typing import Any, Mapping


ParameterMetadata = Mapping[str, Any]


ORCA_DENSITY_DEFAULT_MAXCORE_MB = 2000


RESOURCE_LIMIT_PARAMETER_SPECS: dict[str, ParameterMetadata] = {
    "memory_mb": {
        "description": "Requested memory budget in megabytes when the backend supports it.",
        "default": 4096,
        "type": "integer",
        "minimum": 128,
        "impact": (
            "More memory may enable larger calculations, while excessive per-process memory "
            "combined with many CPU processes can exceed the task budget. The evaluator rejects "
            "single or concurrent requests above the declared per-task maximum."
        ),
    },
    "cpu_cores": {
        "description": "Requested CPU process/thread count for the selected backend.",
        "default": 1,
        "type": "integer",
        "minimum": 1,
        "impact": (
            "More cores may reduce elapsed time, but scaling is backend- and system-dependent "
            "and may increase total memory use. The evaluator rejects single or concurrent "
            "requests above the declared per-task maximum."
        ),
    },
    "gpu_count": {
        "description": "Requested GPU count for a backend that supports GPU execution.",
        "default": 0,
        "type": "integer",
        "minimum": 0,
        "impact": (
            "A positive value requests accelerator resources but does not change the selected "
            "scientific method. Zero disables GPU visibility for managed execution."
        ),
    },
}


BACKEND_PARAMETER_SPECS: dict[
    str, dict[str, dict[str, ParameterMetadata]]
] = {
    "orca": {
        "export_electron_density_grid": {
            "action_settings.grid_points_per_axis": {
                "description": (
                    "Number of ORCA cube grid points along each Cartesian axis when "
                    "exporting an MDCI/CCSD density."
                ),
                "default": 300,
                "type": "integer",
                "minimum": 20,
                "maximum": 400,
                "impact": (
                    "Larger values reduce density discretization and isosurface-area error "
                    "but increase time, memory, and cube size approximately with the cube "
                    "of this value. Fixed point counts also give coarser voxels for larger "
                    "molecular boxes, so quantitative work should verify convergence."
                ),
            },
            "action_settings.electron_count_tolerance_percent": {
                "description": (
                    "Maximum allowed relative difference between the integrated cube "
                    "density and the source density's expected electron count."
                ),
                "default": 0.2,
                "type": "number",
                "minimum": 0.001,
                "maximum": 10.0,
                "impact": (
                    "A smaller tolerance rejects or warns about more discretization loss; "
                    "a larger tolerance accepts coarser cubes but may allow isosurface-area "
                    "bias large enough to change close method rankings."
                ),
            },
            "action_settings.strict_electron_count_validation": {
                "description": (
                    "Whether an electron-count error above the selected tolerance makes "
                    "the cube export fail instead of returning it with a warning."
                ),
                "default": False,
                "type": "boolean",
                "impact": (
                    "Enabling strict validation prevents downstream use of a demonstrably "
                    "under-resolved cube. Disabling it preserves exploratory workflows but "
                    "requires the Agent to treat the warning as numerical uncertainty."
                ),
            },
        },
    },
    "multiwfn": {
        "calculate_electron_isodensity_surface": {
            "action_settings.grid_spacing_bohr": {
                "description": (
                    "Real-space spacing, in bohr, used by Multiwfn when constructing the "
                    "electron-isodensity surface grid."
                ),
                "type": "number",
                "minimum": 0.02,
                "maximum": 1.0,
                "impact": (
                    "A smaller spacing produces a finer surface grid and usually reduces "
                    "discretization error, but increases runtime and memory use. Quantitative "
                    "surface comparisons should verify convergence with at least one finer value."
                ),
            },
            "action_settings.grid_spacing_angstrom": {
                "description": (
                    "Deprecated compatibility alias for grid_spacing_bohr. Despite its historical "
                    "name, its numeric value is interpreted in bohr so existing calls preserve "
                    "their original numerical behavior. Omit it in new requests."
                ),
                "default": None,
                "type": "number | null",
                "minimum": 0.02,
                "maximum": 1.0,
                "deprecated": True,
                "replacement": "action_settings.grid_spacing_bohr",
                "impact": (
                    "When supplied alone, it selects exactly the same bohr spacing as the canonical "
                    "field and emits a deprecation warning. Supplying both fields is rejected."
                ),
            },
        },
    },
}


BACKEND_FIXED_PARAMETER_SPECS: dict[
    str, dict[str, dict[str, ParameterMetadata]]
] = {
    "orca": {
        "export_electron_density_grid": {
            "backend_runtime.cube_boundary_selection": {
                "description": (
                    "ORCA orca_plot determines the density-cube bounding box from the "
                    "calculated molecular density and its internal padding policy."
                ),
                "reason": (
                    "The installed interactive orca_plot adapter currently exposes grid "
                    "resolution but not an independently typed bounding-box override."
                ),
            },
            "backend_runtime.cube_export_parallelism": {
                "description": (
                    "The installed ORCA orca_plot MDCI cube exporter runs as one process; "
                    "resource_limits.cpu_cores does not parallelize this export stage."
                ),
                "reason": (
                    "orca_plot does not expose a validated parallel cube-export control. "
                    "Use sufficient walltime, and parallelize independent molecule exports "
                    "as separate jobs when server capacity permits."
                ),
            },
        },
    },
}


_MISSING = object()


def _register_parameter(
    backend_id: str,
    action_ids: str | tuple[str, ...],
    field_path: str,
    *,
    description: str,
    impact: str,
    default: Any = _MISSING,
    **constraints: Any,
) -> None:
    actions = (action_ids,) if isinstance(action_ids, str) else action_ids
    for action_id in actions:
        metadata: dict[str, Any] = {
            "description": description,
            "impact": impact,
            **constraints,
        }
        if default is not _MISSING:
            metadata["default"] = default
        BACKEND_PARAMETER_SPECS.setdefault(backend_id, {}).setdefault(
            action_id, {}
        )[field_path] = metadata


def _register_fixed(
    backend_id: str,
    action_ids: str | tuple[str, ...],
    field_path: str,
    *,
    description: str,
    reason: str,
) -> None:
    actions = (action_ids,) if isinstance(action_ids, str) else action_ids
    for action_id in actions:
        BACKEND_FIXED_PARAMETER_SPECS.setdefault(backend_id, {}).setdefault(
            action_id, {}
        )[field_path] = {"description": description, "reason": reason}


# RDKit cheminformatics optional controls.
for _action_id in ("calculate_molecular_fingerprint", "calculate_molecular_similarity"):
    _register_parameter(
        "rdkit", _action_id, "action_settings.radius",
        description="Morgan/ECFP neighborhood radius in bonds.", default=2,
        type="integer", minimum=0,
        impact="A larger radius encodes a wider chemical environment and can change similarity while increasing fingerprint construction cost.",
    )
    _register_parameter(
        "rdkit", _action_id, "action_settings.n_bits",
        description="Bit-vector length for Morgan or RDKit fingerprints.", default=2048,
        type="integer", minimum=64, maximum=65536,
        impact="More bits reduce hash collisions and increase memory/output size; MACCS uses its fixed key length instead.",
    )
    _register_parameter(
        "rdkit", _action_id, "action_settings.use_chirality",
        description="Whether fingerprint construction distinguishes stereochemical environments.", default=True,
        type="boolean",
        impact="Enabling chirality can distinguish stereoisomers; disabling it makes fingerprints invariant to encoded stereochemistry.",
    )
    _register_parameter(
        "rdkit", _action_id, "action_settings.include_hydrogens",
        description="Whether the RDKit topological fingerprint includes explicit hydrogen paths.", default=True,
        type="boolean",
        impact="This only affects the RDKit/topological fingerprint branch and can change the set of activated bits.",
    )

_register_parameter(
    "rdkit", "calculate_molecular_descriptors", "action_settings.descriptor_names",
    description="Explicit RDKit descriptor names to calculate.",
    default=["MolWt", "ExactMolWt", "MolLogP", "TPSA", "NumHDonors", "NumHAcceptors", "NumRotatableBonds", "RingCount", "FractionCSP3", "HeavyAtomCount"],
    type="array[string]", maximum_items=256,
    impact="Selecting more descriptors increases output breadth and modestly increases calculation time; values not requested are not computed.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.max_matches", 1000, "Maximum number of local substructure matches returned.", "A larger bound can reveal more matches but increases matching time and output size."),
    ("action_settings.unique", True, "Whether symmetry-equivalent local substructure matches are deduplicated.", "Disabling uniqueness can return repeated symmetry-equivalent atom mappings."),
    ("action_settings.use_chirality", True, "Whether local substructure matching enforces query stereochemistry.", "Enabling chirality makes stereochemical labels part of the match criterion."),
):
    _register_parameter(
        "rdkit", "search_local_substructures", _field_path,
        description=_description, default=_default, impact=_impact,
        type="boolean" if isinstance(_default, bool) else "integer",
    )
_register_parameter(
    "rdkit", "enumerate_stereoisomers", "action_settings.try_embedding",
    description="Whether RDKit attempts a 3D embedding while enumerating stereoisomers.",
    default=False, type="boolean",
    impact="Enabling embedding can filter or validate stereoisomers geometrically but adds stochastic geometry-generation cost.",
)


# Network/data-source retry controls remain Agent-selectable. Timeouts are fixed
# by the evaluation policy and are intentionally absent from this public catalog.
_PUBCHEM_ACTIONS = (
    "search_compounds", "resolve_chemical_identity", "retrieve_compound_properties",
    "retrieve_compound_structure", "search_similar_compounds", "search_substructures",
)
for _field_path, _default, _description, _impact, _extra in (
    ("action_settings.max_retries", 1, "Maximum retry count for a transient PubChem request failure.", "More retries improve resilience but increase worst-case latency and duplicate remote requests.", {"type": "integer", "minimum": 0}),
    ("action_settings.retry_backoff_seconds", 1.0, "Initial delay between PubChem retry attempts.", "Longer backoff reduces pressure on a failing service but increases latency.", {"type": "number", "minimum": 0}),
    ("action_settings.minimum_request_interval_seconds", 0.25, "Cross-worker minimum interval between PubChem HTTP requests.", "A longer interval reduces rate-limit risk but lowers throughput.", {"type": "number", "minimum": 0}),
    ("action_settings.max_poll_attempts", 15, "Maximum PubChem asynchronous-search polling attempts.", "More attempts allow longer remote searches but increase worst-case elapsed time.", {"type": "integer", "minimum": 1}),
    ("action_settings.poll_interval_seconds", 2.0, "Delay between PubChem asynchronous-search polls.", "Longer intervals reduce polling traffic but delay result collection.", {"type": "number", "minimum": 0}),
):
    _register_parameter("pubchem", _PUBCHEM_ACTIONS, _field_path, description=_description, default=_default, impact=_impact, **_extra)
_register_parameter(
    "pubchem", "search_compounds", "action_settings.namespace",
    description="PubChem identifier namespace used to interpret the query.", default="name",
    type="string", allowed_values=["name", "cid", "smiles", "inchi", "inchikey"],
    impact="Changing the namespace changes how the same query text is resolved.",
)
_register_parameter(
    "pubchem", "search_compounds", "action_settings.max_records",
    description="Maximum PubChem compound records returned.", default=10,
    type="integer", minimum=1,
    impact="A larger limit returns more candidates and increases network and output cost.",
)
_register_parameter(
    "pubchem", "resolve_chemical_identity", "action_settings.max_records",
    description="Maximum candidate identities considered before uniqueness checks.", default=10,
    type="integer", minimum=1,
    impact="A larger limit can expose ambiguous matches but increases response processing.",
)
for _backend_id, _action_id, _default_records in (
    ("rcsb_pdb", "search_protein_structures", 10),
    ("materials_project", "search_materials", 20),
    ("catalysis_hub", "search_catalysis_records", 20),
    ("nist_webbook", "lookup_nist_webbook_species", 10),
):
    _register_parameter(
        _backend_id, _action_id, "action_settings.max_records",
        description="Maximum number of remote records returned.", default=_default_records,
        type="integer", minimum=1,
        impact="A larger limit broadens the returned result set and increases network and output size.",
    )
_register_parameter(
    "materials_project", "search_materials", "action_settings.fields",
    description="Explicit Materials Project summary fields requested from the API.",
    default=["material_id", "formula_pretty", "energy_above_hull", "band_gap", "is_stable", "symmetry", "volume", "density"],
    type="array[string]",
    impact="Requesting more fields increases response size and may require permissions for additional API fields.",
)


# Docking backend-specific optional controls.
for _field_path, _description, _impact in (
    ("method_spec.cnn_scoring", "Optional GNINA CNN scoring mode.", "Changing the mode changes whether and when CNN rescoring/refinement is applied."),
    ("method_spec.scoring_function", "Optional explicit GNINA empirical scoring function.", "Changing the scoring function changes pose ranking and reported affinities."),
    ("action_settings.gpu_device", "GPU device identifier used when GNINA use_gpu is true.", "Selecting a different device changes resource placement but not the requested scientific model."),
    ("action_settings.cpu", "GNINA CPU worker count passed to the executable.", "More CPU workers may reduce runtime but increase host contention."),
    ("action_settings.seed", "GNINA stochastic search seed.", "Changing the seed changes stochastic docking trajectories; a fixed seed improves reproducibility."),
):
    _register_parameter("gnina", "dock_ligand", _field_path, description=_description, default=None, impact=_impact)


# Structure and system-construction hidden defaults.
_register_parameter(
    "pymatgen", "enumerate_surface_slabs", "action_settings.symmetrize",
    description="Whether pymatgen attempts to symmetrize generated slab terminations.", default=False,
    type="boolean", impact="Enabling symmetrization can reduce asymmetric artifacts but may alter terminations or reject slabs.",
)
_register_parameter(
    "rdkit", "generate_3d_structure", "action_settings.max_attempts",
    description="Maximum RDKit embedding attempts.", default=1000, type="integer", minimum=1,
    impact="More attempts improve the chance of embedding difficult molecules but increase runtime.",
)
_register_parameter(
    "rdkit_etkdg", "generate_conformer_ensemble", "action_settings.prune_rms_threshold_angstrom",
    description="RMSD threshold used to prune newly generated conformers; a negative value disables pruning.", default=-1.0,
    type="number", impact="Larger positive thresholds retain fewer, more geometrically distinct conformers and reduce downstream cost.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.ionic_strength_molar", 0.0, "Target ionic strength for OpenMM solvation.", "Increasing ionic strength adds counterions/salt and changes the simulated chemical environment."),
    ("action_settings.positive_ion", "Na+", "Positive ion species used by OpenMM solvation.", "Changing the ion changes system composition and force-field requirements."),
    ("action_settings.negative_ion", "Cl-", "Negative ion species used by OpenMM solvation.", "Changing the ion changes system composition and force-field requirements."),
):
    _register_parameter("openmm_builder", "solvate_molecular_system", _field_path, description=_description, default=_default, impact=_impact)
_register_parameter(
    "packmol", "solvate_molecular_system", "action_settings.tolerance_angstrom",
    description="Minimum Packmol interatomic placement tolerance.", default=2.0, type="number", minimum=0,
    impact="A larger tolerance reduces close contacts but makes packing harder and may require a larger box.",
)


# Molecular-dynamics execution and trajectory-analysis optional controls.
_OPENMM_ACTIONS = (
    "minimize_system_energy", "propagate_dynamics", "calculate_force_field_energy",
    "calculate_force_field_forces", "decompose_force_field_energy",
)
for _field_path, _description, _impact in (
    ("method_spec.platform", "Optional explicit OpenMM compute platform name.", "Selecting CPU, CUDA, OpenCL, or another installed platform changes resource placement and may change floating-point reproducibility."),
    ("method_spec.platform_properties", "Optional OpenMM platform-property mapping.", "Properties such as precision or device index change accelerator behavior, performance, and sometimes numerical reproducibility."),
):
    _register_parameter("openmm", _OPENMM_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
for _field_path, _default, _description, _impact, _extra in (
    ("action_settings.friction_per_ps", 1.0, "Langevin collision/friction coefficient for OpenMM NVT/NPT propagation.", "Larger friction produces stronger thermostat coupling and can alter dynamical properties.", {"type": "number", "minimum": 0}),
    ("action_settings.initialize_velocities", True, "Whether OpenMM initializes velocities when no saved state is supplied.", "Disabling initialization requires usable velocities from the supplied state; enabling it samples a Maxwell distribution.", {"type": "boolean"}),
    ("action_settings.random_seed", 0, "Seed used for OpenMM velocity initialization.", "Changing the seed changes initial velocities and the resulting trajectory.", {"type": "integer"}),
    ("action_settings.pressure_bar", None, "Target pressure for OpenMM NPT propagation.", "Changing pressure changes the sampled NPT ensemble; it is ignored outside NPT.", {"type": "number"}),
):
    _register_parameter("openmm", "propagate_dynamics", _field_path, description=_description, default=_default, impact=_impact, **_extra)

_GROMACS_ACTIONS = ("minimize_system_energy", "propagate_dynamics")
_register_parameter(
    "gromacs", _GROMACS_ACTIONS, "method_spec.cutoff_scheme",
    description="GROMACS neighbor-search and nonbonded cutoff scheme.", default="Verlet",
    type="string", impact="Changing the cutoff scheme changes neighbor-list behavior and compatibility with other nonbonded settings.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.continuation", False, "Whether GROMACS dynamics continues from an existing state.", "Continuation changes initialization and thermostat/barostat handling and should match the supplied checkpoint."),
    ("action_settings.temperature_coupling_ps", 1.0, "Thermostat coupling time constant in ps.", "Smaller values couple temperature more strongly and can distort physical dynamics."),
    ("action_settings.pressure_coupling_ps", 5.0, "Barostat coupling time constant in ps.", "Smaller values couple pressure more strongly and can cause unstable volume fluctuations."),
    ("action_settings.compressibility_bar_inverse", 4.5e-5, "Isothermal compressibility used by the GROMACS barostat.", "Changing compressibility changes the volume response to pressure coupling."),
    ("action_settings.pressure_bar", None, "Target pressure required for GROMACS NPT propagation.", "Changing it changes the sampled NPT thermodynamic state."),
    ("action_settings.random_seed", None, "Explicit GROMACS velocity-generation seed required when generate_velocities=true.", "Changing it changes initial velocities and the resulting trajectory."),
    ("action_settings.temperature_coupling_groups", None, "Explicit GROMACS index groups coupled to the thermostat.", "Changing group definitions changes which atoms share thermostat baths and can materially alter dynamics."),
):
    _register_parameter("gromacs", "propagate_dynamics", _field_path, description=_description, default=_default, type="boolean" if isinstance(_default, bool) else "number", impact=_impact)

_LAMMPS_ACTIONS = ("minimize_system_energy", "propagate_dynamics")
for _field_path, _default, _description, _impact in (
    ("method_spec.units", "real", "LAMMPS unit system.", "Changing units changes the interpretation of every numeric force-field and dynamics parameter."),
    ("method_spec.atom_style", "full", "LAMMPS atom style used to read the data file.", "Changing atom style changes required per-atom fields and must match the supplied data file."),
    ("method_spec.neighbor_skin", 2.0, "LAMMPS neighbor-list skin distance in the selected unit system.", "A larger skin reduces rebuild frequency but increases neighbor-list size and memory."),
):
    _register_parameter("lammps", _LAMMPS_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)
_register_parameter(
    "lammps", "minimize_system_energy", "action_settings.max_evaluations",
    description="Maximum LAMMPS force/energy evaluations during minimization.",
    default="10 * max_iterations", type="integer",
    impact="A larger bound may allow difficult minimizations to converge but increases worst-case cost.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.temperature_damping_fs", 100.0, "LAMMPS thermostat damping time in fs.", "Smaller damping couples temperature more strongly and can perturb dynamics."),
    ("action_settings.pressure_damping_fs", 1000.0, "LAMMPS barostat damping time in fs.", "Smaller damping couples pressure more strongly and can destabilize cell fluctuations."),
):
    _register_parameter("lammps", "propagate_dynamics", _field_path, description=_description, default=_default, type="number", minimum=0, impact=_impact)

_HOOMD_ACTIONS = (
    "minimize_system_energy", "propagate_dynamics", "calculate_force_field_energy",
    "calculate_force_field_forces",
)
for _field_path, _default, _description, _impact in (
    ("method_spec.bond_potential", "harmonic", "Optional HOOMD bond-potential family when bonds are present.", "Changing the potential changes bonded energetics and requires compatible parameters."),
    ("method_spec.bond_parameters", None, "Typed HOOMD bond-parameter mapping.", "Changing parameters changes bonded forces and energies; it is required when bonded interactions are present."),
):
    _register_parameter("hoomd", _HOOMD_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)
for _action_id in ("minimize_system_energy", "calculate_force_field_energy", "calculate_force_field_forces"):
    _register_parameter(
        "hoomd", _action_id, "action_settings.random_seed",
        description="HOOMD simulation seed used by stochastic components.", default=0,
        type="integer", impact="Changing the seed changes stochastic state where applicable; fixed seeds improve reproducibility.",
    )
_register_parameter(
    "hoomd", "minimize_system_energy", "action_settings.angular_momentum_tolerance",
    description="FIRE angular-momentum convergence tolerance; defaults to force_tolerance.",
    default="force_tolerance", type="number",
    impact="A smaller tolerance imposes stricter rotational convergence and can increase iterations.",
)
_register_parameter(
    "hoomd", "minimize_system_energy", "action_settings.steps_per_check",
    description="Number of HOOMD FIRE integration steps between convergence checks.", default=10,
    type="integer", minimum=1,
    impact="Larger values reduce checking overhead but can overshoot the earliest converged step.",
)
_register_parameter(
    "hoomd", "propagate_dynamics", "action_settings.thermostat_tau",
    description="HOOMD thermostat coupling time in reduced time units.", default=1.0,
    type="number", minimum=0,
    impact="Smaller values produce stronger temperature coupling and may alter dynamics.",
)

_MDANALYSIS_FRAME_ACTIONS = (
    "calculate_trajectory_rmsd", "calculate_radius_of_gyration",
    "calculate_radial_distribution", "calculate_mean_squared_displacement",
    "calculate_dihedral_distribution",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.start_frame", 0, "First zero-based trajectory frame included.", "Increasing it discards more initial trajectory frames."),
    ("action_settings.stop_frame", -1, "Exclusive final trajectory frame; -1 selects the trajectory end.", "Changing it changes the analyzed time window."),
    ("action_settings.frame_stride", 1, "Trajectory frame stride.", "A larger stride reduces cost and temporal resolution."),
):
    _register_parameter("mdanalysis", _MDANALYSIS_FRAME_ACTIONS, _field_path, description=_description, default=_default, type="integer", impact=_impact)
_register_parameter(
    "mdanalysis", "calculate_trajectory_rmsd", "inputs.reference",
    description="Optional separate reference structure or trajectory for RMSD alignment.", default=None,
    impact="Supplying a different reference changes the absolute RMSD values and alignment target.",
)
_register_parameter(
    "mdanalysis", "calculate_mean_squared_displacement", "action_settings.fft",
    description="Whether MDAnalysis uses its FFT-accelerated MSD implementation.", default=True,
    type="boolean", impact="FFT mode is faster for long trajectories but imposes the backend's FFT algorithm assumptions.",
)
_register_parameter(
    "mdanalysis", "calculate_hydrogen_bonds", "inputs.between_selections",
    description="Optional selection-pair restrictions for hydrogen-bond analysis.", default=None,
    impact="Supplying pairs restricts reported hydrogen bonds to the named groups.",
)
_register_parameter(
    "mdtraj", "calculate_trajectory_rmsd", "inputs.reference",
    description="Optional separate MDTraj reference trajectory.", default=None,
    impact="Changing the reference changes RMSD alignment and values.",
)
_register_parameter(
    "mdtraj", "calculate_contacts", "action_settings.soft_min_beta",
    description="Inverse softness parameter for MDTraj soft-min contact distances.", default=20.0,
    type="number", minimum=0,
    impact="Larger beta approaches a hard minimum; smaller beta averages more atom-pair distances. It is used only when soft_min is enabled.",
)

for _field_path, _default, _description, _impact in (
    ("action_settings.stride", 1, "PLUMED PRINT stride in evaluated driver frames.", "A larger stride writes fewer collective-variable samples."),
    ("action_settings.box_angstrom", None, "Optional periodic box supplied when absent from the trajectory.", "Changing the box changes periodic-image handling of collective variables."),
    ("action_settings.timestep_ps", None, "Optional trajectory timestep metadata in ps.", "Changing it changes the reported time axis but not coordinates."),
    ("action_settings.trajectory_stride", None, "Optional stride of stored frames relative to the original simulation.", "Changing it changes the reconstructed time mapping."),
):
    _register_parameter("plumed", "evaluate_collective_variables", _field_path, description=_description, default=_default, impact=_impact)

_PYMBAR_ACTIONS = (
    "estimate_free_energy_difference", "estimate_thermodynamic_expectations",
    "calculate_potential_of_mean_force", "analyze_free_energy_convergence",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.initialize", "zeros", "PyMBAR initial free-energy estimate strategy.", "Changing initialization can affect convergence speed but should not change a converged solution."),
    ("action_settings.random_seed", 0, "Seed used by PyMBAR bootstrap sampling.", "Changing it changes bootstrap realizations and uncertainty estimates."),
):
    _register_parameter("pymbar", _PYMBAR_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)
for _action_id in ("estimate_free_energy_difference", "analyze_free_energy_convergence"):
    _register_parameter(
        "pymbar", _action_id, "action_settings.bootstrap_samples",
        description="Number of PyMBAR bootstrap replicates when bootstrap uncertainty is selected.", default=0,
        type="integer", minimum=0,
        impact="More replicates improve Monte Carlo stability of uncertainty estimates and increase cost approximately linearly.",
    )
for _action_id in ("estimate_free_energy_difference", "calculate_potential_of_mean_force", "analyze_free_energy_convergence"):
    _register_parameter(
        "pymbar", _action_id, "action_settings.temperature_kelvin",
        description="Optional temperature used to convert reduced free energies to kJ/mol.", default=None,
        type="number", minimum=0,
        impact="It changes only dimensional energy conversion when reduced potentials are already supplied.",
    )
_register_parameter(
    "pymbar", "calculate_potential_of_mean_force", "action_settings.reference_coordinate",
    description="Explicit PMF reference coordinate when reference='specified'.", default=None,
    type="number", impact="Changing the reference adds a constant offset anchored to a different occupied bin.",
)
_register_parameter(
    "pymbar", "calculate_potential_of_mean_force", "action_settings.coordinate_unit",
    description="Label describing the collective-variable coordinate unit.", default="unspecified",
    type="string", impact="This labels output coordinates and does not rescale supplied values.",
)
_register_parameter(
    "pymbar", "estimate_free_energy_difference", "action_settings.include_theta",
    description="Whether PyMBAR returns the asymptotic covariance matrix Theta.", default=False,
    type="boolean", impact="Enabling it increases output size and exposes covariance diagnostics without changing the estimate.",
)


# Molecular electronic-structure and spectrum optional controls.
_XTB_ACTIONS = (
    "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
    "calculate_dipole_moment", "calculate_atomic_charges", "calculate_bond_orders",
)
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional xTB molecular charge override; otherwise structure.charge is used.", "Changing charge changes electron count and the electronic state."),
    ("method_spec.unpaired_electrons", "Optional xTB unpaired-electron count override; otherwise multiplicity-1 is used.", "Changing it changes spin occupation and can produce a different electronic state."),
):
    _register_parameter("xtb", _XTB_ACTIONS, _field_path, description=_description, default=None, impact=_impact)

_PYSCF_ACTIONS = (
    "calculate_energy", "calculate_forces", "calculate_hessian", "calculate_dipole_moment",
    "calculate_atomic_charges", "calculate_orbitals", "calculate_excited_states",
)
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional PySCF molecular charge override; otherwise structure.charge is used.", "Changing charge changes electron count and electronic state."),
    ("method_spec.spin", "Optional PySCF 2S spin value; otherwise multiplicity-1 is used.", "Changing spin changes alpha/beta occupations and electronic state."),
    ("method_spec.functional", "PySCF DFT functional alias used for RKS/UKS methods.", "Changing it changes the density-functional approximation."),
    ("method_spec.xc", "Alternative PySCF exchange-correlation functional field.", "Changing it changes the density-functional approximation."),
):
    _register_parameter("pyscf", _PYSCF_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
_register_parameter(
    "pyscf", _PYSCF_ACTIONS, "action_settings.scf_convergence",
    description="PySCF SCF energy convergence tolerance.", default=1e-9,
    type="number", minimum=0,
    impact="A smaller value requests tighter SCF convergence and usually increases iterations and numerical reliability.",
)
_register_parameter(
    "pyscf", "calculate_atomic_charges", "method_spec.population_analysis",
    description="PySCF population-analysis definition.", default="mulliken",
    type="string", impact="Changing the population definition changes reported atomic charges without changing the wavefunction.",
)
_register_parameter(
    "pyscf", "calculate_orbitals", "action_settings.include_coefficients",
    description="Whether PySCF includes the full molecular-orbital coefficient matrix.", default=False,
    type="boolean", impact="Enabling it substantially increases output size but does not change the calculation.",
)

_NWCHEM_ACTIONS = (
    "calculate_energy", "calculate_forces", "calculate_hessian",
    "calculate_dipole_moment", "calculate_atomic_charges",
)
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional NWChem charge override; otherwise structure metadata is used.", "Changing charge changes electron count and electronic state."),
    ("method_spec.multiplicity", "Optional NWChem spin multiplicity override.", "Changing multiplicity changes spin occupation and electronic state."),
    ("method_spec.functional", "NWChem XC functional required when method=dft.", "Changing it changes the density-functional approximation."),
    ("method_spec.reference", "Optional NWChem RHF/UHF/ROHF reference.", "Changing the reference changes spin treatment and may affect convergence and results."),
):
    _register_parameter("nwchem", _NWCHEM_ACTIONS, _field_path, description=_description, default=None, impact=_impact)

_OPENMOLCAS_ACTIONS = (
    "calculate_energy", "calculate_dipole_moment", "calculate_atomic_charges",
    "calculate_orbitals",
)
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional OpenMolcas molecular charge override.", "Changing charge changes electron count and electronic state."),
    ("method_spec.multiplicity", "Optional OpenMolcas spin multiplicity override.", "Changing multiplicity changes electronic state."),
    ("method_spec.functional", "OpenMolcas/Libxc functional required for DFT.", "Changing it changes the density-functional approximation."),
):
    _register_parameter("openmolcas", _OPENMOLCAS_ACTIONS, _field_path, description=_description, default=None, impact=_impact)

_ASE_HESSIAN_BACKENDS = ("mace", "chgnet", "deepmd", "ase_emt")
for _backend_id in _ASE_HESSIAN_BACKENDS:
    # The field is required in the current public contract, but explicit metadata records
    # the implementation default used by direct backend calls and explains its effect.
    _register_parameter(
        _backend_id, "calculate_hessian", "action_settings.displacement_angstrom",
        description="Central finite-difference displacement used to construct the Hessian.", default=0.01,
        type="number", minimum=0,
        impact="Too large a displacement introduces anharmonic error; too small amplifies force noise and roundoff. Convergence should be checked for noisy potentials.",
    )
_register_parameter(
    "mace", ("calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry"),
    "method_spec.default_dtype",
    description="MACE floating-point dtype.", default="float64", type="string",
    allowed_values=["float32", "float64"],
    impact="float64 improves numerical precision at higher memory/runtime cost; float32 is faster on many accelerators.",
)
for _backend_id in ("nequip", "allegro"):
    _actions = (
        "calculate_periodic_energy", "calculate_periodic_forces",
        "calculate_periodic_stress", "relax_periodic_structure",
    )
    _register_parameter(
        _backend_id, _actions, "method_spec.neighborlist_backend",
        description="Neighbor-list implementation used by compatible MLIP inference.", default="matscipy",
        type="string", impact="Changing the implementation primarily affects compatibility and performance; equivalent implementations should preserve the model definition.",
    )
_register_parameter(
    "deepmd", (
        "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
        "calculate_periodic_energy", "calculate_periodic_forces", "calculate_periodic_stress",
        "relax_periodic_structure",
    ), "method_spec.frame_parameters",
    description="Optional additional DeePMD per-frame model parameters.", default=None,
    impact="Supplying values changes model conditioning and must match the checkpoint's expected parameter schema.",
)

_PSI4_ACTIONS = (
    "calculate_energy", "calculate_hessian", "calculate_dipole_moment",
    "calculate_atomic_charges", "calculate_orbitals",
)
_register_parameter(
    "psi4", _PSI4_ACTIONS, "method_spec.options",
    description="Optional explicit Psi4 option mapping forwarded to the selected calculation.", default=None,
    type="object", impact="Options can change convergence algorithms, integral approximations, reference states, and numerical results; they must be chosen consistently with method and basis.",
)

_ORCA_STANDARD_ACTIONS = (
    "calculate_energy", "calculate_forces", "calculate_hessian", "optimize_geometry",
    "calculate_dipole_moment", "calculate_atomic_charges", "calculate_orbitals",
    "calculate_bond_orders", "calculate_excited_states",
)
for _field_path, _description, _impact in (
    (
        "method_spec.basis",
        "Explicit ORCA orbital basis for ordinary methods; omit it or use method_default/auto for built-in 3c composite methods.",
        "Changing the orbital basis changes basis-set completeness and cost. Built-in 3c methods define their own basis and reject a concrete override.",
    ),
    ("method_spec.dispersion", "Optional ORCA dispersion-correction keyword.", "Adding or changing dispersion alters energies and gradients and can change optimized structures."),
    ("method_spec.solvation_model", "Optional ORCA implicit-solvation model.", "Enabling solvation changes the Hamiltonian/environment and resulting energies, densities, and structures."),
    ("method_spec.solvent", "Solvent name used when an ORCA solvation model is selected.", "Changing solvent changes dielectric/solvation parameters and computed properties."),
    ("method_spec.charge", "Optional ORCA molecular charge override.", "Changing charge changes electron count and electronic state."),
    ("method_spec.multiplicity", "Optional ORCA spin multiplicity override.", "Changing multiplicity changes electronic state and reference occupation."),
):
    _register_parameter("orca", _ORCA_STANDARD_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
_ORCA_DENSITY_ACTION = "calculate_correlated_electron_density"
for _field_path, _description, _impact, _extra in (
    (
        "method_spec.basis",
        "Explicit ORCA orbital basis for ordinary methods; omit it or use method_default/auto for built-in 3c composite methods.",
        "Changing the orbital basis changes density accuracy and cost. Built-in 3c methods define their own basis and reject a concrete override.",
        {},
    ),
    ("method_spec.auxiliary_basis", "Optional ORCA auxiliary/C basis for MP2 or double-hybrid density calculations.", "Changing it changes density-fitting accuracy and cost.", {}),
    ("method_spec.dispersion", "Optional ORCA dispersion-correction keyword.", "Dispersion typically changes energy and gradients; exact density influence depends on the selected ORCA method implementation.", {}),
    ("method_spec.frozen_core", "Whether correlated density calculations use the frozen-core approximation.", "Disabling frozen core correlates more electrons and increases cost; it can change correlated density.", {"type": "boolean"}),
    ("method_spec.pmodel", "Whether ORCA PModel is enabled for the density calculation.", "Changing PModel changes the double-hybrid/MP2 model details used by ORCA.", {"type": "boolean"}),
    ("method_spec.charge", "Optional molecular charge override.", "Changing charge changes electron count and density.", {"type": "integer"}),
    ("method_spec.multiplicity", "Optional spin multiplicity override.", "Changing multiplicity changes electronic state and density.", {"type": "integer", "minimum": 1}),
):
    _register_parameter(
        "orca", _ORCA_DENSITY_ACTION, _field_path,
        description=_description, default=None, impact=_impact, **_extra,
    )
_register_parameter(
    "orca", _ORCA_DENSITY_ACTION, "action_settings.stability_analysis",
    description="Whether ORCA performs an SCF wavefunction-stability analysis before the density calculation.",
    type="boolean",
    impact=(
        "Enabling it can detect and restart an unstable SCF solution at additional cost; "
        "disabling it skips that validation."
    ),
)
_register_parameter(
    "orca", _ORCA_DENSITY_ACTION, "resource_limits.memory_mb",
    description=(
        "Total memory budget in MB across all requested ORCA MPI processes. The adapter "
        "sets %maxcore to floor(memory_mb / cpu_cores), with a 128 MB floor."
    ),
    default=None,
    type="integer | null",
    minimum=128,
    default_behavior=(
        f"When null, the adapter allocates {ORCA_DENSITY_DEFAULT_MAXCORE_MB} MB per "
        "process, so total memory is that value multiplied by the effective cpu_cores."
    ),
    derived_backend_parameter={
        "name": "orca_maxcore_mb_per_process",
        "formula": "max(128, floor(memory_mb / effective_cpu_cores))",
        "null_memory_formula": (
            f"{ORCA_DENSITY_DEFAULT_MAXCORE_MB} MB per process"
        ),
    },
    impact=(
        "Increasing the total budget raises ORCA %maxcore at fixed cpu_cores and can "
        "prevent correlated-method out-of-memory failures. Increasing cpu_cores without "
        "also increasing memory_mb lowers %maxcore per process."
    ),
)

_GAUSSIAN_ACTIONS = ("calculate_energy", "calculate_hessian", "optimize_geometry", "calculate_dipole_moment")
for _field_path, _description, _impact in (
    ("method_spec.dispersion", "Optional Gaussian empirical-dispersion route keyword.", "Changing dispersion changes energy and gradients."),
    ("method_spec.solvation_model", "Optional Gaussian implicit-solvation model.", "Enabling or changing solvation changes the computed environment and properties."),
    ("method_spec.solvent", "Gaussian solvent name used by the solvation model.", "Changing solvent changes solvation parameters and results."),
    ("method_spec.charge", "Optional molecular charge override.", "Changing charge changes electron count and electronic state."),
    ("method_spec.multiplicity", "Optional spin multiplicity override.", "Changing multiplicity changes electronic state."),
):
    _register_parameter("gaussian", _GAUSSIAN_ACTIONS, _field_path, description=_description, default=None, impact=_impact)

_GAMESS_ACTIONS = ("calculate_energy", "optimize_geometry", "calculate_dipole_moment")
for _field_path, _default, _description, _impact in (
    ("method_spec.charge", None, "Optional GAMESS molecular charge override.", "Changing charge changes electron count and electronic state."),
    ("method_spec.multiplicity", None, "Optional GAMESS spin multiplicity override.", "Changing multiplicity changes electronic state."),
    ("method_spec.dfttyp", None, "Optional GAMESS DFT functional keyword.", "Supplying a DFT type changes the electronic method from pure SCF to the selected density functional."),
    ("method_spec.guess", "HUCKEL", "GAMESS initial orbital guess method.", "Changing the guess can alter SCF convergence behavior and, for difficult systems, the converged solution."),
):
    _register_parameter("gamess", _GAMESS_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)

for _field_path, _default, _description, _impact in (
    ("action_settings.min_wavenumber_cm1", "min(frequencies)-5*fwhm, clipped at 0", "Lower IR spectrum grid boundary.", "Extending the range increases output coverage and point spacing at fixed point count."),
    ("action_settings.max_wavenumber_cm1", "max(frequencies)+5*fwhm", "Upper IR spectrum grid boundary.", "Extending the range increases output coverage and point spacing at fixed point count."),
    ("action_settings.points", 4000, "Number of IR spectrum grid points.", "More points improve sampled line-shape resolution and increase output size."),
):
    _register_parameter("internal_spectroscopy", "derive_ir_spectrum", _field_path, description=_description, default=_default, impact=_impact)


# Critic2 optional search, filtering, and validation controls.
for _field_path, _default, _description, _impact in (
    ("action_settings.search_region", None, "Optional typed spatial region restricting critical-point search.", "Restricting the region reduces cost but can omit critical points outside it."),
    ("action_settings.discard_density_below", None, "Optional density threshold below which candidate critical points are discarded.", "Increasing it filters low-density features and may remove physically relevant weak-interaction critical points."),
    ("action_settings.checkpoint_critical_points", False, "Whether Critic2 checkpoints critical points during AUTO search.", "Enabling it adds restart/diagnostic output without changing intended search criteria."),
    ("action_settings.smoothrho_environment_nodes", None, "Optional Smoothrho interpolation environment-node count.", "Increasing it uses a wider interpolation environment and can improve smoothness at higher cost."),
    ("action_settings.smoothrho_distance_factor", None, "Optional Smoothrho maximum-distance factor.", "Changing it changes the interpolation neighborhood and may affect critical-point topology."),
):
    _register_parameter("critic2", "analyze_electron_density_topology", _field_path, description=_description, default=_default, impact=_impact)
_CRITIC2_BASIN_ACTIONS = ("calculate_atomic_basin_properties", "calculate_bader_charges")
for _field_path, _default, _description, _impact in (
    ("action_settings.discard_density_below", None, "Optional density threshold below which integration candidates are discarded.", "Increasing it can reduce noise and cost but may remove low-density basin contributions."),
    ("action_settings.selected_attractors", None, "Optional explicit attractor identifiers to integrate.", "Restricting attractors reduces output and omits all unselected basins."),
    ("action_settings.selected_attractor_range", None, "Optional inclusive attractor identifier range.", "Restricting the range reduces output and excludes basins outside it."),
    ("action_settings.expected_total_charge", None, "Optional expected total molecular/system charge used for a validation warning.", "It does not change integration; it enables a physical consistency check."),
    ("action_settings.total_charge_tolerance", 0.05, "Allowed absolute deviation from expected total charge.", "A smaller tolerance makes validation stricter and may flag grid or partition errors more often."),
    ("action_settings.smoothrho_environment_nodes", None, "Optional Smoothrho interpolation environment-node count.", "Increasing it uses a wider interpolation environment and can improve smoothness at higher cost."),
    ("action_settings.smoothrho_distance_factor", None, "Optional Smoothrho maximum-distance factor.", "Changing it changes the interpolation neighborhood and may affect basin boundaries."),
    ("action_settings.attractor_assignment_radius", None, "Optional YT/Bader attractor-assignment radius.", "Increasing it expands the association radius and can change basin-to-attractor assignments."),
):
    _register_parameter("critic2", _CRITIC2_BASIN_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)


# Remaining data-source, structure, and system-construction controls.
for _field_name in ("match_charges", "match_isotopes"):
    _register_parameter(
        "pubchem", "search_substructures", f"action_settings.{_field_name}",
        description=f"Whether PubChem substructure matching requires exact {_field_name.removeprefix('match_')} annotations.",
        default=False, type="boolean",
        impact="Enabling this restriction narrows matches and can exclude records lacking the requested annotation.",
    )
for _field_path, _description, _impact in (
    ("method_spec.method", "CREST Hamiltonian: GFN1-xTB, GFN2-xTB, or GFN-FF; common compact and -xTB aliases are accepted.", "Changing the Hamiltonian changes conformer energies, geometries, sampling cost, and potentially basin coverage."),
    ("method_spec.charge", "Optional CREST molecular charge override; otherwise the input structure charge is used.", "Changing charge changes electron count and the conformational potential-energy surface."),
    ("method_spec.multiplicity", "Optional CREST spin multiplicity override; otherwise the input structure multiplicity is used.", "Changing multiplicity changes the electronic state used by xTB/CREST."),
    ("method_spec.solvation_model", "Optional CREST implicit-solvation model: ALPB or GBSA.", "Adding or changing implicit solvation changes conformer stabilization and may change the sampled/ranked ensemble."),
    ("method_spec.solvent", "Solvent name passed to CREST when an implicit-solvation model is selected.", "Changing solvent changes implicit-solvation parameters and relative conformer energies."),
):
    _register_parameter("crest", "generate_conformer_ensemble", _field_path, description=_description, default=None, impact=_impact)
_register_parameter(
    "openmm_builder", "solvate_molecular_system", "method_spec.force_field",
    description="Optional OpenMM force-field XML file or list; otherwise the ParameterizedSystem force-field metadata is reused.",
    default=None, type="string | array[string]",
    impact="Changing the force field changes solvent parameters and the generated OpenMM System; it must cover every topology residue.",
)
_register_parameter(
    "crest", "generate_conformer_ensemble", "action_settings.energy_window_kcal_mol",
    description="Optional CREST conformer energy window in kcal/mol.", default=None,
    type="number", minimum=0,
    impact="Increasing it retains higher-energy conformers and increases ensemble size and downstream cost.",
)


# Licensed molecular-dynamics adapters retain task-independent advanced controls.
_register_parameter(
    "namd", ("minimize_system_energy", "propagate_dynamics"), "method_spec.margin_angstrom",
    description="NAMD patch-grid margin in angstrom.", default=1.0, type="number", minimum=0,
    impact="A larger margin can avoid patch-grid failures for moving atoms but increases spatial bookkeeping and memory.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.langevin_damping_per_ps", 1.0, "NAMD Langevin damping coefficient for NVT/NPT.", "Larger damping couples more strongly to the thermostat and can distort dynamics."),
    ("action_settings.langevin_hydrogen", False, "Whether NAMD applies Langevin forces to hydrogen atoms.", "Enabling it changes thermostat coupling of high-frequency hydrogen motion."),
    ("action_settings.piston_period_fs", 200.0, "NAMD Langevin-piston oscillation period for NPT.", "Changing it alters barostat response; overly small values can destabilize volume dynamics."),
    ("action_settings.piston_decay_fs", 100.0, "NAMD Langevin-piston decay time for NPT.", "Changing it alters damping of pressure oscillations."),
    ("action_settings.pressure_bar", None, "Target NAMD pressure required for NPT propagation.", "Changing it changes the sampled thermodynamic state; it is unused for NVE/NVT."),
):
    _register_parameter("namd", "propagate_dynamics", _field_path, description=_description, default=_default, impact=_impact)
_register_parameter(
    "amber_pmemd", ("minimize_system_energy", "propagate_dynamics"), "method_spec.saltcon_molar",
    description="Amber implicit-solvent salt concentration in mol/L.", default=0.0, type="number", minimum=0,
    impact="Increasing it changes electrostatic screening in compatible generalized-Born models.",
)
_register_parameter(
    "amber_pmemd", ("minimize_system_energy", "propagate_dynamics"), "method_spec.igb",
    description="Amber generalized-Born model identifier required when boundary=implicit.",
    default=None, type="integer", allowed_values=[1, 2, 5, 6, 7, 8, 10],
    impact="Changing IGB selects a different implicit-solvent model and can materially change energies and dynamics.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.langevin_collision_per_ps", 1.0, "Amber Langevin collision frequency for NVT/NPT.", "A larger value thermostats more strongly and changes dynamical correlations."),
    ("action_settings.pressure_relaxation_ps", 2.0, "Amber barostat pressure-relaxation time for NPT.", "A smaller value couples pressure more strongly and may destabilize volume fluctuations."),
    ("action_settings.pressure_bar", None, "Target Amber pressure required for NPT.", "Changing it changes the NPT thermodynamic state; it is unused outside NPT."),
):
    _register_parameter("amber_pmemd", "propagate_dynamics", _field_path, description=_description, default=_default, impact=_impact)
_register_parameter(
    "charmm", ("minimize_system_energy", "propagate_dynamics"), "method_spec.constraint_tolerance",
    description="CHARMM SHAKE bond-constraint tolerance.", default=1e-8, type="number", minimum=0,
    impact="A smaller tolerance enforces constraints more tightly and may require more iterations.",
)
_register_parameter(
    "charmm", "propagate_dynamics", "action_settings.temperature_coupling_ps",
    description="CHARMM NVT temperature-coupling time constant.", default=5.0, type="number", minimum=0,
    impact="A smaller value couples temperature more strongly and can perturb physical dynamics.",
)


# GoodVibes options and conditional controls are available on every GoodVibes Action.
_GOODVIBES_ACTIONS = (
    "derive_thermochemistry", "scan_thermochemistry_temperature",
    "analyze_thermochemical_ensemble", "validate_thermochemistry_inputs",
    "analyze_thermochemical_selectivity", "analyze_reaction_free_energy_profile",
)
for _field_path, _description, _impact in (
    ("method_spec.single_point_correction_suffix", "Optional GoodVibes --spc suffix for already-existing single-point files.", "Selecting a suffix replaces frequency-job electronic energies with the matching single-point energies."),
    ("method_spec.custom_file_extensions", "Optional additional quantum-output filename extensions accepted by GoodVibes.", "Adding extensions broadens input discovery but does not change parsed scientific data."),
    ("method_spec.exclude_pattern", "Optional filename glob excluded from GoodVibes analysis.", "A broader pattern removes more structures and can change ensemble/profile conclusions."),
    ("method_spec.free_space_solvent", "Optional GoodVibes free-space solvent correction name.", "Changing the solvent changes the free-volume entropy correction."),
    ("method_spec.media_solvent", "Optional GoodVibes solution-media solvent used for concentration correction.", "Changing the solvent changes the solution-phase standard-state correction applied by GoodVibes."),
):
    _register_parameter("goodvibes", _GOODVIBES_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
for _field_path, _default, _description, _impact in (
    ("action_settings.concentration_mol_l", None, "Custom standard-state concentration used when standard_state=custom_concentration.", "Changing concentration changes the translational standard-state correction."),
    ("action_settings.entropy_frequency_cutoff_cm1", None, "Frequency cutoff for Grimme or Truhlar quasi-harmonic entropy.", "Raising it applies the quasi-harmonic replacement to more low-frequency modes and changes entropy."),
    ("action_settings.free_rotor_inertia_model", None, "Free-rotor inertia model required for Grimme entropy.", "global and per_conformer use different inertia treatments and can change conformer free energies."),
    ("action_settings.enthalpy_frequency_cutoff_cm1", None, "Frequency cutoff for Head-Gordon quasi-harmonic enthalpy.", "Raising it applies the correction to more modes and changes enthalpy."),
    ("action_settings.imaginary_frequency_threshold_cm1", None, "Magnitude threshold used when inverting small imaginary frequencies.", "A larger threshold inverts a wider set of imaginary modes and can mask genuine instabilities if chosen poorly."),
):
    _register_parameter("goodvibes", _GOODVIBES_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)
for _action_id in ("analyze_thermochemical_ensemble", "analyze_thermochemical_selectivity"):
    for _field_path, _description, _impact in (
        ("action_settings.duplicate_energy_cutoff_kcal_mol", "Energy cutoff used when deduplicate_structures=true.", "Increasing it makes more structures eligible to be classified as duplicates."),
        ("action_settings.duplicate_rotational_cutoff_fraction", "Rotational-constant fractional cutoff used for duplicate detection.", "Increasing it makes duplicate classification less strict in rotational constants."),
        ("action_settings.duplicate_rmsd_cutoff_angstrom", "Optional RMSD cutoff used for duplicate detection.", "Increasing it makes geometrically less similar structures eligible as duplicates; null disables this criterion."),
    ):
        _register_parameter("goodvibes", _action_id, _field_path, description=_description, default=None, impact=_impact)


# GPAW and legacy quantum-chemistry advanced controls.
_GPAW_CALCULATION_ACTIONS = (
    "calculate_energy", "calculate_forces", "optimize_geometry",
    "calculate_periodic_energy", "calculate_periodic_forces",
    "calculate_periodic_stress", "relax_periodic_structure",
)
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional GPAW charge override; otherwise structure metadata is used.", "Changing charge changes electron count and electronic state."),
    ("method_spec.ecut_ev", "Plane-wave cutoff required when GPAW mode=pw.", "Increasing it improves plane-wave completeness at rapidly increasing FFT and memory cost; convergence testing is required."),
    ("method_spec.grid_spacing_angstrom", "Real-space grid spacing required when GPAW mode=fd.", "A smaller spacing gives a finer grid and usually better accuracy at sharply increased memory and runtime cost."),
    ("method_spec.basis", "LCAO basis required when GPAW mode=lcao.", "Changing it changes basis completeness, cost, and basis-set error."),
    ("method_spec.occupations_width_ev", "Optional Fermi-Dirac occupation smearing width in eV.", "A larger width can improve metallic SCF convergence but changes fractional occupations and free-energy interpretation."),
    ("method_spec.setups", "Optional GPAW PAW setup selection.", "Changing PAW setups changes the frozen-core/valence representation and numerical results."),
    ("method_spec.initial_magnetic_moments", "Per-atom initial magnetic moments required for spin-polarized GPAW calculations.", "Changing the initial moments can lead SCF to a different magnetic solution."),
):
    _register_parameter("gpaw", _GPAW_CALCULATION_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
for _field_name, _description, _impact, _type in (
    ("ndfunc", "Number of d polarization functions in the GAMESS basis.", "Increasing it enlarges the basis and cost and can improve polarization flexibility.", "integer"),
    ("npfunc", "Number of p polarization functions in the GAMESS basis.", "Increasing it enlarges the basis and cost and can improve polarization flexibility.", "integer"),
    ("nffunc", "Number of f polarization functions in the GAMESS basis.", "Increasing it enlarges the basis and cost and can improve polarization flexibility.", "integer"),
    ("diffsp", "Whether GAMESS adds diffuse s/p functions.", "Enabling diffuse functions is important for anions and diffuse states but increases cost and linear-dependence risk.", "boolean"),
    ("diffs", "Whether GAMESS adds diffuse s functions on hydrogens.", "Enabling it improves diffuse hydrogen basis flexibility at added cost.", "boolean"),
):
    _register_parameter("gamess", _GAMESS_ACTIONS, f"method_spec.{_field_name}", description=_description, default=None, type=_type, impact=_impact)


# Periodic electronic-structure controls.
_PERIODIC_ACTIONS = (
    "calculate_periodic_energy", "calculate_periodic_forces",
    "calculate_periodic_stress", "relax_periodic_structure",
)
for _field_path, _default, _description, _impact in (
    ("method_spec.ecutrho_ry", None, "Quantum ESPRESSO charge-density cutoff in rydberg.", "Increasing it improves density representation for demanding pseudopotentials at substantial FFT/memory cost."),
    ("method_spec.occupations", None, "Quantum ESPRESSO occupation scheme.", "Changing it changes how electronic occupations are assigned, especially for metals."),
    ("method_spec.smearing", None, "Quantum ESPRESSO smearing function.", "Changing the smearing function changes metallic occupation broadening and convergence."),
    ("method_spec.degauss_ry", 0.01, "Quantum ESPRESSO smearing width in rydberg.", "A larger width improves metallic convergence but broadens occupations and changes finite-smearing energies."),
    ("method_spec.atomic_masses", {}, "Optional element-to-mass mapping written to Quantum ESPRESSO.", "Changing masses affects ionic dynamics/phonons but not a static Born-Oppenheimer electronic energy."),
    ("action_settings.scf_convergence_ry", 1e-8, "Quantum ESPRESSO SCF energy threshold in rydberg.", "A smaller threshold tightens SCF convergence and increases iterations."),
):
    _register_parameter("quantum_espresso", _PERIODIC_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)
for _field_path, _default, _description, _impact in (
    ("action_settings.ion_dynamics", "bfgs", "Quantum ESPRESSO ionic optimizer for relaxation.", "Changing it changes the geometry-search algorithm and convergence path."),
    ("action_settings.pressure_threshold_kbar", 0.5, "Cell-pressure convergence threshold for vc-relax in kbar.", "A smaller value requires tighter cell convergence and usually more steps."),
):
    _register_parameter("quantum_espresso", "relax_periodic_structure", _field_path, description=_description, default=_default, impact=_impact)

for _field_path, _default, _description, _impact in (
    ("action_settings.scf_convergence", 1e-6, "CP2K inner-SCF convergence threshold.", "A smaller threshold tightens electronic convergence and increases iterations."),
    ("action_settings.max_scf_cycles", 100, "Maximum CP2K inner-SCF cycles.", "A larger value allows harder SCF problems to converge but increases worst-case time."),
    ("method_spec.basis_set_file", "BASIS_MOLOPT", "CP2K basis-set database filename.", "Changing it changes which named basis definitions are available and must match the installation."),
    ("method_spec.potential_file", "GTH_POTENTIALS", "CP2K pseudopotential database filename.", "Changing it changes available pseudopotential definitions and must match selected potentials."),
):
    _register_parameter("cp2k", _PERIODIC_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)
for _field_path, _default, _description, _impact in (
    ("method_spec.ot_minimizer", "DIIS", "CP2K orbital-transformation minimizer.", "Changing it alters OT convergence behavior."),
    ("method_spec.ot_preconditioner", "FULL_SINGLE_INVERSE", "CP2K OT preconditioner.", "Changing it affects convergence speed, memory, and robustness."),
    ("action_settings.outer_scf_convergence", "same as scf_convergence", "CP2K outer-SCF convergence threshold.", "A smaller threshold tightens outer-loop convergence and increases work."),
    ("action_settings.max_outer_scf_cycles", 20, "Maximum CP2K outer-SCF cycles.", "A larger value permits more recovery iterations at greater worst-case cost."),
    ("method_spec.added_mos", 20, "Additional unoccupied orbitals for CP2K diagonalization.", "More orbitals support smearing/excited occupations but increase diagonalization cost."),
    ("method_spec.electronic_temperature_kelvin", 300.0, "CP2K Fermi-Dirac electronic temperature.", "Increasing it broadens occupations and can improve metallic convergence while changing electronic free energy."),
    ("method_spec.mixing_method", "BROYDEN_MIXING", "CP2K density-mixing algorithm.", "Changing it alters SCF stability and convergence rate."),
    ("method_spec.mixing_alpha", 0.2, "CP2K density-mixing amplitude.", "Larger values update density more aggressively and may accelerate or destabilize SCF."),
):
    _register_parameter("cp2k", _PERIODIC_ACTIONS, _field_path, description=_description, default=_default, impact=_impact)

_DFTB_ACTIONS = ("calculate_periodic_energy", "calculate_periodic_forces", "relax_periodic_structure")
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional DFTB+ total charge.", "Changing charge changes electron count and electronic state."),
    ("method_spec.shell_resolved_scc", "Optional DFTB+ shell-resolved SCC switch.", "Toggling it changes the charge self-consistency model when supported by the parameter set."),
    ("method_spec.third_order_full", "Optional full third-order DFTB correction.", "Enabling it changes the Hamiltonian and requires compatible Hubbard derivatives."),
    ("method_spec.hubbard_derivatives", "Optional element-to-Hubbard-derivative mapping.", "Changing values changes third-order charge corrections and must match the parameter set."),
    ("method_spec.damp_xh_exponent", "Optional X-H damping exponent.", "Changing it alters short-range hydrogen damping in compatible DFTB parameterizations."),
    ("method_spec.fermi_temperature_kelvin", "Optional electronic Fermi temperature.", "Increasing it broadens occupations and can improve metallic SCC convergence."),
):
    _register_parameter("dftbplus", _DFTB_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
_register_parameter(
    "abinit", _PERIODIC_ACTIONS, "action_settings.scf_convergence_hartree",
    description="ABINIT SCF density-residual threshold in hartree units used by this adapter.",
    default=1e-10, type="number", minimum=0,
    impact="A smaller threshold tightens SCF convergence and typically increases iterations.",
)
for _field_path, _description, _impact in (
    ("method_spec.initial_magnetic_moments", "Optional per-atom VASP MAGMOM initialization.", "Changing initial moments can lead to different converged magnetic states."),
    ("method_spec.electron_count", "Optional VASP NELECT override.", "Changing it changes total electron count and charged-state treatment."),
    ("method_spec.additional_incar", "Optional validated additional INCAR mapping excluding Action-semantic keys.", "Additional INCAR tags can materially alter algorithms and results; the Agent is responsible for consistency."),
):
    _register_parameter("vasp", _PERIODIC_ACTIONS, _field_path, description=_description, default=None, impact=_impact)


# Phonon, thermal-transport, and periodic post-processing controls.
_PHONON_HARMONIC_ACTIONS = (
    "generate_displaced_supercells", "assemble_force_constants",
    "calculate_phonon_dispersion", "calculate_phonon_density_of_states",
    "calculate_harmonic_thermodynamics", "calculate_phonon_group_velocities",
)
for _backend_id in ("phonopy", "phono3py"):
    _register_parameter(
        _backend_id, "generate_displaced_supercells", "action_settings.primitive_matrix",
        description="Primitive-cell transformation matrix or 'auto' for phonon construction.",
        default="auto", impact="Changing it changes primitive-cell mapping, displacement symmetry, and reciprocal-space folding.",
    )
_register_parameter(
    "phono3py", "generate_displaced_supercells", "action_settings.phonon_supercell_matrix",
    description="Optional separate second-order phonon supercell matrix.", default="same as supercell_matrix",
    impact="Changing it changes the fc2 displacement cell independently of the fc3 cell and changes cost/finite-size error.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.symmetrize_fc3q", False, "Whether phono3py symmetrizes reciprocal-space third-order force constants.", "Enabling it enforces symmetry relations and can reduce numerical noise."),
    ("action_settings.mass_variances", None, "Optional isotope mass-variance parameters.", "Supplying them changes isotope-scattering rates and thermal conductivity."),
    ("action_settings.use_kappa_star", True, "Whether phono3py uses kappa-star symmetry reduction.", "Disabling it can increase cost and serves as a symmetry/convergence check."),
    ("action_settings.full_phonon_phonon_interaction", False, "Whether phono3py retains the full phonon-phonon interaction representation.", "Enabling it increases memory and cost and can change approximation details."),
    ("action_settings.include_mode_data", False, "Whether per-mode linewidth, velocity, and heat-capacity arrays are returned.", "Enabling it substantially increases output size but not the conductivity solution."),
):
    _register_parameter("phono3py", "calculate_lattice_thermal_conductivity", _field_path, description=_description, default=_default, impact=_impact)
for _backend_id in ("phonopy", "phono3py"):
    for _action_id in ("calculate_phonon_dispersion", "calculate_phonon_group_velocities"):
        _register_parameter(
            _backend_id, _action_id, "action_settings.with_eigenvectors",
            description="Whether phonon eigenvectors are calculated with the band path.", default=False, type="boolean",
            impact="Enabling it increases time/output and provides mode polarization without changing frequencies.",
        )
        _register_parameter(
            _backend_id, _action_id, "action_settings.labels",
            description="Optional labels aligned to q-path segment endpoints.", default=None,
            impact="Labels affect presentation only and do not change the phonon calculation.",
        )
    for _field_path, _default, _description, _impact in (
        ("action_settings.cutoff_frequency_thz", None, "Optional minimum frequency included in harmonic thermodynamics.", "Raising it excludes more low-frequency modes and changes thermodynamic sums."),
        ("action_settings.pretend_real", False, "Whether imaginary phonon frequencies are treated as real magnitudes.", "Enabling it can produce finite thermodynamics for unstable structures but changes physical interpretation."),
        ("action_settings.classical", False, "Whether classical rather than quantum harmonic statistics are used.", "Enabling it changes heat capacities, entropy, and free energy, especially at low temperature."),
    ):
        _register_parameter(_backend_id, "calculate_harmonic_thermodynamics", _field_path, description=_description, default=_default, impact=_impact)

for _backend_id in ("nequip", "allegro", "deepmd"):
    for _field_path, _default, _description, _impact in (
        ("action_settings.hydrostatic_strain", False, "Whether ASE cell relaxation is constrained to hydrostatic strain.", "Enabling it removes shear/deviatoric cell degrees of freedom."),
        ("action_settings.scalar_pressure_ev_per_angstrom3", 0.0, "External scalar pressure supplied to the ASE cell filter.", "Changing it changes the target enthalpy and relaxed cell volume."),
    ):
        _register_parameter(_backend_id, "relax_periodic_structure", _field_path, description=_description, default=_default, impact=_impact)
for _field_path, _description, _impact in (
    ("inputs.born_file", "Optional ShengBTE BORN file staged under its native filename.", "Supplying it enables non-analytical/Born-charge information when required by the model."),
    ("inputs.companion_files", "Optional bounded list of additional native ShengBTE input files.", "Adding files can enable model features but leaves their scientific consistency to the Agent."),
):
    _register_parameter("shengbte", "calculate_lattice_thermal_conductivity", _field_path, description=_description, default=None, impact=_impact)


# Reaction-path, kinetics, and master-equation controls.
_PYSISYPHUS_ACTIONS = (
    "locate_transition_state", "search_reaction_path",
    "scan_reaction_coordinates", "trace_intrinsic_reaction_coordinate",
)
for _field_path, _description, _impact in (
    ("method_spec.charge", "Optional reaction-path molecular charge override.", "Changing charge changes the potential-energy surface."),
    ("method_spec.multiplicity", "Optional reaction-path spin multiplicity override.", "Changing multiplicity changes the electronic-state surface."),
    ("method_spec.basis", "Basis set used by PySCF and optionally ORCA calculators.", "Changing it changes accuracy, cost, and the potential-energy surface."),
    ("method_spec.functional", "DFT functional used by the PySCF calculator.", "Changing it changes the density-functional approximation and reaction path."),
    ("method_spec.solvation_model", "Optional xTB or ORCA implicit-solvation model.", "Enabling it changes the reaction environment and energy surface."),
    ("method_spec.solvent", "Solvent name required when solvation_model is selected.", "Changing solvent changes implicit-solvation parameters and barriers."),
):
    _register_parameter("pysisyphus", _PYSISYPHUS_ACTIONS, _field_path, description=_description, default=None, impact=_impact)
for _field_path, _description, _impact in (
    ("inputs.mechanism", "Optional Cantera mechanism file/name for equilibrium calculation.", "Changing the mechanism changes available species, thermochemistry, and reactions."),
    ("action_settings.mechanism", "Legacy alternative location for the Cantera mechanism.", "Changing the mechanism changes available species, thermochemistry, and reactions."),
):
    _register_parameter("cantera", "calculate_chemical_equilibrium", _field_path, description=_description, default=None, impact=_impact)
_register_parameter(
    "cantera", "calculate_chemical_equilibrium", "action_settings.report_threshold",
    description="Minimum equilibrium mole fraction included in the result.", default=1e-12, type="number", minimum=0,
    impact="Increasing it shortens output but hides more trace species; it does not change equilibrium itself.",
)
for _field_path, _default, _description, _impact in (
    ("action_settings.integrator", "LSODA", "SciPy solve_ivp integration method.", "Changing it alters stiffness handling, stability, and cost; converged solutions should agree within tolerances."),
    ("action_settings.relative_tolerance", 1e-8, "Relative ODE integration tolerance.", "A smaller value tightens integration accuracy and increases solver work."),
    ("action_settings.absolute_tolerance", 1e-12, "Absolute ODE integration tolerance.", "A smaller value resolves lower concentrations more accurately and increases solver work."),
):
    _register_parameter("scipy", "integrate_reaction_network", _field_path, description=_description, default=_default, impact=_impact)
_register_parameter(
    "rmg", "calculate_rate_constants", "inputs.kinetics_model",
    description=("Typed RMG kinetics model. Agent-controlled nested fields include type, reaction_order, "
                 "Arrhenius terms, temperature bounds, pressure grids/bounds, Chebyshev coefficients, and units."),
    impact="Changing any nested model coefficient, validity range, pressure, or unit changes calculated rate coefficients.",
    nested_fields={
        "type": "arrhenius | multi_arrhenius | pressure_dependent_arrhenius | chebyshev",
        "reaction_order": "1..4; determines output rate unit",
        "minimum_temperature_kelvin": "optional validity lower bound",
        "maximum_temperature_kelvin": "optional validity upper bound",
        "terms": "Arrhenius term or term list",
        "pressures_bar": "tabulated pressures for pressure-dependent Arrhenius",
        "coefficients": "Chebyshev coefficient matrix",
        "minimum_pressure_bar": "Chebyshev validity lower bound",
        "maximum_pressure_bar": "Chebyshev validity upper bound",
    },
)


# Record the native Multiwfn unit as an implementation fact, separate from the
# Agent-controlled canonical grid_spacing_bohr request parameter.
_register_fixed(
    "multiwfn", "calculate_electron_isodensity_surface", "backend_runtime.native_grid_spacing_unit",
    description="The installed Multiwfn surface-grid menu accepts grid spacing in bohr.",
    reason="The software-native unit is fixed by Multiwfn; the public Action exposes it explicitly as action_settings.grid_spacing_bohr.",
)


def parameter_specs_for_backend(
    backend_id: str,
) -> Mapping[str, Mapping[str, ParameterMetadata]]:
    return BACKEND_PARAMETER_SPECS.get(backend_id, {})


def fixed_parameter_specs_for_backend(
    backend_id: str,
) -> Mapping[str, Mapping[str, ParameterMetadata]]:
    return BACKEND_FIXED_PARAMETER_SPECS.get(backend_id, {})


def common_fixed_parameter_specs(
    *,
    runtime: str,
    executables: tuple[str, ...],
    python_modules: tuple[str, ...],
    resource_constraints: Mapping[str, Any],
    validation_level: str | None,
) -> dict[str, dict[str, Any]]:
    """Describe implementation constraints that remain fixed after provider selection."""

    implementation = ", ".join(executables or python_modules) or "internal implementation"
    values: dict[str, dict[str, Any]] = {
        "backend_runtime.runtime_family": {
            "description": f"Selected provider executes through the {runtime!r} runtime family.",
            "reason": "The Agent can select another advertised backend, but cannot replace the implementation behind a selected backend id inside a predefined Action call.",
        },
        "backend_runtime.implementation": {
            "description": f"Executable/module implementation: {implementation}.",
            "reason": "Executable and module allowlists are operator-installed security and reproducibility boundaries.",
        },
        "backend_runtime.automatic_fallback": {
            "description": "Automatic fallback to another scientific backend is disabled.",
            "reason": "Benchmark provenance requires the declared provider to be executed or to fail explicitly.",
        },
    }
    if validation_level:
        values["backend_runtime.validation_level"] = {
            "description": f"Declared adapter validation level: {validation_level}.",
            "reason": "Validation status records tested implementation coverage; it is not a per-call scientific parameter.",
        }
    for field_name in ("maximum_cpu_cores", "maximum_walltime_seconds"):
        if field_name in resource_constraints:
            reason_key = (
                "walltime_reason"
                if field_name == "maximum_walltime_seconds"
                else "reason"
            )
            values[f"resource_limits.{field_name}"] = {
                "description": f"Backend-enforced {field_name.replace('_', ' ')}: {resource_constraints[field_name]}.",
                "reason": str(resource_constraints.get(reason_key) or "Operator-defined backend resource safety cap."),
            }
    return values


_FIELD_DESCRIPTIONS = {
    "method": "Electronic-structure, force-field, kinetic, or statistical method selected by the Agent.",
    "basis": "Orbital basis set used by the selected quantum-chemistry method.",
    "basis_set": "Basis-set family or exact basis resource used by the backend.",
    "functional": "Density-functional approximation selected for the calculation.",
    "xc": "Exchange-correlation functional selected for the calculation.",
    "charge": "Net system charge in units of the elementary charge.",
    "multiplicity": "Spin multiplicity, equal to two times total spin plus one.",
    "spin": "Backend-specific spin or number of unpaired electrons.",
    "temperature_kelvin": "Thermodynamic or simulation temperature in kelvin.",
    "pressure_bar": "Pressure in bar.",
    "random_seed": "Random-number seed controlling reproducible stochastic sampling.",
    "max_steps": "Maximum number of optimization, dynamics, or iteration steps.",
    "max_iterations": "Maximum number of numerical iterations.",
    "max_cycles": "Maximum number of solver or optimizer cycles.",
    "grid_points_per_axis": "Number of density-grid samples along every Cartesian axis.",
    "grid_spacing_bohr": "Requested real-space grid spacing in bohr.",
    "grid_spacing_angstrom": "Requested real-space grid spacing as currently named by the backend contract.",
    "cutoffs_au": "Explicit electron-density isovalue list in atomic units.",
    "output_format": "Agent-selected representation or serialization format for the result.",
    "density_source": "Named electronic density stored by the preceding calculation.",
    "properties": "Explicit result properties requested from the parser or data source.",
}


def inferred_parameter_metadata(
    section: str,
    field_name: str,
    *,
    required: bool,
) -> dict[str, Any]:
    """Provide a complete fallback explanation for every public field.

    Backend-specific registrations override these neutral descriptions.  The
    fallback prevents a required field from appearing in discovery or audit
    output without any statement of purpose or directional effect.
    """

    description = _FIELD_DESCRIPTIONS.get(field_name)
    if description is None:
        readable = field_name.replace("_", " ")
        if section == "inputs":
            description = f"Input value for {readable}."
        elif section == "method_spec":
            description = f"Agent-selected scientific method parameter controlling {readable}."
        elif section == "action_settings":
            description = f"Agent-selected execution setting controlling {readable}."
        else:
            description = f"Agent-controlled parameter for {readable}."

    lower = field_name.casefold()
    if any(token in lower for token in ("tolerance", "convergence", "threshold")):
        impact = (
            "A stricter numerical threshold usually improves convergence quality or filtering "
            "selectivity but may increase cost or reject more results; interpret the direction "
            "according to the selected backend definition."
        )
    elif any(token in lower for token in ("max_steps", "max_iterations", "max_cycles", "max_records", "max_")):
        impact = (
            "A larger bound allows more search, iteration, or returned records and can increase "
            "runtime and output size; it does not guarantee convergence or higher scientific quality."
        )
    elif any(token in lower for token in ("grid", "points", "bins")):
        impact = (
            "Finer or more numerous samples can reduce discretization error or increase resolution "
            "at greater runtime, memory, and output cost; convergence should be checked."
        )
    elif "cutoff" in lower or "range" in lower:
        impact = (
            "Changing this boundary changes which interactions, structures, records, or numerical "
            "region are included and may also change cost."
        )
    elif "temperature" in lower or "pressure" in lower:
        impact = "Changing this thermodynamic state variable changes the physical ensemble or state evaluated."
    elif "seed" in lower:
        impact = "Changing the seed changes a stochastic realization; fixed seeds improve reproducibility."
    elif lower.startswith(("include_", "use_", "allow_", "fix_", "keep_", "require_", "relax_", "generate_")):
        impact = "Toggling this flag enables or disables the named behavior and can change both results and cost."
    elif section == "method_spec":
        impact = "Changing this value changes the scientific model or representation used by the backend."
    elif section == "inputs":
        impact = "Changing this value changes the scientific data supplied to the Action."
    else:
        impact = "Changing this value changes the named Action behavior or numerical result."

    value: dict[str, Any] = {"description": description, "impact": impact}
    if not required:
        value["default"] = None
    return value
