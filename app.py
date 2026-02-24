"""
TubeFit - YouTube Comment Suitability Analyser
Streamlit entry point.
"""
import time
import streamlit as st
import pandas as pd
from datetime import datetime

from src.styles import STYLES
from src.utils import extract_video_id, format_number, generate_report_markdown
from src.youtube_api import get_video_metadata, get_youtube_comments
from src.gemini_ai import analyze_comments_with_gemini

st.set_page_config(
    page_title="TubeFit – Comment Intelligence",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(STYLES, unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:
    st.markdown("""
    <div style="padding:1.2rem 0 0.8rem 0;">
        <p style="color:#fff;font-size:1.1rem;font-weight:700;margin:0;letter-spacing:-0.3px;">TubeFit</p>
        <p style="color:#666;font-size:0.75rem;margin:0.2rem 0 0 0;">Comment Intelligence</p>
    </div>
    <hr style="margin:0 0 1.2rem 0;border-color:#222;">
    """, unsafe_allow_html=True)

    st.markdown("### Settings")
    max_comments = st.slider(
        "Comments to analyse", min_value=25, max_value=100, value=75, step=25,
        help="More comments = deeper analysis, slightly slower",
    )
    sort_order = st.selectbox(
        "Sort comments by", ["relevance", "time"],
        help="Relevance surfaces the most-interacted comments first",
    )
    st.markdown("<hr style='border-color:#222;margin:1rem 0;'>", unsafe_allow_html=True)

    st.markdown("### Display")
    show_top_comments = st.toggle("Top Liked Comments",  value=True)
    show_sentiment    = st.toggle("Sentiment Breakdown", value=True)
    show_keywords     = st.toggle("Keywords",            value=True)
    show_tips         = st.toggle("Community Tips",      value=True)
    st.markdown("<hr style='border-color:#222;margin:1rem 0;'>", unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#777;font-size:0.75rem;line-height:1.9;">
        1. Paste a YouTube URL<br>
        2. Pick your viewer persona<br>
        3. AI reads the comment section<br>
        4. Get your suitability verdict
    </div>""", unsafe_allow_html=True)

    st.markdown("""
    <div style="color:#444;font-size:0.7rem;margin-top:2rem;padding-top:1rem;border-top:1px solid #222;">
        Gemini 2.5 Flash · YouTube Data API v3
    </div>""", unsafe_allow_html=True)

# HERO
st.markdown("""
<div class="hero-container">
    <div class="hero-badge">AI-Powered · YouTube Comment Analysis</div>
    <div class="hero-wordmark"><span class="hero-dot"></span></div>
    <h1 class="hero-title">TubeFit<span>.</span></h1>
    <p class="hero-subtitle">Skip the scroll. Know if a YouTube video suits you — before you watch it.</p>
</div>
""", unsafe_allow_html=True)

# INPUT
PERSONA_OPTIONS = {
    "The Debugger":      "A developer troubleshooting a specific issue. Wants to know if the code in the video actually works, or if it is broken/outdated.",
    "The Newbie":        "A complete beginner with zero prior experience. Wants to know if the tutorial is too fast, skips steps, or assumes prior knowledge.",
    "The Legacy User":   "Someone on older hardware or an older software version. Wants to know if the tutorial applies to their specific setup.",
    "The Speed Learner": "An experienced person who just wants a quick overview. Wants to know if the video is concise or overly padded.",
    "The Professional":  "A professional evaluating if this content is accurate, credible, and production-ready.",
    "Custom":            "Describe your own situation in detail.",
}

st.markdown('<div class="input-section">', unsafe_allow_html=True)
col_url, col_persona = st.columns([1, 1], gap="large")

with col_url:
    st.markdown('<p class="section-header">Video URL</p>', unsafe_allow_html=True)
    url = st.text_input(
        "url", placeholder="https://www.youtube.com/watch?v=...",
        label_visibility="collapsed",
    )
    st.markdown('<p class="section-header" style="margin-top:1.4rem;">Viewer Persona</p>', unsafe_allow_html=True)
    selected_persona = st.selectbox(
        "Persona", list(PERSONA_OPTIONS.keys()), label_visibility="collapsed",
    )

with col_persona:
    st.markdown('<p class="section-header">Persona Profile</p>', unsafe_allow_html=True)
    if selected_persona == "Custom":
        persona_description = st.text_area(
            "Custom description",
            placeholder="e.g., I'm a data scientist learning PyTorch on Mac M2 with no prior deep learning experience…",
            height=130,
            label_visibility="collapsed",
        )
    else:
        persona_description = PERSONA_OPTIONS[selected_persona]
        st.markdown(
            f'<div class="persona-desc"><p style="color:#999;font-size:0.88rem;margin:0;line-height:1.65;">{persona_description}</p></div>',
            unsafe_allow_html=True,
        )

st.markdown("</div>", unsafe_allow_html=True)

_, btn_col, _ = st.columns([1, 1, 1])
with btn_col:
    analyse_clicked = st.button("Analyse Suitability", type="primary", use_container_width=True)

# ANALYSIS
if analyse_clicked:
    if not url:
        st.warning("⚠️ Please enter a YouTube URL.")
    elif selected_persona == "Custom" and not persona_description.strip():
        st.warning("⚠️ Please describe your custom persona.")
    else:
        video_id = extract_video_id(url)
        if not video_id:
            st.error("❌ Invalid YouTube URL — please check and try again.")
        else:
            st.markdown("---")
            bar = st.progress(0, text="Starting analysis…")
            time.sleep(0.2)

            bar.progress(15, text="Fetching video information…")
            video_meta = get_video_metadata(video_id)

            bar.progress(35, text=f"Collecting {max_comments} comments…")
            comments = get_youtube_comments(video_id, max_results=max_comments, sort_by=sort_order)

            if not comments:
                st.warning("⚠️ No comments found or comments are disabled for this video.")
                bar.empty()
            else:
                bar.progress(62, text=f"Gemini is analysing {len(comments)} comments for your persona…")
                result = analyze_comments_with_gemini(comments, persona_description)
                bar.progress(100, text="Analysis complete!")
                time.sleep(0.4)
                bar.empty()

                if result:
                    # Video metadata card
                    if video_meta:
                        thumb = (
                            f"<img src='{video_meta['thumbnail']}' style='width:130px;border-radius:6px;flex-shrink:0;object-fit:cover;'>"
                            if video_meta.get("thumbnail") else ""
                        )
                        title   = video_meta["title"]
                        channel = video_meta["channel"]
                        pub     = video_meta["published_at"]
                        views   = format_number(video_meta["view_count"])
                        likes_v = format_number(video_meta["like_count"])
                        cmt_cnt = format_number(video_meta["comment_count"])
                        st.markdown(f"""
                        <div class="video-info-card">
                            {thumb}
                            <div style="flex:1;min-width:0;">
                                <p style="color:#f0f0f0;font-weight:700;font-size:0.98rem;margin:0 0 0.25rem 0;
                                          line-height:1.4;white-space:nowrap;overflow:hidden;text-overflow:ellipsis;">
                                    {title}
                                </p>
                                <p style="color:#666;font-size:0.82rem;margin:0 0 0.7rem 0;">
                                    {channel} &nbsp;·&nbsp; {pub}
                                </p>
                                <div style="display:flex;gap:1.2rem;flex-wrap:wrap;">
                                    <span style="color:#666;font-size:0.78rem;">{views} views</span>
                                    <span style="color:#666;font-size:0.78rem;">{likes_v} likes</span>
                                    <span style="color:#666;font-size:0.78rem;">{cmt_cnt} comments</span>
                                </div>
                            </div>
                        </div>""", unsafe_allow_html=True)

                    # Verdict
                    verdict    = result.get("verdict", "CAUTION")
                    confidence = result.get("confidence_score", 0)
                    difficulty = result.get("difficulty_level", "Mixed")

                    if verdict == "FIT":
                        v_class = "verdict-fit"
                        v_emoji, v_text, v_color = "✅", "FIT — Worth Watching", "#22c55e"
                    elif verdict == "NO_FIT":
                        v_class = "verdict-nofit"
                        v_emoji, v_text, v_color = "❌", "NO FIT — Not Recommended", "#ef4444"
                    else:
                        v_class = "verdict-caution"
                        v_emoji, v_text, v_color = "⚠️", "CAUTION — Proceed Carefully", "#eab308"

                    st.markdown(f"""
                    <div class="{v_class}">
                        <div class="verdict-emoji">{v_emoji}</div>
                        <div class="verdict-title" style="color:{v_color};">{v_text}</div>
                        <p style="color:#777;font-size:0.85rem;margin:0.6rem 0 0 0;font-weight:400;">
                            Confidence &nbsp;<strong style="color:{v_color};font-size:1rem;">{confidence}%</strong>
                            &nbsp;&nbsp;·&nbsp;&nbsp;
                            Level &nbsp;<strong style="color:#bbb;">{difficulty}</strong>
                        </p>
                    </div>""", unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Stats row
                    s_data = result.get("sentiment_breakdown", {})
                    pos_c  = s_data.get("positive", 0)
                    neg_c  = s_data.get("negative", 0)
                    mc1, mc2, mc3, mc4 = st.columns(4)
                    with mc1:
                        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(comments)}</div><div class="metric-label">Comments Read</div></div>', unsafe_allow_html=True)
                    with mc2:
                        pc = "#22c55e" if pos_c >= 50 else "#fff"
                        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{pc};">{pos_c}%</div><div class="metric-label">Positive</div></div>', unsafe_allow_html=True)
                    with mc3:
                        nc = "#ef4444" if neg_c >= 30 else "#fff"
                        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{nc};">{neg_c}%</div><div class="metric-label">Negative</div></div>', unsafe_allow_html=True)
                    with mc4:
                        cc = "#22c55e" if confidence >= 70 else ("#eab308" if confidence >= 45 else "#ef4444")
                        st.markdown(f'<div class="metric-card"><div class="metric-value" style="color:{cc};">{confidence}%</div><div class="metric-label">Confidence</div></div>', unsafe_allow_html=True)

                    st.markdown("<br>", unsafe_allow_html=True)

                    # Tabs
                    tab1, tab2, tab3, tab4, tab5 = st.tabs([
                        "📋 Analysis", "💬 Top Comments",
                        "📈 Sentiment", "💡 Tips & Keywords", "📥 Export"
                    ])

                    # Tab 1 - Analysis
                    with tab1:
                        rec = result.get("recommendation", "")
                        if rec:
                            st.markdown(f"""
                            <div style="background:#111;border:1px solid #222;border-left:3px solid #fff;
                                border-radius:0 8px 8px 0;padding:1.1rem 1.4rem;margin-bottom:1.5rem;
                                animation:fadeInUp 0.4s ease both;">
                                <span style="font-size:0.68rem;color:#555;text-transform:uppercase;
                                             letter-spacing:0.1em;font-weight:600;">Recommendation</span>
                                <p style="color:#e5e5e5;font-size:0.93rem;margin:0.4rem 0 0 0;
                                          line-height:1.65;font-weight:500;">{rec}</p>
                            </div>""", unsafe_allow_html=True)

                        st.markdown('<p class="section-header">Community Consensus</p>', unsafe_allow_html=True)
                        summary = result.get("summary", "No summary.")
                        st.markdown(
                            f'<div class="glass-card"><p style="color:#aaa;font-size:0.92rem;line-height:1.75;margin:0;">{summary}</p></div>',
                            unsafe_allow_html=True,
                        )
                        pcol, rcol = st.columns(2, gap="medium")
                        with pcol:
                            st.markdown('<p class="section-header">What''s Good</p>', unsafe_allow_html=True)
                            for p in result.get("positive_aspects", []):
                                st.markdown(f'<div class="pro-item">{p}</div>', unsafe_allow_html=True)
                        with rcol:
                            st.markdown('<p class="section-header">Red Flags</p>', unsafe_allow_html=True)
                            flags = result.get("red_flags", [])
                            if flags:
                                for fl in flags:
                                    st.markdown(f'<div class="red-flag-item">{fl}</div>', unsafe_allow_html=True)
                            else:
                                st.markdown('<div class="pro-item">No major red flags detected.</div>', unsafe_allow_html=True)
                        version = result.get("version_concerns", "None")
                        if version and version.lower() != "none":
                            st.markdown('<p class="section-header" style="margin-top:1.2rem;">Compatibility Note</p>', unsafe_allow_html=True)
                            st.markdown(f"""
                            <div style="background:#161200;border:1px solid #2e2800;border-left:3px solid #eab308;
                                border-radius:0 7px 7px 0;padding:0.85rem 1.1rem;">
                                <p style="color:#ca8a04;font-size:0.88rem;margin:0;line-height:1.6;">{version}</p>
                            </div>""", unsafe_allow_html=True)

                    # Tab 2 - Top Comments
                    with tab2:
                        if show_top_comments:
                            st.markdown('<p class="section-header">Top Liked Comments</p>', unsafe_allow_html=True)
                            for i, c in enumerate(comments[:10]):
                                likes_str = format_number(c["likes"]) if c["likes"] > 0 else "—"
                                author    = c["author"]
                                pub_at    = c["published_at"]
                                text_raw  = c["text"]
                                text_disp = text_raw[:320] + ("..." if len(text_raw) > 320 else "")
                                st.markdown(f"""
                                <div class="comment-card" style="animation-delay:{i * 0.05}s;">
                                    <div style="display:flex;justify-content:space-between;align-items:center;">
                                        <span class="comment-author">{author}</span>
                                        <span class="comment-likes">{likes_str} likes · {pub_at}</span>
                                    </div>
                                    <p class="comment-text">{text_disp}</p>
                                </div>""", unsafe_allow_html=True)
                        else:
                            st.info("Enable 'Top Liked Comments' in the sidebar.")

                    # Tab 3 - Sentiment
                    with tab3:
                        if show_sentiment:
                            st.markdown('<p class="section-header">Sentiment Breakdown</p>', unsafe_allow_html=True)
                            pos = s_data.get("positive", 0)
                            neu = s_data.get("neutral",  0)
                            neg = s_data.get("negative", 0)
                            for label, val, bar_c, txt_c in [
                                ("Positive", pos, "#22c55e", "#4ade80"),
                                ("Neutral",  neu, "#444",    "#888"),
                                ("Negative", neg, "#ef4444", "#f87171"),
                            ]:
                                st.markdown(f"""
                                <div style="margin-bottom:1.3rem;">
                                    <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:0.4rem;">
                                        <span style="color:#bbb;font-size:0.85rem;font-weight:500;">{label}</span>
                                        <span style="color:{txt_c};font-weight:700;font-size:0.9rem;">{val}%</span>
                                    </div>
                                    <div style="background:#1a1a1a;border-radius:3px;height:6px;overflow:hidden;">
                                        <div style="width:{val}%;height:100%;background:{bar_c};border-radius:3px;
                                            animation:barGrow 0.8s ease both;"></div>
                                    </div>
                                </div>""", unsafe_allow_html=True)
                            st.markdown("<br>", unsafe_allow_html=True)
                            df = pd.DataFrame({
                                "Sentiment":  ["Positive", "Neutral", "Negative"],
                                "Percentage": [pos, neu, neg],
                            })
                            st.bar_chart(df.set_index("Sentiment"), color=["#ffffff"],
                                         use_container_width=True, height=220)
                        else:
                            st.info("Enable 'Sentiment Breakdown' in the sidebar.")

                    # Tab 4 - Tips & Keywords
                    with tab4:
                        if show_tips:
                            tips = result.get("community_tips", [])
                            if tips:
                                st.markdown('<p class="section-header">From the Comment Section</p>', unsafe_allow_html=True)
                                for tip in tips:
                                    st.markdown(f"""
                                    <div style="background:#111;border:1px solid #222;border-left:3px solid #2a2a2a;
                                        border-radius:0 7px 7px 0;padding:0.8rem 1.1rem;margin-bottom:0.5rem;">
                                        <p style="color:#aaa;font-size:0.88rem;margin:0;line-height:1.55;">{tip}</p>
                                    </div>""", unsafe_allow_html=True)
                        if show_keywords:
                            keywords = result.get("top_keywords", [])
                            if keywords:
                                st.markdown('<p class="section-header" style="margin-top:1.3rem;">Keywords</p>', unsafe_allow_html=True)
                                chips = "".join(
                                    f'<span class="keyword-chip">{kw}</span>'
                                    for kw in keywords
                                )
                                st.markdown(f'<div style="padding:0.3rem 0;">{chips}</div>', unsafe_allow_html=True)
                        if not show_tips and not show_keywords:
                            st.info("Enable tips/keywords in the sidebar.")

                    # Tab 5 - Export
                    with tab5:
                        st.markdown('<p class="section-header">Download Report</p>', unsafe_allow_html=True)
                        report_md = generate_report_markdown(
                            video_meta, result, persona_description, len(comments)
                        )
                        ts = datetime.now().strftime("%Y%m%d_%H%M")
                        st.download_button(
                            label="Download Full Report (.md)",
                            data=report_md,
                            file_name=f"tubefit_{video_id}_{ts}.md",
                            mime="text/markdown",
                            use_container_width=True,
                        )
                        st.markdown("<br>", unsafe_allow_html=True)
                        st.markdown('<p class="section-header">Raw JSON</p>', unsafe_allow_html=True)
                        with st.expander("View Gemini response"):
                            st.json(result)
                        analysed_at = datetime.now().strftime("%b %d, %Y at %H:%M")
                        st.markdown(f"""
                        <div class="glass-card" style="margin-top:1rem;">
                            <p style="color:#555;font-size:0.82rem;margin:0;line-height:1.9;">
                                Video ID &nbsp;·&nbsp; <span style="color:#888;">{video_id}</span><br>
                                Analysed &nbsp;·&nbsp; <span style="color:#888;">{analysed_at}</span><br>
                                Comments &nbsp;·&nbsp; <span style="color:#888;">{len(comments)}</span><br>
                                Persona  &nbsp;·&nbsp; <span style="color:#888;">{selected_persona}</span>
                            </p>
                        </div>""", unsafe_allow_html=True)

# FOOTER
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style="padding:1.5rem 0;border-top:1px solid #1e1e1e;margin-top:2rem;
    display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:0.5rem;">
    <span style="color:#444;font-size:0.78rem;font-weight:600;letter-spacing:-0.2px;">TubeFit.</span>
    <span style="color:#333;font-size:0.72rem;">Watch smarter, not longer.</span>
</div>
""", unsafe_allow_html=True)