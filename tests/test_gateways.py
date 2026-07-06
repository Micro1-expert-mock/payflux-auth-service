"""Tests for gateway adapters (transport mocked)."""
from app.gateways import AcmePayGateway, NorthBridgeGateway
from app.models import AuthorizationRequest, CardNetwork


class _FakeResponse:
    def __init__(self, payload):
        self._payload = payload

    def raise_for_status(self):
        return None

    def json(self):
        return self._payload


class _FakeClient:
    """Captures the outbound payload and returns a canned response."""

    def __init__(self, response):
        self._response = response
        self.last_payload = None
        self.last_url = None

    def post(self, url, json):  # noqa: A002 - mirrors httpx signature
        self.last_url = url
        self.last_payload = json
        return _FakeResponse(self._response)


def _req(currency="USD", amount="12.50", network=CardNetwork.VISA, country="US"):
    return AuthorizationRequest(
        merchant_id="M-4821",
        amount=amount,
        currency=currency,
        card_network=network,
        issuer_country=country,
    )


def test_acmepay_approved_payload_uses_minor_units():
    client = _FakeClient({"response_code": "00"})
    gw = AcmePayGateway(client=client)
    resp = gw.authorize(_req(currency="USD", amount="12.50"), "TXN-TEST-1")
    assert client.last_payload["amount"] == 1250
    assert client.last_payload["currency"] == "USD"
    assert resp.approved is True
    assert resp.gateway == "acmepay"


def test_acmepay_decline_maps_reason():
    client = _FakeClient({"response_code": "51", "reason": "insufficient_funds"})
    gw = AcmePayGateway(client=client)
    resp = gw.authorize(_req(currency="EUR", amount="40.00"), "TXN-TEST-2")
    assert resp.approved is False
    assert resp.response_code == "51"
    assert resp.reason == "insufficient_funds"
    assert client.last_payload["amount"] == 4000


def test_northbridge_approved():
    client = _FakeClient({"status": "APPROVED", "code": "00"})
    gw = NorthBridgeGateway(client=client)
    resp = gw.authorize(_req(currency="EUR", amount="10.00", country="DE"), "TXN-TEST-3")
    assert resp.approved is True
    assert resp.gateway == "northbridge"
    assert client.last_payload["amount"] == 1000


def test_northbridge_decline():
    client = _FakeClient({"status": "DECLINED", "code": "05", "reason": "do_not_honor"})
    gw = NorthBridgeGateway(client=client)
    resp = gw.authorize(_req(currency="USD", amount="99.00"), "TXN-TEST-4")
    assert resp.approved is False
    assert resp.response_code == "05"
