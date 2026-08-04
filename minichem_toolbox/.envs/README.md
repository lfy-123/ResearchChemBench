# MiniChem Environment Directory

This directory owns the dedicated Conda environment used only by MiniChem.

```text
.envs/
├── environment.yml
├── requirements-runtime.txt
├── manifest.json
├── minichem/                       # ignored physical Conda prefix
└── runtime_packs/minichem.tar.gz   # ignored optional conda-pack archive
```

Run `bash scripts/bootstrap.sh` from the toolbox root. The script reuses `.envs/minichem`, unpacks
the runtime archive, or creates the environment from `environment.yml`, in that order. It never
installs packages into the benchmark main environment or the comprehensive toolbox environments.

Set `MINICHEM_PYPI_INDEX_URL` when the default `https://pypi.org/simple` is not reachable.
Set `MINICHEM_PIP_OFFLINE=1` when reusing a complete runtime pack without network access.
