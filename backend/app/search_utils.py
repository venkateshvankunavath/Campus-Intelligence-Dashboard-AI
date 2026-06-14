"""Shared keyword extraction so searches work on full natural-language questions.

In Gemini mode the model extracts the search term; in offline/fallback mode the
raw sentence is passed through. This tokenizer makes both robust: it strips
question/stop words and matches on the meaningful keywords (any-token OR match).
"""
import re

STOPWORDS = {
    "is", "the", "a", "an", "of", "for", "to", "in", "on", "at", "and", "or",
    "what", "when", "where", "which", "who", "whom", "how", "why", "do", "does",
    "did", "are", "was", "were", "be", "been", "available", "there", "here",
    "i", "my", "me", "we", "our", "you", "your", "it", "its", "this", "that",
    "get", "got", "find", "show", "tell", "about", "please", "can", "could",
    "would", "should", "any", "some", "have", "has", "with", "today", "todays",
}


def keywords(text: str | None) -> list[str]:
    """Return meaningful keyword tokens from a query/sentence."""
    if not text:
        return []
    toks = re.findall(r"[a-zA-Z0-9]+", text.lower())
    kw = [t for t in toks if len(t) >= 3 and t not in STOPWORDS]
    return kw or toks  # if everything got filtered, fall back to raw tokens
