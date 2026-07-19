from fintech_lab.domain.exceptions import PermissionDeniedError
from fintech_lab.domain.investor import Investor
from fintech_lab.domain.permission import Permission
from fintech_lab.domain.user import User


class Adviser:
    """Manages a set of Investors. Backed by a User for identity and
    permissions (composition — same HAS-A relationship as InvestmentAccount
    HAS-A Investor), rather than Adviser inheriting from User: an adviser
    *has* a login identity, it isn't a specialization of one.
    """

    def __init__(self, adviser_id: int, user: User) -> None:
        self.adviser_id = adviser_id
        self.user = user  # composition: adviser HAS-A user
        self.managed_investors: list[Investor] = []

    def assign_investor(self, investor: Investor) -> None:
        if not self.user.has_permission(Permission.MANAGE_INVESTORS):
            raise PermissionDeniedError(f"{self.user.username} lacks permission to manage investors")
        self.managed_investors.append(investor)

    def __repr__(self) -> str:
        return f"Adviser(adviser_id={self.adviser_id!r}, user={self.user.username!r})"
