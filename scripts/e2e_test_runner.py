#!/usr/bin/env python
"""End-to-end test runner for local QA.

This script simulates the full pipeline:
1. Mock portal scrape using static sample files.
2. Parse the files and insert records into an in-memory SQLite DB.
3. Generate a summary of lab results.
4. Query the `/ask` endpoint using ``httpx.AsyncClient``.

Outputs from each stage are printed with clear headers so QA can verify
behaviour without external dependencies.
"""

from __future__ import annotations

import importlib
import os
import sys
import tempfile
from pathlib import Path
from typing import Dict, List
import asyncio

# Ensure repo root is on sys.path so `app` package resolves
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import openai
import httpx


# ---------------------------------------------------------------------------
# Utilities to create sample input files
# ---------------------------------------------------------------------------

def create_sample_pdf(path: Path) -> None:
    import fitz  # PyMuPDF

    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), "Cholesterol 5.8 mmol/L 2023-05-01")
    page.insert_text((72, 90), "Hemoglobin 13.5 g/dL 2023-05-02")
    doc.save(path)
    doc.close()


def create_sample_html(path: Path) -> None:
    html = """
    <html><body>
      <div class='visit'>
        <span class='date'>2023-06-01</span>
        <span class='provider'>General Hospital</span>
        <span class='doctor'>Dr. Jones</span>
        <p class='notes'>Routine check</p>
      </div>
    </body></html>
    """
    path.write_text(html, encoding="utf-8")


# ---------------------------------------------------------------------------
# Main pipeline logic
# ---------------------------------------------------------------------------

def main() -> None:
    tmp_db = tempfile.NamedTemporaryFile(delete=False)
    tmp_db.close()
    os.environ["DATABASE_URL"] = f"sqlite:///{tmp_db.name}"

    # Reload DB modules so they pick up the in-memory database
    import app.storage.db as db_module
    import app.storage.models as models_module

    db = importlib.reload(db_module)
    models = importlib.reload(models_module)
    db.init_db()

    with tempfile.TemporaryDirectory() as tmpdir:
        tmp = Path(tmpdir)
        pdf_path = tmp / "labs.pdf"
        html_path = tmp / "visits.html"
        create_sample_pdf(pdf_path)
        create_sample_html(html_path)

        # ------------------------------------------------------------------
        # Step 1: Mock portal scrape
        # ------------------------------------------------------------------
        print("=== STEP 1: Mock Portal Scrape ===")

        def fake_scraper(*_args, **_kwargs) -> Dict[str, List[str]]:
            return {"files": [str(html_path), str(pdf_path)]}

        import app.orchestrator as orch_module

        orch = importlib.reload(orch_module)
        orch._load_scraper = lambda name: fake_scraper

        orch.run_etl_for_portal("portal_a")

        # ------------------------------------------------------------------
        # Step 2: Inspect inserted records
        # ------------------------------------------------------------------
        print("\n=== STEP 2: DB Records ===")
        session = db.SessionLocal()
        labs = session.query(models.LabResult).all()
        visits = session.query(models.VisitSummary).all()
        session.close()

        for lab in labs:
            print(f"Lab: {lab.test_name} {lab.value} {lab.units} ({lab.date})")
        for visit in visits:
            print(
                f"Visit: {visit.date} - {visit.provider} - {visit.doctor}: {visit.notes}"
            )

        # ------------------------------------------------------------------
        # Step 3: Summarize lab results
        # ------------------------------------------------------------------
        def fake_create(*args, **kwargs):
            prompt = kwargs["messages"][0]["content"]
            if "Question:" in prompt:
                return {"choices": [{"message": {"content": "Mock answer"}}]}
            return {"choices": [{"message": {"content": "Mock summary"}}]}

        openai.ChatCompletion.create = fake_create

        from app.prompts.summarizer import summarize_blocks

        lab_data = [
            {
                "test_name": l.test_name,
                "value": l.value,
                "units": l.units,
                "date": l.date.isoformat(),
            }
            for l in labs
        ]

        print("\n=== STEP 3: summarize_blocks() ===")
        summary = summarize_blocks([{"text": str(item)} for item in lab_data])
        print(summary)

        # ------------------------------------------------------------------
        # Step 4: Query the /ask endpoint
        # ------------------------------------------------------------------
        print("\n=== STEP 4: /ask Endpoint ===")
        import app.main as main_module

        main_app = importlib.reload(main_module)
        transport = httpx.ASGITransport(app=main_app.app)
        async def call_api():
            async with httpx.AsyncClient(transport=transport, base_url="http://test") as client:
                return await client.post("/ask", json={"query": "How am I doing?"})

        resp = asyncio.run(call_api())
        print(f"Status: {resp.status_code} - Response: {resp.json()}")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"ERROR: {exc}")
        sys.exit(1)
