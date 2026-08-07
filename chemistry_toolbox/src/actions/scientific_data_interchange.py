"""ActionSpec declarations for scientific_data_interchange."""

from __future__ import annotations

from .._spec_builders import action as _action


ACTION_SPECS = (
    _action(
            "normalize_qcschema_molecule",
            "scientific_data_interchange",
            "Validate and normalize one supplied molecular structure into a QCSchema Molecule record without launching a calculation.",
            "QCSchemaMolecule",
            ("qcelemental",),
            ("structure",),
            input_description="AtomicStructure or existing QCSchema Molecule mapping",
            selection_policy="internal_deterministic",
        ),
    _action(
            "validate_qcschema_record",
            "scientific_data_interchange",
            "Validate one explicit QCSchema/QCArchive record type and return a normalized record or structured validation errors without executing it.",
            "QCSchemaValidationResult",
            ("qcelemental",),
            ("record",),
            input_description="JSON-compatible record mapping or workspace JSON Artifact",
            selection_policy="internal_deterministic",
        ),
    _action(
            "parse_quantum_chemistry_output",
            "scientific_data_interchange",
            "Parse explicitly selected properties from one existing quantum-chemistry output file without rerunning the calculation.",
            "ParsedQuantumChemistryResult",
            ("cclib",),
            ("output_file",),
            input_description="workspace Gaussian, ORCA, NWChem, GAMESS, Q-Chem, Molpro, or other cclib-supported output Artifact",
            selection_policy="internal_deterministic",
        ),
)
