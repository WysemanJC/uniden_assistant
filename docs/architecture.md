# API Architecture (Strict Multi‑Tier)

This application enforces a strict multi‑tier API hierarchy. The front end must **only** communicate with the Uniden Manager API. All other APIs are internal tiers and must **never** be called directly by the front end.

## API Tiers

### 1) Uniden Manager (Front‑End Gateway)
- **Base:** /api/uniden_manager/
- **Purpose:** Gateway for all front‑end requests.
- **Rule:** Does **not** read from or write to any database.
- **Behavior:** Proxies/aggregates data from the internal tier APIs below.

### 2) Favourites API
- **Base:** /api/favourites/
- **Purpose:** User‑scoped favorites lists, scanner profiles, frequencies, and import/export functionality.
- **Database:** Dedicated SQLite database file (favourites only).
- **Rule:** Does **not** read or write any other database.

## Database Isolation

- **SQLite (default):** Django core tables only (auth, admin, sessions, etc.).
- **SQLite (favourites):** User favorites and scanner profiles in a dedicated database file.

## Front‑End Routing Rule

**The front end MUST ONLY call** /api/uniden_manager/.

All internal APIs are **server‑side only** and should never be invoked by the UI.

## Simplified Architecture

The application was originally designed with three separate MongoDB databases (HPDB, User Settings, App Config) but has been simplified to:

- **Dedicated SQLite database** for all user-facing functionality (favourites, scanner profiles, frequencies)
- **Removed:** HPDB (historical frequency database) functionality
- **Removed:** App Config (unused scanner model configuration)
- **Consolidated:** User settings renamed to "favourites" for clarity

This simplification reduces operational complexity while maintaining the strict multi-tier API architecture.
