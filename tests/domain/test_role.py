from fintech_lab.domain.permission import Permission
from fintech_lab.domain.role import Role


def test_role_allows_permissions_it_was_given():
    role = Role(name="adviser", permissions=frozenset({Permission.MANAGE_INVESTORS}))

    assert role.allows(Permission.MANAGE_INVESTORS) is True


def test_role_does_not_allow_permissions_it_was_not_given():
    role = Role(name="investor", permissions=frozenset({Permission.VIEW_PORTFOLIO}))

    assert role.allows(Permission.MANAGE_INVESTORS) is False
