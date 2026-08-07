# Rebuild the Software Cache Step by Step

This guide reconstructs a functional `.software_cache` from a fresh repository
checkout. If the directory already contains installed software, preserve it
outside the repository or start from a fresh checkout before following this
procedure.

The cache is not a Python environment. Rebuild `.envs/` first from the tracked
environment definitions. The cache then holds native binaries, source snapshots,
original packages, scientific data, local state, documentation, build logs, and
validation evidence.

A fully public build can be automated. A complete build cannot be unattended
because several programs require registration, license acceptance, purchase, or
operator-supplied scientific data. The commands below stop at those boundaries
instead of downloading unofficial copies.

## Step 0: Prepare the Repository Environments

Follow the root `README.md` and build all required `.envs` profiles. At minimum,
the framework and the two environments used in the tested examples must exist:

```bash
test -x .envs/researchchembench/bin/python
test -x .envs/general-modern-openmpi5/bin/python
test -x .envs/equivariant-ml/bin/x86_64-conda-linux-gnu-gfortran
```

Expected result: all three checks return silently with exit code zero. Do not
copy `.envs` from another host; reconstruct it from the repository locks.

## Step 1: Select an Empty Destination

Run every later command from the repository root and use the standard software
cache path:

```bash
export RCB_ROOT="$(git rev-parse --show-toplevel)"
export RCB_PYTHON="$RCB_ROOT/.envs/researchchembench/bin/python"
export RESEARCHCHEMBENCH_SOFTWARE_ROOT="$RCB_ROOT/.software_cache"

mkdir -p "$RESEARCHCHEMBENCH_SOFTWARE_ROOT"
if git ls-files --others --ignored --exclude-standard -- \
    "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" | grep -q .; then
  echo "ERROR: $RESEARCHCHEMBENCH_SOFTWARE_ROOT already contains software payloads" >&2
  exit 1
fi
```

`RESEARCHCHEMBENCH_SOFTWARE_ROOT` is also read by toolbox runtime path
resolution. Keep it exported while testing the candidate.

## Step 2: Initialize and Inspect the Managed Layout

```bash
"$RCB_PYTHON" -m chemistry_toolbox.software_management \
  --cache-root "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" init

"$RCB_PYTHON" -m chemistry_toolbox.software_management \
  --cache-root "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" status \
  > "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/status-initial.json"

"$RCB_PYTHON" - "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/status-initial.json" <<'PY'
import json, sys
items = json.load(open(sys.argv[1]))
print(f"catalog entries: {len(items)}")
print(f"initially installed: {sum(item['installed'] for item in items)}")
PY
```

Expected result: `catalog entries: 37` and `initially installed: 0` for a new
cache. Initialization creates these fixed roles:

| Directory | Reconstruct or retain |
|---|---|
| `packages/` | Original downloaded/operator-supplied archives and their hashes |
| `installations/` | Published runnable native installations |
| `sources/` | Pinned source checkouts; not automatically runnable |
| `shared/` | MPI sources/runtimes, pseudopotentials, basis sets, parameters |
| `state/` | Local profiles and application state; never put credentials here |
| `documentation/` | Generated local software-document index and optional snapshots |
| `build/` | Rebuildable compiler output and diagnostic logs |
| `validation/` | Smoke inputs, outputs, and reconstruction evidence |
| `staging/` | Temporary atomic-install workspace; normally empty after a run |
| `receipts/` | Package hashes, installation records, and migration records |

The catalog is
`chemistry_toolbox/software_management/manifests/catalog.yaml`. `automatic`
means publicly obtainable, not necessarily precompiled. `manual` means a form,
account, or license is required. `bundled` and `external` entries are supplied
by tracked data, `.envs`, or optional local state.

## Step 3: Download Public Package and Source Inputs

The helper below fetches exactly one Git commit without downloading full
history. It also verifies the checked-out commit before returning:

```bash
export RCB_SOURCES="$RESEARCHCHEMBENCH_SOFTWARE_ROOT/sources"

clone_commit() {
  url=$1
  destination=$2
  commit=$3
  if [ -d "$destination/.git" ]; then
    test "$(git -C "$destination" rev-parse HEAD)" = "$commit"
    return
  fi
  mkdir -p "$(dirname "$destination")"
  git init -q "$destination"
  git -C "$destination" remote add origin "$url"
  git -C "$destination" fetch -q --depth 1 origin "$commit"
  git -C "$destination" checkout -q --detach FETCH_HEAD
  test "$(git -C "$destination" rev-parse HEAD)" = "$commit"
}

mkdir -p \
  "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/acpype/2023.10.27" \
  "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/gmx_mmpbsa/1.6.5" \
  "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/rmg_assets/4.0.0" \
  "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/shared/mpi/openmpi/source"

"$RCB_PYTHON" -m pip download --no-deps acpype==2023.10.27 \
  -d "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/acpype/2023.10.27"
"$RCB_PYTHON" -m pip download --no-deps gmx_MMPBSA==1.6.5 \
  -d "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/gmx_mmpbsa/1.6.5"

clone_commit https://github.com/emartineznunez/AutoMeKin.git \
  "$RCB_SOURCES/automekin/source" 6c15f6fb043d07ea30c1c2d312a740286656a257
clone_commit https://github.com/aoterodelaroza/critic2.git \
  "$RCB_SOURCES/critic2/source" 43ca79442d1deda6b86b0dbfbc4ee026321f772b
clone_commit https://github.com/deGrootLab/pmx.git \
  "$RCB_SOURCES/pmx/develop-0dd5f0a" 0dd5f0a9cdf26109eff98bdfeb4ac4e55353aa76
clone_commit https://github.com/TheoChem-VU/PyFrag.git \
  "$RCB_SOURCES/pyfrag/2019/source" af2a122d7676ee1578ac895ac4f076fdecaccdf5
clone_commit https://github.com/sharc-md/sharc4.git \
  "$RCB_SOURCES/sharc/source" 8f11e3f521857f80c9747d60eb930d14dbd0e89c
clone_commit https://bitbucket.org/sousaw/shengbte.git \
  "$RCB_SOURCES/shengbte/source" b0d209068239c37fc86d2021efda131ad854f1c1
clone_commit https://github.com/rouyang2017/SISSO.git \
  "$RCB_SOURCES/sisso/3.5/source" bc18cae50e1e204cd72b2a9dfd6832225b0d8ccc
clone_commit https://github.com/tdep-developers/tdep.git \
  "$RCB_SOURCES/tdep/25.03/source" d38f435d75f33e0e86629ce7b7059ce95fbc06c5
clone_commit https://github.com/wannier-developers/wannier90.git \
  "$RCB_SOURCES/wannier90/3.1.0" 1d6b187374a2d50b509e5e79e2cab01a79ff7ce1

curl -fL --retry 8 --retry-delay 3 --retry-all-errors \
  https://github.com/ReactionMechanismGenerator/RMG-Py/archive/refs/tags/4.0.0.tar.gz \
  -o "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/rmg_assets/4.0.0/RMG-Py-4.0.0.tar.gz"
curl -fL --retry 8 --retry-delay 3 --retry-all-errors \
  https://github.com/ReactionMechanismGenerator/RMG-database/archive/refs/tags/4.0.0.tar.gz \
  -o "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/rmg_assets/4.0.0/RMG-database-4.0.0.tar.gz"
curl -fL --retry 8 --retry-delay 3 --retry-all-errors \
  https://download.open-mpi.org/release/open-mpi/v4.1/openmpi-4.1.8.tar.bz2 \
  -o "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/shared/mpi/openmpi/source/openmpi-4.1.8.tar.bz2"
```

Verify the deterministic public package inputs:

```bash
sha256sum -c <<EOF
58690dac7ba83961ab84ca995b712d55ec799bab0e4bd4d4dac794e306acee9b  $RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/acpype/2023.10.27/acpype-2023.10.27-py3-none-any.whl
9a21be091d8dade8862cd957c51e97c0d72fedd7927bb63105234e13ba257cfc  $RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/gmx_mmpbsa/1.6.5/gmx_mmpbsa-1.6.5-py3-none-any.whl
7012256a43a9c04cce47ecbdf3f96001dd84d3754fd0d1d8969564e07a2711cb  $RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/rmg_assets/4.0.0/RMG-Py-4.0.0.tar.gz
2fb8f2e365845347c44a88dc59eadc4aab192ce8d7d93febfb941c1f2f5553cc  $RESEARCHCHEMBENCH_SOFTWARE_ROOT/packages/rmg_assets/4.0.0/RMG-database-4.0.0.tar.gz
466f68e3132a1dc02710cc2011fafced8336d98359fa2dae4dddcfd5719f12a9  $RESEARCHCHEMBENCH_SOFTWARE_ROOT/shared/mpi/openmpi/source/openmpi-4.1.8.tar.bz2
EOF
```

GNINA is a public raw executable, not an archive. Download and stage it as
follows. The file is about 2 GB:

```bash
curl -fL --retry 8 --retry-delay 3 --retry-all-errors -C - \
  https://github.com/gnina/gnina/releases/download/v1.3.3/gnina.cuda12.8.static \
  -o "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/gnina.cuda12.8.static.part"
mv "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/gnina.cuda12.8.static.part" \
  "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/gnina.cuda12.8.static"
echo '3340c1f49cd3c7c84d8699182a1c6af13c7fa2a22448d1204640446106f72172  '"$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/gnina.cuda12.8.static" | sha256sum -c
```

OpenMolcas and KinBot are also public, but their runtime construction is tied to
the matching `.envs` profiles. Obtain their exact source only when rebuilding
those profiles:

```bash
clone_commit https://github.com/zadorlab/KinBot.git \
  "$RCB_SOURCES/kinbot/2.2.2" 2b530ad24a4dd6a52743a783752821d5d2560519

if [ ! -d "$RCB_SOURCES/openmolcas/25.10/.git" ]; then
  git clone --branch v25.10 --depth 1 --recurse-submodules --shallow-submodules \
    https://gitlab.com/Molcas/OpenMolcas.git "$RCB_SOURCES/openmolcas/25.10"
fi
test "$(git -C "$RCB_SOURCES/openmolcas/25.10" rev-parse HEAD)" = \
  4abfbe4647f11adf036347ac0d63a8f5bdb6ed05
if git -C "$RCB_SOURCES/openmolcas/25.10" submodule status | grep -q '^-'; then
  git -C "$RCB_SOURCES/openmolcas/25.10" \
    submodule update --init --recursive --depth 1
fi
if git -C "$RCB_SOURCES/openmolcas/25.10" submodule status | grep -q '^-'; then
  echo 'ERROR: OpenMolcas submodules are incomplete' >&2
  exit 1
fi
```

If a submodule connection is interrupted, rerun only the `submodule update`
command. A leading `-` in `git submodule status` means the source tree is still
incomplete and must not be used for a build.

## Step 4: Obtain Free Packages with Manual Terms

The following programs are free to use under their own terms, but their sites
do not provide a stable anonymous command suitable for this repository. Each
operator must use the official page, preserve the exact filename, and compare
the hash before staging:

| ID | Version and official page | Expected filename | Reference SHA-256 |
|---|---|---|---|
| `multiwfn` | 2026.7.15 [official](http://sobereva.com/multiwfn/) | `Multiwfn_2026.7.15_bin_Linux_noGUI.zip` | `c5f399cf48cb2f7fedcba82396c564bb0873d2da385a84b12bbb35d0000cbf96` |
| `vesta` | 3.90.5a [official](https://jp-minerals.org/vesta/jp/download.html) | `VESTA-gtk3-x86_64-3.90.5a.tar.bz2` | `5af3be45cd19d4b601b9d3e190d39fd8cf66f013e012420839847bb4519a33a6` |
| `vaspkit` | 1.5.1 [official](https://vaspkit.com/installation.html) | `vaspkit.1.5.1.linux.x64.tar.gz` | `41bbdc0759f72cd43ef7e2f541d228a639bd95dba2a549398b28f47d760d72b1` |
| `newton_x` | package 26a [official](https://newtonx.org/download/) | `newton-x-package-26a.tar.gz` | `66ce15b3bba454eb241ce8fbde917c53b2478e58a53720581db5df2e344195fe` |

Hashes identify the packages used for the validated cache. If the official
provider publishes a newer build under the same version, do not silently accept
it: inspect the change, update the catalog and tests, then record the new hash.

## Step 5: Obtain Registered and Licensed Packages

These downloads cannot be automated by this project. Log in to the official
provider, accept the applicable terms, and place the original package outside
the repository before calling `stage`.

| ID | Version | Access | Official provider | Accepted package form |
|---|---:|---|---|---|
| `amber_pmemd` | 26 | Academic/commercial license | [Amber](https://ambermd.org/GetAmber.php) | `amber26-prepared*.tar.*` after licensed build |
| `charmm` | c50b2 | Academic registration or commercial | [CHARMM](https://academiccharmm.org/) | `charmm50b2-prepared*.tar.*` |
| `gamess` | 2024 R2 P1 | Free registration | [GAMESS](https://www.msg.chem.iastate.edu/GAMESS/download/register/) | `gamess-2024-r2-p1-prepared.tar.*` |
| `gaussian` | G16 C.01 | Commercial | [Gaussian](https://gaussian.com/) | `gaussian-g16-prepared.tar.*` |
| `lobster` | 5.1.0 | Free academic registration | [LOBSTER](https://www.cohp.de/) | official archive |
| `multiwell` | 2023.1 | Free form/terms | [MultiWell](https://multiwell.engin.umich.edu/downloads/) | currently manual; no runnable cache contract |
| `namd` | 3.0.2 | Free registration | [NAMD](https://www.ks.uiuc.edu/Research/namd/) | `NAMD_3.0.2_Linux-x86_64-multicore*.tar.gz` |
| `orca` | 6.1.1 OpenMPI 4.1 | Free academic registration | [FACCTs](https://www.faccts.de/orca/) | exact `...openmpi418_nodmrg.tar.xz` archive |
| `vasp` | 6.3.2 | Commercial | [VASP](https://www.vasp.at/) | prepared binary archive; POTCAR imported separately |

Never put credentials or license keys in the cache. Do not redistribute these
packages, installed trees, or VASP POTCAR data unless the license permits it.

## Step 6: Build Source Programs into Prepared Archives

The manager publishes a source build only after it has been converted to a
prepared archive containing the entrypoint declared in `catalog.yaml`. This
separates site-specific compilation from deterministic installation.

The following complete Wannier90 example was tested from an empty cache:

```bash
export W90_SOURCE="$RCB_SOURCES/wannier90/3.1.0"
export W90_BUILD="$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/wannier90/3.1.0"
export W90_FC="$RCB_ROOT/.envs/equivariant-ml/bin/x86_64-conda-linux-gnu-gfortran"
export W90_LIB="$RCB_ROOT/.envs/general-modern-openmpi5/lib"

mkdir -p "$W90_BUILD/prefix/wannier90-3.1.0"
cp "$W90_SOURCE/config/make.inc.gfort" "$W90_SOURCE/make.inc"
make -C "$W90_SOURCE" -j4 wannier \
  F90="$W90_FC" FCOPTS='-O2 -fbacktrace' \
  LIBS="-L$W90_LIB -llapack -lblas"
cp "$W90_SOURCE/wannier90.x" \
  "$W90_BUILD/prefix/wannier90-3.1.0/wannier90.x"

export LD_LIBRARY_PATH="$W90_LIB${LD_LIBRARY_PATH:+:$LD_LIBRARY_PATH}"
"$W90_BUILD/prefix/wannier90-3.1.0/wannier90.x" --version

tar -C "$W90_BUILD/prefix" -cJf \
  "$W90_BUILD/wannier90-3.1.0-prepared.tar.xz" wannier90-3.1.0
```

Expected output: `Wannier90: 3.1.0`. The runtime library path matters because
this build links to libraries reconstructed in `.envs/general-modern-openmpi5`.

Other `BUILD` entries use the same prepared-archive contract. Consult the pinned
source's own build instructions, use the repository environment named in
`chemistry_toolbox/config/mcp_profiles.yaml`, and make the archive contain these
relative entrypoints:

| ID | Prepared archive must contain |
|---|---|
| `automekin` | `bin/amk.sh` |
| `bagel` | `bin/BAGEL` |
| `critic2` | `bin/critic2` |
| `mesmer` | `bin/mesmer` |
| `mess` | `mess` |
| `openmolcas` | `pymolcas` plus its basis/runtime tree |
| `pyfrag` | `bin/pyfrag-orca` including the tracked compatibility patch |
| `sharc` | `bin/sharc.x` |
| `shengbte` | `ShengBTE` |
| `sisso` | `bin/SISSO_run` and `bin/SISSO_predict` |
| `tdep` | `bin/extract_forceconstants`; use the validated `-O0` constraint |

This repository does not currently encode all upstream compiler invocations as
automatic recipes. Do not claim a complete clean-room build until each required
entry above has a prepared archive and passes Step 7. The prior build notes are
in `docs/tools_v2/CHEMISTRY_TOOLBOX_ADJUSTMENT_LOG.md` and
`docs/tools_v2/CHEMISTRY_TOOLBOX_SOFTWARE_EXPANSION_LOG.md`.

## Step 7: Stage, Install, Verify, and Smoke Each Package

Use the same lifecycle for every archive or raw binary:

```bash
stage_install_verify() {
  software_id=$1
  package=$2
  "$RCB_PYTHON" -m chemistry_toolbox.software_management \
    --cache-root "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" \
    stage "$software_id" "$package"
  "$RCB_PYTHON" -m chemistry_toolbox.software_management \
    --cache-root "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" install "$software_id"
  "$RCB_PYTHON" -m chemistry_toolbox.software_management \
    --cache-root "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" verify "$software_id"
}

stage_install_verify multiwfn /path/to/Multiwfn_2026.7.15_bin_Linux_noGUI.zip
stage_install_verify vesta /path/to/VESTA-gtk3-x86_64-3.90.5a.tar.bz2
stage_install_verify gnina "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/gnina.cuda12.8.static"
stage_install_verify wannier90 \
  "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/build/wannier90/3.1.0/wannier90-3.1.0-prepared.tar.xz"
```

Run real command smokes after structural verification:

```bash
MULTIWFN_HOME="$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/multiwfn/2026.7.15/Multiwfn_2026.7.15_bin_Linux_noGUI"
(cd "$MULTIWFN_HOME" && printf 'q\n' | ./Multiwfn_noGUI examples/H2.fch) \
  | grep 'Loaded examples/H2.fch successfully'

(cd "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/vesta/3.90.5a" && \
  timeout 10 ./VESTA -nogui)
"$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/gnina/1.3.3/gnina" --version
"$RESEARCHCHEMBENCH_SOFTWARE_ROOT/installations/wannier90/3.1.0-source/wannier90.x" --version
```

`stage` retains the original package and hash. `install` builds in `staging/`,
checks declared entrypoints, atomically publishes the installation, and writes
`receipts/<id>/<version>.json`. A failed verification leaves no partial published
installation. If multiple accepted files are staged, pass the desired file with
`install SOFTWARE_ID --package /exact/path`.

Do not call `install` for `handler: external` or `handler: manual` entries.

## Step 8: Reconstruct Shared Scientific Data

Model checkpoints belong in `.model_cache`, not here. Public pseudopotentials
and parameter archives belong under `shared/scientific-data` at the paths and
hashes declared in `chemistry_toolbox/config/toolbox_resources.json`.

Install the GPAW data without modifying the user's home directory:

```bash
export GPAW_DATA="$RESEARCHCHEMBENCH_SOFTWARE_ROOT/shared/scientific-data/gpaw-setups"
export GPAW_ARCHIVE="$RESEARCHCHEMBENCH_SOFTWARE_ROOT/shared/scientific-data/gpaw-setups-24.11.0.tar.gz"
mkdir -p "$GPAW_DATA"
curl -fL --retry 8 --retry-delay 3 --retry-all-errors -C - \
  https://wiki.fysik.dtu.dk/gpaw-files/gpaw-setups-24.11.0.tar.gz \
  -o "$GPAW_ARCHIVE.part"
mv "$GPAW_ARCHIVE.part" "$GPAW_ARCHIVE"
"$RCB_ROOT/.envs/general-modern-openmpi5/bin/gpaw" install-data \
  --tarball "$GPAW_ARCHIVE" --no-register "$GPAW_DATA"
test "$(find "$GPAW_DATA" -type f | wc -l)" -gt 0
```

The selected GPAW dataset version is fixed at `24.11.0`. An interrupted
`curl` leaves a resumable `.part`; do not treat an empty destination as success.

Download the QE SSSP, Siesta/ABINIT PseudoDojo, and DFTB parameter archives from
the `source_url` values in `toolbox_resources.json`, place them at each declared
`archive.path`, and then run:

```bash
"$RCB_PYTHON" chemistry_toolbox/scripts/configure_toolbox_resources.py \
  --quick --no-write
```

The script verifies hashes and paths. Run it without `--no-write` only after all
operator-provided archives are present and extraction/symlink creation is desired.

For an authorized VASP potential library, use the dedicated importer:

```bash
"$RCB_PYTHON" chemistry_toolbox/scripts/import_vasp_potcar_library.py --help
```

VASP POTCAR files are licensed, non-redistributable inputs. They cannot be
reconstructed from public commands.

## Step 9: Rebuild Documentation and Local State

Generate the documentation index from tracked configuration:

```bash
"$RCB_PYTHON" chemistry_toolbox/scripts/cache_software_documentation.py
test -s "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/documentation/index.json"
```

To add bounded official HTML/PDF snapshots:

```bash
"$RCB_PYTHON" chemistry_toolbox/scripts/cache_software_documentation.py \
  --download --max-mib 100
```

Network failures are recorded as metadata. Directories such as
`documentation_alias_fix_seed_*` and `documentation_pre_version_fix_*` are old
migration artifacts and must not be recreated.

Create AiiDA, CENSO, RMG, PubChem, or VASPKIT state only through their normal
configuration commands. Never transfer API keys in `state/` or commit
`config.local.env`.

## Step 10: Validate the Candidate

First validate the manager itself, then the installed subset, then toolbox
integration:

```bash
"$RCB_PYTHON" -m pytest -q chemistry_toolbox/tests/test_software_management.py

"$RCB_PYTHON" -m chemistry_toolbox.software_management \
  --cache-root "$RESEARCHCHEMBENCH_SOFTWARE_ROOT" verify \
  > "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/validation/manager-verify.json" || true

"$RCB_PYTHON" chemistry_toolbox/scripts/configure_toolbox_resources.py \
  --verify-only --quick --no-write

"$RCB_PYTHON" chemistry_toolbox/scripts/check_mcp_profile_envs.py \
  --no-write --timeout-seconds 120
```

The all-software manager command returns nonzero until every required native
entry has been installed. Inspect `manager-verify.json`; do not hide missing
licensed programs. A public-only or partial cache is valid for the software it
reports as `pass`, but it is not a complete replacement for the active cache.

Inspect payload and receipts:

```bash
du -sh "$RESEARCHCHEMBENCH_SOFTWARE_ROOT"
find "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/receipts" -type f -print | sort
find "$RESEARCHCHEMBENCH_SOFTWARE_ROOT/staging" -mindepth 1 -print
```

Expected result: every installed program has a receipt and `staging/` is empty.

## Step 11: Resume, Transfer, or Finish

Downloads ending in `.part` are incomplete. Rerun the same `curl -C -` command;
do not rename the file until its checksum passes. Failed builds remain in
`build/` for diagnosis and may be removed after the corresponding installation
and receipt pass.

For an exact authorized transfer between compatible hosts, preserve permissions,
links, and all license constraints. A copied compiled cache is only portable
across compatible Linux distribution, CPU architecture, glibc/libstdc++, MPI,
compiler runtime, and GPU driver stacks.

After all validation passes, clear the explicit override and verify that the
runtime resolves the standard cache:

```bash
unset RESEARCHCHEMBENCH_SOFTWARE_ROOT

"$RCB_PYTHON" -m chemistry_toolbox.software_management status
```

Expected result: the manager resolves `.software_cache` and reports the rebuilt
installations without path errors.
