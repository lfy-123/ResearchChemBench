# Consolidated six-environment layout

This directory is the portable build source for the consolidated chemistry
toolbox runtimes.  The legacy 42 prefixes are intentionally not referenced by
these files.

Each environment contains:

- `environment.yml`: human-maintained Conda requirements and ABI constraints;
- `requirements.txt`: pip-only packages, including exact VCS revisions where
  applicable;
- `locks/linux-64/*.explicit.txt`: exact Conda artifact URLs captured from the
  tested server;
- `locks/linux-64/*.pip-freeze.txt`: the corresponding pip inventory.

Use `chemistry_toolbox/scripts/build_merged_environments.sh` for a portable
rebuild.  The human-maintained definitions are preferred across platforms;
the explicit lock files are intended for exact Linux x86-64 replay.

## Build and select the layout

Install the host packages listed in `system-requirements.txt`, then run from
the repository root:

```bash
# Cross-platform dependency solve from the maintained specifications.
bash chemistry_toolbox/scripts/build_merged_environments.sh all

# Exact replay of the tested linux-64 Conda artifacts.
bash chemistry_toolbox/scripts/build_merged_environments.sh --from-lock all

# Refresh locks after an intentional environment change.
bash chemistry_toolbox/scripts/capture_merged_environment_locks.sh
```

The toolbox selects the consolidated layout automatically when the prefixes
exist.  Operators can make the selection explicit or relocate all six
prefixes without changing profile configuration:

```bash
export RESEARCHCHEM_ENV_LAYOUT=merged
export RCB_MERGED_ENV_ROOT=/path/to/researchchem-envs  # optional
```

Set `RESEARCHCHEM_ENV_LAYOUT=legacy` for a controlled fallback while the old
prefixes are retained.  Do not remove the legacy environments until the full
verification suite and representative real calculations pass on the target
host.

## Compatibility boundaries

- OpenFF/AmberTools requires NumPy 1.x, so it is separate from the modern
  NumPy 2.x quantum-analysis runtime.
- CatMAP 0.3.1 requires ASE 3.17 and is isolated from modern ASE consumers.
- CP2K 2026.1 requires MPICH 5 and libxc 7. ABINIT 10.0.3 and LAMMPS use the
  MPICH-4 reaction/kinetics environment rather than the CP2K environment.
- AmberTools 26 declares a conflict with the standalone Packmol package.
  Packmol is therefore installed once in the general environment and shared
  with the molecular-dynamics runtime through its configured PATH.
- Yambo remains with its OpenMPI-4 stack and therefore does not share the
  OpenMPI-5 general runtime.
