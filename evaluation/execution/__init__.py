"""Workspace preparation and Agent process execution.

The package must stay cheap to import.  In particular, lightweight modules
such as ``resume_policy`` are used while a launcher is still constructing its
selected task snapshot.  Eagerly importing ``runner`` here imports settings
too early, freezing the repository task roots before the launcher can point
the evaluator at that snapshot.
"""

__all__ = ["TaskRunner"]


def __getattr__(name):
    if name == "TaskRunner":
        from .runner import TaskRunner

        return TaskRunner
    raise AttributeError(name)
