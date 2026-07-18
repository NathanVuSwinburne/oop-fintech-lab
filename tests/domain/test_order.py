from decimal import Decimal

from fintech_lab.domain.order import Order
from fintech_lab.domain.order_execution import LimitOrderExecution, MarketOrderExecution
from fintech_lab.domain.products import Stock


def make_stock(price: str) -> Stock:
    return Stock(product_id=1, name="Acme Corp", market_price=Decimal(price))


def test_market_order_fills_at_current_price():
    order = Order(product=make_stock("100"), quantity=Decimal("10"), strategy=MarketOrderExecution())

    order.execute()

    assert order.filled is True
    assert order.fill_price == Decimal("100")


def test_limit_order_fills_when_market_price_is_at_or_below_limit():
    order = Order(
        product=make_stock("95"),
        quantity=Decimal("10"),
        strategy=LimitOrderExecution(limit_price=Decimal("100")),
    )

    order.execute()

    assert order.filled is True
    assert order.fill_price == Decimal("95")


def test_limit_order_does_not_fill_when_market_price_exceeds_limit():
    order = Order(
        product=make_stock("110"),
        quantity=Decimal("10"),
        strategy=LimitOrderExecution(limit_price=Decimal("100")),
    )

    order.execute()

    assert order.filled is False
    assert order.fill_price is None


def test_same_order_class_works_with_either_strategy():
    # this is the point of Strategy: Order never changes, only what's injected does
    stock = make_stock("100")

    market_order = Order(product=stock, quantity=Decimal("1"), strategy=MarketOrderExecution())
    limit_order = Order(
        product=stock, quantity=Decimal("1"), strategy=LimitOrderExecution(limit_price=Decimal("100"))
    )

    market_order.execute()
    limit_order.execute()

    assert market_order.filled and limit_order.filled
