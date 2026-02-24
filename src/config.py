"""
Centralised config — reads API keys from Streamlit secrets (Cloud / local
.streamlit/secrets.toml) with a fallback to environment variables.
"""
import os
import streamlit as st


def _get_secret(key: str) -> str:
    try:
        return st.secrets[key]
    except (KeyError, FileNotFoundError):
        val = os.getenv(key, "")
        return val


YOUTUBE_API_KEY: str = _get_secret("YOUTUBE_API_KEY")
GEMINI_API_KEY: str = _get_secret("GEMINI_API_KEY")
