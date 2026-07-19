from fintech_lab.domain.permission import Permission
from fintech_lab.domain.role import Role


class User:
    """A login identity, authorized through zero or more Roles."""

    def __init__(self, user_id: int, username: str, roles: list[Role] | None = None) -> None:
        self.user_id = user_id
        self.username = username
        self.roles = roles or []

    def has_permission(self, permission: Permission) -> bool:
        return any(role.allows(permission) for role in self.roles)

    def __repr__(self) -> str:
        return f"User(user_id={self.user_id!r}, username={self.username!r})"
