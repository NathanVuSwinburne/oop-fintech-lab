from decimal import Decimal

from fintech_lab.domain.holding import Holding
from fintech_lab.domain.portfolio import Portfolio
from fintech_lab.domain.products import Bond, Stock


def test_holding_market_value_is_price_times_quantity():
    stock = Stock(product_id=1, name="Acme Corp", market_price=Decimal("10"))
    holding = Holding(product=stock, quantity=Decimal("5"))

    assert holding.market_value() == Decimal("50")


def test_empty_portfolio_has_zero_total_value():
    portfolio = Portfolio(portfolio_id=1)

    assert portfolio.total_value() == Decimal("0")


def test_portfolio_total_value_sums_all_holdings():
    portfolio = Portfolio(portfolio_id=1)
    stock = Stock(product_id=1, name="Acme Corp", market_price=Decimal("10"))
    bond = Bond(product_id=2, name="Gov Bond 2030", face_value=Decimal("1000"))

    portfolio.add_holding(Holding(product=stock, quantity=Decimal("5")))  # 50
    portfolio.add_holding(Holding(product=bond, quantity=Decimal("2")))  # 2000

    assert portfolio.total_value() == Decimal("2050")


def test_holdings_property_returns_a_copy_not_the_internal_list():
    portfolio = Portfolio(portfolio_id=1)
    stock = Stock(product_id=1, name="Acme Corp", market_price=Decimal("10"))
    portfolio.add_holding(Holding(product=stock, quantity=Decimal("1")))

    portfolio.holdings.append("sneaky")  # mutating the returned list

    assert len(portfolio.holdings) == 1  # internal state is untouched
