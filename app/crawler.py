"""Simple portal crawler with heuristic link scoring."""

from __future__ import annotations

from collections import deque
from typing import Callable, Dict, List, Tuple
from urllib.parse import urljoin, urlparse

from bs4 import BeautifulSoup


Link = Dict[str, str]


def extract_internal_links(html: str, base_url: str) -> List[Link]:
    """Return internal links with anchor text from ``html``.

    Parameters
    ----------
    html:
        Page HTML markup.
    base_url:
        Absolute base URL used to resolve relative links.
    """
    soup = BeautifulSoup(html, "html.parser")
    base_netloc = urlparse(base_url).netloc
    links: List[Link] = []
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"])
        if urlparse(href).netloc != base_netloc:
            continue
        links.append({"url": href, "text": a.get_text(" ", strip=True)})
    return links


def score_link(link: Link) -> float:
    """Score link usefulness using anchor text and URL patterns."""
    text = link.get("text", "").lower()
    path = urlparse(link.get("url", "")).path.lower()
    score = 0.0
    if "lab" in text or "lab" in path:
        score += 3
    if "download" in text:
        score += 2
    if "result" in text:
        score += 1.5
    if path.endswith(".pdf"):
        score += 2.5
    return score


def crawl_portal(
    start_html: str,
    base_url: str,
    fetch_html: Callable[[str], str],
    limit: int = 10,
) -> Tuple[List[Dict[str, str]], set[str]]:
    """Traverse links starting from ``start_html`` using ``fetch_html``.

    ``fetch_html`` should accept a URL and return HTML content. The crawl
    is limited by ``limit`` total pages visited.
    """
    initial_links = sorted(
        extract_internal_links(start_html, base_url),
        key=score_link,
        reverse=True,
    )
    queue = deque(link["url"] for link in initial_links)
    visited: set[str] = set()
    pages: List[Dict[str, str]] = []

    while queue and len(visited) < limit:
        url = queue.popleft()
        if url in visited:
            continue
        visited.add(url)
        html = fetch_html(url)
        pages.append({"url": url, "html": html})
        if len(visited) >= limit:
            break
        new_links = sorted(
            extract_internal_links(html, base_url),
            key=score_link,
            reverse=True,
        )
        for link in new_links:
            href = link["url"]
            if (
                href not in visited
                and href not in queue
                and len(visited) + len(queue) < limit
            ):
                queue.append(href)
    return pages, visited
