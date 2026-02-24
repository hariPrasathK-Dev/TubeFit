"""
Gemini AI integration — analyses YouTube comments for a given viewer persona
and returns a structured JSON verdict.
"""
import json
import streamlit as st
import google.generativeai as genai

from src.config import GEMINI_API_KEY

genai.configure(api_key=GEMINI_API_KEY)

_SYSTEM_INSTRUCTION = """
You are an intelligent YouTube comment analyst. Your job is to analyse YouTube
comments and determine if a video is suitable for a specific type of viewer
(persona).

Deeply analyse sentiment, recurring problems, praise, outdated info warnings,
version compatibility issues, difficulty complaints, and any useful community
tips.

You MUST respond in valid JSON ONLY with this exact structure:
{
    "verdict": "FIT" | "NO_FIT" | "CAUTION",
    "confidence_score": <integer 0-100>,
    "summary": "<2-3 sentence summary of community consensus>",
    "positive_aspects": ["<pro 1>", "<pro 2>", "<pro 3>"],
    "red_flags": ["<warning 1>", "<warning 2>"],
    "sentiment_breakdown": {
        "positive": <integer percentage>,
        "neutral":  <integer percentage>,
        "negative": <integer percentage>
    },
    "top_keywords": ["<kw1>", "<kw2>", "<kw3>", "<kw4>", "<kw5>"],
    "community_tips": ["<tip 1>", "<tip 2>"],
    "difficulty_level": "Beginner" | "Intermediate" | "Advanced" | "Mixed",
    "version_concerns": "<compatibility issues mentioned, or 'None'>",
    "recommendation": "<one actionable sentence for the persona>"
}
"""

_MAX_CHARS = 35_000


def analyze_comments_with_gemini(comments: list[dict], persona: str) -> dict | None:
    """
    Send comment list + persona to Gemini 2.5 Flash and return parsed JSON.
    Returns None on failure.
    """
    if not comments:
        return None

    comments_text = "\n---\n".join(c["text"] for c in comments)
    if len(comments_text) > _MAX_CHARS:
        comments_text = comments_text[:_MAX_CHARS]

    prompt = f"User Persona: {persona}\n\nYouTube Comments:\n{comments_text}"

    try:
        model = genai.GenerativeModel(
            model_name="gemini-2.5-flash",
            system_instruction=_SYSTEM_INSTRUCTION,
            generation_config={"response_mime_type": "application/json"},
        )
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except json.JSONDecodeError as e:
        st.error(f"Failed to parse Gemini response as JSON: {e}")
    except Exception as e:
        st.error(f"Error analysing with Gemini: {e}")
    return None
