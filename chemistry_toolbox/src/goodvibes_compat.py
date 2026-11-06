"""Explicit GoodVibes 4.3 --check adapter; no changes to installed packages."""
from __future__ import annotations

import copy
import importlib.metadata
import json
from pathlib import Path
import sys

ADAPTER_VERSION = "goodvibes-check-1"


def solvation_record(value, filename, read_initial):
    """Normalize metadata only; a blank parser value is never assumed gas phase."""
    source = "parsed_metadata"
    if isinstance(value, (tuple, list)) and len(value) == 2 and all(isinstance(x, str) and x.strip() for x in value):
        return list(value), source
    if not isinstance(value, str) or not value.strip():
        source = "native_read_initial"
        initial = read_initial(filename)
        # Require a recognized, normally terminated calculation before using the
        # native initial reader's independent model-chemistry metadata.
        value = initial[1] if initial[2] == "Normal" and initial[0] != "none/none" else None
    if not isinstance(value, str) or not value.strip():
        return ["unknown", "unknown"], "unavailable"
    return [value.strip(), value.strip()], source


def check_metadata(thermo_data, options, level_of_theory, *, native_check, read_initial, records):
    normalized = {}
    for key, entry in thermo_data.items():
        cloned = copy.copy(entry)
        cloned.solvation_model, source = solvation_record(entry.solvation_model, entry.file, read_initial)
        records.append({"file": entry.file, "solvation_model": cloned.solvation_model[1], "source": source})
        normalized[key] = cloned
    return native_check(normalized, options, level_of_theory)


def main():
    if importlib.metadata.version("goodvibes") != "4.3.0":
        raise RuntimeError("The GoodVibes check adapter is validated for version 4.3.0")
    from goodvibes import GoodVibes as cli
    from goodvibes.io import read_initial
    original = cli.check_files
    records = []
    def checked(thermo_data, options, level_of_theory):
        return check_metadata(thermo_data, options, level_of_theory,
                              native_check=original, read_initial=read_initial, records=records)
    cli.check_files = checked
    try:
        cli.main()
    finally:
        cli.check_files = original
    # Native JSON is written before --check. Append metadata provenance only;
    # thermochemistry values and the native scientific checks stay untouched.
    if "--json" in sys.argv:
        output = Path(sys.argv[sys.argv.index("--json") + 1])
        payload = json.loads(output.read_text())
        payload["toolbox_compatibility"] = {"adapter": ADAPTER_VERSION, "metadata": records}
        output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


if __name__ == "__main__":
    main()
