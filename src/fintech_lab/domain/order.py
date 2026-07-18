from decimal import Decimal

from fintech_lab.domain.financial_product import FinancialProduct
from fintech_lab.domain.order_execution import OrderExecutionStrategy
from fintech_lab.domain.order_observer import OrderObserver


class Order:
    """A request to buy a quantity of a product, filled via an injected strategy."""

    def __init__(
        self,
        product: FinancialProduct,
        quantity: Decimal,
        strategy: OrderExecutionStrategy,
        observers: list[OrderObserver] | None = None,
    ) -> None:
        self.product = product
        self.quantity = quantity
        self.strategy = strategy  # dependency injection: Order doesn't build its own strategy
        self.filled = False
        self.fill_price: Decimal | None = None
        self._observers = observers or []

    def add_observer(self, observer: OrderObserver) -> None:
        self._observers.append(observer)

    def execute(self) -> None:
        price = self.strategy.execution_price(self.product)
        if price is None:
            return
        self.fill_price = price
        self.filled = True
        for observer in self._observers:
            observer.on_filled(self)

    def __repr__(self) -> str:
        return (
            f"Order(product={self.product.name!r}, quantity={self.quantity!r}, "
            f"filled={self.filled!r}, fill_price={self.fill_price!r})"
        )
