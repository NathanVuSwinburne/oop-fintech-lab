from fintech_lab.domain.investor import Investor
from fintech_lab.domain.repositories import InvestorRepository


class InMemoryInvestorRepository(InvestorRepository):
    """Stores investors in a dict. Stands in for a real database in tests/demos."""

    def __init__(self) -> None:
        self._investors: dict[int, Investor] = {}

    def add(self, investor: Investor) -> None:
        self._investors[investor.investor_id] = investor

    def get(self, investor_id: int) -> Investor | None:
        return self._investors.get(investor_id)

    def list(self) -> list[Investor]:
        return list(self._investors.values())
