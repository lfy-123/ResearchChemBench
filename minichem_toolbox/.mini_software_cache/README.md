# MiniChem Software Cache

This directory is copied with the toolbox but its binary payloads are not committed to Git.

Expected layout:

```text
.mini_software_cache/
├── gaussian/g16/                  # operator-supplied licensed Gaussian 16 tree
├── multiwfn/2026.7.15/            # Multiwfn noGUI distribution
├── runtimes/minichem/             # reconstructed Conda runtime
└── runtime_packs/minichem.tar.gz  # optional relocatable Conda archive
```

Run `scripts/bootstrap.sh` after copying the toolbox. The script reuses an existing runtime,
unpacks `runtime_packs/minichem.tar.gz`, or creates the runtime from `environment.yml` in that
order. Gaussian remains subject to its license and must only be copied where that license permits.
Set `MINICHEM_PYPI_INDEX_URL` when the default `https://pypi.org/simple` is not reachable.
