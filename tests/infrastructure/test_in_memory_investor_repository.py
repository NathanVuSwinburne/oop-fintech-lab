from fintech_lab.domain.investor import Investor
from fintech_lab.infrastructure.in_memory_investor_repository import InMemoryInvestorRepository


def test_added_investor_can_be_retrieved_by_id():
    repo = InMemoryInvestorRepository()
    investor = Investor(investor_id=1, name="Ada Lovelace")

    repo.add(investor)

    assert repo.get(1) is investor


def test_get_returns_none_for_unknown_id():
    repo = InMemoryInvestorRepository()

    assert repo.get(999) is None


def test_list_returns_all_added_investors():
    repo = InMemoryInvestorRepository()
    ada = Investor(investor_id=1, name="Ada Lovelace")
    alan = Investor(investor_id=2, name="Alan Turing")

    repo.add(ada)
    repo.add(alan)

    assert repo.list() == [ada, alan]


def test_adding_with_same_id_overwrites():
    repo = InMemoryInvestorRepository()
    repo.add(Investor(investor_id=1, name="Ada Lovelace"))
    replacement = Investor(investor_id=1, name="Ada, Countess of Lovelace")

    repo.add(replacement)

    assert repo.get(1) is replacement
    assert len(repo.list()) == 1
