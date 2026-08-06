from __future__ import annotations

import ast
from pathlib import Path

from chemistry_toolbox.src.backend_specs import BACKEND_SPECS
from chemistry_toolbox.src.catalog import catalog_snapshot, validate_catalog
from chemistry_toolbox.src.discovery import inspect_action, search_actions
from chemistry_toolbox.src.actions import ACTION_SPECS


def _contract_fields(contract: dict, section: str) -> dict[str, dict]:
    section_value = contract["sections"][section]
    values = [
        *section_value.get("required", []),
        *section_value.get("optional", []),
        *section_value.get("optional_documented", []),
        *section_value.get("optional_with_defaults", []),
    ]
    return {str(item["name"]): item for item in values}


def test_every_action_provider_exposes_complete_parameter_metadata():
    validate_catalog()
    snapshot = catalog_snapshot(include_health=False)
    action_map = {item.id: item for item in ACTION_SPECS}

    for backend in BACKEND_SPECS:
        for action_id in backend.capabilities:
            contract = inspect_action(
                action_id, backend_id=backend.id, snapshot=snapshot
            )["selected_request_contract"]
            assert contract is not None

            by_section = {
                section: _contract_fields(contract, section)
                for section in ("inputs", "method_spec", "action_settings")
            }
            resource_fields = _contract_fields(contract, "resource_limits")

            for section, fields in by_section.items():
                for field_name, metadata in fields.items():
                    assert metadata.get("description"), (
                        backend.id, action_id, section, field_name, "description"
                    )
                    assert metadata.get("impact"), (
                        backend.id, action_id, section, field_name, "impact"
                    )
                    if not metadata["required"]:
                        assert "default" in metadata, (
                            backend.id, action_id, section, field_name, "default"
                        )
                    else:
                        assert "default" not in metadata, (
                            backend.id, action_id, section, field_name,
                            "required fields must not advertise a public default",
                        )

            for field_name, metadata in resource_fields.items():
                assert "default" in metadata
                assert metadata.get("description")
                assert metadata.get("impact")

            action = action_map[action_id]
            expected_inputs = {
                *action.required_inputs,
                *action.optional_inputs,
                *backend.required_input_fields.get(action_id, ()),
            }
            assert expected_inputs.issubset(by_section["inputs"])
            assert set(backend.required_method_fields.get(action_id, ())).issubset(
                by_section["method_spec"]
            )
            assert set(backend.required_setting_fields.get(action_id, ())).issubset(
                by_section["action_settings"]
            )

            for field_path in backend.parameter_specs.get(action_id, {}):
                section, field_name = field_path.split(".", 1)
                target = resource_fields if section == "resource_limits" else by_section[section]
                assert field_name in target, (backend.id, action_id, field_path)

            fixed = contract["backend_fixed_parameters"]
            assert fixed
            for item in fixed:
                assert item.get("path")
                assert item.get("description")
                assert item.get("reason")


def test_backend_mapping_defaults_are_not_hidden_from_the_catalog():
    """Fail when a literal mapping fallback/conditional is not public anywhere.

    Exact Action/backend membership is verified above for registered metadata.  This
    source scan is a maintenance tripwire for newly introduced ``mapping.get`` or
    ``'field' in mapping`` controls that were never declared at all.
    """

    public = {section: set() for section in ("inputs", "method_spec", "action_settings")}
    for action in ACTION_SPECS:
        public["inputs"].update(action.required_inputs)
        public["inputs"].update(action.optional_inputs)
    for backend in BACKEND_SPECS:
        for fields in backend.required_input_fields.values():
            public["inputs"].update(fields)
        for fields in backend.required_method_fields.values():
            public["method_spec"].update(fields)
        for fields in backend.required_setting_fields.values():
            public["action_settings"].update(fields)
        for fields in backend.allowed_method_values.values():
            public["method_spec"].update(fields)
        for fields in backend.allowed_setting_values.values():
            public["action_settings"].update(fields)
        for fields in backend.parameter_specs.values():
            for field_path in fields:
                section, field_name = field_path.split(".", 1)
                if section in public:
                    public[section].add(field_name)

    source_root = Path(__file__).parents[1] / "src" / "backends"
    missing: list[tuple[str, int, str, str]] = []
    mapping_sections = {
        "inputs": "inputs",
        "method": "method_spec",
        "settings": "action_settings",
    }
    for path in sorted(source_root.rglob("*.py")):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            section = None
            field_name = None
            if (
                isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute)
                and node.func.attr == "get"
                and isinstance(node.func.value, ast.Name)
                and node.args
                and isinstance(node.args[0], ast.Constant)
                and isinstance(node.args[0].value, str)
            ):
                section = mapping_sections.get(node.func.value.id)
                field_name = node.args[0].value
            elif (
                isinstance(node, ast.Compare)
                and len(node.ops) == 1
                and isinstance(node.ops[0], (ast.In, ast.NotIn))
                and isinstance(node.left, ast.Constant)
                and isinstance(node.left.value, str)
                and len(node.comparators) == 1
                and isinstance(node.comparators[0], ast.Name)
            ):
                section = mapping_sections.get(node.comparators[0].id)
                field_name = node.left.value
            if (
                section
                and field_name
                and field_name not in public[section]
                and not (
                    section == "action_settings"
                    and field_name == "timeout_seconds"
                )
            ):
                missing.append(
                    (str(path.relative_to(source_root)), node.lineno, section, field_name)
                )

    assert missing == []


def test_timeout_is_fixed_policy_not_agent_controllable():
    snapshot = catalog_snapshot(include_health=False)
    for action in ACTION_SPECS:
        backend_id = action.backend_ids[0]
        inspected = inspect_action(
            action.id, backend_id=backend_id, snapshot=snapshot
        )
        contract = inspected["selected_request_contract"]
        assert "walltime_seconds" not in contract["execute_action_request_template"][
            "resource_limits"
        ]
        assert "timeout_seconds" not in contract["execute_action_request_template"][
            "action_settings"
        ]
        policy = contract["execution_timeout_policy"]
        assert policy["agent_controllable"] is False
        assert policy["execution_class"] == ("fast" if action.data_action else "compute")
        assert policy["timeout_seconds"] == (60 if action.data_action else 7200)
        assert inspected["execution_timeout_policy"] == policy

    searched = search_actions(query="search compounds", snapshot=snapshot)
    search_policy = searched["actions"][0]["execution_timeout_policy"]
    assert search_policy == {
        "execution_class": "fast",
        "timeout_seconds": 60,
        "source": "evaluation_policy",
        "agent_controllable": False,
    }


def test_goodvibes_population_dependency_is_exposed_to_agents():
    snapshot = catalog_snapshot(include_health=False)
    inspected = inspect_action(
        "analyze_thermochemical_ensemble",
        backend_id="goodvibes",
        snapshot=snapshot,
    )
    rules = inspected["selected_request_contract"]["conditional_requirements"]
    population_rule = next(
        item for item in rules if item["name"] == "population_basis_conditionals"
    )
    assert "quasi_harmonic_gibbs" in population_rule["rule"]
    assert "entropy_model=grimme or truhlar" in population_rule["rule"]
    assert "entropy_frequency_cutoff_cm1" in population_rule["rule"]


def test_pysisyphus_scan_steps_are_documented_as_intervals():
    snapshot = catalog_snapshot(include_health=False)
    contract = inspect_action(
        "scan_reaction_coordinates", backend_id="pysisyphus", snapshot=snapshot
    )["selected_request_contract"]
    fields = _contract_fields(contract, "action_settings")
    steps = fields["steps"]
    assert steps["type"] == "integer"
    assert steps["minimum"] == 1
    assert "interval" in steps["description"].casefold()
    assert "steps + 1" in steps["description"]


def test_orca_density_grid_default_is_300_cubed_and_agent_overridable():
    snapshot = catalog_snapshot(include_health=False)
    contract = inspect_action(
        "export_electron_density_grid", backend_id="orca", snapshot=snapshot
    )["selected_request_contract"]
    fields = _contract_fields(contract, "action_settings")
    grid = fields["grid_points_per_axis"]
    assert grid["default"] == 300
    assert grid["minimum"] == 20
    assert grid["maximum"] == 400
    assert "cube" in grid["impact"].casefold()
