from fintech_lab.domain.exceptions import (
    FintechLabError,
    InsufficientFundsError,
    OrderNotFilledError,
    ValidationError,
)


def test_all_domain_exceptions_are_fintech_lab_errors():
    # the point of a base class: callers can catch FintechLabError once instead
    # of listing every specific exception type
    assert issubclass(ValidationError, FintechLabError)
    assert issubclass(InsufficientFundsError, FintechLabError)
    assert issubclass(OrderNotFilledError, FintechLabError)
