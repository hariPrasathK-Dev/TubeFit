"""
YouTube Data API v3 helpers.
Fetches video metadata and top-level comments.
"""
import streamlit as st
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from src.config import YOUTUBE_API_KEY


def _build_client():
    return build("youtube", "v3", developerKey=YOUTUBE_API_KEY)


def get_video_metadata(video_id: str) -> dict | None:
    """Return a dict of video info (title, channel, stats, thumbnail)."""
    try:
        yt = _build_client()
        resp = yt.videos().list(part="snippet,statistics", id=video_id).execute()
        if not resp.get("items"):
            return None
        item = resp["items"][0]
        snip = item["snippet"]
        stats = item.get("statistics", {})
        return {
            "title": snip.get("title", "Unknown Title"),
            "channel": snip.get("channelTitle", "Unknown Channel"),
            "published_at": snip.get("publishedAt", "")[:10],
            "thumbnail": snip.get("thumbnails", {}).get("medium", {}).get("url", ""),
            "view_count": int(stats.get("viewCount", 0)),
            "like_count": int(stats.get("likeCount", 0)),
            "comment_count": int(stats.get("commentCount", 0)),
        }
    except HttpError as e:
        st.warning(f"Could not fetch video metadata: {e}")
    except Exception as e:
        st.warning(f"Unexpected error fetching metadata: {e}")
    return None


def get_youtube_comments(
    video_id: str,
    max_results: int = 100,
    sort_by: str = "relevance",
) -> list[dict]:
    """
    Fetch top-level comments for a video.
    Returns a list of dicts sorted by like count descending.
    """
    try:
        yt = _build_client()
        resp = (
            yt.commentThreads()
            .list(
                part="snippet",
                videoId=video_id,
                maxResults=max_results,
                textFormat="plainText",
                order=sort_by,
            )
            .execute()
        )
        comments = []
        for item in resp.get("items", []):
            s = item["snippet"]["topLevelComment"]["snippet"]
            comments.append(
                {
                    "text": s.get("textDisplay", ""),
                    "author": s.get("authorDisplayName", "Anonymous"),
                    "likes": s.get("likeCount", 0),
                    "published_at": s.get("publishedAt", "")[:10],
                }
            )
        comments.sort(key=lambda x: x["likes"], reverse=True)
        return comments
    except HttpError as e:
        st.error(f"YouTube API error: {e}")
    except Exception as e:
        st.error(f"Error fetching comments: {e}")
    return []
