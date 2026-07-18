from decimal import Decimal

from fintech_lab.application.composition_root import place_market_order


def test_place_market_order_wires_everything_and_records_a_transaction():
    recorder = place_market_order(
        investor_name="Ada Lovelace",
        product_type="stock",
        product_name="Acme Corp",
        price=Decimal("100"),
        quantity=Decimal("10"),
    )

    assert len(recorder.transactions) == 1
    transaction = recorder.transactions[0]
    assert transaction.account.investor.name == "Ada Lovelace"
    assert transaction.product.name == "Acme Corp"
    assert transaction.quantity == Decimal("10")
    assert transaction.price == Decimal("100")
    assert transaction.total_value == Decimal("1000")
