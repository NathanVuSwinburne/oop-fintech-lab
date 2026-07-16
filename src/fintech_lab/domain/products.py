from decimal import Decimal

from fintech_lab.domain.financial_product import FinancialProduct


class Stock(FinancialProduct):
    """Priced at whatever the market is currently quoting."""

    def __init__(self, product_id: int, name: str, market_price: Decimal) -> None:
        super().__init__(product_id, name)
        self.market_price = market_price

    def price(self) -> Decimal:
        return self.market_price


class Bond(FinancialProduct):
    """Simplified: priced at face value regardless of market movement."""

    def __init__(self, product_id: int, name: str, face_value: Decimal) -> None:
        super().__init__(product_id, name)
        self.face_value = face_value

    def price(self) -> Decimal:
        return self.face_value


class Fund(FinancialProduct):
    """Priced at its published unit price (like a mutual fund's NAV)."""

    def __init__(self, product_id: int, name: str, unit_price: Decimal) -> None:
        super().__init__(product_id, name)
        self.unit_price = unit_price

    def price(self) -> Decimal:
        return self.unit_price
