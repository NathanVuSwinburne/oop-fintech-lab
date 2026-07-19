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

    def register(self, name: str) -> Investor:
        investor = Investor(investor_id=self._next_id(), name=name)
        self._repository.add(investor)
        return investor

    def find(self, investor_id: int) -> Investor | None:
        return self._repository.get(investor_id)

    def _next_id(self) -> int:
        # derived from the repository, not a local counter: a local counter
        # would collide with ids already in a non-empty repository (e.g. one
        # shared with another service instance, or restored from storage)
        existing_ids = [investor.investor_id for investor in self._repository.list()]
        return max(existing_ids, default=0) + 1
