class Investor:
    """A person who holds one or more investment accounts."""

    def __init__(self, investor_id: int, name: str) -> None:
        self.investor_id = investor_id
        self.name = name  # goes through the property setter below

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        value = value.strip()
        if not value:
            raise ValueError("Investor name cannot be empty")
        self._name = value

    def __repr__(self) -> str:
        return f"Investor(investor_id={self.investor_id!r}, name={self.name!r})"
