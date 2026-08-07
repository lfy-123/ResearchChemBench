"""ActionSpec declarations for docking."""

from __future__ import annotations

from .._spec_builders import action as _action


ACTION_SPECS = (
    _action(
            "dock_ligand",
            "docking",
            "Dock an already prepared ligand into an already prepared receptor using an explicit search space.",
            "DockingResult",
            ("vina", "gnina"),
            ("receptor", "ligand", "search_space"),
            ("charges",),
            input_description="prepared receptor/ligand Artifacts and explicit box center/size",
        ),
)
