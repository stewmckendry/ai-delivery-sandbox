import argparse
import os
import json
from app.engines.memory_sync import save_session_snapshot

def main():
    parser = argparse.ArgumentParser(description="Create a session snapshot from input file")
    parser.add_argument("--session_id", required=True, help="Session identifier")
    parser.add_argument("--snapshot_path", required=True, help="Path to the snapshot data file")
    parser.add_argument("--notes", help="Optional notes for the snapshot")
    parser.add_argument("--user_id", help="Optional user identifier")

    args = parser.parse_args()

    save_session_snapshot(
        session_id=args.session_id,
        snapshot_path=args.snapshot_path,
        notes=args.notes,
        user_id=args.user_id
    )

if __name__ == "__main__":
    main()