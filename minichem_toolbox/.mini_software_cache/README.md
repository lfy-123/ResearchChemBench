# MiniChem Software Cache

This directory is copied with the toolbox but its binary payloads are not committed to Git.

Expected layout:

```text
.mini_software_cache/
├── gaussian/g16/                  # operator-supplied licensed Gaussian 16 tree
└── multiwfn/2026.7.15/            # Multiwfn noGUI distribution
```

The dedicated Conda environment is intentionally stored separately under `.envs/minichem`.
Gaussian remains subject to its license and must only be copied where that license permits.
