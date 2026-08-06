"""Declarative installation and cache management for chemistry software."""

from .manager import SoftwareManager
from .manifests import load_catalog
from .paths import CACHE_ROOT_ENV, cache_root

__all__ = ["CACHE_ROOT_ENV", "SoftwareManager", "cache_root", "load_catalog"]
