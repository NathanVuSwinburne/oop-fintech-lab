from fintech_lab.domain.permission import Permission
from fintech_lab.domain.role import Role
from fintech_lab.domain.user import User


def test_user_has_permission_granted_by_one_of_its_roles():
    adviser_role = Role(name="adviser", permissions=frozenset({Permission.MANAGE_INVESTORS}))
    user = User(user_id=1, username="ada", roles=[adviser_role])

    assert user.has_permission(Permission.MANAGE_INVESTORS) is True


def test_user_does_not_have_permission_none_of_its_roles_grant():
    investor_role = Role(name="investor", permissions=frozenset({Permission.VIEW_PORTFOLIO}))
    user = User(user_id=1, username="ada", roles=[investor_role])

    assert user.has_permission(Permission.MANAGE_INVESTORS) is False


def test_user_with_no_roles_has_no_permissions():
    user = User(user_id=1, username="ada")

    assert user.has_permission(Permission.VIEW_PORTFOLIO) is False
