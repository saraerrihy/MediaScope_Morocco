SELECTOR_CANDIDATES = {
    "article": [
        "article",
        "main",
        "div[itemprop='articleBody']",
        "div.article-body",
        "section.article-body",
        "div.story-body",
    ],
    "title": ["h1"],
    "author": [
        "meta[name='author']",
        "span.byline__name",
        "div.author-name",
        "a[rel='author']",
    ],
    "date": [
        "time",
        "meta[property='article:published_time']",
        "meta[name='pubdate']",
    ],
}
