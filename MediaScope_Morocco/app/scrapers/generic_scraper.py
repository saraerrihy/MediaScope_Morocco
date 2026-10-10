import json
import re
from datetime import datetime
from typing import Dict, List

import feedparser
import requests
import yaml
from bs4 import BeautifulSoup
from dateutil import parser as date_parser

from app.scrapers.config import SELECTOR_CANDIDATES

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"
}


def load_sources(config_path: str = "config/sources.yaml") -> List[Dict]:
    with open(config_path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("sources", [])


def detect_language_simple(text: str) -> str:
    if not text:
        return "unknown"
    arabic_chars = sum(1 for ch in text if "\u0600" <= ch <= "\u06FF")
    latin_chars = sum(1 for ch in text if ch.isalpha() and ch.isascii())
    if arabic_chars > latin_chars:
        return "ar"
    if any(word in text.lower() for word in ["the", "and", "with", "from", "news"]):
        return "en"
    return "fr"


def clean_text(text: str) -> str:
    text = re.sub(r"\s+", " ", text or "").strip()
    return text


def first_content(soup: BeautifulSoup, selectors: List[str]):
    for selector in selectors:
        el = soup.select_one(selector)
        if el:
            return el
    return None


def parse_date(raw_date: str) -> str:
    if not raw_date:
        return ""
    try:
        return date_parser.parse(raw_date).isoformat()
    except Exception:
        return ""


def scrape_article(url: str, source_name: str, default_category: str = "general") -> Dict:
    try:
        response = requests.get(url, headers=HEADERS, timeout=20)
        response.raise_for_status()
    except Exception:
        return {}

    soup = BeautifulSoup(response.text, "html.parser")

    title_el = first_content(soup, SELECTOR_CANDIDATES["title"])
    article_el = first_content(soup, SELECTOR_CANDIDATES["article"])
    author_el = first_content(soup, SELECTOR_CANDIDATES["author"])
    date_el = first_content(soup, SELECTOR_CANDIDATES["date"])

    title = clean_text(title_el.get_text(" ", strip=True) if title_el else "")

    paragraphs = []
    if article_el:
        paragraphs = [p.get_text(" ", strip=True) for p in article_el.find_all(["p", "h2", "li"])]
    content = clean_text(" ".join(paragraphs))

    author = ""
    if author_el:
        author = author_el.get("content", "") or author_el.get_text(" ", strip=True)
    author = clean_text(author)

    raw_date = ""
    if date_el:
        raw_date = date_el.get("datetime", "") or date_el.get("content", "") or date_el.get_text(" ", strip=True)
    publication_date = parse_date(raw_date)

    record = {
        "title": title,
        "author": author,
        "publication_date": publication_date,
        "category": default_category,
        "content": content,
        "source": source_name,
        "url": url,
        "scraping_date": datetime.utcnow().isoformat(),
        "language": detect_language_simple(f"{title} {content}"),
    }
    return record


def scrape_from_rss(limit_per_source: int = 10) -> List[Dict]:
    all_records = []
    for source in load_sources():
        feed = feedparser.parse(source["rss"])
        for entry in feed.entries[:limit_per_source]:
            url = entry.get("link", "")
            if not url:
                continue
            record = scrape_article(url, source["name"], source.get("category", "general"))
            if not record:
                continue
            if not record["title"] and entry.get("title"):
                record["title"] = clean_text(entry.get("title"))
            if not record["publication_date"]:
                record["publication_date"] = parse_date(entry.get("published", ""))
            all_records.append(record)
    return all_records


if __name__ == "__main__":
    data = scrape_from_rss(limit_per_source=3)
    print(json.dumps(data[:2], ensure_ascii=False, indent=2))
