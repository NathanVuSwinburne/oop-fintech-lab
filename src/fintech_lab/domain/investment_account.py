from decimal import Decimal

from fintech_lab.domain.exceptions import InsufficientFundsError, ValidationError
from fintech_lab.domain.investor import Investor


class InvestmentAccount:
    """An account, owned by one Investor, holding a cash balance."""

    def __init__(self, account_id: int, investor: Investor) -> None:
        self.account_id = account_id
        self.investor = investor  # composition: account HAS-A investor
        self._balance = Decimal("0")

    @property
    def balance(self) -> Decimal:
        return self._balance

    def deposit(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValidationError("Deposit amount must be positive")
        self._balance += amount

    def withdraw(self, amount: Decimal) -> None:
        if amount <= 0:
            raise ValidationError("Withdrawal amount must be positive")
        if amount > self._balance:
            raise InsufficientFundsError("Insufficient funds")
        self._balance -= amount

    def __repr__(self) -> str:
        return (
            f"InvestmentAccount(account_id={self.account_id!r}, "
            f"investor={self.investor.name!r}, balance={self.balance!r})"
        )
