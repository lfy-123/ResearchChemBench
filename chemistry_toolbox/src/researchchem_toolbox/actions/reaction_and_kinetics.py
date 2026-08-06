"""ActionSpec declarations for reaction_and_kinetics."""

from __future__ import annotations

from .._spec_builders import action as _action


ACTION_SPECS = (
    _action(
            "explore_reaction_network",
            "reaction_and_kinetics",
            "Run an explicit KinBot full-PES input and return the discovered wells, reaction summaries, and native network artifacts without choosing reaction families or electronic-structure settings.",
            "ReactionNetworkExplorationResult",
            ("kinbot",),
            ("input_file",),
            input_description="complete KinBot JSON input with explicit species, reaction families, PES controls, electronic-structure method, and execution mode",
        ),
    _action(
            "locate_transition_state",
            "reaction_and_kinetics",
            "Locate one candidate transition-state structure without automatically running frequencies or IRC.",
            "AtomicStructure",
            ("pysisyphus", "sella"),
            ("initial_guess",),
            input_description="candidate structure; use search_reaction_path when two endpoints should drive the search",
        ),
    _action(
            "search_reaction_path",
            "reaction_and_kinetics",
            "Run an explicitly selected double-ended chain-of-states search between supplied reactant and product structures without asserting that the highest image is a validated transition state.",
            "ReactionPath",
            ("pysisyphus",),
            ("reactant", "product"),
            input_description="atom-order-matched reactant and product endpoint structures",
        ),
    _action(
            "scan_reaction_coordinates",
            "reaction_and_kinetics",
            "Run one relaxed one-dimensional internal-coordinate scan from a supplied structure using explicit coordinate, range, optimizer, and calculator settings.",
            "ReactionCoordinateScan",
            ("pysisyphus",),
            ("structure",),
            input_description="one starting structure; the scanned atom indices and range are explicit action settings",
        ),
    _action(
            "validate_reaction_path",
            "reaction_and_kinetics",
            "Check atom/state consistency, endpoint agreement, image continuity, and optional bond-change progress for an already calculated reaction path.",
            "ReactionPathValidationResult",
            ("internal_reaction_analysis",),
            ("path", "reactant", "product"),
            ("bond_changes",),
            input_description="calculated path plus the intended endpoint structures and optional forming/breaking bond definitions",
            selection_policy="internal_deterministic",
        ),
    _action(
            "analyze_reaction_coordinate",
            "reaction_and_kinetics",
            "Convert supplied path images and aligned electronic energies into a normalized reaction-coordinate profile with relative energies and highest-image candidates.",
            "ReactionCoordinateAnalysisResult",
            ("internal_reaction_analysis",),
            ("path", "energies"),
            ("bond_changes",),
            input_description="calculated path and one explicitly aligned energy value per image",
            selection_policy="internal_deterministic",
        ),
    _action(
            "trace_intrinsic_reaction_coordinate",
            "reaction_and_kinetics",
            "Trace an IRC from an already supplied transition-state structure.",
            "ReactionPath",
            ("pysisyphus",),
            ("transition_state",),
            input_description="validated candidate transition-state structure",
        ),
    _action(
            "calculate_chemical_equilibrium",
            "reaction_and_kinetics",
            "Calculate an equilibrium composition/state for an explicitly supplied mechanism and thermodynamic condition.",
            "EquilibriumResult",
            ("cantera",),
            ("composition",),
            ("mechanism",),
            input_description="composition and optional mechanism Artifact",
        ),
    _action(
            "integrate_reaction_network",
            "reaction_and_kinetics",
            "Integrate one explicitly specified reaction network over time.",
            "KineticsTrajectory",
            ("scipy", "cantera"),
            ("network", "initial_state"),
            input_description="ReactionNetwork and initial concentrations/state",
        ),
    _action(
            "calculate_rate_constants",
            "reaction_and_kinetics",
            "Evaluate an explicitly supplied Arrhenius, multi-Arrhenius, pressure-dependent Arrhenius, or Chebyshev kinetics model on explicit temperature/pressure points.",
            "RateConstantResult",
            ("rmg",),
            ("kinetics_model", "temperatures_kelvin"),
            ("pressures_pa",),
            input_description="typed kinetics model plus temperature points and, for pressure-dependent models, pressure points",
        ),
    _action(
            "calculate_tunneling_correction",
            "reaction_and_kinetics",
            "Calculate Wigner or Eckart transition-state tunneling correction factors at explicit temperatures.",
            "TunnelingCorrectionResult",
            ("rmg",),
            ("temperatures_kelvin", "imaginary_frequency_cm1"),
            ("reactant_energy_kj_mol", "transition_state_energy_kj_mol", "product_energy_kj_mol"),
            input_description="temperature grid, imaginary transition-state frequency, and explicit Eckart energies when selected",
        ),
    _action(
            "solve_master_equation",
            "reaction_and_kinetics",
            "Solve an explicitly supplied gas-phase chemical master-equation model and extract pressure/temperature-dependent phenomenological rate coefficients without constructing or modifying the reaction model.",
            "MasterEquationResult",
            ("mess", "mesmer"),
            ("model_file",),
            ("companion_files", "model_relative_path"),
            input_description=(
                "native MESS input or MESMER XML model Artifact; optional explicitly listed "
                "companion files and safe staged relative paths preserve model-local references"
            ),
        ),
    _action(
            "solve_microkinetic_model",
            "reaction_and_kinetics",
            "Solve one explicitly supplied microkinetic model without constructing the reaction model for the agent.",
            "MicrokineticResult",
            ("catmap",),
            ("model",),
            input_description=(
                "typed CatMAP model fields, including explicit reaction expressions, species/site "
                "definitions, descriptor space, energetics input Artifact, thermochemistry modes, "
                "solver controls, and requested output variables"
            ),
        ),
    _action(
            "analyze_thermochemical_selectivity",
            "reaction_and_kinetics",
            "Calculate N-way thermodynamic selectivity from explicitly labeled structure ensembles, including two-label excess and delta-delta-G when applicable.",
            "ThermochemicalSelectivityResult",
            ("goodvibes",),
            ("output_files", "label_groups"),
            input_description=(
                "compatible completed quantum outputs plus a mapping from at least two Agent-defined "
                "labels to exact members of output_files"
            ),
        ),
    _action(
            "analyze_reaction_free_energy_profile",
            "reaction_and_kinetics",
            "Calculate relative electronic and thermochemical energies along explicitly defined reaction pathways, including stoichiometric sums and conformer ensembles.",
            "ReactionFreeEnergyProfileResult",
            ("goodvibes",),
            ("output_files", "profile_definition_file"),
            input_description=(
                "compatible completed quantum outputs plus an Agent-authored GoodVibes PES YAML "
                "defining pathways, species membership, zero references, and units"
            ),
        ),
    _action(
            "analyze_activation_strain_profile",
            "reaction_and_kinetics",
            "Calculate an ORCA activation-strain profile along an explicitly supplied reaction path with explicit fragment partitions, reference energies, electronic-structure keywords, and reaction coordinate.",
            "ActivationStrainProfileResult",
            ("pyfrag",),
            ("reaction_path_file",),
            input_description=(
                "AMV or multi-XYZ reaction path; fragment membership, isolated-fragment reference "
                "energies, charge, multiplicity, ORCA keywords, and printed bond coordinate remain "
                "explicit Agent choices"
            ),
        ),
    _action(
            "summarize_activation_strain_profile",
            "reaction_and_kinetics",
            "Parse a bounded PyFrag activation-strain table and report extrema and decomposition-closure diagnostics without rerunning electronic-structure calculations.",
            "ActivationStrainProfileSummary",
            ("pyfrag",),
            ("profile_file",),
            input_description="existing PyFrag fragment_energies.txt output",
        ),
    _action(
            "validate_activation_strain_profile",
            "reaction_and_kinetics",
            "Validate record count, finite values, sequential point identifiers, and total-energy decomposition closure in an existing PyFrag activation-strain table.",
            "ActivationStrainProfileValidationResult",
            ("pyfrag",),
            ("profile_file",),
            input_description="existing PyFrag fragment_energies.txt output plus explicit validation tolerances",
        ),
    _action(
            "analyze_post_transition_state_trajectory_ensemble",
            "reaction_and_kinetics",
            "Calculate product branching, recrossing, unassigned fraction, and binomial confidence intervals from explicit per-trajectory outcome classifications.",
            "PostTransitionStateTrajectoryEnsembleResult",
            ("internal_reaction_analysis",),
            ("trajectory_outcomes",),
            input_description="trajectory identifiers with explicit success/failure, product label, and recrossing classification",
            selection_policy="internal_deterministic",
        ),
)
