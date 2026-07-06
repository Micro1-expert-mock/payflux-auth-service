"""Shared gateway adapter machinery."""
from __future__ import annotations

import abc
import logging
from typing import Any, Dict

from ..amounts import to_minor_units
from ..models import AuthorizationRequest, AuthorizationResponse

logger = logging.getLogger("gateway")


class Gateway(abc.ABC):
    """Base class for acquirer gateway adapters."""

    name: str = "base"

    def build_payload(self, request: AuthorizationRequest, txn_id: str) -> Dict[str, Any]:
        """Build the outbound gateway payload for ``request``.

        The gateway API expects the amount as integer minor units.
        """
        amount_minor = to_minor_units(request.amount, request.currency)
        return {
            "merchant": request.merchant_id,
            "amount": amount_minor,
            "currency": request.currency.upper(),
            "network": request.card_network,
            "funding": request.card_funding,
            "issuer_country": request.issuer_country.upper(),
            "reference": txn_id,
        }

    @abc.abstractmethod
    def authorize(self, request: AuthorizationRequest, txn_id: str) -> AuthorizationResponse:
        """Send ``request`` to the acquirer and map the result."""
        raise NotImplementedError
