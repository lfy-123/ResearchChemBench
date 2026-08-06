"""Installation handlers selected by software manifests."""

from .archive import install_archive
from .commands import install_commands
from .copy import install_copy

__all__ = ["install_archive", "install_commands", "install_copy"]
