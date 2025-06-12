from app.processors.visit_html_parser import extract_visit_summaries


def test_extract_visit_summaries():
    html = """
    <html>
      <body>
        <div class='visit'>
          <span class='date'>2023-06-01</span>
          <span class='provider'>General Hospital</span>
          <span class='doctor'>Dr. Jones</span>
          <p class='notes'>Follow-up recommended.</p>
        </div>
        <div class='visit'>
          <span class='date'>2023-07-10</span>
          <span class='provider'>City Clinic</span>
          <span class='doctor'>Dr. Smith</span>
          <p class='notes'>All good.</p>
        </div>
      </body>
    </html>
    """
    expected = [
        {
            "date": "2023-06-01",
            "provider": "General Hospital",
            "doctor": "Dr. Jones",
            "notes": "Follow-up recommended.",
        },
        {
            "date": "2023-07-10",
            "provider": "City Clinic",
            "doctor": "Dr. Smith",
            "notes": "All good.",
        },
    ]

    assert extract_visit_summaries(html) == expected
