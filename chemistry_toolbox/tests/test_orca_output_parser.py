"""Small format regressions, independent of any benchmark paper or workspace."""

import math

import pytest

from cclib.parser.orcaparser import ORCA

from chemistry_toolbox.src.backends.interchange import _parse_quantum_output, _read_quantum_output
from chemistry_toolbox.src.execution_feedback import execution_feedback


HEADER = """O   R   C   A
Program Version 6.1.1

INPUT FILE
==========
NAME = water.inp
| 1> ! HF def2-SVP
| 2> ****END OF INPUT****
==========
CARTESIAN COORDINATES (ANGSTROEM)
-------------------------------
O 0.0 0.0 0.0
H 0.0 0.7 0.5
H 0.0 -0.7 0.5

 # of contracted basis functions         8
"""

SCF = """ORCA LEAN-SCF
----------------------------------------D-I-I-S--------------------------------------------
Iteration    Energy (Eh)           Delta-E    RMSDP     MaxDP     DIISErr   Damp  Time(sec)
-------------------------------------------------------------------------------------------
    1    -74.9    0.0      0.002     0.009     0.2   0.7   0.3
                              *** Initializing SOSCF ***
---------------------------------------S-O-S-C-F--------------------------------------
Iteration    Energy (Eh)           Delta-E    RMSDP     MaxDP     MaxGrad    Time(sec)
--------------------------------------------------------------------------------------
    2    -75.0   -0.1      0.0002    0.0009    0.0001      0.1
               *           SCF CONVERGED AFTER  2 CYCLES          *
TOTAL SCF ENERGY
----------------
Total Energy       :       -75.0 Eh
SCF CONVERGENCE
---------------
  Last Energy change         ...    1.0e-8  Tolerance :   1.0000e-08
  Last MAX-Density change    ...    3.0e-6  Tolerance :   1.0000e-07
  Last RMS-Density change    ...    2.0e-6  Tolerance :   5.0000e-09

"""

ORBITALS = """ORBITAL ENERGIES
----------------

  NO   OCC          E(Eh)            E(eV)
   0   2.0000     -19.000000      -517.0163
   1   2.0000      -1.000000       -27.2114
   2   2.0000      -0.800000       -21.7691
   3   2.0000      -0.500000       -13.6057
   4   2.0000      -0.300000        -8.1634
   5   0.0000       0.200000         5.4423
*Only the first 1 virtual orbitals were printed.

----------------
"""

DIPOLE = """DIPOLE MOMENT
-------------

Method             : SCF
Type of density    : Electron Density
Multiplicity       :   1
Irrep              :   0
Energy             :  -75.0 Eh
Basis              : AO
                                X                 Y                 Z
Electronic contribution:      0.10       0.20       -0.30
Nuclear contribution   :      0.00       0.00        0.00
                        -----------------------------------------
Total Dipole Moment    :       0.10       0.20       -0.30
                        -----------------------------------------
Magnitude (Debye)      :       0.95

"""

FREQUENCIES = """VIBRATIONAL FREQUENCIES
-----------------------

Scaling factor for frequencies =  1.000000000

    0: 0.00 cm**-1
    1: 0.00 cm**-1
    2: 0.00 cm**-1
    3: 0.00 cm**-1
    4: 0.00 cm**-1
    5: 0.00 cm**-1
    6: -321.25 cm**-1 ***imaginary mode***
    7: 1010.50 cm**-1
    8: 3550.25 cm**-1

"""

THERMO = """THERMOCHEMISTRY AT 298.15K
--------------------------

Temperature         ...   298.15 K
Pressure            ...     1.00 atm
Total Mass          ...    18.02 AMU
Quasi RRHO          ...     True
Electronic energy                ...    -75.0 Eh
Zero point energy                ...      0.02 Eh
ENTHALPY
Total thermal energy             ...    -74.971 Eh
Total Enthalpy                   ...    -74.970 Eh
ENTROPY
Final entropy term               ...      0.025 Eh
GIBBS FREE ENERGY
Final Gibbs free energy          ...    -74.995 Eh

"""

END = "****ORCA TERMINATED NORMALLY****\nTOTAL RUN TIME: 0 days 0 hours 0 minutes 1 seconds 0 msec\n"


def _output(tmp_path, text):
    source = tmp_path / "orca.log"
    source.write_text(text)
    return source


def _action(tmp_path, monkeypatch, text, groups):
    source = _output(tmp_path, text)
    monkeypatch.setenv("RESEARCHCHEMBENCH_WORKSPACE", str(tmp_path))
    return _parse_quantum_output({
        "inputs": {"output_file": source.name}, "method_spec": {},
        "action_settings": {
            "properties": groups, "coordinate_frames": "last",
            "include_orbital_coefficients": False,
            "include_excited_state_configurations": False,
            "max_array_elements": 100000,
        },
    })


def test_lean_scf_columns_solver_switch_and_separate_cycles(tmp_path):
    original = ORCA._append_scfvalues_scftargets
    source = _output(tmp_path, HEADER + SCF + SCF.replace("-75.0", "-76.0") + END)
    data, details = _read_quantum_output(source)
    assert data is not None, details
    assert len(data.scfvalues) == 2
    assert data.scfvalues[0].tolist() == [
        [0.0, 0.009, 0.002], [-0.1, 0.0009, 0.0002], [1e-8, 3e-6, 2e-6],
    ]
    assert data.scfenergies.tolist() == pytest.approx([-2040.85396, -2068.06534], abs=0.0002)
    assert details["source_termination"] == "normal"
    assert ORCA._append_scfvalues_scftargets is original


@pytest.mark.parametrize("print_iterations", [True, False])
def test_legacy_orca_missing_first_rms_target_without_private_paper_files(tmp_path, print_iterations):
    legacy = """SCF ITERATIONS
--------------
ITER       Energy         Delta-E        Max-DP      RMS-DP      [F,P]     Damp
   0   -74.9   0.0    0.009    0.002    0.2   0.7
   1   -75.0  -0.1    0.0009   0.0002   0.0001 0.0

"""
    summary = SCF[SCF.index("               *           SCF CONVERGED"):]
    summary = "\n".join(line for line in summary.splitlines() if "Last RMS-Density" not in line) + "\n\n"
    source = _output(tmp_path, HEADER.replace("6.1.1", "4.0.1") + (legacy if print_iterations else "") + summary + END)
    data, info = _read_quantum_output(source)
    assert data is not None, info
    assert len(data.scfenergies) == 1
    assert math.isnan(data.scftargets[0][2])
    if print_iterations:
        assert data.scfvalues[0][-1][2] == 0.0002
    else:
        assert math.isnan(data.scfvalues[0][-1][2])
    assert any("compatibility fix" in issue["message"] for issue in info["diagnostics"])


@pytest.mark.parametrize("groups,expected", [
    (["energies", "vibrational_frequencies", "multipoles"], "success"),
    (["energies", "molecular_orbitals"], "partial_success"),
])
def test_orbital_footnote_preserves_other_properties_and_marks_partial(tmp_path, monkeypatch, groups, expected):
    result = _action(tmp_path, monkeypatch, HEADER + SCF + ORBITALS + DIPOLE + FREQUENCIES + THERMO + END, groups)
    assert result["status"] == expected, result
    props = result["result"]["properties"]
    assert props["freeenergy"] == -74.995
    assert props["enthalpy"] == -74.970
    assert props["entropy"] == pytest.approx(0.025 / 298.15)
    if "molecular_orbitals" in groups:
        assert len(props["moenergies"][0]) == 6
        assert result["result"]["incomplete_property_groups"] == ["molecular_orbitals"]
    else:
        assert props["vibfreqs"] == [-321.25, 1010.5, 3550.25]
        assert props["moments"][1] == pytest.approx([0.2541746, 0.5083492, -0.7625238], abs=1e-6)
        sources = result["result"]["property_sources"]
        assert sources["scfenergies"]["last_block_end_line"] < sources["vibfreqs"]["last_block_start_line"]
        assert sources["vibfreqs"]["last_block_end_line"] < sources["freeenergy"]["last_block_start_line"]


def test_open_shell_orbital_tables_and_d_notation(tmp_path):
    table = """ORBITAL ENERGIES
----------------
                 SPIN UP ORBITALS
  NO   OCC          E(Eh)            E(eV)
   0   1.0000     -1.0D+00          -27.2114
   1   0.0000      0.2D+00            5.4423
*Only the first 1 virtual orbitals were printed.

                 SPIN DOWN ORBITALS
  NO   OCC          E(Eh)            E(eV)
   0   1.0000     -0.9D+00          -24.4902
   1   0.0000      0.3D+00            8.1634
*Only the first 1 virtual orbitals were printed.

----------------
"""
    data, info = _read_quantum_output(_output(tmp_path, HEADER + table + END))
    assert data is not None, info
    assert data.homos.tolist() == [0, 0]
    assert data.moenergies[0][0] == pytest.approx(-27.21138505)
    assert data.moenergies[1][0] == pytest.approx(-24.490246545)


def test_truncated_frequency_table_is_not_zero_padded(tmp_path, monkeypatch):
    text = HEADER + SCF + FREQUENCIES.split("    7:")[0]
    result = _action(tmp_path, monkeypatch, text, ["energies", "vibrational_frequencies"])
    assert result["status"] == "partial_success", result
    assert "vibfreqs" not in result["result"]["properties"]
    assert result["result"]["incomplete_property_groups"] == ["vibrational_frequencies"]
    assert result["result"]["source_termination"] == "not_observed"


def test_orca6_labelled_absorption_rows_keep_energy_units_and_states(tmp_path):
    table = """ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------------------------------------------------------------------------------------------
                     Transition      Energy     Energy  Wavelength fosc(D2)      D2        DX        DY        DZ
                                      (eV)      (cm-1)    (nm)                 (au**2)    (au)      (au)      (au)
----------------------------------------------------------------------------------------------------
  0-6A  ->  1-6A    3.362525   27120.6   368.7   0.000799477   0.00970  -0.00492   0.01981  -0.09637
  0-6A  ->  2-6A    3.367953   27164.4   368.1   0.000717470   0.00870  -0.00046  -0.09149  -0.01802
----------------------------------------------------------------------------------------------------
"""
    from chemistry_toolbox.src.backends.interchange import _read_quantum_output
    data, info = _read_quantum_output(_output(tmp_path, HEADER + table + END))
    assert data is not None, info
    assert data.etenergies.tolist() == pytest.approx([27120.6, 27164.4])
    from cclib.parser import utils
    assert utils.convertor(data.etenergies[0], "wavenumber", "eV") == pytest.approx(3.362525, abs=1e-5)
    assert data.etoscs.tolist() == pytest.approx([0.000799477, 0.000717470])
    assert data.metadata["absorption_tables"][0]["transition_labels"] == [("0-6A", "1-6A"), ("0-6A", "2-6A")]


def test_truncated_thermochemistry_keeps_known_values_without_previous_gibbs(tmp_path, monkeypatch):
    text = HEADER + SCF + THERMO + THERMO.split("Final entropy term")[0]
    result = _action(tmp_path, monkeypatch, text, ["energies"])
    assert result["status"] == "partial_success", result
    properties = result["result"]["properties"]
    assert properties["enthalpy"] == -74.970
    assert "freeenergy" not in properties
    assert "entropy" not in properties


def test_legacy_absorption_keeps_velocity_gauge_separate(tmp_path):
    electric = "ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS"
    velocity = electric.replace("ELECTRIC", "VELOCITY")
    table = """
-------------------------------------------------------------------
State Energy Wavelength fosc D2 DX DY DZ
      (cm-1) (nm) (au**2) (au) (au) (au)
-------------------------------------------------------------------
1 27120.6 368.7 0.001 0.01 0.01 0.01 0.01

"""
    data, info = _read_quantum_output(_output(tmp_path, HEADER + electric + table + velocity + table.replace("0.001", "0.009") + END))
    assert data is not None, info
    assert data.etenergies.tolist() == pytest.approx([27120.6])
    assert data.etoscs.tolist() == pytest.approx([0.001])
    assert data.transprop[velocity][1].tolist() == pytest.approx([0.009])


def test_unsupported_absorption_units_fail_with_source_location(tmp_path):
    table = """ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS
----------------
State Energy Wavelength fosc D2 DX DY DZ
      (unknown) (nm) (au**2) (au) (au) (au)
----------------
1 27120.6 368.7 0.001 0.01 0.01 0.01 0.01

"""
    data, info = _read_quantum_output(_output(tmp_path, HEADER + table + END))
    assert data is None
    assert "Unsupported absorption columns/units" in info["error"]["reason"]
    assert info["error"]["line_number"] > 0


def test_nonconvergence_does_not_turn_delta_e_into_absolute_energy(tmp_path, monkeypatch):
    text = HEADER + SCF.replace("SCF CONVERGED AFTER", "SCF NOT CONVERGED AFTER")
    text += "ORCA finished by error termination in orca_scf\nTOTAL RUN TIME: 0 days 0 hours 0 minutes 1 seconds 0 msec\n"
    result = _action(tmp_path, monkeypatch, text, ["metadata", "energies"])
    assert result["status"] == "partial_success", result
    assert result["result"]["source_termination"] == "abnormal"
    assert result["result"]["properties"]["metadata"]["success"] is False
    assert "scfenergies" not in result["result"]["properties"]


@pytest.mark.parametrize("bad_table", [
    ORBITALS.replace("0.200000", "broken"),
    ORBITALS.replace("*Only the first 1 virtual orbitals were printed.", "unrecognized row inside table"),
])
def test_unknown_parse_errors_keep_location_through_wait_feedback(tmp_path, monkeypatch, bad_table):
    result = _action(tmp_path, monkeypatch, HEADER + SCF + bad_table + END, ["energies"])
    assert result["status"] == "failed", result
    error = result["error"]
    assert error["code"] == "output_parse_failed"
    assert error["source_path"] == "orca.log"
    assert error["line_number"] > 0
    assert error["line_preview"]
    assert error["section"] == "ORBITAL ENERGIES"
    view = execution_feedback(status={"status": "failed"}, action_result=result)
    assert view["diagnostic"]["category"] == "output_parsing"
    assert view["diagnostic"]["failure_stage"] == "output_parsing"
    assert view["diagnostic"]["evidence"][0]["path"] == "orca.log"
    assert "reparse the saved file" in view["diagnostic"]["repair_advice"]["message"]
