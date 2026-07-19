class FintechLabError(Exception):
    """Base class for all domain errors. Catch this to handle any of them at once."""


class ValidationError(FintechLabError):
    """Input to a domain operation violated a business rule (e.g. a negative amount)."""


class InsufficientFundsError(FintechLabError):
    """A withdrawal (or other debit) exceeds the available balance."""


class OrderNotFilledError(FintechLabError):
    """An operation required a filled Order, but the Order hasn't filled."""


class PermissionDeniedError(FintechLabError):
    """A user attempted an operation their roles don't grant permission for."""
