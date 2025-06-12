# Delegation Token + Identity-Aware Proxy Design

## 🎯 Goal
Provide a secure mechanism for users to delegate short-lived access to a portal. The
AI agent receives a scoped token instead of raw credentials.

---

## 🔐 Flow Overview
```text
User Consent -> Token Service -> Scoped Token -> Identity-Aware Proxy -> Portal
```
1. **Consent** – User approves portal access via the backend API.
2. **Token Issue** – Backend generates a token with metadata (user, agent,
   portal scope, expiry).
3. **Agent Presentation** – The browser used by the agent includes the token
   (HTTP header or cookie) when visiting the proxy.
4. **Proxy Validation** – A lightweight proxy verifies the token and injects a
   logged-in session for the portal.
5. **Cleanup** – Token expires after a few minutes or on logout and the session
   is destroyed.

---

## 💡 Token Options
- **JWT**: Signed with HS256/RS256, includes `exp`, `sub` (user ID), `aud`
  (agent), and `portal` claims.
- **Signed Cookie**: Server-side secret generates an HMAC signature appended to a
  base64 payload.
- **OAuth 2.0**: Issue a bearer token with custom claims; useful if integrating
  with existing auth providers.

Regardless of format, the token must be:
- Short lived (e.g., 5–10 minutes)
- Scoped to a single portal and specific agent session
- Logged for audit purposes

---

## 🔐 Session Cleanup
1. Proxy clears portal cookies and invalidates the token on logout.
2. Redis or database entry for the token is deleted.
3. Audit log records the end of the delegated session.

---

## 📦 Future Enhancements
- Central service to rotate signing keys.
- Refresh tokens for longer workflows (requires re-prompting the user).
- UI view for users to revoke active tokens.

---

## 🧮 Prototype Module
A simple token utility could live in `app/auth/token.py`:
```python
from __future__ import annotations
from datetime import datetime, timedelta
import base64
import hashlib
import hmac
import json
import os
from typing import Dict, Optional

SECRET = os.getenv("DELEGATION_SECRET", "change-me")
ALGO = hashlib.sha256
DEFAULT_MINUTES = 10


def _sign(data: str) -> str:
    return hmac.new(SECRET.encode(), data.encode(), ALGO).hexdigest()


def create_token(user_id: str, agent_id: str, portal: str, minutes: int = DEFAULT_MINUTES) -> str:
    exp = (datetime.utcnow() + timedelta(minutes=minutes)).timestamp()
    payload = json.dumps({"user": user_id, "agent": agent_id, "portal": portal, "exp": exp})
    return base64.urlsafe_b64encode(payload.encode()).decode() + "." + _sign(payload)


def verify_token(token: str) -> Optional[Dict[str, str]]:
    try:
        data, sig = token.rsplit(".", 1)
        payload = base64.urlsafe_b64decode(data.encode()).decode()
        if _sign(payload) != sig:
            return None
        claims = json.loads(payload)
        if claims.get("exp", 0) < datetime.utcnow().timestamp():
            return None
        return claims
    except Exception:
        return None
```
This helper demonstrates how a short-lived signed token might be created and
validated without relying on external dependencies.
