from abc import ABC, abstractmethod
from decimal import Decimal

from fintech_lab.domain.financial_product import FinancialProduct


class OrderExecutionStrategy(ABC):
    """How an order decides the price it fills at (or whether it fills at all)."""

    @abstractmethod
    def execution_price(self, product: FinancialProduct) -> Decimal | None:
        """Return the fill price, or None if the order shouldn't fill right now."""


class MarketOrderExecution(OrderExecutionStrategy):
    """Fills immediately at whatever the current price is."""

    def execution_price(self, product: FinancialProduct) -> Decimal | None:
        return product.price()


class LimitOrderExecution(OrderExecutionStrategy):
    """Only fills if the market price is at or below the limit."""

    def __init__(self, limit_price: Decimal) -> None:
        self.limit_price = limit_price

    def execution_price(self, product: FinancialProduct) -> Decimal | None:
        market_price = product.price()
        if market_price > self.limit_price:
            return None
        return market_price
