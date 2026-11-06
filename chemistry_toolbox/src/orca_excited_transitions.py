"""Read printed ORCA orbital contributions without inventing omitted weights."""
from __future__ import annotations

import re

_NUMBER = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[EeDd][-+]?\d+)?"
_STATE = re.compile(r"^STATE\s+(\d+):.*", re.M)
_TERM = re.compile(r"^\s*(\d+)([ab]?)\s*->\s*(\d+)([ab]?)\s*:\s*("+_NUMBER+r")(?:\s|$)")
_NOTICE = re.compile(r"the\s+(weight|amplitude)s?\s+of.*?printed\s+if\s+larger\s+than\s+("+_NUMBER+r")", re.I)


def parse_orbital_transitions(text: str, *, source_path: str, source_sha256: str) -> dict[int, dict]:
    """Keys are header character offsets: repeated state indices never get merged."""
    states = list(_STATE.finditer(text))
    notices = list(_NOTICE.finditer(text))
    output = {}
    for i, header in enumerate(states):
        notice = next((n for n in reversed(notices) if n.start() < header.start()), None)
        kind = notice.group(1).lower() if notice else "unknown"
        threshold = float(notice.group(2).replace("D","E").replace("d","e")) if notice else None
        end = states[i+1].start() if i+1<len(states) else len(text)
        first_line = text.count("\n",0,header.start()) + 1
        terms, unsupported = [], []
        last_line = first_line
        for offset, line in enumerate(text[header.end():end].splitlines(), start=0):
            line_number = first_line + offset
            # header.end() points before its newline; its empty remainder is line 0.
            match = _TERM.match(line)
            if match:
                a, spin_a, b, spin_b, value = match.groups()
                terms.append({"from_orbital_label":a+spin_a,"to_orbital_label":b+spin_b,
                              "from_orbital_index_printed":int(a),"to_orbital_index_printed":int(b),
                              "from_spin_label":spin_a or None,"to_spin_label":spin_b or None,
                              "printed_value":float(value.replace("D","E").replace("d","e")),
                              "value_kind":kind,"source_line":line_number})
                last_line = line_number
            elif "->" in line:
                unsupported.append(line_number)
            elif line.strip():
                # Stop at the next non-contribution section; spectra are not configurations.
                break
        status = "parsed_printed_terms" if terms and not unsupported and kind!="unknown" else "partial" if terms else "not_parsed"
        ranked = sorted(terms,key=lambda t:abs(t["printed_value"]),reverse=True) if kind!="unknown" else terms
        output[header.start()] = {
            "orbital_transitions":terms,
            "dominant_orbital_transitions":ranked[:3],
            "transition_parse":{
                "status":status,"state_label":header.group(0),"orbital_numbering":"as_printed",
                "value_kind":kind,"printing_threshold":threshold,"parsed_term_count":len(terms),
                "inline_term_count":min(3,len(terms)),"unparsed_lines":unsupported,
                "omitted_small_contributions":threshold is not None,
                "all_physical_contributions_known":False,
                "source":{"path":source_path,"sha256":source_sha256,"line_start":first_line,"line_end":last_line},
            },
        }
    return output
