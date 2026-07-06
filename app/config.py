"""Service configuration: timeouts, retry policy and gateway endpoints."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict


@dataclass(frozen=True)
class RetryPolicy:
    """Outbound retry behaviour for gateway calls."""

    max_retries: int = 2
    backoff_ms: int = 150
    retry_on_status: tuple = (502, 503, 504)


@dataclass(frozen=True)
class GatewayEndpoint:
    name: str
    base_url: str
    timeout_ms: int


@dataclass(frozen=True)
class Settings:
    request_timeout_ms: int = 800
    retry_policy: RetryPolicy = field(default_factory=RetryPolicy)
    gateways: Dict[str, GatewayEndpoint] = field(
        default_factory=lambda: {
            "acmepay": GatewayEndpoint(
                name="acmepay",
                base_url="https://gw.acmepay.example/v2",
                timeout_ms=800,
            ),
            "northbridge": GatewayEndpoint(
                name="northbridge",
                base_url="https://api.northbridge.example/authorize",
                timeout_ms=900,
            ),
        }
    )


settings = Settings()
