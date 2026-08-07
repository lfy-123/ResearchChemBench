# Software cache management v2

## Result

The active cache is `.software_cache`. The untouched legacy source cache is retained
as `.software_cache_legacy_20260806`. Temporary incomplete and misclassified v2
candidates were removed after the final switch.

The cache layout is now:

| Directory | Responsibility |
|---|---|
| `documentation/` | Searchable software documentation |
| `installations/` | Runnable native software |
| `packages/` | Original or operator-provided installation packages |
| `sources/` | Inactive source snapshots |
| `shared/` | MPI, basis sets, pseudopotentials, and shared scientific data |
| `state/` | Mutable application state and local profiles |
| `build/` | Rebuildable build products and logs |
| `validation/` | Smoke inputs, reference outputs, and validation artifacts |
| `staging/` | Temporary atomic installation workspace |
| `receipts/` | Migration, relocation, and installation records |

Conda/Python runtimes remain in `.envs` and are rebuilt from the repository's exact
locks. They are not stored inside the software cache.

## Management interface

Implementation: `chemistry_toolbox/software_management`.

```bash
python -m chemistry_toolbox.software_management --cache-root /path/to/cache init
python -m chemistry_toolbox.software_management --cache-root /path/to/cache status
python -m chemistry_toolbox.software_management --cache-root /path/to/cache stage SOFTWARE_ID /path/to/package
python -m chemistry_toolbox.software_management --cache-root /path/to/cache install SOFTWARE_ID
python -m chemistry_toolbox.software_management --cache-root /path/to/cache verify SOFTWARE_ID
```

The catalog records acquisition and license policy. Registered or commercial
software is never downloaded or licensed automatically. Installations are extracted
and verified in staging, then atomically published. A failed verification leaves no
partial installation.

## Migration

The final migration classified 128,800 legacy paths with no destination collisions:

- 114,578 regular files hard-linked without modifying the legacy source.
- 12,226 directories and 1,996 symbolic links migrated.
- 57,917 obsolete, dangling, generated, or cache-embedded Conda paths excluded.
- No unresolved symbolic links remained.
- Six GAMESS host-specific shebangs made portable.
- 53 AIRSS absolute wrapper paths rewritten relative to their launchers.
- PyFrag received a managed compatibility link from its installation to `sources/`.
- RMG state uses `RESEARCHCHEMBENCH_SOFTWARE_ROOT` instead of a server path.
- `gmx_MMPBSA` is rebuilt in `.envs/gmx-mmpbsa`; only its package provenance and
  validation data remain in `.software_cache`.

Runtime path resolution uses `RESEARCHCHEMBENCH_SOFTWARE_ROOT`. Active configuration,
source, MCP, script, and test references were rewritten to the managed layout; the
path rewrite audit reports zero pending references.

## Verification

Final checks on the active cache:

- Software-management catalog: 37/37 passed.
- MCP runtime profiles: 50/50 ready, 150 public Actions catalogued.
- Scientific resources: 27/27 passed.
- Requested software inventory: 57 configured plus one QCSchema specification,
  complete 58/58.
- Representative native/scientific tests: ORCA, Critic2, TDEP, SHARC, KinBot,
  AIRSS, Multiwfn, NWChem, PyFrag, and `gmx_MMPBSA` passed.
- Full repository suite: 589 passed, 1 conditionally skipped.
- No unresolved cache symlinks. SISSO retains two intentional Intel MPI compatibility
  loop links (`release` and `release_mt`).

The cache is not a universal binary distribution. Moving native binaries requires a
compatible Linux/CPU/libc/compiler runtime. Rebuild `.envs` from locks on the target
server, keep licensed packages private, set `RESEARCHCHEMBENCH_SOFTWARE_ROOT` when
using a non-default location, and rerun both profile and scientific tests.
