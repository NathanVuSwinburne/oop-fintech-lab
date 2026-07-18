from collections.abc import Callable
from decimal import Decimal

from fintech_lab.domain.exceptions import ValidationError
from fintech_lab.domain.financial_product import FinancialProduct
from fintech_lab.domain.products import Bond, Fund, Stock


class FinancialProductFactory:
    """Builds a FinancialProduct without the caller knowing which concrete
    class to use, or that each one names its price parameter differently
    (market_price / face_value / unit_price). Contrast with Strategy (Order):
    a factory picks *which class* to build; a strategy picks *which behavior*
    an already-built object runs.
    """

    _builders: dict[str, Callable[[int, str, Decimal], FinancialProduct]] = {
        "stock": lambda product_id, name, price: Stock(product_id, name, market_price=price),
        "bond": lambda product_id, name, price: Bond(product_id, name, face_value=price),
        "fund": lambda product_id, name, price: Fund(product_id, name, unit_price=price),
    }

    @staticmethod
    def create(product_type: str, product_id: int, name: str, price: Decimal) -> FinancialProduct:
        try:
            builder = FinancialProductFactory._builders[product_type]
        except KeyError:
            raise ValidationError(f"Unknown product type: {product_type!r}") from None
        return builder(product_id, name, price)
