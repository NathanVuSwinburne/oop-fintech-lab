from decimal import Decimal

import pytest

from fintech_lab.domain.exceptions import ValidationError
from fintech_lab.domain.product_factory import FinancialProductFactory
from fintech_lab.domain.products import Bond, Fund, Stock


def test_creates_a_stock():
    product = FinancialProductFactory.create("stock", product_id=1, name="Acme Corp", price=Decimal("100"))

    assert isinstance(product, Stock)
    assert product.price() == Decimal("100")


def test_creates_a_bond():
    product = FinancialProductFactory.create("bond", product_id=2, name="Treasury", price=Decimal("1000"))

    assert isinstance(product, Bond)
    assert product.price() == Decimal("1000")


def test_creates_a_fund():
    product = FinancialProductFactory.create("fund", product_id=3, name="Index Fund", price=Decimal("50"))

    assert isinstance(product, Fund)
    assert product.price() == Decimal("50")


def test_unknown_product_type_is_rejected():
    with pytest.raises(ValidationError):
        FinancialProductFactory.create("crypto", product_id=4, name="Bitcoin", price=Decimal("1"))
