"""
All custom CSS for TubeFit.
Import and inject via:  st.markdown(STYLES, unsafe_allow_html=True)
"""

STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

    /* ── Keyframe Animations ── */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(18px); }
        to   { opacity: 1; transform: translateY(0); }
    }
    @keyframes fadeIn {
        from { opacity: 0; }
        to   { opacity: 1; }
    }
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-14px); }
        to   { opacity: 1; transform: translateX(0); }
    }
    @keyframes pulseDot {
        0%, 100% { opacity: 1; transform: scale(1); }
        50%       { opacity: 0.5; transform: scale(0.75); }
    }
    @keyframes barGrow {
        from { width: 0%; }
        to   { width: var(--bar-w); }
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Base ── */
    .stApp {
        background: #0d0d0d;
        color: #f0f0f0;
    }

    /* ── Sidebar ──
       Slightly lighter than main bg so it reads as a distinct panel,
       text colors bumped to ensure readability.
    */
    [data-testid="stSidebar"] {
        background: #141414 !important;
        border-right: 1px solid #222 !important;
    }
    [data-testid="stSidebar"] .stMarkdown p,
    [data-testid="stSidebar"] .stMarkdown div {
        color: #999 !important;
    }
    [data-testid="stSidebar"] .stMarkdown h3 {
        color: #bbb !important;
        font-size: 0.72rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.1em !important;
        font-weight: 600 !important;
    }
    [data-testid="stSidebar"] label {
        color: #aaa !important;
        font-size: 0.85rem !important;
    }
    /* Slider / toggle labels */
    [data-testid="stSidebar"] [data-testid="stWidgetLabel"] p {
        color: #bbb !important;
    }

    /* ── Hero ── */
    .hero-container {
        text-align: center;
        padding: 3rem 1rem 2.2rem 1rem;
        border-bottom: 1px solid #1e1e1e;
        margin-bottom: 2.5rem;
        animation: fadeIn 0.6s ease both;
    }
    .hero-badge {
        display: inline-block;
        background: transparent;
        border: 1px solid #2a2a2a;
        color: #777;
        padding: 0.25rem 0.8rem;
        border-radius: 4px;
        font-size: 0.7rem;
        font-weight: 500;
        letter-spacing: 0.1em;
        text-transform: uppercase;
        margin-bottom: 1.2rem;
    }
    .hero-wordmark {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 0.6rem;
    }
    .hero-dot {
        width: 9px;
        height: 9px;
        background: #fff;
        border-radius: 50%;
        display: inline-block;
        animation: pulseDot 2.4s ease-in-out infinite;
    }
    .hero-title {
        font-size: clamp(2.2rem, 5vw, 3.4rem);
        font-weight: 800;
        color: #ffffff;
        margin: 0;
        letter-spacing: -1.5px;
        line-height: 1.1;
    }
    .hero-title span { color: #555; }
    .hero-subtitle {
        font-size: 1rem;
        color: #888;
        margin-top: 0.75rem;
        font-weight: 400;
        max-width: 480px;
        margin-left: auto;
        margin-right: auto;
        line-height: 1.6;
    }

    /* ── Input panel ── */
    .input-section {
        background: #121212;
        border: 1px solid #222;
        border-radius: 12px;
        padding: 1.8rem 2rem;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.45s ease both;
    }

    /* ── Section header labels ── */
    .section-header {
        font-size: 0.7rem;
        font-weight: 600;
        color: #666;
        border-bottom: 1px solid #1e1e1e;
        padding-bottom: 0.45rem;
        margin-bottom: 0.9rem;
        letter-spacing: 0.1em;
        text-transform: uppercase;
    }

    /* ── Generic glass card ── */
    .glass-card {
        background: #131313;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 1.4rem;
        margin-bottom: 1rem;
        transition: border-color 0.2s ease;
        animation: fadeInUp 0.4s ease both;
    }
    .glass-card:hover { border-color: #2e2e2e; }

    /* ── Persona description box ── */
    .persona-desc {
        background: #111;
        border: 1px solid #222;
        border-radius: 8px;
        padding: 0.9rem 1.1rem;
        margin-top: 0.5rem;
    }

    /* ── Verdict cards ── */
    .verdict-fit {
        background: #0d1a12;
        border: 1px solid #1a3d26;
        border-left: 4px solid #22c55e;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        animation: fadeInUp 0.5s ease both;
    }
    .verdict-nofit {
        background: #1a0d0d;
        border: 1px solid #3d1a1a;
        border-left: 4px solid #ef4444;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        animation: fadeInUp 0.5s ease both;
    }
    .verdict-caution {
        background: #1a1600;
        border: 1px solid #3d3000;
        border-left: 4px solid #eab308;
        border-radius: 10px;
        padding: 2rem;
        text-align: center;
        animation: fadeInUp 0.5s ease both;
    }
    .verdict-emoji { font-size: 2.4rem; }
    .verdict-title {
        font-size: 1.8rem;
        font-weight: 800;
        margin: 0.5rem 0 0 0;
        letter-spacing: -0.5px;
    }

    /* ── Stat metric cards ── */
    .metric-card {
        background: #131313;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 1.2rem 1rem;
        text-align: center;
        transition: border-color 0.2s ease, transform 0.2s ease;
        animation: fadeInUp 0.4s ease both;
    }
    .metric-card:hover {
        border-color: #333;
        transform: translateY(-2px);
    }
    .metric-value {
        font-size: 1.9rem;
        font-weight: 700;
        color: #fff;
    }
    .metric-label {
        font-size: 0.7rem;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-top: 0.3rem;
    }

    /* ── Video info card ── */
    .video-info-card {
        background: #131313;
        border: 1px solid #222;
        border-radius: 10px;
        padding: 1.2rem 1.4rem;
        display: flex;
        gap: 1.1rem;
        align-items: flex-start;
        margin-bottom: 1.5rem;
        animation: fadeInUp 0.4s ease both;
    }

    /* ── Comment card ── */
    .comment-card {
        background: #111;
        border: 1px solid #1e1e1e;
        border-left: 3px solid #2a2a2a;
        border-radius: 0 8px 8px 0;
        padding: 0.95rem 1.2rem;
        margin-bottom: 0.65rem;
        transition: border-left-color 0.2s ease, background 0.2s ease;
        animation: slideInLeft 0.35s ease both;
    }
    .comment-card:hover {
        border-left-color: #fff;
        background: #161616;
    }
    .comment-author {
        font-weight: 600;
        font-size: 0.83rem;
        color: #ddd;
    }
    .comment-likes {
        font-size: 0.75rem;
        color: #666;
        display: inline-block;
        margin-left: 0.5rem;
    }
    .comment-text {
        font-size: 0.88rem;
        color: #999;
        margin-top: 0.4rem;
        line-height: 1.55;
    }

    /* ── Pro / Red-flag items ── */
    .pro-item {
        background: #0d1610;
        border: 1px solid #153318;
        border-left: 3px solid #22c55e;
        border-radius: 0 7px 7px 0;
        padding: 0.6rem 1rem;
        margin-bottom: 0.4rem;
        font-size: 0.87rem;
        color: #4ade80;
        animation: slideInLeft 0.3s ease both;
    }
    .red-flag-item {
        background: #160d0d;
        border: 1px solid #2a1515;
        border-left: 3px solid #ef4444;
        border-radius: 0 7px 7px 0;
        padding: 0.6rem 1rem;
        margin-bottom: 0.4rem;
        font-size: 0.87rem;
        color: #f87171;
        animation: slideInLeft 0.3s ease both;
    }

    /* ── Keyword chips ── */
    .keyword-chip {
        display: inline-block;
        background: #161616;
        border: 1px solid #2a2a2a;
        color: #888;
        padding: 0.22rem 0.65rem;
        border-radius: 4px;
        font-size: 0.76rem;
        margin: 0.18rem;
        font-weight: 500;
        transition: border-color 0.15s ease, color 0.15s ease;
    }
    .keyword-chip:hover { border-color: #555; color: #ccc; }

    /* ── Streamlit native overrides ── */

    /* Button */
    .stButton > button {
        background: #fff !important;
        color: #000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.65rem 2rem !important;
        font-weight: 600 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        transition: background 0.2s ease, transform 0.15s ease, box-shadow 0.2s ease !important;
        width: 100% !important;
    }
    .stButton > button:hover {
        background: #e8e8e8 !important;
        transform: translateY(-1px) !important;
        box-shadow: 0 6px 20px rgba(255,255,255,0.09) !important;
    }
    .stButton > button:active { transform: translateY(0px) !important; }

    /* Inputs */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea {
        background: #0f0f0f !important;
        border: 1px solid #262626 !important;
        border-radius: 8px !important;
        color: #f0f0f0 !important;
        font-size: 0.93rem !important;
        transition: border-color 0.2s ease !important;
    }
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #555 !important;
        box-shadow: 0 0 0 3px rgba(255,255,255,0.04) !important;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        background: #0f0f0f !important;
        border: 1px solid #262626 !important;
        border-radius: 8px !important;
        color: #f0f0f0 !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        background: #111 !important;
        border: 1px solid #222 !important;
        border-radius: 8px !important;
        gap: 2px !important;
        padding: 3px !important;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 6px !important;
        color: #666 !important;
        font-weight: 500 !important;
        font-size: 0.85rem !important;
    }
    .stTabs [aria-selected="true"] {
        background: #1e1e1e !important;
        color: #e5e5e5 !important;
    }

    /* Slider */
    .stSlider > div > div > div > div { background: #fff !important; }

    /* Progress */
    .stProgress > div > div > div > div { background: #fff !important; }

    /* Spinner */
    .stSpinner > div { border-top-color: #fff !important; }

    /* HR */
    hr { border-color: #1e1e1e !important; }

    /* Scrollbar */
    ::-webkit-scrollbar        { width: 5px; }
    ::-webkit-scrollbar-track  { background: transparent; }
    ::-webkit-scrollbar-thumb  { background: #333; border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: #555; }

    /* ── Responsive ── */
    @media (max-width: 768px) {
        .hero-title        { font-size: 2rem; }
        .video-info-card   { flex-direction: column; }
        .video-info-card img { width: 100% !important; max-width: 280px; }
        .input-section     { padding: 1.2rem 1rem; }
        .metric-value      { font-size: 1.5rem; }
    }
</style>
"""
