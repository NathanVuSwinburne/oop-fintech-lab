from dataclasses import FrozenInstanceError
from datetime import datetime
from decimal import Decimal

import pytest

from fintech_lab.domain.exceptions import OrderNotFilledError
from fintech_lab.domain.investment_account import InvestmentAccount
from fintech_lab.domain.investor import Investor
from fintech_lab.domain.order import Order
from fintech_lab.domain.order_execution import MarketOrderExecution
from fintech_lab.domain.products import Stock
from fintech_lab.domain.transaction import Transaction


def make_filled_order(price: str = "100") -> Order:
    stock = Stock(product_id=1, name="Acme Corp", market_price=Decimal(price))
    order = Order(product=stock, quantity=Decimal("10"), strategy=MarketOrderExecution())
    order.execute()
    return order


def make_account() -> InvestmentAccount:
    return InvestmentAccount(account_id=1, investor=Investor(investor_id=1, name="Ada"))


def test_transaction_built_from_filled_order_captures_product_quantity_and_price():
    order = make_filled_order(price="100")
    account = make_account()

    transaction = Transaction.from_order(transaction_id=1, account=account, order=order)

    assert transaction.product is order.product
    assert transaction.quantity == Decimal("10")
    assert transaction.price == Decimal("100")
    assert transaction.total_value == Decimal("1000")
    assert isinstance(transaction.executed_at, datetime)


def test_transaction_cannot_be_built_from_an_unfilled_order():
    stock = Stock(product_id=1, name="Acme Corp", market_price=Decimal("100"))
    unfilled_order = Order(product=stock, quantity=Decimal("10"), strategy=MarketOrderExecution())

    with pytest.raises(OrderNotFilledError):
        Transaction.from_order(transaction_id=1, account=make_account(), order=unfilled_order)


def test_transaction_is_immutable():
    transaction = Transaction.from_order(transaction_id=1, account=make_account(), order=make_filled_order())

    with pytest.raises(FrozenInstanceError):
        transaction.price = Decimal("999")
