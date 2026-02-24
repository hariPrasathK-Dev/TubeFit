"""
Utility helpers: URL parsing, number formatting, report generation.
"""
import re
from datetime import datetime


def extract_video_id(url: str) -> str | None:
    """Extract the 11-character YouTube video ID from any valid URL format."""
    pattern = (
        r'(?:https?:\/\/)?(?:www\.)?'
        r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)'
        r'|youtu\.be\/)([a-zA-Z0-9_-]{11})'
    )
    match = re.search(pattern, url)
    return match.group(1) if match else None


def format_number(n: int) -> str:
    """Format integer into human-readable K / M notation."""
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{n / 1_000:.1f}K"
    return str(n)


def generate_report_markdown(
    video_meta: dict | None,
    result: dict,
    persona: str,
    num_comments: int,
) -> str:
    """Produce a clean Markdown report suitable for download."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    s = result.get("sentiment_breakdown", {})

    video_block = (
        f"- **Title:** {video_meta.get('title', 'N/A')}\n"
        f"- **Channel:** {video_meta.get('channel', 'N/A')}\n"
        f"- **Published:** {video_meta.get('published_at', 'N/A')}"
        if video_meta
        else "- N/A"
    )

    return f"""# TubeFit Analysis Report

> Generated: {now}  
> Persona: {persona}  
> Comments Analysed: {num_comments}

---

## Video

{video_block}

---

## Verdict: {result.get('verdict', 'N/A')}

| Field | Value |
|---|---|
| Confidence | {result.get('confidence_score', 'N/A')}% |
| Difficulty | {result.get('difficulty_level', 'N/A')} |

### Summary
{result.get('summary', 'N/A')}

### Recommendation
{result.get('recommendation', 'N/A')}

---

## What's Good
{chr(10).join(f"- {p}" for p in result.get('positive_aspects', []))}

## Red Flags
{chr(10).join(f"- {r}" for r in result.get('red_flags', []))}

## Community Tips
{chr(10).join(f"- {t}" for t in result.get('community_tips', []))}

## Sentiment
- Positive: {s.get('positive', 'N/A')}%
- Neutral: {s.get('neutral', 'N/A')}%
- Negative: {s.get('negative', 'N/A')}%

## Compatibility / Version Concerns
{result.get('version_concerns', 'None')}
"""
