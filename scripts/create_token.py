#!/usr/bin/env python
"""Generate a signed delegation token for API calls."""
from __future__ import annotations

import argparse
import sys
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.auth.token import create_token


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a short-lived token")
    parser.add_argument("--user", required=True, help="User identifier")
    parser.add_argument("--agent", required=True, help="Agent identifier")
    parser.add_argument("--portal", required=True, help="Portal name")
    parser.add_argument(
        "--minutes",
        type=int,
        default=10,
        help="Token lifetime in minutes (default: 10)",
    )
    args = parser.parse_args()

    token = create_token(args.user, args.agent, args.portal, minutes=args.minutes)
    print(token)


if __name__ == "__main__":  # pragma: no cover - CLI entry
    main()