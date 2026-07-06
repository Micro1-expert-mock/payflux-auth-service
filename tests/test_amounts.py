"""Tests for amount normalization.

Coverage note: the payments team's card mix is predominantly USD and EUR, so
these are the currencies exercised here.
"""
from decimal import Decimal

import pytest

from app.amounts import normalize_currency, to_minor_units


@pytest.mark.parametrize(
    "amount,expected",
    [
        ("12.50", 1250),
        ("0.99", 99),
        (100, 10000),
        (Decimal("19.95"), 1995),
        ("1499.00", 149900),
    ],
)
def test_to_minor_units_usd(amount, expected):
    assert to_minor_units(amount, "USD") == expected


@pytest.mark.parametrize(
    "amount,expected",
    [
        ("10.00", 1000),
        ("7.49", 749),
        (250, 25000),
        ("0.05", 5),
    ],
)
def test_to_minor_units_eur(amount, expected):
    assert to_minor_units(amount, "EUR") == expected


def test_to_minor_units_is_case_insensitive():
    assert to_minor_units("5.00", "usd") == 500


@pytest.mark.parametrize(
    "currency,amount,expected",
    [
        ("JPY", "3527", 3527),
        ("KRW", "155575", 155575),
        (" jpy ", "2843", 2843),
    ],
)
def test_to_minor_units_zero_decimal_currency(currency, amount, expected):
    assert to_minor_units(amount, currency) == expected


def test_normalize_currency():
    assert normalize_currency(" eur ") == "EUR"
