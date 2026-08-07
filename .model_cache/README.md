# Rebuild the Model Cache Step by Step

This procedure reconstructs every required model file in `.model_cache` from a
fresh repository checkout. Run every command from the repository root and do
not skip a checksum step.

If the directory already contains downloaded model payloads, preserve them
outside the repository or start from a fresh checkout before following this
procedure.

## Step 0: Build the Required Environments

Follow the root README to build `.envs/researchchembench` and
`.envs/general-modern-openmpi5`. Confirm both Python executables exist:

```bash
test -x .envs/researchchembench/bin/python
test -x .envs/general-modern-openmpi5/bin/python
```

Expected result: both commands return silently with exit code zero.

## Step 1: Select the Destination

Use the repository's standard model-cache directory:

```bash
export RCB_ROOT="$(git rev-parse --show-toplevel)"
export RCB_MODEL_CACHE="$RCB_ROOT/.model_cache"

# Use all four variables. Different toolbox components read different names.
export RESEARCHCHEMBENCH_MODEL_CACHE="$RCB_MODEL_CACHE"
export RESEARCHCHEM_MINILM_MODEL_DIR="$RCB_MODEL_CACHE/all-MiniLM-L6-v2"
export RESEARCHCHEM_ACTION_EMBEDDING_CACHE="$RCB_MODEL_CACHE/action_embeddings.npz"
export XDG_CACHE_HOME="$RCB_MODEL_CACHE"

printf 'Model cache target: %s\n' "$RCB_MODEL_CACHE"
```

## Step 2: Initialize an Empty Cache

The following check allows the tracked README, metadata, and directory skeleton,
but stops if ignored model payloads already exist. This prevents an accidental
mixture of old and newly downloaded weights.

```bash
mkdir -p "$RCB_MODEL_CACHE"

if git ls-files --others --ignored --exclude-standard -- "$RCB_MODEL_CACHE" \
    | grep -q .; then
  echo "ERROR: $RCB_MODEL_CACHE already contains model payloads" >&2
  exit 1
fi

mkdir -p \
  "$RCB_MODEL_CACHE/all-MiniLM-L6-v2" \
  "$RCB_MODEL_CACHE/nequip/0.1" \
  "$RCB_MODEL_CACHE/deepmd/pretrained" \
  "$RCB_MODEL_CACHE/mace"
```

Expected result:

```text
all-MiniLM-L6-v2/
deepmd/pretrained/
mace/
nequip/0.1/
```

## Step 3: Download MiniLM and Generate Search Indexes

This repository script downloads the pinned quantized ONNX model and tokenizer,
checks their SHA-256 values, then generates Action and software-document indexes:

```bash
"$RCB_ROOT/.envs/researchchembench/bin/python" \
  chemistry_toolbox/scripts/cache_minilm_model.py
```

Verify the two downloaded files explicitly:

```bash
(
  cd "$RCB_MODEL_CACHE/all-MiniLM-L6-v2"
  sha256sum -c <<'EOF'
b941bf19f1f1283680f449fa6a7336bb5600bdcd5f84d10ddc5cd72218a0fd21  model.onnx
be50c3628f2bf5bb5e3a7f17b1f74611b2561a3a27eeab05e5aa30f411572037  tokenizer.json
EOF
)
```

Expected result: two `OK` lines, plus `action_embeddings.npz` and one
`software_docs_*.npz` file per indexed native-software document set. The `.npz`
files are generated locally and must not be downloaded from another project.

## Step 4: Download All NequIP and Allegro Models

The helper below downloads to a `.part` file, supports resuming, and only
publishes the final name after a complete transfer:

```bash
download_file() {
  url=$1
  destination=$2
  mkdir -p "$(dirname "$destination")"
  curl -fL --retry 8 --retry-delay 3 --retry-all-errors \
    -C - "$url" -o "$destination.part"
  mv "$destination.part" "$destination"
}

export NEQUIP_DEST="$RCB_MODEL_CACHE/nequip/0.1"
export NEQUIP_BASE="https://zenodo.org/records/18775904/files"

for name in \
  NequIP-OAM-S-0.1.nequip.zip \
  NequIP-OAM-M-0.1.nequip.zip \
  NequIP-OAM-L-0.1.nequip.zip \
  NequIP-OAM-XL-0.1.nequip.zip \
  NequIP-MP-L-0.1.nequip.zip \
  Allegro-OAM-L-0.1.nequip.zip \
  Allegro-MP-L-0.1.nequip.zip
do
  download_file "$NEQUIP_BASE/$name?download=1" "$NEQUIP_DEST/$name"
done
```

Verify all seven files before continuing:

```bash
(
  cd "$NEQUIP_DEST"
  sha256sum -c <<'EOF'
63d4bafd872850a014fd21dedeea416b61173a17750dee0b2b8dd2b126f407aa  NequIP-OAM-S-0.1.nequip.zip
3b528d235a98d6daa582ab17d4bac44aa108659b8a69046ba8f4f51c257fb328  NequIP-OAM-M-0.1.nequip.zip
5d01a4fab228abb3cdb6ace0033f93993729956bca6a42234a2a8816825b9a0f  NequIP-OAM-L-0.1.nequip.zip
99c3799b28026f1ecf66c413292038a27a0749d4d4d7cd0b3a642f2e68df9e9c  NequIP-OAM-XL-0.1.nequip.zip
dfbb68f6fab8d8135fc2be9c1cd92d468fe858254f2454fb891ea0da08dd6592  NequIP-MP-L-0.1.nequip.zip
3f0d3ca7bb136d4c2ee76278170fcbe756436f037e16c673a86e2c57d271c64e  Allegro-OAM-L-0.1.nequip.zip
ccc412a2e46b70528235067d45baab2bcc8ca48fda85516529de6caa030eeb8b  Allegro-MP-L-0.1.nequip.zip
EOF
)
```

Expected result: seven `OK` lines. A failed hash means the file must not be used;
leave the target cache inactive and rerun only that download.

## Step 5: Download All DeePMD Models

The URLs are pinned to immutable repository revisions. The toolbox uses the
patched multitask DPA-2.4 file and deliberately saves it under the configured
shorter destination name.

```bash
export DEEPMD_DEST="$RCB_MODEL_CACHE/deepmd/pretrained"

download_file \
  'https://huggingface.co/deepmodelingcommunity/DPA-3.1-3M/resolve/cac67b9c29b05d5dcd81c17e7be49bd433c887e8/DPA-3.1-3M.pt' \
  "$DEEPMD_DEST/DPA-3.1-3M.pt"
download_file \
  'https://huggingface.co/deepmodelingcommunity/DPA-3.2-5M/resolve/d948cf25158122ed8639b04791f252eec0ea8428/DPA-3.2-5M.pt' \
  "$DEEPMD_DEST/DPA-3.2-5M.pt"
download_file \
  'https://huggingface.co/deepmodelingcommunity/DPA-3.3-1M/resolve/3fd3eb72425381bcade321a89b3f77143f8fe128/DPA-3.3-1M.pt' \
  "$DEEPMD_DEST/DPA-3.3-1M.pt"
download_file \
  'https://huggingface.co/deepmodelingcommunity/DPA-2.4-7M/resolve/0634b77077973a8652ce292a71eed999f5161630/DPA-2.4-7M-patched-mt.pt' \
  "$DEEPMD_DEST/dpa-2.4-7M.pt"
download_file \
  'https://huggingface.co/deepmodelingcommunity/DPA3-Omol-Large/resolve/a1075fbde99dd542348083d72a3e4468bb02b6dc/DPA3-Omol-Large.pt' \
  "$DEEPMD_DEST/DPA3-Omol-Large.pt"
```

Verify all five files:

```bash
(
  cd "$DEEPMD_DEST"
  sha256sum -c <<'EOF'
86dd3a804d78ca5d203ebf98747e8f16dff9713ba8950097ceb760b161e19907  DPA-3.1-3M.pt
876354744aeaae17b2639a6a690514470273784f2b4836280850f50cbb799165  DPA-3.2-5M.pt
36fe440c111108d60cda54aa7d3fccac743794de25abef4d49564b9fb896a55b  DPA-3.3-1M.pt
904eb5560af9ff644347dedd3ebf1e9c97929d02ee37ce3cbe895de3df711198  dpa-2.4-7M.pt
dc4d252b31450b41eb3546cc48f640ad0831c0b5d069ce27d996e0ff58fc037a  DPA3-Omol-Large.pt
EOF
)
```

Expected result: five `OK` lines. The moving `dp pretrained download` registry
is convenient but is not used for this strict reconstruction.

### If a Large Download Is Interrupted

Do not delete the `.part` file. `curl -C -` resumes it on the next run. Only the
successful command moves it to the final filename, and the following checksum
step still decides whether it can be used. A very slow but advancing transfer is
a network condition, not a reason to bypass the checksum.

If an existing trusted cache is available on the same site, an offline recovery
is also valid. Copy only files whose source checksum already matches this README,
then rerun the complete destination checksum blocks in Steps 4 and 5:

```bash
export TRUSTED_MODEL_CACHE=/path/to/trusted/.model_cache

for name in \
  NequIP-OAM-S-0.1.nequip.zip \
  NequIP-OAM-M-0.1.nequip.zip \
  NequIP-OAM-L-0.1.nequip.zip \
  NequIP-OAM-XL-0.1.nequip.zip \
  NequIP-MP-L-0.1.nequip.zip \
  Allegro-OAM-L-0.1.nequip.zip \
  Allegro-MP-L-0.1.nequip.zip
do
  cp --reflink=auto \
    "$TRUSTED_MODEL_CACHE/nequip/0.1/$name" "$NEQUIP_DEST/$name"
done

for name in \
  DPA-3.1-3M.pt DPA-3.2-5M.pt DPA-3.3-1M.pt \
  dpa-2.4-7M.pt DPA3-Omol-Large.pt
do
  cp --reflink=auto \
    "$TRUSTED_MODEL_CACHE/deepmd/pretrained/$name" "$DEEPMD_DEST/$name"
done
```

This is an offline reconstruction, not an upstream download test. Record which
method was used. Never accept matching filenames without matching SHA-256 values.

## Step 6: Optionally Prewarm the Two MACE Aliases

The MACE cache is not part of the 12 selectable resources, but prewarming it
allows the installed `medium` and `medium-mpa-0` aliases to run without a later
network request:

```bash
"$RCB_ROOT/.envs/general-modern-openmpi5/bin/python" - <<'PY'
from mace.calculators import mace_mp

mace_mp(model="medium", device="cpu", default_dtype="float64")
mace_mp(model="medium-mpa-0", device="cpu", default_dtype="float64")
PY

test -s "$RCB_MODEL_CACHE/mace/20231203mace128L1_epoch199model"
test -s "$RCB_MODEL_CACHE/mace/macempa0mediummodel"
```

CHGNet weights and OpenFF NAGL AM1-BCC models come from their locked Python
packages. An empty `OPENFF_NAGL_MODELS/` directory is normal.

## Step 7: Verify the Complete Candidate Cache

This check remaps every registered `.model_cache/...` path to the selected
candidate root, verifies all 12 hashes, and does not modify tracked files:

```bash
"$RCB_ROOT/.envs/researchchembench/bin/python" - "$RCB_MODEL_CACHE" <<'PY'
import hashlib
import json
import sys
from pathlib import Path

root = Path(sys.argv[1]).resolve()
config = json.loads(Path("chemistry_toolbox/config/toolbox_resources.json").read_text())
models = [item for item in config["resources"] if item.get("kind") == "model_checkpoint"]
for item in models:
    relative = Path(item["path"]).relative_to(".model_cache")
    path = root / relative
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != item["checksum"]:
        raise SystemExit(f"FAIL {item['id']}: {path} -> {digest}")
    print(f"PASS {item['id']}: {path}")
print(f"Verified {len(models)} registered model checkpoints")
PY

"$RCB_ROOT/.envs/researchchembench/bin/python" \
  chemistry_toolbox/scripts/verify_toolbox.py --no-write
```

Expected result: 12 `PASS` lines, `Verified 12 registered model checkpoints`,
and all `verify_toolbox.py` checks marked `pass`.

Inspect the final payload:

```bash
du -sh "$RCB_MODEL_CACHE"
find "$RCB_MODEL_CACHE" -maxdepth 3 -type f -printf '%P\t%s bytes\n' | sort
```

Transient directories such as `huggingface/`, `matplotlib/`,
`mesa_shader_cache/`, `pip/`, `opencode/`, and zero-byte lock files are not
reconstruction inputs.

## Step 8: Confirm the Active Cache

After Step 7 passes, clear the temporary environment overrides and verify the
standard runtime configuration:

```bash
unset RCB_MODEL_CACHE
unset RESEARCHCHEMBENCH_MODEL_CACHE
unset RESEARCHCHEM_MINILM_MODEL_DIR
unset RESEARCHCHEM_ACTION_EMBEDDING_CACHE
unset XDG_CACHE_HOME

"$RCB_ROOT/.envs/researchchembench/bin/python" \
  chemistry_toolbox/scripts/configure_toolbox_resources.py \
  --verify-only --quick --no-write
```

Expected result: the runtime resolves all model files from `.model_cache` and
the verification command exits successfully.
