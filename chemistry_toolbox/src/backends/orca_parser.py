"""Local, format-based ORCA adaptations for the pinned cclib parser.

Only the affected blocks are read here. All other scientific properties retain
cclib's parsing and units; no cclib class or installed dependency is modified.
"""

from __future__ import annotations

import math
import re

from cclib.parser import utils
from cclib.parser.orcaparser import ORCA


def _number(text: str) -> float:
    value = float(text.replace("D", "E").replace("d", "e"))
    if not math.isfinite(value):
        raise ValueError(f"Non-finite numeric output: {text!r}")
    return value


class TrackedLines:
    """Add line numbers and one-line lookahead to cclib's file wrapper."""

    def __init__(self, wrapped, observe=None):
        self.wrapped = wrapped
        self.observe = observe
        self.line_number = 0
        self.last_line = ""
        self.pending = None

    def __getattr__(self, name):
        return getattr(self.wrapped, name)

    def __iter__(self):
        return self

    def __next__(self):
        if self.pending is None:
            line = next(self.wrapped)
            if self.observe:
                self.observe(line)
        else:
            line, self.pending = self.pending, None
        self.line_number += 1
        self.last_line = line
        return line

    def push_back(self, line):
        if self.pending is not None:
            raise RuntimeError("Parser lookahead was not consumed")
        self.pending = line
        self.line_number -= 1


class CompatibleORCA(ORCA):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.diagnostics = []
        self.incomplete_properties = set()
        self.property_sources = {}
        self.source_termination = "not_observed"
        self.section = "file header"
        self.inputfile = TrackedLines(self.inputfile, self._observe)

    def before_parsing(self):
        super().before_parsing()
        self._lean_open = False
        self._summaries = 0

    def _observe(self, line):
        text = line.strip().strip("* ")
        if text == "ORCA TERMINATED NORMALLY":
            self.source_termination = "normal"
        elif text.startswith(("ORCA finished by error termination", "ORCA TERMINATED ABNORMALLY")):
            self.source_termination = "abnormal"

    def _issue(self, code, message, properties=()):
        for entry in self.diagnostics:
            if entry["code"] == code:
                entry["occurrences"] += 1
                entry["last_line"] = self.inputfile.line_number
                return
        self.diagnostics.append({
            "code": code, "section": self.section, "message": message,
            "properties": list(properties), "line_number": self.inputfile.line_number,
            "last_line": self.inputfile.line_number, "occurrences": 1,
        })

    def _record_source(self, names, start_line):
        for name in names:
            if hasattr(self, name):
                self.property_sources[name] = {
                    "section": self.section, "last_block_start_line": start_line,
                    "last_block_end_line": self.inputfile.line_number,
                }

    def extract(self, inputfile, line):
        text = line.strip()
        start_line = inputfile.line_number
        if text:
            self.section = text[:160]
        try:
            # ORCA 6's LEAN-SCF has no old "SCF ITERATIONS" heading, and
            # prints RMSDP before MaxDP. Solver switches belong to one SCF.
            columns = re.sub(r"Energy\s+\([^)]*\)", "Energy", text).split()
            if columns[:2] == ["Iteration", "Energy"] and all(
                name in columns for name in ("Delta-E", "RMSDP", "MaxDP")
            ):
                self.section = "SCF iterations"
                self._read_scf_table(inputfile, columns)
                return
            if "SCF NOT CONVERGED AFTER" in line:
                # The upstream fallback treats an iteration's Delta-E as an
                # absolute energy. Keep this failure explicit instead.
                self.metadata["scf_nonconvergence_observed"] = True
                self._issue("scf_not_converged", "ORCA reported SCF nonconvergence; no converged energy is inferred.")
                self._lean_open = False
                return
            if text == "ORBITAL ENERGIES":
                self._read_orbitals(inputfile)
                return
            if text == "DIPOLE MOMENT":
                self._read_dipole(inputfile)
                return
            if text.startswith("THERMOCHEMISTRY AT"):
                self._read_thermochemistry(inputfile)
                return
            if text == "VIBRATIONAL FREQUENCIES":
                self._read_frequencies(inputfile)
                return
            if text in {"ABSORPTION SPECTRUM VIA TRANSITION ELECTRIC DIPOLE MOMENTS",
                        "ABSORPTION SPECTRUM VIA TRANSITION VELOCITY DIPOLE MOMENTS"}:
                self._read_absorption(inputfile, text, start_line)
                return
            super().extract(inputfile, line)
            if "SCF CONVERGED AFTER" in line:
                self._record_source(("scfenergies",), start_line)
            elif text == "CARTESIAN COORDINATES (ANGSTROEM)":
                self._record_source(("atomcoords", "atomnos"), start_line)
        except StopIteration:
            # cclib catches EOF internally; preserve it as incomplete parsing.
            self.incomplete_properties.add("all")
            self._issue("unexpected_eof", "The output ended inside a data block; parsed values may be incomplete.")
            raise

    def _read_absorption(self, inputfile, title, start_line):
        """ORCA 5 state rows and ORCA 6 labelled transitions, in printed cm-1."""
        import numpy as np
        header = [next(inputfile) for _ in range(4)]
        columns, units = header[1].split(), header[2].split()
        modern = columns[:4] == ["Transition", "Energy", "Energy", "Wavelength"] and units[:3] == ["(eV)", "(cm-1)", "(nm)"]
        legacy = columns[:3] == ["State", "Energy", "Wavelength"] and units[:2] == ["(cm-1)", "(nm)"]
        if not (modern or legacy) or not any(c.startswith("fosc") for c in columns):
            raise ValueError("Unsupported absorption columns/units: " + "".join(header).strip())
        energies, strengths, labels = [], [], []
        for line in inputfile:
            text, fields = line.strip(), line.split()
            if not text or set(text) == {"-"}:
                break
            if modern:
                if len(fields) < 7 or fields[1] != "->":
                    raise ValueError("Malformed absorption transition: " + text)
                labels.append((fields[0], fields[2]))
                energy, strength = fields[4], fields[6]
            else:
                if len(fields) < 4 or not fields[0].isdigit():
                    raise ValueError("Malformed absorption state: " + text)
                labels.append(("0", fields[0]))
                energy, strength = fields[1], fields[3]
            energies.append(_number(energy))
            strengths.append(_number(strength))
        else:
            raise StopIteration
        self.transprop = getattr(self, "transprop", {})
        self.transprop[title] = (np.asarray(energies), np.asarray(strengths))
        self.metadata.setdefault("absorption_tables", []).append({"title": title, "start_line": start_line,
            "end_line": inputfile.line_number, "energy_unit": "cm-1", "transition_labels": labels})
        if "VELOCITY" in title:
            # Keep gauges separately; the velocity table must not overwrite
            # cclib's canonical electric-dipole oscillator strengths.
            return
        previous = getattr(self, "etenergies", None)
        ordered = all(re.match(r"0(?:-|$)", a) and re.match(rf"{i}(?:-|$)", b) for i, (a, b) in enumerate(labels, 1))
        aligned = previous is None or (len(previous) == len(energies) and all(round(a) == round(b) for a,b in zip(previous, energies)))
        if energies and ordered and aligned:
            if previous is None:
                self.set_attribute("etenergies", energies)
                self._record_source(("etenergies",), start_line)
            self.set_attribute("etoscs", strengths)
            self._record_source(("etoscs",), start_line)
        else:
            self._issue("absorption_state_mapping_unresolved", "Spectrum retained in transprop; no correspondence to existing excited-state arrays is asserted.", ("etoscs",))

    def _read_scf_table(self, inputfile, columns):
        if not hasattr(self, "scfvalues"):
            self.scfvalues = []
        if not self._lean_open:
            self.scfvalues.append([])
            self._lean_open = True
        positions = [columns.index(name) for name in ("Delta-E", "MaxDP", "RMSDP")]
        for line in inputfile:
            text = line.strip()
            values = text.split()
            if values and values[0].isdigit():
                self.scfvalues[-1].append([_number(values[i]) for i in positions])
            elif "SCF CONVERGED AFTER" in text or "SCF NOT CONVERGED AFTER" in text:
                inputfile.push_back(line)
                return
            elif not text or set(text) == {"-"} or text.startswith("***"):
                continue
            else:
                inputfile.push_back(line)
                return
        raise StopIteration

    def _append_scfvalues_scftargets(self, inputfile, line):
        self.section = "SCF convergence"
        while "Last Energy change" not in line:
            if line.strip() == "ORBITAL ENERGIES" or "ORCA TERMINATED" in line:
                inputfile.push_back(line)
                self._issue("missing_scf_summary", "SCF convergence details were not printed.")
                self._lean_open = False
                return
            line = next(inputfile)
        values, targets = {}, {}
        pattern = r"Last (.+?)\s+\.\.\.\s+(\S+)\s+Tolerance\s*:\s*(\S+)"
        while line.strip().startswith("Last "):
            match = re.fullmatch(pattern, line.strip())
            if match and match[1] in {"Energy change", "MAX-Density change", "RMS-Density change"}:
                values[match[1]], targets[match[1]] = _number(match[2]), _number(match[3])
            elif any(name in line for name in ("Energy change", "MAX-Density change", "RMS-Density change")):
                raise ValueError(f"Malformed SCF convergence row: {line.strip()}")
            line = next(inputfile)
        inputfile.push_back(line)
        if not hasattr(self, "scfvalues"):
            self.scfvalues = []
        if not hasattr(self, "scftargets"):
            self.scftargets = []
        if len(self.scfvalues) <= self._summaries:
            self.scfvalues.append([])
        names = ("Energy change", "MAX-Density change", "RMS-Density change")
        previous = self.scfvalues[-1][-1] if self.scfvalues[-1] else []
        row = [values.get(name, previous[i] if len(previous) > i else math.nan) for i, name in enumerate(names)]
        target = [targets.get(name, math.nan) for name in names]
        if "RMS-Density change" not in targets:
            if self.scftargets and target[:2] == self.scftargets[-1][:2]:
                target[2] = self.scftargets[-1][2]
            self._issue("missing_scf_rms", "Applied the ORCA compatibility fix for an omitted RMS-density target; unavailable convergence metadata remains missing.")
        self.scfvalues[-1].append(row)
        self.scftargets.append(target)
        self._summaries += 1
        self._lean_open = False

    def _read_orbitals(self, inputfile):
        start_line = inputfile.line_number
        attributes = ("moenergies", "mosyms", "homos")
        self.incomplete_properties.difference_update(attributes)
        for name in (*attributes, "mooccnos"):
            self.property_sources.pop(name, None)
            if hasattr(self, name):
                delattr(self, name)
        energies, occupations, symmetries, indices = [[]], [[]], [[]], [[]]
        incomplete = False
        for line in inputfile:
            text = line.strip()
            fields = text.split()
            if fields and fields[0].isdigit():
                if len(fields) < 4:
                    raise ValueError(f"Malformed orbital row: {text}")
                index = int(fields[0])
                if index != len(indices[-1]):
                    raise ValueError(f"Non-contiguous orbital indices at {text}")
                indices[-1].append(index)
                occupations[-1].append(_number(fields[1]))
                energies[-1].append(utils.convertor(_number(fields[2]), "hartree", "eV"))
                symmetries[-1].append(self.normalisesym(fields[4].split("-", 1)[-1]) if self.uses_symmetry else "A")
            elif text.startswith("*Only the first") and "virtual orbitals" in text:
                incomplete = True
            elif text == "SPIN DOWN ORBITALS":
                if not energies[-1] or len(energies) != 1:
                    raise ValueError("Unexpected spin-down orbital table")
                energies.append([])
                occupations.append([])
                symmetries.append([])
                indices.append([])
            elif text == "SPIN UP ORBITALS" or fields[:2] == ["NO", "OCC"]:
                continue
            elif not text:
                continue
            elif set(text) == {"-"} and not energies[-1]:
                continue
            elif set(text) <= {"-", "*"} or text.startswith("Total"):
                inputfile.push_back(line)
                break
            else:
                raise ValueError(f"Unrecognized orbital table row: {text}")
        else:
            incomplete = True
            self._issue("unexpected_eof", "The output ended inside the orbital table.", attributes)
        if not all(energies):
            raise ValueError("Orbital table contains no numeric rows for one or more spin channels")
        self.moenergies, self.mooccnos, self.mosyms = energies, occupations, symmetries
        if all(value in (0.0, 1.0, 2.0) for channel in occupations for value in channel):
            self.homos = [max((i for i, value in enumerate(channel) if value > 0), default=-1) for channel in occupations]
            if len(occupations) == 1 and 1.0 in occupations[0] and 2.0 in occupations[0]:
                self.homos.append(max(i for i, value in enumerate(occupations[0]) if value == 2.0))
        self._record_source(attributes, start_line)
        if hasattr(self, "nbasis") and any(len(channel) < self.nbasis for channel in energies):
            incomplete = True
        if incomplete:
            self.incomplete_properties.update(("moenergies", "mosyms"))
            self._issue("incomplete_orbitals", "ORCA printed only part of the orbital table; omitted orbitals were not reconstructed.", ("moenergies", "mosyms"))

    def _read_dipole(self, inputfile):
        start_line = inputfile.line_number
        # ORCA 6 inserts method/density/irrep metadata ahead of the vector.
        for line in inputfile:
            if line.strip().startswith("Total Dipole Moment"):
                values = line.split(":", 1)[1].split()
                if len(values) != 3:
                    raise ValueError("Expected three dipole components")
                self.moments = [[0.0, 0.0, 0.0],
                                [utils.convertor(_number(x), "ebohr", "Debye") for x in values]]
                self._record_source(("moments",), start_line)
                return
            if "Magnitude (Debye)" in line or "ORCA TERMINATED" in line:
                raise ValueError("Dipole block ended without its total vector")
        raise StopIteration

    def _read_thermochemistry(self, inputfile):
        fields = {
            "temperature": ("temperature", "K"),
            "pressure": ("pressure", "atm"),
            "zero point energy": ("zpve", "Eh"),
            "total enthalpy": ("enthalpy", "Eh"),
            "final entropy term": ("entropy", "Eh"),
            "final gibbs free energy": ("freeenergy", "Eh"),
            "final gibbs free enthalpy": ("freeenergy", "Eh"),
        }
        expected = {"temperature", "zpve", "enthalpy", "entropy", "freeenergy"}
        self.incomplete_properties.difference_update(expected)
        for name in expected:
            self.property_sources.pop(name, None)
            if hasattr(self, name):
                delattr(self, name)
        for line in inputfile:
            if "ORCA TERMINATED" in line or line.strip() in {"ORCA LEAN-SCF", "VIBRATIONAL FREQUENCIES", "SUGGESTED CITATIONS FOR THIS RUN"}:
                inputfile.push_back(line)
                break
            match = re.fullmatch(r"(.+?)\s+\.\.\.\s+(\S+)\s+(\S+).*", line.strip())
            if not match or match[1].lower() not in fields:
                continue
            name, unit = fields[match[1].lower()]
            if match[3] != unit:
                raise ValueError(f"Unexpected {name} unit: {match[3]}")
            if match[2].lower() in {"-inf", "inf", "+inf", "nan"}:
                self._issue("nonfinite_thermochemistry", "ORCA reported non-finite thermochemistry; unavailable values were omitted.")
            else:
                value = _number(match[2])
                if name == "entropy":
                    if not hasattr(self, "temperature") or self.temperature <= 0:
                        raise ValueError("A positive temperature is required to convert the printed T*S term to entropy")
                    value /= self.temperature
                setattr(self, name, value)
                self._record_source((name,), inputfile.line_number)
            if name == "freeenergy":
                break
        missing = sorted(name for name in expected if not hasattr(self, name))
        if missing:
            self.incomplete_properties.update(missing)
            self._issue("incomplete_thermochemistry", "Thermochemistry fields are missing: " + ", ".join(missing), missing)

    def _read_frequencies(self, inputfile):
        # Do not fill truncated tables with zeros or classify stationary points.
        start_line = inputfile.line_number
        for name in ("vibfreqs", "vibdisps"):
            self.property_sources.pop(name, None)
            if hasattr(self, name):
                delattr(self, name)
        self.incomplete_properties.difference_update(("vibfreqs", "vibdisps"))
        values = []
        for line in inputfile:
            text = line.strip()
            match = re.match(r"(\d+):\s+(\S+)\s+cm\*\*-1", text)
            if match:
                if int(match[1]) != len(values):
                    raise ValueError(f"Non-contiguous frequency mode: {text}")
                values.append(_number(match[2]))
                if len(values) == 3 * self.natom:
                    self.first_mode = next((i for i, value in enumerate(values) if value != 0), len(values))
                    self.num_modes = len(values) - self.first_mode
                    self.vibfreqs = values[self.first_mode:]
                    self._record_source(("vibfreqs",), start_line)
                    return
            elif not text or set(text) == {"-"} or text.startswith("Scaling factor for frequencies"):
                continue
            else:
                if re.match(r"\d+:", text):
                    raise ValueError(f"Malformed frequency row: {text}")
                inputfile.push_back(line)
                break
        self.incomplete_properties.update(("vibfreqs", "vibdisps"))
        self._issue("incomplete_frequencies", f"Only {len(values)} of {3 * self.natom} frequency rows were present; the incomplete table was omitted.", ("vibfreqs", "vibdisps"))

    def after_parsing(self):
        super().after_parsing()
        # Runtime timing alone (cclib's default) is not a normal-termination marker.
        self.metadata["success"] = self.source_termination == "normal"
