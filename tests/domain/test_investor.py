import pytest

from fintech_lab.domain.exceptions import ValidationError
from fintech_lab.domain.investor import Investor


def test_investor_stores_id_and_name():
    investor = Investor(investor_id=1, name="Ada Lovelace")

    assert investor.investor_id == 1
    assert investor.name == "Ada Lovelace"


def test_name_is_stripped():
    investor = Investor(investor_id=1, name="  Ada  ")

    assert investor.name == "Ada"


def test_empty_name_is_rejected():
    with pytest.raises(ValidationError):
        Investor(investor_id=1, name="   ")


def test_repr_includes_id_and_name():
    investor = Investor(investor_id=1, name="Ada Lovelace")

    assert "Ada Lovelace" in repr(investor)
