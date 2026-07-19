from fintech_lab.application.investor_service import InvestorService
from fintech_lab.domain.investor import Investor
from fintech_lab.infrastructure.in_memory_investor_repository import InMemoryInvestorRepository


def make_service() -> InvestorService:
    return InvestorService(repository=InMemoryInvestorRepository())


def test_register_assigns_sequential_ids():
    service = make_service()

    first = service.register("Ada Lovelace")
    second = service.register("Alan Turing")

    assert first.investor_id == 1
    assert second.investor_id == 2


def test_register_persists_the_investor():
    repository = InMemoryInvestorRepository()
    service = InvestorService(repository=repository)

    investor = service.register("Ada Lovelace")

    assert repository.get(investor.investor_id) is investor


def test_find_returns_a_registered_investor():
    service = make_service()
    investor = service.register("Ada Lovelace")

    assert service.find(investor.investor_id) is investor


def test_find_returns_none_for_unknown_id():
    service = make_service()

    assert service.find(999) is None


def test_register_avoids_id_collision_when_repository_is_not_empty():
    repository = InMemoryInvestorRepository()
    repository.add(Investor(investor_id=5, name="Existing Investor"))
    service = InvestorService(repository=repository)

    investor = service.register("Ada Lovelace")

    assert investor.investor_id == 6
