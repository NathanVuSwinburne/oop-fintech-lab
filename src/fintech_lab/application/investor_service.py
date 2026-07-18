from fintech_lab.domain.investor import Investor
from fintech_lab.domain.repositories import InvestorRepository


class InvestorService:
    """Orchestrates registering and looking up investors.

    The service layer sits above the domain: it coordinates an entity
    (Investor) with a port (InvestorRepository), and owns use-case logic that
    doesn't belong on the entity itself — like assigning the next id. It has
    no business rules of its own (those live in Investor); it just wires
    things together. The repository is injected (dependency injection), so
    this service works unchanged with any implementation of the port.
    """

    def __init__(self, repository: InvestorRepository) -> None:
        self._repository = repository
        self._next_id = 1

    def register(self, name: str) -> Investor:
        investor = Investor(investor_id=self._next_id, name=name)
        self._repository.add(investor)
        self._next_id += 1
        return investor

    def find(self, investor_id: int) -> Investor | None:
        return self._repository.get(investor_id)
