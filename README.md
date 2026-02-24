# TubeFit — YouTube Comment Intelligence

> **Skip the scroll. Know if a YouTube video suits _you_ — before you watch it.**

[![Live App](https://img.shields.io/badge/Live%20App-tubefit.streamlit.app-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://tubefit.streamlit.app/)

TubeFit reads a video's comment section with Gemini AI and delivers a personalised suitability verdict based on your viewer persona (beginner, debugger, speed learner, etc.).

---

## Features

| Feature                    | Description                                         |
| -------------------------- | --------------------------------------------------- |
| **AI Suitability Verdict** | FIT / CAUTION / NO FIT with confidence score        |
| **Viewer Personas**        | 5 presets + free-form custom persona                |
| **Sentiment Breakdown**    | Positive / Neutral / Negative % across all comments |
| **Top Liked Comments**     | The community's most-upvoted reactions at a glance  |
| **Keywords**               | Recurring themes extracted by Gemini                |
| **Community Tips**         | Practical advice pulled from the comment section    |
| **Compatibility Notes**    | Version / platform concerns flagged automatically   |
| **Export**                 | Download a full Markdown report or copy raw JSON    |

---

## Tech Stack

- **Frontend** — [Streamlit](https://streamlit.io) (wide layout, animated CSS)
- **Comment data** — [YouTube Data API v3](https://developers.google.com/youtube/v3)
- **AI analysis** — [Google Gemini 2.5 Flash](https://ai.google.dev)
- **Caching** — In-memory two-layer TTL cache (`src/cache.py`)

---

## Caching Architecture

TubeFit uses a two-layer in-memory cache to minimise API quota consumption.
Both YouTube and Gemini calls are skipped whenever a warm cache entry exists.

```
┌───────────────────────────────────────────────────────────────┐
│  Layer 1 — Comment + Metadata Cache  (TTL = 3 h)       │
│  Key   : video_id                                      │
│  Saves : 1 YouTube Data API call per video             │
├───────────────────────────────────────────────────────────────┤
│  Layer 2 — Analysis Cache             (TTL = 6 h)       │
│  Key   : video_id + SHA-256(persona_text)              │
│  Saves : 1 Gemini API call per (video, persona) pair   │
└───────────────────────────────────────────────────────────────┘
```

| Scenario | YouTube API calls | Gemini API calls |
|---|---|---|
| First request for a video | 1 | 1 |
| Same video, same persona (within TTL) | 0 | 0 |
| Same video, different persona (within TTL) | 0 | 1 |

Cache hit/miss status is visible live in the sidebar and in the Export tab.

---

## Project Structure

```
YTCommentsAnalyser/
├── app.py                      # Streamlit entry point
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml             # Dark theme + server settings
│   ├── secrets.toml            # ← gitignored, your real keys go here
│   └── secrets.toml.example    # Safe template committed to repo
└── src/
    ├── __init__.py
    ├── cache.py                # Two-layer TTL cache (Layer 1: comments, Layer 2: AI analysis)
    ├── config.py               # API key loading (st.secrets → env fallback)
    ├── styles.py               # All CSS injected via st.markdown
    ├── utils.py                # extract_video_id, format_number, report generator
    ├── youtube_api.py          # get_video_metadata, get_youtube_comments
    └── gemini_ai.py            # analyze_comments_with_gemini
```

---

## Local Development

### 1. Clone

```bash
git clone https://github.com/hariPrasathK-Dev/TubeFit.git
cd TubeFit
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Add API keys

Copy the example secrets file and fill in your keys:

```bash
cp .streamlit/secrets.toml.example .streamlit/secrets.toml
```

Edit `.streamlit/secrets.toml`:

```toml
YOUTUBE_API_KEY = "your_youtube_data_api_v3_key"
GEMINI_API_KEY  = "your_google_gemini_api_key"
```

> **Get your keys:**
>
> - [YouTube Data API v3](https://console.cloud.google.com/) — enable the API, create credentials
> - [Gemini API](https://aistudio.google.com/app/apikey)

### 4. Run

```bash
streamlit run app.py
```

---

## Live App

**TubeFit is deployed and live:**

> ### [https://tubefit.streamlit.app/](https://tubefit.streamlit.app/)

No setup needed — just open the link and paste a YouTube URL.

---

## Personas

| Persona           | Best for                                                       |
| ----------------- | -------------------------------------------------------------- |
| The Debugger      | Developers troubleshooting broken or outdated code             |
| The Newbie        | Complete beginners checking if a tutorial is beginner-friendly |
| The Legacy User   | People on older hardware / older software versions             |
| The Speed Learner | Experienced folks who want concise, no-fluff content           |
| The Professional  | Evaluating accuracy and production-readiness                   |
| Custom            | Any situation — describe yourself in free text                 |

---

## License

MIT — do whatever you want, attribution appreciated.
