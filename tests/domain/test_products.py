from decimal import Decimal

from fintech_lab.domain.products import Bond, Fund, Stock


def test_stock_price_is_its_market_price():
    stock = Stock(product_id=1, name="Acme Corp", market_price=Decimal("123.45"))

    assert stock.price() == Decimal("123.45")


def test_bond_price_is_its_face_value():
    bond = Bond(product_id=2, name="Gov Bond 2030", face_value=Decimal("1000"))

    assert bond.price() == Decimal("1000")


def test_fund_price_is_its_unit_price():
    fund = Fund(product_id=3, name="Index Fund", unit_price=Decimal("55.10"))

    assert fund.price() == Decimal("55.10")


def test_polymorphism_price_called_uniformly_across_product_types():
    products = [
        Stock(product_id=1, name="Acme Corp", market_price=Decimal("123.45")),
        Bond(product_id=2, name="Gov Bond 2030", face_value=Decimal("1000")),
        Fund(product_id=3, name="Index Fund", unit_price=Decimal("55.10")),
    ]

    # caller doesn't know or care which concrete type each product is
    prices = [product.price() for product in products]

    assert prices == [Decimal("123.45"), Decimal("1000"), Decimal("55.10")]
