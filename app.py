import streamlit as st
import plotly.express as px
from pathlib import Path
import base64
import os

import datetime

from src.etl import DB_PATH
from src.analytics import count_exoplanets_discovered, count_confirmed_hosts, recent_exoplanet_discovered, count_exoplanets_discovered_by_year, count_exoplanets_discovered_by_method, count_exoplanets_discovered_by_facility
from src.pipeline import run

st.set_page_config(page_title="Exoplanet Analytics", layout="wide")

ROOT = Path(__file__).parent

def load_css(css_file: str, bg_file: str) -> str:
    encoded = base64.b64encode((ROOT / bg_file).read_bytes()).decode()
    css = (ROOT / css_file).read_text()
    return f"<style>{css.replace('__BG__', encoded)}</style>"

st.markdown(
    load_css("assets/styles.css", "images/star-background.jpg"),
    unsafe_allow_html=True,
)

def db_date():
    return datetime.date.fromtimestamp(os.path.getmtime(DB_PATH))

if not os.path.exists(DB_PATH) or db_date() < datetime.date.today():
    with st.spinner("Retrieving latest data from today's NASA Exoplanet Archive"):
        pipeline_succeeded = run()
    if not pipeline_succeeded and not os.path.exists(DB_PATH):
        st.error(
            "Could not retrieve data from the NASA Exoplanet Archive and no local data is available. Please try again later."
        )
        st.stop()

last_retrieved = db_date()

st.title("Exoplanet Analytics Dashboard")
st.markdown(f":shimmer[Data last retrieved {last_retrieved} via the NASA Exoplanet Archive (TAP/ADQL) API]")

c1, c2, c3 = st.columns(3)

with c1:
    total_exoplanets = count_exoplanets_discovered()
    st.metric(label="Total Confirmed Exoplanets", value=total_exoplanets.iloc[0, 0])

with c2:
    total_hosts = count_confirmed_hosts()
    st.metric(label="Total Confirmed Hosts", value=total_hosts.iloc[0, 0])

with c3:
    recent_planet = recent_exoplanet_discovered()
    st.metric(label=f"Recent Discovery ({recent_planet.iloc[0, 1]})", value=recent_planet.iloc[0, 0])

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

with st.container(border=False):
    st.markdown(
        """
        <div style="text-align: center; font-size: 14px; color: rgba(128,128,128,0.9);">
            Built by Efthimios Mallous
            &nbsp;·&nbsp;
            <a href="https://github.com/ChimoMallous" target="_blank" style="color: #4A9EFF; text-decoration: none;">GitHub</a>
            &nbsp;·&nbsp;
            <a href="https://www.linkedin.com/in/efthimios-mallous-07b4b6378/" target="_blank" style="color: #4A9EFF; text-decoration: none;">LinkedIn</a>
            <br>
            <span style="font-size: 14px;">Data: NASA Exoplanet Archive (TAP/ADQL) API &nbsp;·&nbsp; Updated daily via ETL pipeline</span>
        </div>
        """,
        unsafe_allow_html=True,
    )