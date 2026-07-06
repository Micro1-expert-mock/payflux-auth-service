"""AcmePay acquirer gateway adapter."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from ..config import settings
from ..models import AuthorizationRequest, AuthorizationResponse
from .base import Gateway

logger = logging.getLogger("gateway.acmepay")

# AcmePay approval / decline response codes.
_APPROVED = "00"


class AcmePayGateway(Gateway):
    """Adapter for the AcmePay authorization API."""

    name = "acmepay"

    def __init__(self, client: Optional[Any] = None) -> None:
        self._client = client
        self._endpoint = settings.gateways["acmepay"]

    def _send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST the payload to AcmePay and return the decoded JSON body."""
        if self._client is None:  # pragma: no cover - exercised via integration
            import httpx

            self._client = httpx.Client(timeout=self._endpoint.timeout_ms / 1000)
        resp = self._client.post(f"{self._endpoint.base_url}/authorizations", json=payload)
        resp.raise_for_status()
        return resp.json()

    def authorize(self, request: AuthorizationRequest, txn_id: str) -> AuthorizationResponse:
        payload = self.build_payload(request, txn_id)
        logger.info(
            "dispatching authorization merchant=%s currency=%s amount_minor=%s txn=%s",
            payload["merchant"],
            payload["currency"],
            payload["amount"],
            txn_id,
        )
        body = self._send(payload)
        code = body.get("response_code", _APPROVED)
        approved = code == _APPROVED
        return AuthorizationResponse(
            approved=approved,
            gateway=self.name,
            response_code=code,
            reason=body.get("reason"),
            txn_id=txn_id,
            amount_minor=payload["amount"],
            currency=payload["currency"],
        )
