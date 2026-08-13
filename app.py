import streamlit as st
import plotly.express as px
from pathlib import Path
import base64
import os

import datetime

from src.etl import DB_PATH
from src.analytics import count_exoplanets_discovered, count_confirmed_hosts, recent_exoplanet_discovered, count_exoplanets_discovered_by_year, count_exoplanets_discovered_by_method, sky_positions, exoplanet_classifications
from src.pipeline import run

st.set_page_config(page_title="Exoplanet Analytics", layout="wide")

ROOT = Path(__file__).parent

def load_css(css_file: str, bg_file: str) -> str:
    encoded = base64.b64encode((ROOT / bg_file).read_bytes()).decode()
    css = (ROOT / css_file).read_text()
    return f"<style>{css.replace('__BG__', encoded)}</style>"

CHART_AXIS_TITLE = dict(family="IBM Plex Mono, monospace", size=11, color="#FFFFFF")
CHART_TICK = dict(family="IBM Plex Mono, monospace", size=11, color="#FFFFFF")

def style_chart(fig, x_title="", y_title=""):
    """
    Applies the dashboard's shared chart theme so every figure matches the metric
    tiles: mono uppercase axis titles, muted gridlines, and glass tooltips.
    -
    Args:
        fig (Figure): Plotly figure to restyle in place.
        x_title (str): X axis label, rendered uppercase.
        y_title (str): Y axis label, rendered uppercase.
    -
    Returns:
        Figure: The same figure, restyled.
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans, sans-serif", color="#FFFFFF", size=12),
        hoverlabel=dict(
            bgcolor="rgba(12,18,32,0.96)",
            bordercolor="rgba(143,208,255,0.35)",
            font=dict(family="IBM Plex Mono, monospace", color="#FFFFFF", size=12),
        ),
        xaxis=dict(
            title=dict(text=x_title.upper(), font=CHART_AXIS_TITLE, standoff=16),
            tickfont=CHART_TICK,
            showgrid=False,
            showline=True,
            linecolor="rgba(255,255,255,0.12)",
            ticks="outside",
            tickcolor="rgba(255,255,255,0.12)",
            ticklen=4,
        ),
        yaxis=dict(
            title=dict(text=y_title.upper(), font=CHART_AXIS_TITLE, standoff=16),
            tickfont=CHART_TICK,
            showgrid=True,
            gridcolor="rgba(255,255,255,0.055)",
            zeroline=False,
        ),
        margin=dict(l=10, r=18, t=18, b=10),
    )
    return fig

st.markdown(
    load_css("assets/styles.css", "images/star-background.jpg"),
    unsafe_allow_html=True,
)

METHOD_DESCRIPTIONS = {
    "Transit": "The planet crosses in front of its star, dimming the starlight by a measurable fraction.",
    "Radial Velocity": "The planet's gravity tugs its star into a small orbit, shifting the star's light red and blue.",
    "Microlensing": "A foreground star's gravity magnifies a distant star, and an orbiting planet adds a brief extra spike.",
    "Imaging": "The planet is photographed directly once the star's overwhelming glare is blocked out.",
    "Transit Timing Variations": "An unseen planet's gravity makes a known transiting planet arrive early or late.",
    "Eclipse Timing Variations": "A planet orbiting a binary pair shifts the timing of the two stars' mutual eclipses.",
    "Orbital Brightness Modulation": "The planet's changing phases and reflected light vary the system's total brightness.",
    "Pulsar Timing": "A planet shifts the arrival time of a pulsar's otherwise metronomic radio pulses.",
    "Astrometry": "The star's position on the sky traces a tiny orbit around the system's center of mass.",
    "Pulsation Timing Variations": "A planet shifts the timing of a pulsating star's regular brightness cycles.",
    "Disk Kinematics": "A forming planet disturbs the gas motion in a young star's disk, leaving a detectable kink.",
}

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

st.subheader("Overview")

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

g1, g2 = st.columns(2, vertical_alignment="top", gap="medium")

with g1:
    st.subheader("Exoplanet Types")
    classes = exoplanet_classifications()
    classes["exoplanet_bin"] = classes["exoplanet_bin"].str.upper()

    CLASS_ORDER = ["TERRESTRIAL", "SUPER EARTH", "NEPTUNE-LIKE", "GAS GIANT"]
    fig = px.pie(
        classes,
        names="exoplanet_bin",
        values="planet_count",
        hole=0.25,
        color="exoplanet_bin",
        category_orders={"exoplanet_bin": CLASS_ORDER},
        color_discrete_map={
            "TERRESTRIAL":  "#ABB7FA",
            "SUPER EARTH":  "#8091ED",
            "NEPTUNE-LIKE": "#4159E4",
            "GAS GIANT":    "#0122DB",
        },
    )
    fig.update_traces(
        sort=False,
        direction="clockwise",
        textposition="outside",
        texttemplate="%{label} (%{value})<br>%{percent}",
        textfont=dict(family="IBM Plex Mono, monospace", size=11, color="#FFFFFF"),
        marker=dict(line=dict(color="rgba(10,14,24,0.9)", width=2)),
        hovertemplate="<b>%{label}</b><br>%{value} planets<br>%{percent}<extra></extra>",
    )
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="IBM Plex Sans, sans-serif", color="#FFFFFF", size=12),
        hoverlabel=dict(
            bgcolor="rgba(12,18,32,0.96)",
            bordercolor="rgba(143,208,255,0.35)",
            font=dict(family="IBM Plex Mono, monospace", color="#FFFFFF", size=12),
        ),
        showlegend=False,
        height=400,
        margin=dict(l=100, r=130, t=30, b=30),
    )

    with st.container(key="chart_classes"):
        st.plotly_chart(fig, config={"displayModeBar": False})

with g2:
    st.subheader("Top Discovery Methods")
    top_methods = count_exoplanets_discovered_by_method()
    with st.container(key="method_shares"):
        top_row = st.columns(2)
        bottom_row = st.columns(2)
        for cell, row in zip(top_row + bottom_row, top_methods.head(4).itertuples()):
            with cell:
                st.metric(
                    label=f"{row.discovery_method} ({row.method_frequency})",
                    value=f"{row.share_of_total}%",
                    help=METHOD_DESCRIPTIONS.get(
                        row.discovery_method,
                        "Detection method recorded by the NASA Exoplanet Archive.",
                    ),
                    height=215,
                )

st.caption(
    "Planets are classified by mass where measured and by radius otherwise: Terrestrial up to "
    "2 Earth masses or 1.25 Earth radii, Super Earth up to 10 or 2, Neptune-like up to 50 or 6, "
    "and Gas Giant above that. The 50 Earth-mass boundary sits between Neptune at 17 and Saturn "
    "at 95. Masses use the archive's best available value, which for radial-velocity detections "
    "is a lower bound rather than a true mass. 15 planets have neither measurement."
)

@st.cache_data
def load_sky():
    return sky_positions()

st.subheader("Where We Have Actually Looked")

sky = load_sky()
year = st.slider("Discoveries up to", 1992, int(sky["discovery_year"].max()),
                 value=int(sky["discovery_year"].max()), key="sky_year")
shown = sky[sky["discovery_year"] <= year]

SURVEY_ORDER = ["Kepler", "TESS", "K2", "All other facilities"]
SURVEY_COLORS = {
    "Kepler": "#FFA53C",              
    "TESS": "#22D3EE",                
    "K2": "#F472B6",                    
    "All other facilities": "#0122DB",  
}

counts = shown["survey"].value_counts()
labels = {s: f"{s} ({counts.get(s, 0)})" for s in SURVEY_ORDER}
shown = shown.assign(survey_label=shown["survey"].map(labels))

fig = px.scatter(
    shown,
    x="right_ascension", y="declination", color="survey_label",
    category_orders={"survey_label": [labels[s] for s in SURVEY_ORDER]},
    color_discrete_map={labels[s]: SURVEY_COLORS[s] for s in SURVEY_ORDER},
    hover_name="name",
    custom_data=["discovery_facility", "discovery_method", "discovery_year"],
    labels={"right_ascension": "", "declination": "", "survey_label": ""},
)
fig.update_traces(
    marker=dict(line=dict(width=0)),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "%{customdata[0]}<br>"
        "%{customdata[1]} Method<br>"
        "Discovered %{customdata[2]}<br>"
        "RA %{x:.1f}°   Dec %{y:.1f}°"
        "<extra></extra>"
    ),
)
fig.for_each_trace(
    lambda t: t.update(marker_opacity=.5, marker_size=3)
    if t.name.startswith("All other")
    else t.update(marker_opacity=0.95, marker_size=5)
)
style_chart(fig, x_title="Right ascension (deg)", y_title="Declination (deg)")
fig.update_layout(
    height=520,
    xaxis=dict(range=[0, 360], dtick=60),
    yaxis=dict(range=[-90, 90], dtick=30),
    legend=dict(orientation="h", y=-0.18, x=0, title=""),
)

with st.container(key="chart_sky"):
    st.plotly_chart(fig, config={"displayModeBar": False})

st.caption(
    "As of 2026, The Kepler cluster covers 0.58% of the sky and holds 44% of all confirmed planets. K2's arc "
    "traces the ecliptic, the only plane the spacecraft could hold steady on after a 2013 reaction "
    "wheel failure; TESS scatters across the whole sky by design; and the group near RA 268°, "
    "Dec −29° is the galactic center, where microlensing surveys point for dense background stars."
)

st.subheader("Discovery Over Time")

planets_by_year = count_exoplanets_discovered_by_year()
fig = px.line(
    planets_by_year,
    x='year',
    y='total_exoplanets_discovered',
    color_discrete_sequence=["#0122DB"],
)
fig.update_traces(
    line=dict(width=3.5, shape='spline'),
    mode='lines+markers',
    marker=dict(size=4, line=dict(width=0)),
    fill='tozeroy',
    fillcolor='rgba(1,34,219,0.20)',
    hovertemplate="<b>%{x}</b><br>%{y} Exoplanets discovered<extra></extra>",
)
style_chart(fig, x_title="Year", y_title="Exoplanets Discovered")
fig.update_layout(height=380)
with st.container(key="chart_year"):
    st.plotly_chart(fig, config={"displayModeBar": False})
st.caption("The dramatic increases in exoplanet discoveries in 2014 and 2016 were driven by two massive data releases from NASA's Kepler Space Telescope, which used the transit method to spot exoplanets. In 2014, scientists verified over 700 new exoplanets simultaneously by focusing on systems with multiple candidates. In 2016, an even larger spike occurred when NASA announced more than 1,200 new planets at once, a breakthrough made possible by an automated data-vetting software called Robovetter.")

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