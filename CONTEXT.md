# CONTEXT.md

This file exists so another coding agent (or a future session) can pick up this
project without re-deriving the plan from scratch.

## Original prompt

> Build a Python project called **OOP Fintech Lab**.
>
> The project should be a simulated investment-platform backend that helps me learn
> the software engineering knowledge expected from a graduate developer.
>
> I want to learn through a real, well-organised codebase rather than isolated
> examples.
>
> The project should gradually teach and demonstrate: classes and objects,
> constructors/self/attributes/state/methods, encapsulation, abstraction,
> inheritance, polymorphism, composition, method overriding, class/static methods,
> properties/getters/setters, abstract classes and interfaces, SOLID principles,
> coupling and cohesion, dependency injection, repository pattern, service-layer
> pattern, strategy pattern, factory pattern, observer pattern, unit of work
> pattern, exception handling, type hints, clean code and refactoring, unit and
> integration testing with pytest, and debugging realistic software problems.
>
> The fintech domain should gradually include: Investor, Investment account,
> Financial product, Portfolio, Holding, Order, Transaction, Adviser, User, Role
> and permission.
>
> Also wanted: how to structure a professional Python repository; how to separate
> domain/application/infrastructure logic; how to organise files as the project
> grows; when a new folder/class/abstraction is justified vs overengineering; how
> to document design decisions; how to write meaningful git commits.
>
> After the OOP foundation, gradually extend to: raw SQL, PostgreSQL, schema
> design, keys, UUIDs, relationships/normalisation, CRUD, joins/aggregations,
> constraints/indexes, transactions/ACID, concurrency, SQLAlchemy, FastAPI, REST
> APIs, auth, logging, env config, migrations, Docker, CI/CD, performance and
> security.
>
> Use `Decimal` for financial values, explain fintech-specific engineering
> decisions. Work incrementally, one small part at a time, explained and
> implemented before being quizzed on it. User says "next" to advance.

The full agreed roadmap (proposed before any code was written, still governing
the plan) lives in the conversation history; the short version is reproduced
below under "Roadmap" so it survives even if history is lost.

## Working agreement

- One small step per turn. Explain + implement + test, then stop and let the
  user ask questions. Do not jump ahead.
- User says **"next"** to advance to the next roadmap item.
- `domain/` stays framework-free — no DB, no HTTP, no I/O. Layer boundary is a
  deliberate teaching point.
- Every step gets a runnable `pytest` test alongside the code, in `tests/`
  mirroring the `src/` layout.
- No abstractions added ahead of need (YAGNI) — e.g. no `Money` value object
  yet because nothing handles multiple currencies. `infrastructure/` (step 10)
  and `application/` (step 11) now exist, holding only what those steps needed.

## Roadmap (Phase A — OOP foundations)

1. ✅ `Investor` — class, constructor, `self`, attributes, encapsulation (properties)
2. ✅ `InvestmentAccount` — composition, state mutation
3. ✅ `Decimal` handling — why `float` is wrong for finance (`tests/test_decimal_basics.py`)
4. ✅ `FinancialProduct` abstract base — abstraction, ABCs
5. ✅ Concrete products (`Stock`, `Bond`, `Fund`) — inheritance, polymorphism, overriding
6. ✅ `Holding`, `Portfolio` — composition, aggregate calculations
7. ✅ `Order` + `OrderExecutionStrategy` — Strategy pattern, DI preview
8. ✅ `Transaction` — immutability, value objects (frozen dataclass)
9. ✅ Custom exceptions — exception hierarchy
10. ✅ Repository pattern (in-memory first)
11. ✅ Service layer
12. ✅ Factory pattern
13. ⬜ Observer pattern **(NEXT)**
14. ⬜ Dependency injection (formalized, beyond the Order preview)
15. ⬜ Unit of Work
16. ⬜ `User`, `Role`, `Adviser`, permissions
17. ⬜ Refactor pass — SOLID review, coupling/cohesion
18. ⬜ Full `pytest` suite pass — fixtures, test doubles

**Phase B — Systems/infra** (after Phase A): PostgreSQL schema design →
raw-SQL repository → SQLAlchemy → FastAPI → auth → logging/config → Alembic
migrations → Docker → CI/CD → performance & security.

## Current repo state

```
src/fintech_lab/domain/
  investor.py            Investor
  investment_account.py  InvestmentAccount
  financial_product.py   FinancialProduct (ABC)
  products.py             Stock, Bond, Fund
  holding.py              Holding
  portfolio.py            Portfolio
  order.py                Order
  order_execution.py      OrderExecutionStrategy, MarketOrderExecution, LimitOrderExecution
  transaction.py           Transaction (frozen dataclass, built via Transaction.from_order)
  exceptions.py            FintechLabError base + ValidationError, InsufficientFundsError,
                            OrderNotFilledError
  repositories.py          InvestorRepository (ABC) — the port, no I/O

src/fintech_lab/infrastructure/
  in_memory_investor_repository.py   InMemoryInvestorRepository — the adapter

src/fintech_lab/application/
  investor_service.py      InvestorService — register()/find(), DI'd InvestorRepository,
                            owns id-assignment orchestration (not a domain rule)

domain/product_factory.py  FinancialProductFactory — static create(type, id, name, price),
                            dispatches to Stock/Bond/Fund, ValidationError on unknown type

tests/                   mirrors src/, one test file per module, 44 tests passing
tests/test_decimal_basics.py   language-level Decimal-vs-float demo (not domain-specific)
```

Run tests: `pytest` (rootdir is repo root, `pythonpath = ["src"]` set in `pyproject.toml`).

## Next step

**Step 13: Observer pattern.** Introduce an observer/event mechanism — likely
on `Order` or `InvestmentAccount` (e.g. notify observers when an order fills,
or when a balance changes) — so interested parties (a logger, a notification
stub) can react to domain events without the subject knowing who they are.
