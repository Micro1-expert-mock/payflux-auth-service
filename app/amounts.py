"""Currency and amount utilities.

Gateways expect integer *minor units* (e.g. cents) in their payloads. This
module converts human-facing major-unit amounts into that representation.
"""
from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Union

Number = Union[int, float, str, Decimal]

_CENTS = Decimal("100")
_ONE = Decimal("1")
_ZERO_DECIMAL_CURRENCIES = frozenset({"JPY", "KRW"})


def normalize_currency(currency: str) -> str:
    """Return the canonical upper-case ISO 4217 alpha code."""
    return currency.strip().upper()


def to_minor_units(amount: Number, currency: str) -> int:
    """Convert a major-unit ``amount`` to integer minor units.

    Examples:
        >>> to_minor_units("12.50", "USD")
        1250
    """
    scale = _ONE if normalize_currency(currency) in _ZERO_DECIMAL_CURRENCIES else _CENTS
    value = Decimal(str(amount)) * scale
    return int(value.quantize(_ONE, rounding=ROUND_HALF_UP))
