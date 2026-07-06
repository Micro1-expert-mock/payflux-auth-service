# payflux-auth-service

Card authorization routing service for **PayFlux**. It accepts authorization
requests and routes each one to the appropriate acquirer gateway (**AcmePay**
or **NorthBridge**) based on the card network and issuer country.

## Overview

```
client ─▶ POST /authorize ─▶ routing.select_gateway ─▶ AcmePay | NorthBridge ─▶ response
```

- `app/main.py` — FastAPI app, exposes `POST /authorize` and `GET /healthz`.
- `app/routing.py` — gateway selection rules (network + issuer country).
- `app/amounts.py` — currency/amount helpers (major → minor units).
- `app/gateways/` — AcmePay and NorthBridge adapters (build payload, call API).
- `app/models.py` — request/response models.
- `app/config.py` — timeouts, retry policy, gateway endpoints.

## Running locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```

Example request:

```bash
curl -s localhost:8080/authorize -H 'content-type: application/json' -d '{
  "merchant_id": "M-4821",
  "amount": "42.00",
  "currency": "USD",
  "card_network": "visa",
  "card_funding": "credit",
  "issuer_country": "US"
}'
```

## Testing

```bash
pip install -r requirements-dev.txt
pytest
```

## Operations

- Application logs are shipped to the central log store; a daily archive copy is
  kept under `ops/logs/`.
- KPI dashboards (authorization rate, latency) live under `docs/dashboards/`.
- Release history is tracked in [RELEASES.md](RELEASES.md).
