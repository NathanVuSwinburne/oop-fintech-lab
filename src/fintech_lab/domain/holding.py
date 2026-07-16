from decimal import Decimal

from fintech_lab.domain.financial_product import FinancialProduct


class Holding:
    """A quantity of one FinancialProduct owned within a portfolio."""

    def __init__(self, product: FinancialProduct, quantity: Decimal) -> None:
        self.product = product
        self.quantity = quantity

    def market_value(self) -> Decimal:
        return self.product.price() * self.quantity

    def __repr__(self) -> str:
        return f"Holding(product={self.product.name!r}, quantity={self.quantity!r})"
