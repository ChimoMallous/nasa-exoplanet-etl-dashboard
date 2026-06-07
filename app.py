import streamlit as st
import plotly.express as px
import base64
import os
from datetime import datetime
from src.analytics import count_exoplanets_discovered, count_confirmed_hosts, newest_exoplanet_discovered, count_exoplanets_discovered_by_year, count_exoplanets_discovered_by_method, count_exoplanets_discovered_by_facility

st.set_page_config(page_title="Exoplanet Analytics", layout="wide")

if not os.path.exists("exoplanet_db"):
    from src.pipeline import run
    run()

if os.path.exists("exoplanet_db"):
    last_retrieved = datetime.fromtimestamp(os.path.getmtime("exoplanet_db")).strftime("%Y-%m-%d")
else:
    last_retrieved = "N/A"

with open("images/star_background.jpg", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
/* ── Background image ── */
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{encoded}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
/* ── Dark overlay ── */
[data-testid="stAppViewContainer"]::before {{
    content: "";
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.45);
    pointer-events: none;
    z-index: 0;
}}
[data-testid="stAppViewContainer"] > * {{
    position: relative;
    z-index: 1;
}}
/* ── Strip default Streamlit backgrounds ── */
.stApp, section.main, div.block-container,
header, footer {{
    background: transparent !important;
    box-shadow: none !important;
}}
/* ── Glass cards on metrics only ── */
[data-testid="stMetric"] {{
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 14px;
    padding: 16px !important;
}}
/* ── Glass bubble on captions ── */
[data-testid="stCaptionContainer"] {{
    background: rgba(255, 255, 255, 0.07) !important;
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.12);
    border-radius: 10px;
    padding: 10px 14px !important;
    margin-bottom: 7px !important;
}}
/* ── Sidebar glass ── */
[data-testid="stSidebar"] {{
    background: rgba(0, 0, 0, 0.40) !important;
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border-right: 1px solid rgba(255, 255, 255, 0.08);
}}
/* ── Transparent charts so nebula shows through ── */
.js-plotly-plot .plotly,
.js-plotly-plot .plotly .bg,
.stPlotlyChart,
.stPlotlyChart > div,
iframe {{
    background: transparent !important;
    background-color: transparent !important;
}}
/* ── Text readable on dark bg ── */
[data-testid="stMetricLabel"],
[data-testid="stMetricValue"],
[data-testid="stMetricDelta"],
p, h1, h2, h3, label {{
    color: rgba(255, 255, 255, 0.90) !important;
    text-shadow: 0 1px 4px rgba(0,0,0,0.6);
}}
</style>
""", unsafe_allow_html=True)

st.title("Exoplanet Analytics Dashboard")
st.markdown(f":shimmer[Data retrieved via the NASA Exoplanet Archive API (Planetary Systems Table)]")

c1, c2, c3 = st.columns(3)

with c1:
    total_exoplanets = count_exoplanets_discovered()
    st.metric(label="Total Confirmed Exoplanets", value=total_exoplanets.iloc[0, 0])

with c2:
    total_hosts = count_confirmed_hosts()
    st.metric(label="Total Confirmed Hosts", value=total_hosts.iloc[0, 0])

with c3:
    newest_planet = newest_exoplanet_discovered()
    st.metric(label=f"Recently Discovered Exoplanet ({newest_planet.iloc[0, 1]})", value=newest_planet.iloc[0, 0])

g1, g2 = st.columns(2)

with g1:
    top_methods = count_exoplanets_discovered_by_method()
    fig = px.bar(
        top_methods,
        x='discovery_method',
        y='method_frequency',
        title="Exoplanets Discovered by Method",
        labels={'discovery_method': 'Discovery Method', 'method_frequency': 'Number of Exoplanets Discovered'},
        color_discrete_sequence=["#0122DB"]
        )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        yaxis=dict(showgrid=False)
    )
    with st.container(border=True):
        st.plotly_chart(fig)
    st.caption("Transit photometry dominates exoplanet detection, accounting for over 70% of all confirmed discoveries driven by the Kepler and TESS space telescopes.")

with g2:
    top_facilities = count_exoplanets_discovered_by_facility()
    fig = px.bar(
        top_facilities,
        x='discovery_facility',
        y='exoplanets_discovered',
        title="Exoplanets Discovered by Facility (Top 10)",
        labels={
            "exoplanets_discovered": "Number of Exoplanets Discovered",
            "discovery_facility": "Discovery Facility"
        },
        color_discrete_sequence=["#0122DB"]
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="white",
        yaxis=dict(showgrid=False)
    )
    with st.container(border=True):
        st.plotly_chart(fig)
    st.caption("The Kepler Mission leads discoveries, accounting for roughly 44% of confirmed worlds. TESS has also contributed significantly, confirming around 14% of exoplanets.")

planets_by_year = count_exoplanets_discovered_by_year()
fig = px.line(
    planets_by_year,
    x='year',
    y='total_exoplanets_discovered',
    title='Exoplanets Discovered by Year',
    labels={'year': 'Year', 'total_exoplanets_discovered': 'Number of Exoplanets Discovered'},
    color_discrete_sequence=["#0122DB"]
)
fig.update_layout(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    yaxis=dict(showgrid=False)
)
fig.update_traces(
    line=dict(width=5, shape='spline'),
    mode='lines+markers',
    marker=dict(size=5)
)
with st.container(border=True):
    st.plotly_chart(fig)
st.caption("The dramatic increases in exoplanet discoveries in 2014 and 2016 were driven by two massive data releases from NASA’s Kepler Space Telescope, which used the transit method to spot exoplanets. In 2014, scientists verified over 700 new exoplanets simultaneously by focusing on systems with multiple candidates. In 2016, an even larger spike occurred when NASA announced more than 1,200 new planets at once, a breakthrough made possible by an automated data-vetting software called Robovetter.")

st.markdown(f":grey[Data last retrieved on {last_retrieved}]")