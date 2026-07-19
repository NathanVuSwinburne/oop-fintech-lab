from fintech_lab.domain.permission import Permission


class Role:
    """A named bundle of permissions. Users don't hold permissions directly —
    they hold roles, and a role's permissions apply to every user with it.
    """

    def __init__(self, name: str, permissions: frozenset[Permission]) -> None:
        self.name = name
        self.permissions = permissions

    def allows(self, permission: Permission) -> bool:
        return permission in self.permissions

    def __repr__(self) -> str:
        granted = sorted(permission.name for permission in self.permissions)
        return f"Role(name={self.name!r}, permissions={granted!r})"
