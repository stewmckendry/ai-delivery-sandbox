from urllib.parse import urlparse

from app.crawler import crawl_portal, score_link


def test_score_link_prioritization():
    link_good = {"url": "https://portal.test/labs", "text": "Lab Results"}
    link_bad = {"url": "https://portal.test/news", "text": "News"}
    assert score_link(link_good) > score_link(link_bad)


def test_crawl_portal():
    start_html = """
    <html><body>
        <a href='/news'>News</a>
        <a href='/labs'>Lab Results</a>
    </body></html>
    """
    labs_html = """
    <html><body>
        <a href='/reports/report1.pdf'>Download Report</a>
        <a href='/profile'>Profile</a>
    </body></html>
    """
    news_html = "<html><body>Latest</body></html>"
    pages = {
        "https://portal.test/labs": labs_html,
        "https://portal.test/news": news_html,
        "https://portal.test/reports/report1.pdf": ""
    }

    def fetch(url: str) -> str:
        return pages.get(url, "")

    results, visited = crawl_portal(start_html, "https://portal.test", fetch, limit=3)

    visited_paths = [urlparse(r["url"]).path for r in results]
    assert visited_paths[0] == "/labs"  # high priority first
    assert set(visited) == {
        "https://portal.test/labs",
        "https://portal.test/reports/report1.pdf",
        "https://portal.test/news",
    }
    assert len(results) == 3
