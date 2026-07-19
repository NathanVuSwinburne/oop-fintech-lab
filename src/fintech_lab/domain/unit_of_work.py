from abc import ABC, abstractmethod
from types import TracebackType

from fintech_lab.domain.repositories import InvestorRepository


class UnitOfWork(ABC):
    """Groups a batch of repository changes so they commit or roll back together.

    Used as a context manager: work happens against `.investors` inside the
    `with` block, then the caller calls `commit()` explicitly. If the block
    ends without a commit — an exception, or the caller just forgetting — the
    default on exit is `rollback()`, so a multi-step operation can never leave
    the repository half-updated. This in-memory version can't offer real
    atomicity the way a database transaction can, but it enforces the same
    commit-or-nothing discipline at the code level, which is what Phase B's
    SQLAlchemy Unit of Work will back with a real transaction later.
    """

    investors: InvestorRepository

    @abstractmethod
    def commit(self) -> None:
        """Persist everything done against `.investors` in this unit of work."""

    @abstractmethod
    def rollback(self) -> None:
        """Discard everything done against `.investors` in this unit of work."""

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        self.rollback()
