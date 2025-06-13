import argparse
import importlib
import json
import os
import tempfile
from pathlib import Path
from typing import List, Dict

from app.utils import llm

# Ensure repo root on path for `app` imports when executed directly
ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in os.sys.path:
    os.sys.path.insert(0, str(ROOT_DIR))

from app.processors.lab_pdf_parser import extract_lab_results_with_date
from app.processors.visit_html_parser import extract_visit_summaries
from app.processors.structuring import insert_lab_results, insert_visit_summaries
from app.prompts.summarizer import summarize_blocks
from app.api.rag import ask_question, QueryRequest
from app.utils.sample_files import create_sample_pdf, create_sample_html



def _maybe_mock_openai() -> None:
    """Mock OpenAI API if no API key is configured."""
    if os.getenv("OPENAI_API_KEY"):
        return

    def fake_create(messages, **_kwargs):
        content = messages[0]["content"]
        if "Question:" in content:
            return "Mock answer"
        return "Mock summary"

    llm.chat_completion = fake_create


def load_lab_data(path: Path) -> List[Dict]:
    if path.suffix.lower() == ".pdf":
        return extract_lab_results_with_date(str(path))
    return json.loads(path.read_text())


def load_visit_data(path: Path) -> List[Dict]:
    if path.suffix.lower() == ".html":
        return extract_visit_summaries(path.read_text())
    return json.loads(path.read_text())


def query_ask(question: str) -> str:
    resp = ask_question(QueryRequest(query=question))
    return resp["answer"]


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed DB and preview responses")
    parser.add_argument("--lab-file", help="Path to lab PDF or JSON")
    parser.add_argument("--visit-file", help="Path to visit HTML or JSON")
    parser.add_argument("--db", default="health_data.db", help="SQLite DB path")
    parser.add_argument("--summary", action="store_true", help="Show lab summary")
    parser.add_argument("--ask", metavar="QUESTION", help="Query for /ask endpoint")
    args = parser.parse_args()

    if not args.lab_file:
        ans = input("Lab file path (blank for sample): ").strip()
        if ans:
            lab_path = Path(ans)
        else:
            tmp = Path(tempfile.gettempdir()) / "sample_labs.pdf"
            create_sample_pdf(tmp)
            lab_path = tmp
    else:
        lab_path = Path(args.lab_file)

    if not args.visit_file:
        ans = input("Visit file path (blank for sample): ").strip()
        if ans:
            visit_path = Path(ans)
        else:
            tmp = Path(tempfile.gettempdir()) / "sample_visits.html"
            create_sample_html(tmp)
            visit_path = tmp
    else:
        visit_path = Path(args.visit_file)

    os.environ["DATABASE_URL"] = f"sqlite:///{args.db}"

    # Reload DB modules so they pick up the new DB URL
    import app.storage.db as db_module
    import app.storage.models as models_module

    db_module = importlib.reload(db_module)
    models_module = importlib.reload(models_module)
    db_module.init_db()

    session = db_module.SessionLocal()

    try:
        labs = load_lab_data(lab_path)
        visits = load_visit_data(visit_path)
        insert_lab_results(session, labs)
        insert_visit_summaries(session, visits)
    finally:
        session.close()

    print("=== Database Seeded ===")
    print(f"Labs inserted: {len(labs)}")
    print(f"Visits inserted: {len(visits)}")

    _maybe_mock_openai()

    if args.summary:
        session = db_module.SessionLocal()
        db_labs = session.query(models_module.LabResult).order_by(models_module.LabResult.date).all()
        session.close()
        lab_data = [
            {
                "test_name": l.test_name,
                "value": l.value,
                "units": l.units,
                "date": l.date.isoformat(),
            }
            for l in db_labs
        ]
        print("\n=== summarize_blocks() ===")
        summary = summarize_blocks([{"text": str(item)} for item in lab_data])
        print(summary)

    if args.ask:
        print("\n=== POST /ask ===")
        answer = query_ask(args.ask)
        print(answer)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # pragma: no cover - manual script
        print(f"ERROR: {exc}")
        raise
