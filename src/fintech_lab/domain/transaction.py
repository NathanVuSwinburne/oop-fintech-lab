from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal

from fintech_lab.domain.exceptions import OrderNotFilledError
from fintech_lab.domain.financial_product import FinancialProduct
from fintech_lab.domain.investment_account import InvestmentAccount
from fintech_lab.domain.order import Order


@dataclass(frozen=True)
class Transaction:
    """An immutable record of a completed trade, built from a filled Order.

    Unlike Investor/InvestmentAccount (mutable entities with state that changes
    over time), a Transaction is a value object: once a trade has happened, the
    record of it never changes. `frozen=True` makes that a language-enforced
    rule, not just a convention.
    """

    transaction_id: int
    account: InvestmentAccount
    product: FinancialProduct
    quantity: Decimal
    price: Decimal
    executed_at: datetime

    @property
    def total_value(self) -> Decimal:
        return self.quantity * self.price

    @classmethod
    def from_order(cls, transaction_id: int, account: InvestmentAccount, order: Order) -> "Transaction":
        if not order.filled:
            raise OrderNotFilledError("Cannot create a Transaction from an unfilled order")
        return cls(
            transaction_id=transaction_id,
            account=account,
            product=order.product,
            quantity=order.quantity,
            price=order.fill_price,
            executed_at=datetime.now(timezone.utc),
        )
