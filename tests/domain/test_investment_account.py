from decimal import Decimal

import pytest

from fintech_lab.domain.investment_account import InvestmentAccount
from fintech_lab.domain.investor import Investor


def make_account() -> InvestmentAccount:
    investor = Investor(investor_id=1, name="Ada Lovelace")
    return InvestmentAccount(account_id=100, investor=investor)


def test_new_account_starts_at_zero_balance():
    account = make_account()

    assert account.balance == Decimal("0")


def test_deposit_increases_balance():
    account = make_account()

    account.deposit(Decimal("50"))

    assert account.balance == Decimal("50")


def test_withdraw_decreases_balance():
    account = make_account()
    account.deposit(Decimal("50"))

    account.withdraw(Decimal("20"))

    assert account.balance == Decimal("30")


def test_withdraw_more_than_balance_is_rejected():
    account = make_account()
    account.deposit(Decimal("10"))

    with pytest.raises(ValueError):
        account.withdraw(Decimal("20"))


def test_negative_deposit_is_rejected():
    account = make_account()

    with pytest.raises(ValueError):
        account.deposit(Decimal("-5"))


def test_account_holds_a_reference_to_its_investor():
    account = make_account()

    assert account.investor.name == "Ada Lovelace"
