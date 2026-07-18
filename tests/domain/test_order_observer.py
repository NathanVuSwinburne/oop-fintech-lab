from decimal import Decimal

from fintech_lab.domain.investment_account import InvestmentAccount
from fintech_lab.domain.investor import Investor
from fintech_lab.domain.order import Order
from fintech_lab.domain.order_execution import LimitOrderExecution, MarketOrderExecution
from fintech_lab.domain.order_observer import OrderObserver, TransactionRecorder
from fintech_lab.domain.products import Stock


def make_stock(price: str) -> Stock:
    return Stock(product_id=1, name="Acme Corp", market_price=Decimal(price))


def make_account() -> InvestmentAccount:
    return InvestmentAccount(account_id=1, investor=Investor(investor_id=1, name="Ada"))


class SpyObserver(OrderObserver):
    def __init__(self) -> None:
        self.notified_orders: list[Order] = []

    def on_filled(self, order: Order) -> None:
        self.notified_orders.append(order)


def test_observer_is_notified_when_order_fills():
    spy = SpyObserver()
    order = Order(
        product=make_stock("100"), quantity=Decimal("10"), strategy=MarketOrderExecution(), observers=[spy]
    )

    order.execute()

    assert spy.notified_orders == [order]


def test_observer_is_not_notified_when_order_does_not_fill():
    spy = SpyObserver()
    order = Order(
        product=make_stock("110"),
        quantity=Decimal("10"),
        strategy=LimitOrderExecution(limit_price=Decimal("100")),
        observers=[spy],
    )

    order.execute()

    assert spy.notified_orders == []


def test_add_observer_after_construction():
    spy = SpyObserver()
    order = Order(product=make_stock("100"), quantity=Decimal("10"), strategy=MarketOrderExecution())
    order.add_observer(spy)

    order.execute()

    assert spy.notified_orders == [order]


def test_multiple_observers_are_all_notified():
    first, second = SpyObserver(), SpyObserver()
    order = Order(
        product=make_stock("100"),
        quantity=Decimal("10"),
        strategy=MarketOrderExecution(),
        observers=[first, second],
    )

    order.execute()

    assert first.notified_orders == [order]
    assert second.notified_orders == [order]


def test_transaction_recorder_builds_a_transaction_when_order_fills():
    account = make_account()
    recorder = TransactionRecorder(account=account)
    order = Order(
        product=make_stock("100"), quantity=Decimal("10"), strategy=MarketOrderExecution(), observers=[recorder]
    )

    order.execute()

    assert len(recorder.transactions) == 1
    transaction = recorder.transactions[0]
    assert transaction.account is account
    assert transaction.product is order.product
    assert transaction.quantity == Decimal("10")
    assert transaction.price == Decimal("100")


def test_transaction_recorder_assigns_sequential_ids_across_fills():
    account = make_account()
    recorder = TransactionRecorder(account=account)
    first_order = Order(
        product=make_stock("100"), quantity=Decimal("10"), strategy=MarketOrderExecution(), observers=[recorder]
    )
    second_order = Order(
        product=make_stock("50"), quantity=Decimal("5"), strategy=MarketOrderExecution(), observers=[recorder]
    )

    first_order.execute()
    second_order.execute()

    assert [t.transaction_id for t in recorder.transactions] == [1, 2]
