"""
Two-layer in-memory TTL cache for TubeFit.

Layer 1 — Comment Cache
  key  : video_id
  value: list of comment dicts
  TTL  : COMMENT_TTL (default 3 h)
  saves: 1 YouTube Data API call per video

Layer 2 — Analysis Cache
  key  : video_id + SHA-256(persona_text)
  value: full Gemini JSON result dict
  TTL  : ANALYSIS_TTL (default 6 h)
  saves: 1 Gemini API call per (video, persona) pair

Metadata (video title, stats, thumbnail) shares the comment TTL.

The store is a plain module-level dict.  Because Python modules are
imported once per server process, the dict survives across Streamlit
reruns for every user in the same session.
"""
import time
import hashlib
from typing import Any

# ─────────────────────────────────────────────────────────
# TTL constants (seconds)
# ─────────────────────────────────────────────────────────
COMMENT_TTL  = 3 * 60 * 60   # 3 hours
ANALYSIS_TTL = 6 * 60 * 60   # 6 hours
METADATA_TTL = 3 * 60 * 60   # 3 hours — same cadence as comments

# ─────────────────────────────────────────────────────────
# Internal store
# { sha256_key: {"data": <any>, "expires_at": float} }
# ─────────────────────────────────────────────────────────
_store: dict[str, dict] = {}


# ─────────────────────────────────────────────────────────
# Private helpers
# ─────────────────────────────────────────────────────────
def _make_key(*parts: str) -> str:
    """Deterministic SHA-256 key from one or more string parts."""
    raw = "\x00".join(parts)          # null byte separator — avoids collisions
    return hashlib.sha256(raw.encode()).hexdigest()


def _set(key: str, value: Any, ttl: int) -> None:
    _store[key] = {
        "data": value,
        "expires_at": time.monotonic() + ttl,
    }


def _get(key: str) -> Any | None:
    entry = _store.get(key)
    if entry is None:
        return None
    if time.monotonic() > entry["expires_at"]:
        del _store[key]               # lazy eviction on read
        return None
    return entry["data"]


def _evict_expired() -> int:
    """Remove all expired entries; return how many were removed."""
    now     = time.monotonic()
    expired = [k for k, v in _store.items() if now > v["expires_at"]]
    for k in expired:
        del _store[k]
    return len(expired)


# ─────────────────────────────────────────────────────────
# Public API — Layer 1: Comments
# ─────────────────────────────────────────────────────────
def get_cached_comments(video_id: str) -> list | None:
    return _get(_make_key("comments", video_id))


def set_cached_comments(video_id: str, comments: list) -> None:
    _set(_make_key("comments", video_id), comments, COMMENT_TTL)


# ─────────────────────────────────────────────────────────
# Public API — Layer 1: Metadata
# ─────────────────────────────────────────────────────────
def get_cached_metadata(video_id: str) -> dict | None:
    return _get(_make_key("metadata", video_id))


def set_cached_metadata(video_id: str, metadata: dict) -> None:
    _set(_make_key("metadata", video_id), metadata, METADATA_TTL)


# ─────────────────────────────────────────────────────────
# Public API — Layer 2: AI Analysis (per video + persona)
# ─────────────────────────────────────────────────────────
def get_cached_analysis(video_id: str, persona: str) -> dict | None:
    return _get(_make_key("analysis", video_id, persona))


def set_cached_analysis(video_id: str, persona: str, result: dict) -> None:
    _set(_make_key("analysis", video_id, persona), result, ANALYSIS_TTL)


# ─────────────────────────────────────────────────────────
# Stats (shown in sidebar)
# ─────────────────────────────────────────────────────────
def cache_stats() -> dict:
    """Return live statistics without mutating the store."""
    _evict_expired()                  # clean up before reporting
    now     = time.monotonic()
    comment_hits  = sum(1 for k in _store if _make_key("comments",  "")[:8] == k[:8])
    metadata_hits = sum(1 for k in _store if _make_key("metadata",  "")[:8] == k[:8])
    analysis_hits = sum(1 for k in _store if _make_key("analysis",  "")[:8] == k[:8])
    return {
        "total"   : len(_store),
        "comments": comment_hits,
        "metadata": metadata_hits,
        "analysis": analysis_hits,
    }
