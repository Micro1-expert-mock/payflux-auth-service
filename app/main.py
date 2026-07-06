"""FastAPI application exposing the card authorization endpoint."""
from __future__ import annotations

import logging
import uuid

from fastapi import FastAPI

from . import __version__
from .gateways import AcmePayGateway, NorthBridgeGateway
from .models import AuthorizationRequest, AuthorizationResponse
from .routing import ACMEPAY, select_gateway

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("app")

app = FastAPI(title="payflux-auth-service", version=__version__)

_GATEWAYS = {
    "acmepay": AcmePayGateway(),
    "northbridge": NorthBridgeGateway(),
}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "ok", "version": __version__}


@app.post("/authorize", response_model=AuthorizationResponse)
def authorize(request: AuthorizationRequest) -> AuthorizationResponse:
    """Route an authorization request to the appropriate acquirer gateway."""
    txn_id = f"TXN-{uuid.uuid4().hex[:12].upper()}"
    gateway_name = select_gateway(request)
    gateway = _GATEWAYS.get(gateway_name, _GATEWAYS[ACMEPAY])
    logger.info("routing txn=%s to gateway=%s", txn_id, gateway_name)
    return gateway.authorize(request, txn_id)
