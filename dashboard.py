import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(page_title="IPL Key Stats 2008-2025", layout="wide")

# -------------------------------------------------
# LOAD DATA
# -------------------------------------------------
matches = pd.read_csv("data/matches.csv")
deliveries = pd.read_csv("data/deliveries.csv")

# Handle column differences safely
batsman_col = "batter" if "batter" in deliveries.columns else "batsman"

# -------------------------------------------------
# CUSTOM STYLING (Premium Look)
# -------------------------------------------------
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
    color: white;
}
.metric-card {
    background: rgba(255,255,255,0.08);
    padding: 25px;
    border-radius: 12px;
    text-align: center;
    backdrop-filter: blur(8px);
}
.section-box {
    background: rgba(255,255,255,0.06);
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 15px;
}
h1, h2, h3, h4 {
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("🏏 IPL Key Stats 2008–2025")

season_option = st.selectbox(
    "Select Season",
    ["All"] + sorted(matches['season'].dropna().unique())
)

if season_option != "All":
    matches = matches[matches['season'] == season_option]

# -------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------
total_matches = len(matches)
total_runs = deliveries['total_runs'].sum()
total_wickets = deliveries['dismissal_kind'].notna().sum()
avg_runs = round(total_runs / total_matches, 2) if total_matches else 0
avg_wickets = round(total_wickets / total_matches, 2) if total_matches else 0

# -------------------------------------------------
# KPI ROW
# -------------------------------------------------
k1, k2, k3, k4, k5 = st.columns(5)

kpi_data = [
    ("Total Matches", total_matches),
    ("Total Runs", f"{total_runs:,}"),
    ("Total Wickets", f"{total_wickets:,}"),
    ("Avg Runs", avg_runs),
    ("Avg Wickets", avg_wickets),
]

for col, (title, value) in zip([k1, k2, k3, k4, k5], kpi_data):
    with col:
        st.markdown(f"""
        <div class="metric-card">
            <h4>{title}</h4>
            <h2>{value}</h2>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# SECOND ROW (3 PANELS)
# -------------------------------------------------
col1, col2, col3 = st.columns([1,1.2,1])

# -----------------------------
# Toss Decision Pie
# -----------------------------
with col1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Toss Decision")

    toss_counts = matches['toss_decision'].value_counts()

    fig1 = px.pie(
        values=toss_counts.values,
        names=toss_counts.index,
        hole=0.4
    )
    fig1.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Team Run Distribution
# -----------------------------
with col2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Team Run Distribution")

    if 'target_runs' in matches.columns:
        bins = [0, 35, 70, 105, 140, 175, 210, 245, 280]
        matches['run_bin'] = pd.cut(matches['target_runs'], bins)
        run_dist = matches['run_bin'].value_counts().sort_index()

        fig2 = px.bar(
            x=run_dist.index.astype(str),
            y=run_dist.values
        )
        fig2.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Run distribution data not available in dataset.")

    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Superover Wins
# -----------------------------
with col3:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Superover Wins")

    if 'result' in matches.columns:
        superover = matches[matches['result'] == 'tie']
        winner_counts = superover['winner'].value_counts().head(7)

        fig3 = px.bar(
            x=winner_counts.values,
            y=winner_counts.index,
            orientation='h'
        )
        fig3.update_layout(template="plotly_dark", height=350)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Superover data not available.")

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------
# BOTTOM SECTION (2 WIDE CHARTS)
# -------------------------------------------------
bottom1, bottom2 = st.columns(2)

# -----------------------------
# Team Total Wins
# -----------------------------
with bottom1:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Team Total Wins")

    team_wins = matches['winner'].value_counts()

    fig4 = px.bar(
        x=team_wins.values,
        y=team_wins.index,
        orientation='h'
    )
    fig4.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Season Match Count
# -----------------------------
with bottom2:
    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("Season Match Count")

    season_counts = matches['season'].value_counts().sort_index()

    fig5 = px.bar(
        x=season_counts.index,
        y=season_counts.values
    )
    fig5.update_layout(template="plotly_dark", height=350)
    st.plotly_chart(fig5, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.success("Professional IPL Dashboard Loaded Successfully 🚀")