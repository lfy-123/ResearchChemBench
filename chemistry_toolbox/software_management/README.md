# Chemistry software management

This package creates and validates the runtime asset layout used by the chemistry
toolbox. The managed cache may start empty. Repository code and manifests stay in
Git; downloaded software, licensed packages, build products, state, and validation
outputs stay outside Git.

## Layout

| Directory | Contents |
|---|---|
| `documentation/` | Searchable software documentation cache |
| `installations/` | Runnable native installations |
| `packages/` | Original user-provided/downloaded archives |
| `sources/` | Source snapshots that are not the active installation |
| `shared/` | MPI runtimes, basis sets, pseudopotentials, and datasets |
| `state/` | Mutable application state and local profiles |
| `build/` | Rebuildable compiler output and logs |
| `validation/` | Smoke-test inputs and outputs |
| `staging/` | Temporary atomic-install workspace |
| `receipts/` | Checksums, installation records, and migration reports |

`.envs/` remains separate: its Conda/Python runtimes are reconstructed from the
repository environment definitions and lock files.

## Empty-cache workflow

```bash
python -m chemistry_toolbox.software_management --cache-root /path/to/cache init
python -m chemistry_toolbox.software_management --cache-root /path/to/cache status
python -m chemistry_toolbox.software_management --cache-root /path/to/cache stage orca /path/to/orca_6_1_1_linux_x86-64_shared_openmpi418_nodmrg.tar.xz
python -m chemistry_toolbox.software_management --cache-root /path/to/cache install orca
python -m chemistry_toolbox.software_management --cache-root /path/to/cache verify orca
```

The catalog records whether acquisition is automatic, requires registration, or
requires a commercial license. The manager never downloads or accepts a license on
the user's behalf. `archive` entries install a staged binary/prepared archive
atomically. `external` entries document assets whose executable runtime lives in
`.envs`. `manual` entries deliberately stop with instructions rather than reporting
a partial source tree as a working installation.

Archive installation is verified inside a temporary cache root before it is
published. A source archive or incorrectly prepared bundle that does not contain
the declared executable layout is rejected and leaves no installation directory.
Package-name matching only selects a staged package; it is not a substitute for
the entrypoint and command probes.

`RESEARCHCHEMBENCH_SOFTWARE_ROOT` selects the cache root at runtime. Paths in
manifests are cache-relative and are rejected if they escape that root.

## Legacy migration

```bash
python -m chemistry_toolbox.software_management \
  plan-v2 --legacy-root .software_cache
python -m chemistry_toolbox.software_management \
  --cache-root .software_cache_v2 \
  migrate-v2 --legacy-root .software_cache
```

The migration is non-destructive. It classifies each legacy path using
`legacy_layout.yaml`, hard-links regular files when possible, rewrites internal
symbolic links, excludes declared obsolete roots, and writes a receipt. The source
cache remains unchanged until the operator explicitly performs the final switch.
Host-specific script interpreters are rewritten copy-on-write to `/usr/bin/env -S`
launchers. `relocate-v2` also repairs declared wrapper/config paths and creates
declared cross-role compatibility links. It can apply the same repairs to an
already generated v2 cache.

## Validation levels

`researchchem-software verify` checks the managed installation contract in the
catalog. Rebuild `.envs` from the repository locks and use the toolbox checks for
runtime and scientific validation:

```bash
python chemistry_toolbox/scripts/check_mcp_profile_envs.py --no-write --timeout-seconds 120
python -m pytest -q
```

Binary installations are portable only across compatible Linux distribution,
architecture, libc, compiler-runtime, and driver stacks. `.envs` is intentionally
reconstructed instead of copied. Licensed archives and scientific data remain the
operator's responsibility and must not be redistributed without permission.
