"""Exercise native transport command discovery; no scientific calculation implied."""
import pytest

from chemistry_toolbox.mcp.software_catalog import native_command_guide, validate_native_guides


def test_tbtrans_exposed_in_same_runtime_as_integrated_transiesta():
    validate_native_guides()
    siesta = native_command_guide('siesta', 'siesta')
    tbtrans = native_command_guide('siesta', 'tbtrans')
    assert tbtrans['runtime'] == siesta['runtime'] == 'periodic'
    assert tbtrans['input_mode'] == 'stdin_file'
    assert tbtrans['example_arguments'] == []
    assert any('Hamiltonian' in item for item in tbtrans['required_files'])


def test_undeclared_standalone_transiesta_remains_rejected():
    # In SIESTA 5.x, TranSIESTA is selected by FDF, not an invented binary.
    with pytest.raises(ValueError, match='not an executable declared'):
        native_command_guide('siesta', 'transiesta')
