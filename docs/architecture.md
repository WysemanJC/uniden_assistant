# API Architecture (Strict Multi‑Tier)

This application enforces a strict multi‑tier API hierarchy. The front end must **only** communicate with the Uniden Manager API. All other APIs are internal tiers and must **never** be called directly by the front end.

## API Tiers

### 1) Uniden Manager (Front‑End Gateway)
- **Base:** /api/uniden_manager/
- **Purpose:** Gateway for all front‑end requests.
- **Rule:** Does **not** read from or write to any database.
- **Behavior:** Proxies/aggregates data from the internal tier APIs below.

### 2) HPDB API
- **Base:** /api/hpdb/
- **Purpose:** Read‑only HPDB data (countries, states, counties, agencies, channel groups, frequencies, tree).
- **Database:** Dedicated MongoDB database (HPDB only).
- **Rule:** Does **not** read or write any other database.

### 3) User Settings API
- **Base:** /api/usersettings/
- **Purpose:** User‑scoped settings, profiles, favorites, and SD import/export.
- **Database:** Dedicated MongoDB database (user settings only).
- **Rule:** Does **not** read or write any other database.

### 4) App Config API
- **Base:** /api/appconfig/
- **Purpose:** Static configuration (e.g., supported scanner models).
- **Database:** Dedicated MongoDB database (app config only).
- **Rule:** Does **not** read or write any other database.

## Database Isolation

- **SQLite:** Django core tables only (auth, admin, sessions, etc.).
- **MongoDB:**
  - HPDB data in its own database.
  - User settings/favorites in its own database.
  - App configuration in its own database.

## Front‑End Routing Rule

**The front end MUST ONLY call** /api/uniden_manager/.

All internal APIs are **server‑side only** and should never be invoked by the UI.
