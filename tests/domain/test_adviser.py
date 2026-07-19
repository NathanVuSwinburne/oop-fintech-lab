import pytest

from fintech_lab.domain.adviser import Adviser
from fintech_lab.domain.exceptions import PermissionDeniedError
from fintech_lab.domain.investor import Investor
from fintech_lab.domain.permission import Permission
from fintech_lab.domain.role import Role
from fintech_lab.domain.user import User


def make_user_with_role(*permissions: Permission) -> User:
    role = Role(name="adviser", permissions=frozenset(permissions))
    return User(user_id=1, username="ada", roles=[role])


def test_adviser_with_permission_can_be_assigned_an_investor():
    adviser = Adviser(adviser_id=1, user=make_user_with_role(Permission.MANAGE_INVESTORS))
    investor = Investor(investor_id=1, name="Alan Turing")

    adviser.assign_investor(investor)

    assert adviser.managed_investors == [investor]


def test_adviser_without_permission_cannot_be_assigned_an_investor():
    adviser = Adviser(adviser_id=1, user=make_user_with_role(Permission.VIEW_PORTFOLIO))
    investor = Investor(investor_id=1, name="Alan Turing")

    with pytest.raises(PermissionDeniedError):
        adviser.assign_investor(investor)

    assert adviser.managed_investors == []
