"""Gateway routing rules.

Authorization traffic is split between two acquirer gateways, AcmePay and
NorthBridge, based on the card network and the issuer country. The rules below
reflect the acquirer coverage agreements currently in force.
"""
from __future__ import annotations

from .models import AuthorizationRequest, CardNetwork

ACMEPAY = "acmepay"
NORTHBRIDGE = "northbridge"

# Issuer countries for which NorthBridge offers better interchange / coverage.
_NORTHBRIDGE_COUNTRIES = {"JP", "KR", "SG", "HK", "AU", "NZ", "IN"}

# AmEx and JCB are not certified on NorthBridge; they always route to AcmePay.
_ACMEPAY_ONLY_NETWORKS = {CardNetwork.AMEX.value, CardNetwork.JCB.value}


def select_gateway(request: AuthorizationRequest) -> str:
    """Return the gateway name that should handle ``request``.

    Rules (first match wins):
      1. AmEx / JCB are only certified on AcmePay.
      2. Cards issued in the APAC/ANZ + India coverage set prefer NorthBridge.
      3. Everything else routes to AcmePay.
    """
    network = request.card_network
    if isinstance(network, CardNetwork):
        network = network.value

    if network in _ACMEPAY_ONLY_NETWORKS:
        return ACMEPAY

    if request.issuer_country.upper() in _NORTHBRIDGE_COUNTRIES:
        return NORTHBRIDGE

    return ACMEPAY
