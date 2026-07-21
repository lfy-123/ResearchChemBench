# Atomic toolbox tests

The legacy one-test-per-`run_*` layout was removed with the legacy public tools.

The active suites under `tests/` validate the complete versioned Scientific/Data
Action catalog, exact Agent-selected backend dispatch, zero automatic
fallback, one unified MCP server, Artifact chaining, runtime coverage, and
real RDKit/ASE smoke calculations.

```bash
bash chemistry_toolbox/mcp/test_tools/run_tests.sh
```
