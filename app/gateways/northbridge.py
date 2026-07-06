"""NorthBridge acquirer gateway adapter."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

from ..config import settings
from ..models import AuthorizationRequest, AuthorizationResponse
from .base import Gateway

logger = logging.getLogger("gateway.northbridge")

# NorthBridge returns "approved": true/false plus a decline code string.
_APPROVED_CODE = "APPROVED"


class NorthBridgeGateway(Gateway):
    """Adapter for the NorthBridge authorization API."""

    name = "northbridge"

    def __init__(self, client: Optional[Any] = None) -> None:
        self._client = client
        self._endpoint = settings.gateways["northbridge"]

    def _send(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """POST the payload to NorthBridge and return the decoded JSON body."""
        if self._client is None:  # pragma: no cover - exercised via integration
            import httpx

            self._client = httpx.Client(timeout=self._endpoint.timeout_ms / 1000)
        resp = self._client.post(self._endpoint.base_url, json=payload)
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
        status = body.get("status", _APPROVED_CODE)
        approved = status == _APPROVED_CODE
        return AuthorizationResponse(
            approved=approved,
            gateway=self.name,
            response_code=body.get("code", "00" if approved else "05"),
            reason=body.get("reason"),
            txn_id=txn_id,
            amount_minor=payload["amount"],
            currency=payload["currency"],
        )
