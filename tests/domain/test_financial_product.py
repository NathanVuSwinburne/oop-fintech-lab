from decimal import Decimal

import pytest

from fintech_lab.domain.financial_product import FinancialProduct


def test_financial_product_cannot_be_instantiated_directly():
    with pytest.raises(TypeError):
        FinancialProduct(product_id=1, name="Something")


def test_subclass_must_implement_price():
    class Incomplete(FinancialProduct):
        pass

    with pytest.raises(TypeError):
        Incomplete(product_id=1, name="Something")


def test_subclass_implementing_price_can_be_instantiated():
    class FixedPriceProduct(FinancialProduct):
        def price(self) -> Decimal:
            return Decimal("10")

    product = FixedPriceProduct(product_id=1, name="Test Product")

    assert product.price() == Decimal("10")
    assert "Test Product" in repr(product)
