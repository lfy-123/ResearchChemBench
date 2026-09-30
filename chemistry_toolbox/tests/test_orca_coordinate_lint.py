import pytest

from chemistry_toolbox.mcp.orca_input_lint import lint_orca_input


def lint(text, targets=(), cpu=2, memory=1024):
    return lint_orca_input(text, staged_targets=set(targets), cpu_cores=cpu, memory_mb=memory)


@pytest.mark.parametrize("kind", ["xyzfile", "XYZFILE", "gzmtfile"])
def test_external_coordinates_are_a_single_line(kind):
    result = lint(f'# input comment\n! HF\n* {kind} -1 1 "coords file.xyz" # no closing star\n', ["coords file.xyz"])
    assert result["coordinate_sections"][0]["target"] == "coords file.xyz"
    assert not result["warnings"]


@pytest.mark.parametrize("kind", ["xyz", "int", "internal", "gzmt"])
def test_inline_coordinates_require_their_own_closure(kind):
    assert lint(f"! HF\n* {kind} 0 1\nH 0 0 0\n* # closed\n")["coordinate_section_count"] == 1
    with pytest.raises(ValueError, match="unclosed_coordinates"):
        lint(f"! HF\n* {kind} 0 1\nH 0 0 0\n$new_job\n! HF\n* xyz 0 1\nH 0 0 0\n*\n")
    with pytest.raises(ValueError, match="unclosed_coordinates"):
        lint(f"! HF\n* {kind} 0 1\nH 0 0 0\n* xyz 0 1\nH 0 0 0\n*\n")


def test_coordinate_block_and_multijob_reuse():
    text = "# comment\n%coords\n CTyp xyz\n Charge 0\n Mult 1\n coords\n H 0 0 0\n end\nend\n! HF\n"
    assert lint(text)["coverage"] == "supported_subset"
    with pytest.raises(ValueError, match="unclosed_block"):
        lint(text.replace("end\nend", "end"))
    result = lint("! HF Opt\n* xyz 0 1\nH 0 0 0\n*\n$new_job\n! HF\n* xyzfile 0 1\n")
    assert result["job_segment_count"] == 2
    assert result["coordinate_sections"][1]["source"] == "previous_job"


@pytest.mark.parametrize(("text", "message"), [
    ("! HF\n* xyzfile 0 1 missing.xyz\n", "missing_geometry"),
    ("! HF\n* xyzfile 0 1 ../outside.xyz\n", "geometry_path"),
    ("! HF\n* xyzfile 0 1 /outside.xyz\n", "geometry_path"),
    ("! HF\n* xyzfile 0 1\n", "coordinate_header"),
    ("! HF\n* xyzfile 0 1 geom.xyz", "coordinate_newline"),
    ("! HF PAL4\n* xyzfile 0 1 geom.xyz\n", "cpu_mismatch"),
    ("! HF\n%pal nprocs 1 end\n* xyzfile 0 1 geom.xyz\n$new_job\n! HF\n%pal nprocs 3 end\n* xyzfile 0 1\n", "cpu_mismatch"),
    ("! HF\n%maxcore 600\n%pal nprocs 2 end\n* xyzfile 0 1 geom.xyz\n", "memory_mismatch"),
    ("! HF\n%scf\n$new_job\n! HF\nend\n", "unclosed_block"),
])
def test_definite_errors_fail(text, message):
    with pytest.raises(ValueError, match=message):
        lint(text, ["geom.xyz"])


def test_uncovered_syntax_is_reported_without_guessing():
    result = lint("! HF\n%future_version_block\nend\n* future_coordinates 0 1 data\n")
    assert result["coverage"] == "partial"
    assert len(result["warnings"]) == 2
    assert lint("! HF\n# %pal nprocs 99 end\n* xyzfile 0 1 geom.xyz\n", ["geom.xyz"])["warnings"] == []
