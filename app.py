import json
import streamlit as st
import plotly.graph_objects as go

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
    --warn: #F59E0B;
    --danger: #EF4444;
    --bg: #0B1220;
    --card: #131B2E;
    --text: #F8FAFC;
    --muted: #94A3B8;
}
.block-container { padding-top: 2rem; padding-bottom: 2rem; max-width: 1200px; }

.hero-title {
    font-size: 3rem; font-weight: 800; text-align: center;
    background: linear-gradient(90deg,#2E7DFF,#22C55E);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    margin-bottom: 0.5rem;
}
.hero-sub { text-align:center; color: var(--muted); font-size: 1.1rem; margin-bottom: 2rem; }

.slide-title {
    font-size: 2rem; font-weight: 700; color: var(--text);
    border-left: 6px solid var(--accent); padding-left: 16px;
    margin-bottom: 1.5rem;
}

.card {
    background: var(--card); border: 1px solid #1E293B;
    border-radius: 12px; padding: 18px; margin-bottom: 12px;
    transition: 0.2s;
}
.card:hover { border-color: var(--accent); transform: translateY(-2px); }

.card-header {
    color: var(--accent); font-weight: 700;
    font-size: 1.05rem; margin-bottom: 10px;
}
.card-item {
    color: var(--text); padding: 6px 0;
    border-bottom: 1px solid #1E293B; font-size: 0.95rem;
}
.card-item:last-child { border-bottom: none; }

.funnel-step {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    color: white; font-weight: 600; padding: 12px 20px;
    border-radius: 8px; margin: 6px auto; text-align: center;
}
.priority-item {
    background: var(--card); border-left: 4px solid var(--accent);
    border-radius: 8px; padding: 14px 18px; margin-bottom: 8px;
    color: var(--text); font-size: 1rem;
}
.priority-num {
    display: inline-block; width: 28px; height: 28px;
    background: var(--accent); color: white; border-radius: 50%;
    text-align: center; line-height: 28px; font-weight: 700;
    margin-right: 12px;
}
.ask-box {
    background: linear-gradient(90deg,#2E7DFF22,#22C55E22);
    border: 2px solid var(--accent2); border-radius: 12px;
    padding: 20px; margin-top: 20px; color: var(--text);
    font-weight: 600;
}
.footer { text-align: center; color: var(--muted); font-size: 0.8rem; padding-top: 40px; }
</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD DATA
# =========================================================
@st.cache_data
def load_deck(path="slides.json"):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

deck = load_deck()

# =========================================================
# SIDEBAR NAVIGATION
# =========================================================
st.sidebar.markdown("## 📊 Deck Navigation")
slide_titles = [f"{s['id']:02d}. {s['title']}" for s in deck["slides"]]
choice = st.sidebar.radio("Slides", slide_titles, label_visibility="collapsed")

selected_id = int(choice.split(".")[0])
slide = next(s for s in deck["slides"] if s["id"] == selected_id)

# progress + prev/next
st.sidebar.markdown("---")
st.sidebar.progress(selected_id / len(deck["slides"]))
st.sidebar.caption(f"Slide {selected_id} of {len(deck['slides'])}")

col_prev, col_next = st.sidebar.columns(2)
with col_prev:
    if st.button("← Prev", use_container_width=True, disabled=selected_id == 1):
        st.session_state["nav"] = selected_id - 1
        st.rerun()
with col_next:
    if st.button("Next →", use_container_width=True, disabled=selected_id == len(deck["slides"])):
        st.session_state["nav"] = selected_id + 1
        st.rerun()

st.sidebar.markdown("---")
st.sidebar.caption(deck["footer"])

# =========================================================
# RENDERERS
# =========================================================
def render_title(s):
    st.markdown(f"<div class='hero-title'>{s['title']}</div>", unsafe_allow_html=True)
    st.markdown(f"<div class='hero-sub'>{s['subtitle']}</div>", unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)
    cols = st.columns(len(s.get("body", [])))
    for col, line in zip(cols, s.get("body", [])):
        with col:
            st.markdown(f"<div class='card'>{line}</div>", unsafe_allow_html=True)

def render_funnel(s):
    st.markdown(f"<div class='slide-title'>{s['title']}</div>", unsafe_allow_html=True)
    col1, col2 = st.columns([2, 1])
    with col1:
        n = len(s["funnel"])
        for i, step in enumerate(s["funnel"]):
            width = 100 - (i * 8)
            st.markdown(
                f"<div class='funnel-step' style='width:{width}%;'>{step}</div>",
                unsafe_allow_html=True,
            )
    with col2:
        st.markdown("#### Key KPIs")
        for kpi in s.get("kpis", []):
            st.markdown(f"<div class='card'>{kpi}</div>", unsafe_allow_html=True)

def render_table(s):
    st.markdown(f"<div class='slide-title'>{s['title']}</div>", unsafe_allow_html=True)
    import pandas as pd
    df = pd.DataFrame(s["rows"], columns=s["columns"])
    st.dataframe(df, use_container_width=True, hide_index=True, height=min(500, 60 + len(df) * 45))

def render_list(s):
    st.markdown(f"<div class='slide-title'>{s['title']}</div>", unsafe_allow_html=True)
    for i, item in enumerate(s["items"], 1):
        st.markdown(
            f"<div class='priority-item'><span class='priority-num'>{i}</span>{item}</div>",
            unsafe_allow_html=True,
        )

def render_columns(s):
    st.markdown(f"<div class='slide-title'>{s['title']}</div>", unsafe_allow_html=True)
    cols = st.columns(len(s["columns"]))
    for col, block in zip(cols, s["columns"]):
        with col:
            items_html = "".join(f"<div class='card-item'>• {i}</div>" for i in block["items"])
            st.markdown(
                f"<div class='card'><div class='card-header'>{block['header']}</div>{items_html}</div>",
                unsafe_allow_html=True,
            )

def render_flow(s):
    st.markdown(f"<div class='slide-title'>{s['title']}</div>", unsafe_allow_html=True)
    steps = s["steps"]
    html = " <span style='color:#2E7DFF;font-weight:700;'>→</span> ".join(
        f"<span style='background:#131B2E;border:1px solid #2E7DFF;padding:10px 16px;"
        f"border-radius:8px;color:#F8FAFC;display:inline-block;margin:6px 4px;'>{x}</span>"
        for x in steps
    )
    st.markdown(f"<div style='text-align:center;'>{html}</div>", unsafe_allow_html=True)

def render_quadrants(s):
    st.markdown(f"<div class='slide-title'>{s['title']}</div>", unsafe_allow_html=True)
    colors = {"SCALE": "#22C55E", "FIX": "#F59E0B", "STOP": "#EF4444", "TEST": "#2E7DFF"}
    cols = st.columns(2)
    for i, q in enumerate(s["quadrants"]):
        with cols[i % 2]:
            color = colors.get(q["label"], "#2E7DFF")
            items_html = "".join(f"<div class='card-item'>• {x}</div>" for x in q["items"])
            st.markdown(
                f"<div class='card' style='border-left:5px solid {color};'>"
                f"<div class='card-header' style='color:{color};'>{q['label']}</div>"
                f"{items_html}</div>",
                unsafe_allow_html=True,
            )

# =========================================================
# OPTIONAL CHART TAB (Plotly)
# =========================================================
def render_charts_tab():
    st.markdown("### 📊 Visual Analytics")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("#### Tools Cost Breakdown")
        fig = go.Figure(data=[go.Pie(
            labels=["Webshell", "RDP", "Google Dev", "3rd Party"],
            values=[400, 50, 25, 65],
            hole=0.55,
            marker=dict(colors=["#2E7DFF", "#22C55E", "#F59E0B", "#EF4444"]),
        )])
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), height=350, margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("#### Funnel Drop-off Model (Illustrative)")
        stages = ["Impressions", "Clicks", "Landing", "Registration", "Conversion", "Revenue"]
        values = [100000, 8000, 6000, 1200, 300, 90]
        fig2 = go.Figure(go.Funnel(
            y=stages, x=values,
            marker=dict(color=["#2E7DFF", "#3B82F6", "#22C55E", "#F59E0B", "#EF4444", "#A855F7"]),
        ))
        fig2.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#F8FAFC"), height=350, margin=dict(t=20, b=20),
        )
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### Roadmap Timeline")
    fig3 = go.Figure()
    phases = [
        ("Foundation", 0, 2, "#2E7DFF"),
        ("Cleanup", 2, 4, "#22C55E"),
        ("Growth", 4, 8, "#F59E0B"),
        ("Scale", 8, 12, "#A855F7"),
    ]
    for name, start, end, color in phases:
        fig3.add_trace(go.Bar(
            y=["Roadmap"], x=[end - start], base=[start],
            orientation="h", name=name,
            marker=dict(color=color), text=name, textposition="inside",
        ))
    fig3.update_layout(
        barmode="stack", showlegend=False, height=220,
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#F8FAFC"),
        xaxis=dict(title="Weeks", gridcolor="#1E293B"),
        yaxis=dict(showticklabels=False),
        margin=dict(t=20, b=20),
    )
    st.plotly_chart(fig3, use_container_width=True)

# =========================================================
# MAIN DISPATCH
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

tab_deck, tab_charts = st.tabs(["📑 Deck", "📊 Charts"])

with tab_deck:
    renderers.get(slide["type"], render_list)(slide)

with tab_charts:
    render_charts_tab()

st.markdown(f"<div class='footer'>{deck['footer']}</div>", unsafe_allow_html=True)
