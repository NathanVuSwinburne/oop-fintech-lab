from decimal import Decimal

from fintech_lab.domain.holding import Holding


class Portfolio:
    """A collection of Holdings, aggregated into a total value."""

    def __init__(self, portfolio_id: int) -> None:
        self.portfolio_id = portfolio_id
        self._holdings: list[Holding] = []

    @property
    def holdings(self) -> list[Holding]:
        return list(self._holdings)  # copy: caller can't mutate our internal list

    def add_holding(self, holding: Holding) -> None:
        self._holdings.append(holding)

    def total_value(self) -> Decimal:
        return sum((holding.market_value() for holding in self._holdings), Decimal("0"))

    def __repr__(self) -> str:
        return f"Portfolio(portfolio_id={self.portfolio_id!r}, holdings={len(self._holdings)})"
