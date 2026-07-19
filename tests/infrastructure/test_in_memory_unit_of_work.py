import pytest

from fintech_lab.domain.investor import Investor
from fintech_lab.infrastructure.in_memory_investor_repository import InMemoryInvestorRepository
from fintech_lab.infrastructure.in_memory_unit_of_work import InMemoryUnitOfWork


def test_committed_changes_are_visible_after_the_block():
    committed = InMemoryInvestorRepository()

    with InMemoryUnitOfWork(committed_investors=committed) as uow:
        uow.investors.add(Investor(investor_id=1, name="Ada Lovelace"))
        uow.commit()

    assert committed.get(1) is not None


def test_uncommitted_changes_are_rolled_back_when_the_block_exits_normally():
    committed = InMemoryInvestorRepository()

    with InMemoryUnitOfWork(committed_investors=committed) as uow:
        uow.investors.add(Investor(investor_id=1, name="Ada Lovelace"))
        # no commit() call

    assert committed.get(1) is None


def test_changes_are_rolled_back_when_the_block_raises():
    committed = InMemoryInvestorRepository()

    with pytest.raises(ValueError):
        with InMemoryUnitOfWork(committed_investors=committed) as uow:
            uow.investors.add(Investor(investor_id=1, name="Ada Lovelace"))
            raise ValueError("something went wrong mid-operation")

    assert committed.get(1) is None


def test_unit_of_work_sees_prior_commits_from_earlier_units():
    committed = InMemoryInvestorRepository()
    with InMemoryUnitOfWork(committed_investors=committed) as uow:
        uow.investors.add(Investor(investor_id=1, name="Ada Lovelace"))
        uow.commit()

    with InMemoryUnitOfWork(committed_investors=committed) as uow:
        assert uow.investors.get(1) is not None
        uow.investors.add(Investor(investor_id=2, name="Alan Turing"))
        uow.commit()

    assert {investor.investor_id for investor in committed.list()} == {1, 2}
