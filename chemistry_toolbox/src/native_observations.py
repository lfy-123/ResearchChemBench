"""Versioned, stage-local observations. No mechanism or scientific verdicts."""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path
import copy
import re
import gzip
import time

PARSER_VERSION = "native-observations-4"
_ORCA_MODE = re.compile(r"^\s*(\d+)\s*:\s*([+-]?\d+(?:\.\d+)?)\s+cm\*\*-1")


def parse_native_observations(software_id, files, calculation_context=None):
    paths = [Path(p) for p in files] if isinstance(files, (list, tuple)) else [Path(files)]
    path = paths[0]
    if not path.is_file():
        return {"parser_version": PARSER_VERSION, "software_id": software_id,
                "status": "missing", "source": str(path), "frequency_blocks": []}
    stat = path.stat()
    # Some filesystems coalesce rapid same-size writes into one timestamp.
    # Cache only stable files; never hash multi-GB logs on progress refresh.
    parse = _parse.__wrapped__ if time.time_ns() - stat.st_mtime_ns < 2_000_000_000 else _parse
    record = copy.deepcopy(parse(software_id, str(path.resolve()), stat.st_size, stat.st_mtime_ns))
    if software_id == "orca":
        record["hessian_cross_checks"] = []
        for source in paths[1:]:
            if source.suffix != ".hess" or not source.is_file():
                continue
            if source.is_symlink() or source.resolve().parent != path.resolve().parent:
                record["hessian_cross_checks"].append({"source": str(source), "status": "source_unverified"})
                continue
            info = source.stat()
            parse_hess = _hessian.__wrapped__ if time.time_ns() - info.st_mtime_ns < 2_000_000_000 else _hessian
            hess = parse_hess(str(source.resolve()), info.st_size, info.st_mtime_ns)
            # Log frequencies are rounded to two decimals. This tolerance only
            # compares printed representations; it is not a scientific cutoff.
            matches = [b["index"] for b in record["frequency_blocks"] if b["complete"]
                       and hess["complete"] and len(b["frequencies_cm_1"]) == len(hess["frequencies_cm_1"])
                       and all(abs(a - c) <= 0.0051 for a, c in zip(b["frequencies_cm_1"], hess["frequencies_cm_1"]))]
            summary = {k: v for k, v in hess.items() if k != "frequencies_cm_1"}
            summary.update(source=str(source), matching_blocks=matches, frequency_tolerance_cm_1=0.0051,
                           association="unique_frequency_match" if len(matches) == 1 else "ambiguous" if matches else "unmatched")
            record["hessian_cross_checks"].append(summary)
            if len(matches) == 1:
                record["frequency_blocks"][matches[0]].setdefault("hessian_sources", []).append(str(source))
    return record


@lru_cache(maxsize=256)
def _hessian(filename, size, mtime_ns):
    """Read the documented ORCA HESS sections, not the dense Hessian matrix."""
    frequencies, atoms, indices, expected = [], [], [], {}
    section = None
    result = {"frequency_unit": "cm^-1", "geometry_unit": "bohr", "unit_source": "ORCA_hess_format",
              "source_size": size, "source_mtime_ns": mtime_ns}
    try:
        with open(filename, errors="replace") as stream:
            for number, line in enumerate(stream, 1):
                text = line.strip()
                if text.startswith("$"):
                    section = text if text in {"$vibrational_frequencies", "$atoms"} else None
                    if section:
                        result[section[1:] + "_line"] = number
                    continue
                if not section or not text or text.startswith("#"):
                    continue
                if section not in expected:
                    expected[section] = int(text)
                elif section == "$vibrational_frequencies":
                    parts = text.split()
                    indices.append(int(parts[0]))
                    frequencies.append(float(parts[1]))
                else:
                    parts = text.split()
                    atoms.append((parts[0], *map(float, parts[1:5])))
    except (OSError, ValueError, IndexError) as exc:
        result["parse_error"] = str(exc)
    result.update(frequencies_cm_1=frequencies, atom_count=len(atoms), mode_count=len(frequencies),
                  complete=bool(atoms) and not result.get("parse_error")
                    and expected.get("$atoms") == len(atoms)
                    and expected.get("$vibrational_frequencies") == len(frequencies) == 3 * len(atoms)
                    and indices == list(range(len(frequencies))))
    return result


@lru_cache(maxsize=128)
def _parse(software_id, filename, size, mtime_ns):
    record = {"parser_version": PARSER_VERSION, "software_id": software_id, "source": filename,
              "source_size": size, "source_mtime_ns": mtime_ns, "frequency_blocks": [],
              "normal_termination": None, "scf_converged": None, "optimization_converged": None,
              "status": "unsupported", "segments": []}
    if software_id not in {"orca", "gaussian"}:
        return record
    segments = record["segments"]
    segment = {"index": 0, "line_start": 1, "normal_termination": False,
               "scf_converged": False, "optimization_converged": False,
               "gaussian_requested_max_cycles": [], "gaussian_step_records": []}
    segments.append(segment)
    block = None
    number = 0
    geometry_line = None

    def close_block(end, complete):
        nonlocal block
        if block is None:
            return
        block["line_end"] = end
        modes = block.pop("_indices")
        block["mode_count"] = len(block["frequencies_cm_1"])
        contiguous = bool(modes) and modes == list(range(modes[0], modes[0] + len(modes)))
        block["complete"] = bool(complete and contiguous)
        block["negative_frequencies_cm_1"] = [v for v in block["frequencies_cm_1"] if v < 0]
        block["negative_count_threshold_cm_1"] = 0
        record["frequency_blocks"].append(block)
        block = None

    opener = gzip.open if filename.endswith(".gz") else open
    with opener(filename, "rt", errors="replace") as stream:
        for number, line in enumerate(stream, 1):
            if re.search(r"^\s*(?:JOB NUMBER\s+\d+|\$new_job|--Link1--|Entering Link 1 =)", line, re.I) and number > 1:
                close_block(number - 1, False)
                segment = {"index": len(segments), "line_start": number, "normal_termination": False,
                           "scf_converged": False, "optimization_converged": False,
                           "gaussian_requested_max_cycles": [], "gaussian_step_records": []}
                segments.append(segment)
                geometry_line = None
            if "ORCA TERMINATED NORMALLY" in line or "Normal termination of Gaussian" in line:
                segment["normal_termination"] = True
                segment["termination_line"] = number
            if re.search(r"Error termination|ORCA finished by error|SCF NOT CONVERGED", line, re.I):
                segment["normal_termination"] = False
                segment["error_line"] = number
            if "SCF CONVERGED" in line or "SCF Done:" in line:
                segment["scf_converged"] = True
            if "THE OPTIMIZATION HAS CONVERGED" in line or "Optimization completed" in line:
                segment["optimization_converged"] = True
                segment["optimization_line"] = number
            if "CARTESIAN COORDINATES (ANGSTROEM)" in line or "Standard orientation:" in line:
                geometry_line = number
            if software_id == "orca" and line.strip() == "VIBRATIONAL FREQUENCIES":
                close_block(number - 1, False)
                block = {"index": len(record["frequency_blocks"]), "segment": segment["index"],
                         "line_start": number, "frequencies_cm_1": [], "_indices": [],
                         "geometry_source": {"path": filename, "line_start": geometry_line, "association": "preceding_geometry_in_segment"}
                             if geometry_line else "unverified", "optimization_precedes_block": segment["optimization_converged"]}
            elif block is not None:
                match = _ORCA_MODE.match(line)
                if match:
                    block["_indices"].append(int(match[1]))
                    block["frequencies_cm_1"].append(float(match[2]))
                elif block["_indices"] and (line.strip() in {"NORMAL MODES", "IR SPECTRUM", "THERMOCHEMISTRY"} or "ORCA TERMINATED" in line):
                    close_block(number - 1, True)
            if software_id == "gaussian":
                max_cycles = re.search(r"\bmaxcycles\s*=\s*(\d+)", line, re.I)
                if max_cycles:
                    segment["gaussian_requested_max_cycles"].append({"value": int(max_cycles[1]), "line": number, "source": "route"})
                step = re.search(r"Step number\s+(\d+)\s+out of a maximum of\s+(\d+)", line, re.I)
                if step:
                    segment["gaussian_step_records"].append({"step": int(step[1]), "reported_maximum": int(step[2]), "line": number, "source": "stdout"})
                nstep = re.search(r"\bNStep\s*=\s*(\d+)", line, re.I)
                if nstep:
                    segment["gaussian_nstep"] = {"value": int(nstep[1]), "line": number, "source": "stdout"}
                nimag = re.search(r"NImag=\s*(\d+)", line)
                if nimag:
                    segment["reported_imaginary_frequency_count"] = int(nimag[1])
                    segment["frequency_count_line"] = number
    close_block(number, False)
    record.update({k: segments[-1][k] for k in ("normal_termination", "scf_converged", "optimization_converged")})
    if software_id == "gaussian":
        final_segment = segments[-1]
        steps = final_segment.get("gaussian_step_records", [])
        record["gaussian_requested_max_cycles"] = final_segment.get("gaussian_requested_max_cycles", [])
        record["gaussian_optimization_progress"] = {
            "last_step": steps[-1] if steps else None,
            "reported_maximum": steps[-1]["reported_maximum"] if steps else None,
            "nstep": final_segment.get("gaussian_nstep"),
            "source_segment": final_segment["index"],
        }
    record["status"] = "parsed"
    blocks = record["frequency_blocks"]
    final_blocks = [b for b in blocks if b["segment"] == segments[-1]["index"]]
    if final_blocks:
        candidate = final_blocks[-1]
        record["final_frequency_block"] = candidate["index"] if candidate["complete"] else None
        record["frequency_association"] = "last_complete_block_in_final_segment" if candidate["complete"] else "incomplete"
        if len(segments) > 1:
            record["status"] = "ambiguous"
            record["frequency_association"] = "multiple_calculation_segments"
            record["final_frequency_block"] = None
    else:
        record["final_frequency_block"] = None
        record["frequency_association"] = "unavailable"
    return record
