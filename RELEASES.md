# Release Log

All times UTC. Deploys follow the standard staged rollout (canary → full).

## v2.14.0 — 2026-06-24 14:00
**Amount normalization refactor & payload cleanup**

- Refactored `to_minor_units()` for clarity and consolidated the duplicated
  gateway payload-builder logic into a single shared helper.
- Improved gateway log messages (structured `amount_minor` / `txn` fields).
- No expected behavior change.

Merged: PR "Refactor amount normalization and gateway payload builder"
(Daniel Osei). Deployed 14:00, full rollout 14:07.

## v2.13.2 — 2026-06-16 10:30
- Bumped `httpx` and `pydantic` pins.
- Added routing tests for AmEx/JCB acquirer restrictions.

## v2.13.1 — 2026-06-09 09:45
- NorthBridge adapter: map `status`/`code` fields to the internal response model.
- Minor logging cleanup in the request path.

## v2.13.0 — 2026-06-03 11:00
- Added issuer-country routing rules (APAC/ANZ + India → NorthBridge).
- Introduced `GET /healthz`.

## v2.12.1 — 2026-05-29 14:20
- Configurable request timeout and retry policy.
- Initial gateway adapters (AcmePay, NorthBridge).

## v2.12.0 — 2026-05-28 16:00
- First cut of the authorization routing service (FastAPI, `POST /authorize`).
