import json
import streamlit as st
import pandas as pd

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="SEO / ASO Strategic Plan",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# GLOBAL CSS
# =========================================================
st.markdown("""
<style>
:root {
    --accent: #2E7DFF;
    --accent2: #22C55E;
    --bg: #0B1220;
    --card: #131B2E;
    --border: #1E293B;
    --text: #F8FAFC;
    --muted: #94A3B8;
}

.stApp {
    background:
      radial-gradient(1200px 600px at 10% -10%, #2E7DFF22, transparent 60%),
      radial-gradient(1000px 500px at 100% 0%, #22C55E22, transparent 60%),
      var(--bg);
}

.block-container {
    padding-top: 2.5rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

.hero { text-align: center; padding: 40px 20px 20px 20px; margin-bottom: 10px; }
.hero-badge {
    display: inline-block; padding: 6px 14px;
    border: 1px solid var(--accent); border-radius: 999px;
    color: var(--accent); font-size: 0.8rem;
    letter-spacing: 0.12em; text-transform: uppercase; margin-bottom: 18px;
}
.hero-title {
    font-size: 3rem; font-weight: 800; line-height: 1.1;
    background: linear-gradient(90deg, #2E7DFF 0%, #22C55E 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin: 0 0 12px 0;
}
.hero-sub { color: var(--muted); font-size: 1.15rem; max-width: 700px; margin: 0 auto; }

.slide-head {
    display: flex; align-items: center; gap: 16px;
    margin: 8px 0 24px 0; padding-bottom: 16px;
    border-bottom: 1px solid var(--border);
}
.slide-num {
    width: 44px; height: 44px; border-radius: 12px;
    background: linear-gradient(135deg, #2E7DFF, #22C55E);
    color: #fff; display: flex; align-items: center; justify-content: center;
    font-weight: 800; font-size: 1.1rem;
    box-shadow: 0 8px 24px #2E7DFF44; flex-shrink: 0;
}
.slide-title { font-size: 1.8rem; font-weight: 700; color: var(--text); margin: 0; }
.slide-tag {
    display: inline-block; padding: 3px 10px; border-radius: 999px;
    background: #2E7DFF22; color: var(--accent);
    font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.1em; margin-left: 12px; vertical-align: middle;
}

.card {
    background: linear-gradient(180deg, #131B2E 0%, #0F1728 100%);
    border: 1px solid var(--border); border-radius: 14px;
    padding: 20px; height: 100%; transition: 0.2s ease;
}
.card:hover { border-color: var(--accent); transform: translateY(-2px); box-shadow: 0 12px 32px #2E7DFF1A; }
.card-header {
    color: var(--accent); font-weight: 700; font-size: 1.02rem;
    margin-bottom: 12px; padding-bottom: 10px;
    border-bottom: 1px solid var(--border); letter-spacing: 0.01em;
}
.card-item {
    color: var(--text); padding: 8px 0; font-size: 0.94rem;
    display: flex; align-items: flex-start; gap: 8px;
}
.card-item::before {
    content: ""; width: 6px; height: 6px;
    background: var(--accent); border-radius: 50%;
    margin-top: 8px; flex-shrink: 0;
}

.kpi-tile {
    background: linear-gradient(135deg, #2E7DFF15, #22C55E15);
    border: 1px solid #2E7DFF44; border-radius: 12px;
    padding: 16px 18px; margin-bottom: 10px;
    color: var(--text); font-weight: 600; font-size: 0.95rem;
}
.kpi-tile .kpi-label {
    color: var(--muted); font-size: 0.72rem; text-transform: uppercase;
    letter-spacing: 0.12em; font-weight: 700;
    display: block; margin-bottom: 6px;
}

.funnel-step {
    background: linear-gradient(90deg, #2E7DFF, #22C55E);
    color: #fff; font-weight: 700; padding: 14px 22px;
    border-radius: 10px; margin: 8px auto; text-align: center;
    font-size: 0.98rem; box-shadow: 0 6px 18px #2E7DFF33;
    letter-spacing: 0.01em;
}

.priority-item {
    background: linear-gradient(180deg, #131B2E 0%, #0F1728 100%);
    border: 1px solid var(--border); border-left: 4px solid var(--accent);
    border-radius: 10px; padding: 16px 20px; margin-bottom: 10px;
    color: var(--text); font-size: 1rem;
    display: flex; align-items: center; transition: 0.2s ease;
}
.priority-item:hover { border-left-color: var(--accent2); background: linear-gradient(180deg, #16203A 0%, #131B2E 100%); }
.priority-num {
    display: inline-flex; align-items: center; justify-content: center;
    width: 32px; height: 32px;
    background: linear-gradient(135deg, #2E7DFF, #22C55E);
    color: #fff; border-radius: 8px; font-weight: 800;
    margin-right: 16px; flex-shrink: 0; font-size: 0.9rem;
}

.flow-wrap {
    display: flex; flex-wrap: wrap; justify-content: center;
    align-items: center; gap: 10px; padding: 20px;
}
.flow-chip {
    background: linear-gradient(180deg, #131B2E 0%, #0F1728 100%);
    border: 1px solid var(--accent); color: var(--text);
    padding: 12px 20px; border-radius: 10px; font-weight: 600;
    font-size: 0.95rem; box-shadow: 0 4px 16px #2E7DFF22;
}
.flow-arrow { color: var(--accent2); font-weight: 800; font-size: 1.2rem; }

.quad {
    border-radius: 14px; padding: 20px; height: 100%;
    border: 1px solid var(--border);
    background: linear-gradient(180deg, #131B2E 0%, #0F1728 100%);
}
.quad-label {
    font-weight: 800; font-size: 1.1rem; letter-spacing: 0.06em;
    margin-bottom: 14px; padding-bottom: 10px;
    border-bottom: 1px solid var(--border);
}
.quad-item { color: var(--text); padding: 6px 0; font-size: 0.95rem; }

.ask-box {
    background: linear-gradient(135deg, #2E7DFF22, #22C55E22);
    border: 2px solid var(--accent2); border-radius: 14px;
    padding: 22px 26px; margin-top: 18px; color: var(--text);
    font-weight: 600; font-size: 1rem; box-shadow: 0 8px 32px #22C55E22;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0B1220 0%, #0F1728 100%);
    border-right: 1px solid var(--border);
}
.sidebar-title {
    font-size: 1.1rem; font-weight: 800; color: var(--text);
    letter-spacing: 0.02em; margin-bottom: 14px;
}
.sidebar-meta {
    color: var(--muted); font-size: 0.8rem;
    padding-top: 8px; border-top: 1px solid var(--border); margin-top: 12px;
}

.footer {
    text-align: center; color: var(--muted); font-size: 0.8rem;
    padding-top: 40px; margin-top: 40px;
    border-top: 1px solid var(--border); letter-spacing: 0.05em;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DECK
# =========================================================
@st.cache_data
def load_deck(path="slides.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

deck = load_deck()

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown('<div class="sidebar-title">📊 Deck Navigation</div>', unsafe_allow_html=True)

    slide_titles = [f"{s['id']:02d}  ·  {s['title']}" for s in deck["slides"]]
    choice = st.radio("Slides", slide_titles, label_visibility="collapsed")

    selected_id = int(choice.split("·")[0].strip())
    slide = next(s for s in deck["slides"] if s["id"] == selected_id)

    st.markdown("---")
    st.progress(selected_id / len(deck["slides"]))
    st.markdown(
        f'<div class="sidebar-meta">Slide {selected_id} of {len(deck["slides"])} · {deck["footer"]}</div>',
        unsafe_allow_html=True,
    )

# =========================================================
# SLIDE HEADER
# =========================================================
def slide_header(s):
    tag = s.get("type", "section").upper()
    st.markdown(
        f"""
        <div class="slide-head">
            <div class="slide-num">{s['id']:02d}</div>
            <div>
                <span class="slide-title">{s['title']}</span>
                <span class="slide-tag">{tag}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# =========================================================
# RENDERERS
# =========================================================
def render_title(s):
    st.markdown(
        f"""
        <div class="hero">
            <div class="hero-badge">Strategic Plan</div>
            <div class="hero-title">{s['title']}</div>
            <div class="hero-sub">{s['subtitle']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    cols = st.columns(len(s.get("body", [])) or 1)
    for col, line in zip(cols, s.get("body", [])):
        with col:
            st.markdown(f'<div class="card">{line}</div>', unsafe_allow_html=True)

def render_funnel(s):
    slide_header(s)
    col1, col2 = st.columns([2, 1])
    with col1:
        for i, step in enumerate(s["funnel"]):
            width = 100 - i * 7
            st.markdown(
                f'<div class="funnel-step" style="width:{width}%;">{step}</div>',
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("#### Key KPIs")
        for kpi in s.get("kpis", []):
            st.markdown(
                f'<div class="kpi-tile"><span class="kpi-label">KPI</span>{kpi}</div>',
                unsafe_allow_html=True,
            )

def render_table(s):
    slide_header(s)
    df = pd.DataFrame(s["rows"], columns=s["columns"])
    st.dataframe(df, use_container_width=True, hide_index=True,
                 height=min(520, 70 + len(df) * 40))

def render_list(s):
    slide_header(s)
    for i, item in enumerate(s["items"], 1):
        if item.upper().startswith("ASK"):
            body = item.split(":", 1)[-1].strip()
            st.markdown(f'<div class="ask-box">📌 <b>ASK:</b> {body}</div>', unsafe_allow_html=True)
            continue
        st.markdown(
            f'<div class="priority-item"><span class="priority-num">{i:02d}</span>{item}</div>',
            unsafe_allow_html=True,
        )

def render_columns(s):
    slide_header(s)
    cols = st.columns(len(s["columns"]))
    for col, block in zip(cols, s["columns"]):
        with col:
            items_html = "".join(f'<div class="card-item">{i}</div>' for i in block["items"])
            st.markdown(
                f'<div class="card"><div class="card-header">{block["header"]}</div>{items_html}</div>',
                unsafe_allow_html=True,
            )

def render_flow(s):
    slide_header(s)
    chips = []
    for i, step in enumerate(s["steps"]):
        chips.append(f'<span class="flow-chip">{step}</span>')
        if i < len(s["steps"]) - 1:
            chips.append('<span class="flow-arrow">→</span>')
    st.markdown(f'<div class="flow-wrap">{"".join(chips)}</div>', unsafe_allow_html=True)

def render_quadrants(s):
    slide_header(s)
    colors = {"SCALE": "#22C55E", "FIX": "#F59E0B", "STOP": "#EF4444", "TEST": "#2E7DFF"}
    cols = st.columns(2)
    for i, q in enumerate(s["quadrants"]):
        color = colors.get(q["label"], "#2E7DFF")
        with cols[i % 2]:
            items_html = "".join(f'<div class="quad-item">• {x}</div>' for x in q["items"])
            st.markdown(
                f"""
                <div class="quad" style="border-top:4px solid {color};">
                    <div class="quad-label" style="color:{color};">{q['label']}</div>
                    {items_html}
                </div>
                """,
                unsafe_allow_html=True,
            )
            st.markdown("<br>", unsafe_allow_html=True)

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

# =========================================================
# FOOTER
# =========================================================
st.markdown(f'<div class="footer">{deck["footer"]}</div>', unsafe_allow_html=True)
