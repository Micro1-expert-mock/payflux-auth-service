"""Request/response models for the authorization service."""
from __future__ import annotations

from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel, Field


class CardNetwork(str, Enum):
    VISA = "visa"
    MASTERCARD = "mastercard"
    AMEX = "amex"
    JCB = "jcb"


class CardFunding(str, Enum):
    CREDIT = "credit"
    DEBIT = "debit"
    PREPAID = "prepaid"


class AuthorizationRequest(BaseModel):
    """An inbound card authorization request."""

    merchant_id: str = Field(..., description="Merchant identifier, e.g. M-4821")
    amount: Decimal = Field(..., gt=0, description="Amount in major units (e.g. 1500 JPY, 12.50 USD)")
    currency: str = Field(..., min_length=3, max_length=3, description="ISO 4217 alpha code")
    card_network: CardNetwork
    card_funding: CardFunding = CardFunding.CREDIT
    issuer_country: str = Field(..., min_length=2, max_length=2, description="ISO 3166-1 alpha-2")

    class Config:
        use_enum_values = True


class AuthorizationResponse(BaseModel):
    """The result returned to the caller."""

    approved: bool
    gateway: str
    response_code: str
    reason: Optional[str] = None
    txn_id: str
    amount_minor: int
    currency: str
