from abc import ABC, abstractmethod

from fintech_lab.domain.investor import Investor


class InvestorRepository(ABC):
    """How the domain persists and retrieves Investors, without knowing how.

    This is a port: an interface owned by the domain layer. The domain calls
    it; something outside the domain (in-memory dict, SQL database, ...)
    implements it. That's what keeps `domain/` free of I/O — it depends on
    this abstraction, never on a concrete storage mechanism.
    """

    @abstractmethod
    def add(self, investor: Investor) -> None:
        """Store a new investor."""

    @abstractmethod
    def get(self, investor_id: int) -> Investor | None:
        """Return the investor with this id, or None if there isn't one."""

    @abstractmethod
    def list(self) -> list[Investor]:
        """Return all stored investors."""
