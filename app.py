import json
import os
import streamlit as st

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SEO / ASO Strategic Plan",
    page_icon="📈",
    layout="wide",
)

# =========================================================
# FALLBACK DECK (used if slides.json is missing or invalid)
# =========================================================
FALLBACK_DECK = {
    "title": "Strategic Plan & Approach",
    "subtitle": "Organic Growth via SEO & ASO",
    "footer": "SEO / ASO Strategic Plan - Confidential",
    "slides": [
        {
            "id": 1,
            "title": "Strategic Plan & Approach",
            "subtitle": "Organic Growth via SEO & ASO",
            "type": "title",
            "body": [
                "Team: SEO Lead / On-Page SEO / Off-Page / Intelligence / ASO",
                "Objective: Drive more sales through organic search and app-store visibility",
                "Horizon: 3+ months (Foundation, Cleanup, Growth, Scale)",
            ],
        },
        {
            "id": 2,
            "title": "Executive Summary",
            "type": "funnel",
            "funnel": [
                "Search Demand", "SERP Visibility", "Organic Traffic",
                "Landing Page", "Registration", "First Conversion",
                "Revenue", "Repeat Conversion",
            ],
            "kpis": [
                "Organic Conversions / Revenue",
                "Registrations to First Conversion to Repeat",
                "Installs to Registrations to Revenue (ASO)",
            ],
        },
    ],
}

# =========================================================
# LOAD DECK (with safe error handling)
# =========================================================
@st.cache_data
def load_deck(path="slides.json"):
    if not os.path.exists(path):
        st.warning(f"slides.json not found at {path}. Using fallback deck.")
        return FALLBACK_DECK

    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read().strip()

        if not raw:
            st.warning("slides.json is empty. Using fallback deck.")
            return FALLBACK_DECK

        return json.loads(raw)

    except json.JSONDecodeError as e:
        st.error(
            f"Invalid JSON in slides.json at line {e.lineno}, "
            f"column {e.colno}: {e.msg}\n\n"
            "Falling back to a minimal deck. Fix slides.json and rerun."
        )
        with st.expander("Show raw file (first 800 chars)"):
            st.code(raw[:800], language="json")
        return FALLBACK_DECK


deck = load_deck()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
st.sidebar.title("📊 Deck Navigation")
slide_titles = [f"{s['id']}. {s['title']}" for s in deck["slides"]]
choice = st.sidebar.radio("Go to slide", slide_titles, label_visibility="collapsed")
selected_id = int(choice.split(".")[0])
slide = next(s for s in deck["slides"] if s["id"] == selected_id)

st.sidebar.markdown("---")
st.sidebar.caption(deck["footer"])
st.sidebar.progress(selected_id / len(deck["slides"]))

# =========================================================
# RENDER HELPERS
# =========================================================
def render_title(s):
    st.markdown(
        f"<h1 style='text-align:center;margin-top:10vh;'>{s['title']}</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"<h3 style='text-align:center;color:#2E7DFF;'>{s['subtitle']}</h3>",
        unsafe_allow_html=True,
    )
    for line in s.get("body", []):
        st.markdown(
            f"<p style='text-align:center;'>{line}</p>",
            unsafe_allow_html=True,
        )

def render_funnel(s):
    st.header(s["title"])
    col1, col2 = st.columns([2, 1])
    with col1:
        for i, step in enumerate(s["funnel"]):
            st.markdown(
                f"<div style='background:linear-gradient(90deg,#2E7DFF,#22C55E);"
                f"padding:10px 20px;border-radius:8px;margin:6px 0;"
                f"color:white;font-weight:600;width:{100 - i * 5}%;'>{step}</div>",
                unsafe_allow_html=True,
            )
    with col2:
        for kpi in s.get("kpis", []):
            st.success(kpi)

def render_table(s):
    st.header(s["title"])
    st.dataframe(
        [dict(zip(s["columns"], row)) for row in s["rows"]],
        use_container_width=True,
        hide_index=True,
    )

def render_list(s):
    st.header(s["title"])
    for i, item in enumerate(s["items"], 1):
        st.markdown(f"**{i}.** {item}")

def render_columns(s):
    st.header(s["title"])
    cols = st.columns(len(s["columns"]))
    for col, block in zip(cols, s["columns"]):
        with col:
            st.subheader(block["header"])
            for item in block["items"]:
                st.markdown(f"- {item}")

def render_flow(s):
    st.header(s["title"])
    st.markdown(" -> ".join(f"**{x}**" for x in s["steps"]))

def render_quadrants(s):
    st.header(s["title"])
    cols = st.columns(2)
    for i, q in enumerate(s["quadrants"]):
        with cols[i % 2]:
            st.subheader(q["label"])
            for item in q["items"]:
                st.markdown(f"- {item}")

# =========================================================
# DISPATCH
# =========================================================
renderers = {
    "title": render_title,
    "funnel": render_funnel,
    "table": render_table,
    "list": render_list,
    "columns": render_columns,
    "flow": render_flow,
    "quadrants": render_quadrants,
}

renderers.get(slide["type"], render_list)(slide)
