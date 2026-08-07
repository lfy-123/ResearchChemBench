#!/usr/bin/env python3
"""Check DNS, HTTPS, PUG REST, and PubChemPy connectivity from this server."""

from __future__ import annotations

import argparse
import json
import socket
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable

import httpx
import pubchempy as pcp


TOOLBOX_ROOT = Path(__file__).resolve().parents[1]
PROJECT_ROOT = TOOLBOX_ROOT.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from chemistry_toolbox.src.proxy import configure_pubchem_proxy_environment


HOST = "pubchem.ncbi.nlm.nih.gov"
BASE_URL = f"https://{HOST}"


def _timed(check: Callable[[], dict[str, Any]]) -> dict[str, Any]:
    started = time.monotonic()
    try:
        result = {"ok": True, **check()}
    except Exception as exc:
        result = {
            "ok": False,
            "error_type": type(exc).__name__,
            "error": str(exc),
        }
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", default="water", help="Name used by the PubChemPy check.")
    parser.add_argument("--cid", default="962", help="CID used by the direct PUG REST check.")
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--output", type=Path, help="Optional JSON file for recording the probe result.")
    args = parser.parse_args()

    headers = {
        "Accept": "application/json",
        "User-Agent": "ResearchChemBench/1.0 pubchem-connectivity-check",
    }
    proxy_status = configure_pubchem_proxy_environment()
    results: dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "host": HOST,
        "proxy_environment_present": proxy_status["enabled"],
        "proxy_source": proxy_status["source"],
        "proxy_variables": proxy_status["variables"],
    }

    results["dns"] = _timed(
        lambda: {
            "addresses": sorted(
                {
                    record[4][0]
                    for record in socket.getaddrinfo(HOST, 443, type=socket.SOCK_STREAM)
                }
            )
        }
    )

    with httpx.Client(timeout=args.timeout, follow_redirects=True, headers=headers) as client:
        def homepage() -> dict[str, Any]:
            response = client.get(BASE_URL + "/")
            return {
                "ok": response.is_success,
                "status_code": response.status_code,
                "http_version": response.http_version,
            }

        def pug_rest() -> dict[str, Any]:
            url = (
                BASE_URL
                + f"/rest/pug/compound/cid/{args.cid}/property/ConnectivitySMILES,MolecularFormula/JSON"
            )
            response = client.get(url)
            try:
                payload = response.json()
            except ValueError:
                payload = {}
            properties = ((payload.get("PropertyTable") or {}).get("Properties") or [])
            return {
                "ok": response.is_success,
                "status_code": response.status_code,
                "http_version": response.http_version,
                "record_count": len(properties),
                "retry_after": response.headers.get("retry-after"),
                "x_throttling_control": response.headers.get("x-throttling-control"),
                "url": str(response.request.url),
            }

        results["https_homepage"] = _timed(homepage)
        results["pug_rest_get"] = _timed(pug_rest)

    def pubchempy_lookup() -> dict[str, Any]:
        compounds = pcp.get_compounds(args.name, "name")
        if not compounds:
            raise RuntimeError(f"PubChemPy returned no compound for {args.name!r}")
        compound = compounds[0]
        smiles = getattr(compound, "connectivity_smiles", None)
        if smiles is None:
            smiles = getattr(compound, "canonical_smiles", None)
        return {
            "record_count": len(compounds),
            "first_cid": compound.cid,
            "first_connectivity_smiles": smiles,
            "pubchempy_version": getattr(pcp, "__version__", None),
        }

    results["pubchempy_name_lookup"] = _timed(pubchempy_lookup)
    results["all_ok"] = all(
        bool(results[name]["ok"])
        for name in ("dns", "https_homepage", "pug_rest_get", "pubchempy_name_lookup")
    )
    rendered = json.dumps(results, ensure_ascii=False, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0 if results["all_ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
