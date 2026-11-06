"""Shared ORCA model-chemistry validation for discovery and execution."""

from __future__ import annotations

import re
from typing import Any


ORCA_COMPOSITE_3C_METHODS = {
    "hf-3c": "HF-3c",
    "b97-3c": "B97-3c",
    "r2scan-3c": "r2SCAN-3c",
    "pbeh-3c": "PBEh-3c",
    "b3lyp-3c": "B3LYP-3c",
    "wb97x-3c": "wB97X-3c",
}
ORCA_METHOD_DEFAULT_BASIS_SENTINELS = {
    "auto",
    "builtin",
    "method_default",
    "method-default",
}


class OrcaParameterError(ValueError):
    """Identify an invalid typed field without changing the requested chemistry."""

    def __init__(self, field: str, message: str):
        super().__init__(message)
        self.field = field


def orca_method_token(value: Any) -> str:
    token = value.strip() if isinstance(value, str) else ""
    if not token or not re.fullmatch(r"[A-Za-z0-9_+().,/=-]+", token):
        raise OrcaParameterError(
            "method_spec.method",
            "ORCA method_spec.method must be a single method keyword, not an ORCA "
            "input line. Use the documented typed fields for other options, or "
            "submit a native ORCA input when those options are not exposed.",
        )
    return token


def orca_solvent_token(value: Any) -> str:
    token = value.strip() if isinstance(value, str) else ""
    if not token or not re.fullmatch(r"[A-Za-z0-9_.,+-]+", token):
        raise OrcaParameterError(
            "method_spec.solvent",
            "ORCA method_spec.solvent must be a solvent name using letters, digits, "
            "commas, periods, underscores, plus or minus signs.",
        )
    return token


def normalize_orca_method_basis(
    method_value: Any,
    basis_value: Any | None,
) -> tuple[str, str | None]:
    """Return the ORCA method token and optional explicit orbital-basis token."""

    method = orca_method_token(method_value)
    composite = ORCA_COMPOSITE_3C_METHODS.get(method.casefold())
    basis = "" if basis_value is None else str(basis_value).strip()
    basis_is_default = not basis or basis.casefold() in ORCA_METHOD_DEFAULT_BASIS_SENTINELS
    if composite is not None:
        if not basis_is_default:
            raise ValueError(
                f"ORCA composite method {composite} includes its own orbital basis; "
                "omit method_spec.basis or use method_default/auto, not "
                f"basis={basis!r}"
            )
        return composite, None
    if basis_is_default:
        raise ValueError(
            f"ORCA method {method!r} requires a concrete method_spec.basis; "
            "auto/method_default is valid only for built-in 3c composite methods"
        )
    return method, basis


__all__ = [
    "ORCA_COMPOSITE_3C_METHODS",
    "ORCA_METHOD_DEFAULT_BASIS_SENTINELS",
    "normalize_orca_method_basis",
    "OrcaParameterError",
    "orca_method_token",
    "orca_solvent_token",
]
