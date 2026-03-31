import httpx
import json
from datetime import datetime, timedelta
from typing import Optional

IACR_FEED = "https://eprint.iacr.org/rss/rss.xml"
ARXIV_URL = "https://export.arxiv.org/api/query"

PQC_KEYWORDS = [
    "post-quantum",
    "lattice-based",
    "Dilithium",
    "Falcon",
    "SPHINCS",
    "Kyber",
    "elliptic curve",
    "Shor's algorithm",
    "qubit threshold",
    "quantum resistance",
]

async def fetch_iacr_papers(days_back: int = 1) -> list[dict]:
    """
    Fetch recent IACR ePrint papers and filter by PQC keywords.
    Returns a list of relevant papers from the last N days.
    """
    since = datetime.utcnow() - timedelta(days=days_back)
    results = []

    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(IACR_FEED)
        resp.raise_for_status()
        # naive XML parse — replace with feedparser if available
        entries = resp.text.split("<item>")[1:]
        for entry in entries:
            title = _extract_tag(entry, "title")
            link = _extract_tag(entry, "link")
            summary = _extract_tag(entry, "description")
            if any(kw.lower() in (title + summary).lower() for kw in PQC_KEYWORDS):
                results.append({
                    "title": title,
                    "link": link,
                    "summary": summary[:300],
                    "fetched_at": datetime.utcnow().isoformat(),
                })

    return results


async def fetch_arxiv_papers(max_results: int = 10) -> list[dict]:
    """
    Query arxiv for recent post-quantum cryptography papers.
    """
    params = {
        "search_query": "cat:cs.CR+AND+ti:post-quantum",
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    }
    async with httpx.AsyncClient(timeout=15) as client:
        resp = await client.get(ARXIV_URL, params=params)
        resp.raise_for_status()
    return {"raw": resp.text[:2000]}


def _extract_tag(text: str, tag: str) -> str:
    try:
        return text.split(f"<{tag}>")[1].split(f"</{tag}>")[0].strip()
    except IndexError:
        return ""


def build_digest(papers: list[dict]) -> str:
    """
    Format a list of papers into a readable daily digest string
    for delivery via Telegram or Discord.
    """
    if not papers:
        return "No new PQC papers in the last 24 hours."

    lines = [f"PQC Research Digest -- {datetime.utcnow().strftime('%Y-%m-%d')}\n"]
    for i, p in enumerate(papers, 1):
        lines.append(f"{i}. {p['title']}")
        lines.append(f"   {p['link']}")
        lines.append(f"   {p['summary']}\n")

    return "\n".join(lines)
