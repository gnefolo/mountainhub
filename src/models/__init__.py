"""
Models package for MountainHub.

This module exposes the SQLAlchemy database instance and all model classes so
that they can be imported easily elsewhere in the application. The
initialisation of the database happens in ``src/main.py`` where the
application context is available.
"""

from .user import db  # noqa: F401
from .user import User  # noqa: F401
from .trail import Trail  # noqa: F401
from .equipment import Equipment  # noqa: F401
from .refuge import Refuge  # noqa: F401
from .trip_log import TripLog  # noqa: F401
from .guide import Guide, UserGuideProgress  # noqa: F401

__all__ = [
    "db",
    "User",
    "Trail",
    "Equipment",
    "Refuge",
    "TripLog",
    "Guide",
    "UserGuideProgress",
]
