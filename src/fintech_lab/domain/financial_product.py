from abc import ABC, abstractmethod
from decimal import Decimal


class FinancialProduct(ABC):
    """Something an investor can hold in a portfolio (a stock, bond, fund, ...)."""

    def __init__(self, product_id: int, name: str) -> None:
        self.product_id = product_id
        self.name = name

    @abstractmethod
    def price(self) -> Decimal:
        """Current price of one unit. Each product type prices itself differently."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}(product_id={self.product_id!r}, name={self.name!r})"
