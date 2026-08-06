from __future__ import annotations

from chemistry_toolbox.src.service import execute_action


XVG = """@ title "Synthetic alchemical parser test"
@ xaxis label "Time (ps)"
@ subtitle "T = 300 (K) \\xl\\f{} state 0: (fep-lambda) = (0.0000)"
@ s0 legend "Potential Energy (kJ/mol)"
@ s1 legend "\\xD\\f{}H \\xl\\f{} to (0.0)"
@ s2 legend "\\xD\\f{}H \\xl\\f{} to (1.0)"
0.0 -10.0 0.0 5.0
1.0 -9.5 0.2 4.8
2.0 -9.0 0.4 4.6
"""


def test_alchemlyb_parses_gromacs_reduced_potentials(tmp_path, monkeypatch):
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    path = tmp_path / "dhdl.xvg"
    path.write_text(XVG, encoding="utf-8")
    result = execute_action(
        "parse_alchemical_energy_data",
        {
            "backend_id": "alchemlyb",
            "inputs": {"files": [str(path)]},
            "method_spec": {},
            "action_settings": {
                "engine": "gromacs",
                "observable": "u_nk",
                "temperature_kelvin": 300.0,
                "filter_invalid_rows": True,
            },
        },
    )
    assert result["status"] == "success"
    assert result["result"]["row_count"] == 3
    assert result["result"]["column_count"] == 2
    assert result["result"]["energy_unit"] == "kT"
