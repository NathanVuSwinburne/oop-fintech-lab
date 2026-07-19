from fintech_lab.domain.unit_of_work import UnitOfWork
from fintech_lab.infrastructure.in_memory_investor_repository import InMemoryInvestorRepository


class InMemoryUnitOfWork(UnitOfWork):
    """Stages investor changes in a scratch repository, copying them into the
    real one only on commit(). Entering the `with` block seeds the scratch
    repository with a snapshot of the current data, so reads inside the unit
    of work see prior commits plus this unit's own uncommitted writes.
    """

    def __init__(self, committed_investors: InMemoryInvestorRepository) -> None:
        self._committed = committed_investors

    def __enter__(self) -> "InMemoryUnitOfWork":
        self.investors = InMemoryInvestorRepository()
        for investor in self._committed.list():
            self.investors.add(investor)
        return self

    def commit(self) -> None:
        for investor in self.investors.list():
            self._committed.add(investor)

    def rollback(self) -> None:
        self.investors = InMemoryInvestorRepository()
