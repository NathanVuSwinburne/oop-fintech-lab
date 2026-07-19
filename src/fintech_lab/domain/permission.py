from enum import Enum, auto


class Permission(Enum):
    """A single, granular capability. Roles bundle these; users get them via roles."""

    VIEW_PORTFOLIO = auto()
    PLACE_ORDER = auto()
    MANAGE_INVESTORS = auto()
