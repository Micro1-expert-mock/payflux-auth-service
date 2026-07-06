"""Tests for gateway routing rules."""
import pytest

from app.models import AuthorizationRequest, CardFunding, CardNetwork
from app.routing import ACMEPAY, NORTHBRIDGE, select_gateway


def _req(network, country, funding=CardFunding.CREDIT):
    return AuthorizationRequest(
        merchant_id="M-1000",
        amount="10.00",
        currency="USD",
        card_network=network,
        card_funding=funding,
        issuer_country=country,
    )


@pytest.mark.parametrize("country", ["JP", "KR", "SG", "IN", "AU"])
def test_visa_apac_routes_to_northbridge(country):
    assert select_gateway(_req(CardNetwork.VISA, country)) == NORTHBRIDGE


@pytest.mark.parametrize("country", ["US", "GB", "DE", "FR"])
def test_visa_western_routes_to_acmepay(country):
    assert select_gateway(_req(CardNetwork.VISA, country)) == ACMEPAY


def test_mastercard_follows_country_rules():
    assert select_gateway(_req(CardNetwork.MASTERCARD, "HK")) == NORTHBRIDGE
    assert select_gateway(_req(CardNetwork.MASTERCARD, "US")) == ACMEPAY


@pytest.mark.parametrize("country", ["JP", "US", "SG"])
def test_amex_always_acmepay(country):
    assert select_gateway(_req(CardNetwork.AMEX, country)) == ACMEPAY


def test_jcb_always_acmepay():
    assert select_gateway(_req(CardNetwork.JCB, "JP")) == ACMEPAY
