from evaluation.instructions_tmpl import INSTRUCTIONS_TEMPLATE


def test_managed_program_boundary_is_prominent_and_language_agnostic() -> None:
    boundary = INSTRUCTIONS_TEMPLATE.index("## Managed execution boundary")
    task = INSTRUCTIONS_TEMPLATE.index("## Task")

    assert boundary < task
    assert "Do not\nlaunch Python, PyPy, R, or Julia through a built-in shell" in INSTRUCTIONS_TEMPLATE
    assert "submit_analysis_program" in INSTRUCTIONS_TEMPLATE[boundary:task]
    assert "JobContext" in INSTRUCTIONS_TEMPLATE[boundary:task]
    assert "ctx.write_json" in INSTRUCTIONS_TEMPLATE[boundary:task]
    assert "ctx.register_output" in INSTRUCTIONS_TEMPLATE[boundary:task]
