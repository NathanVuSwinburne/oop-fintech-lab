from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING

from fintech_lab.domain.investment_account import InvestmentAccount
from fintech_lab.domain.transaction import Transaction

if TYPE_CHECKING:
    from fintech_lab.domain.order import Order


class OrderObserver(ABC):
    """Reacts to an Order filling, without Order knowing what it does with that.

    Order is the subject: it holds a list of observers and notifies them when
    it fills. It never depends on a concrete observer type, only this
    interface — so any number of unrelated reactions (logging, recording a
    transaction, sending a notification) can be attached without Order
    changing at all.
    """

    @abstractmethod
    def on_filled(self, order: Order) -> None:
        """Called once, right after an order fills."""


class TransactionRecorder(OrderObserver):
    """Builds a Transaction for each filled order and appends it to a ledger."""

    def __init__(self, account: InvestmentAccount) -> None:
        self._account = account
        self._next_id = 1
        self.transactions: list[Transaction] = []

    def on_filled(self, order: Order) -> None:
        transaction = Transaction.from_order(self._next_id, self._account, order)
        self.transactions.append(transaction)
        self._next_id += 1
