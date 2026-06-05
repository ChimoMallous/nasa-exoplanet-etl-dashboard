import streamlit as st
import plotly.express as px
import base64
import os
from src.analytics import count_exoplanets_discovered, count_exoplanets_discovered_2026, count_exoplanets_discovered_by_year, count_exoplanets_discovered_by_method, count_exoplanets_discovered_by_facility

st.set_page_config(page_title="Exoplanet Analytics", layout="wide")

if not os.path.exists("exoplanet_db"):
    from src.pipeline import run
    run()

with open("images/star_background.jpg", "rb") as f:
    encoded = base64.b64encode(f.read()).decode()

st.markdown(f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/jpeg;base64,{encoded}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}
</style>
""", unsafe_allow_html=True)
st.markdown("""
<style>
* {
    background-color: rgba(0, 0, 0, 0.05) !important;
}
</style>
""", unsafe_allow_html=True)

st.title("Exoplanet Analytics Dashboard")
st.markdown(":shimmer[Data sourced from the NASA Exoplanet Archive API Planetary Systems table]")

c1, c2 = st.columns(2)

with c1:
    total_exoplanets = count_exoplanets_discovered()
    st.metric(label="Total Confirmed Exoplanets Discovered", value=total_exoplanets.iloc[0, 0])

with c2:
    total_exoplanets_2026 = count_exoplanets_discovered_2026()
    st.metric(label="Total Confirmed Exoplanets Discovered This Year", value=total_exoplanets_2026.iloc[0, 0])

with c1:
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
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig)
    st.caption("Transit photometry dominates exoplanet detection, accounting for over 70% of all confirmed discoveries due to the Kepler and TESS space telescopes.")

with c2:
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
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig)
    st.caption("The Kepler Mission leads discoveries, finding roughly 44% of confirmed worlds. TESS has also contributed significantly, confirming around 14% of exoplanets.")

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
    yaxis=dict(showgrid=False)
)
fig.update_traces(
    line=dict(width=5, shape='spline'),
    mode='lines+markers',
    marker=dict(size=5)
)
st.plotly_chart(fig)
st.caption("The dramatic increases in exoplanet discoveries in 2014 and 2016 were driven by two massive data releases from NASA’s Kepler Space Telescope, which used the transit method to spot planets. In 2014, scientists verified over 700 new planets simultaneously by focusing on systems with multiple candidates. In 2016, an even larger spike occurred when NASA announced more than 1,200 new planets at once, a breakthrough made possible by an automated data-vetting software called Robovetter.")