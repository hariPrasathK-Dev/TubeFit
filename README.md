# TubeFit — YouTube Comment Intelligence

> **Skip the scroll. Know if a YouTube video suits _you_ — before you watch it.**

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

---

## Project Structure

```
YTCommentsAnalyser/
├── app.py                      # Streamlit entry point (~200 lines)
├── requirements.txt
├── .gitignore
├── .streamlit/
│   ├── config.toml             # Dark theme + server settings
│   ├── secrets.toml            # ← gitignored, your real keys go here
│   └── secrets.toml.example    # Safe template committed to repo
└── src/
    ├── __init__.py
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
git clone https://github.com/<your-username>/YTCommentsAnalyser.git
cd YTCommentsAnalyser
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

## Deploy to Streamlit Cloud

1. Push this repository to GitHub (make sure `.streamlit/secrets.toml` is in `.gitignore` ✅)
2. Go to [share.streamlit.io](https://share.streamlit.io) → **New app**
3. Select your repo, branch `main`, entry point `app.py`
4. Open **Advanced settings → Secrets** and paste:

```toml
YOUTUBE_API_KEY = "your_youtube_data_api_v3_key"
GEMINI_API_KEY  = "your_google_gemini_api_key"
```

5. Click **Deploy** — that's it.

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
