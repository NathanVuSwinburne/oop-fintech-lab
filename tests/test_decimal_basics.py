from decimal import Decimal


def test_float_arithmetic_drifts():
    assert 0.1 + 0.2 != 0.3  # binary floats can't represent 0.1 or 0.2 exactly


def test_decimal_arithmetic_is_exact():
    assert Decimal("0.1") + Decimal("0.2") == Decimal("0.3")


def test_decimal_from_float_inherits_the_same_drift():
    # constructing from a float bakes the float's rounding error in first —
    # always build Decimal from a string or an int, never from a float.
    assert Decimal(0.1) != Decimal("0.1")
