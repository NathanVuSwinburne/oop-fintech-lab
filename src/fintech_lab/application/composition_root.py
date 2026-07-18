from decimal import Decimal

from fintech_lab.application.investor_service import InvestorService
from fintech_lab.domain.investment_account import InvestmentAccount
from fintech_lab.domain.order import Order
from fintech_lab.domain.order_execution import MarketOrderExecution
from fintech_lab.domain.order_observer import TransactionRecorder
from fintech_lab.domain.product_factory import FinancialProductFactory
from fintech_lab.infrastructure.in_memory_investor_repository import InMemoryInvestorRepository


def place_market_order(
    investor_name: str,
    product_type: str,
    product_name: str,
    price: Decimal,
    quantity: Decimal,
) -> TransactionRecorder:
    """Wires together every piece built so far and runs one trade end-to-end.

    This function is a composition root: the one place allowed to know about
    concrete implementations (InMemoryInvestorRepository, MarketOrderExecution,
    TransactionRecorder, ...) and construct them. Everything it hands those
    concretes to, which are InvestorService, Order, only depends on interfaces
    (InvestorRepository, OrderExecutionStrategy, OrderObserver). That's the
    point of dependency injection: the dependents never import a concrete
    class, only whoever assembles them does.
    """
    investor_service = InvestorService(repository=InMemoryInvestorRepository())
    investor = investor_service.register(investor_name)
    account = InvestmentAccount(account_id=1, investor=investor)

    product = FinancialProductFactory.create(product_type, product_id=1, name=product_name, price=price)
    recorder = TransactionRecorder(account=account)
    order = Order(product=product, quantity=quantity, strategy=MarketOrderExecution(), observers=[recorder])
    order.execute()

    return recorder
