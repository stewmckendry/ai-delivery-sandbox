# Task 23: Delegation Token + Identity-Aware Proxy Design

## 🎯 Goal
Enable secure session delegation where a user grants the AI agent limited access via a short-lived, scoped token.

## 📂 Target Files
- `docs/design/delegation_token_flow.md`
- Optional: `app/auth/token.py`

## 📋 Instructions
- Describe architecture for short-lived delegation tokens:
  - User consents
  - System issues scoped token with expiry + user+agent metadata
  - AI agent browser presents token via secure proxy or cookie
- Explore token types: JWT, signed cookie, OAuth w/ claims
- Include session cleanup/logout flow
- Optionally scaffold token generation module

## 🧪 Test
- None yet — architecture only

## ✅ What to Report Back
- Design doc explaining the delegation token model
- Optional prototype scaffolding