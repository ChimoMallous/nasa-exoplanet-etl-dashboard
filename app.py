import streamlit as st
import plotly.express as px
import base64
from src.analytics import count_exoplanet_discoveries, count_stars_with_exoplanets, count_planets_discovered_by_year, top_exoplanet_discovery_methods
import os

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
    total_exoplanets = count_exoplanet_discoveries()
    st.metric(label="Total Confirmed Exoplanets Discovered", value=total_exoplanets.iloc[0, 0])

with c2:
    total_stars = count_stars_with_exoplanets()
    st.metric(label="Total Confirmed Stars with Planets", value=total_stars.iloc[0, 0])

with c1:
    planets_by_year = count_planets_discovered_by_year()
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
    st.plotly_chart(fig)

with c2:
    top_methods = top_exoplanet_discovery_methods()
    fig = px.bar(
        top_methods,
        x='discovery_method',
        y='method_frequency',
        title="Exoplanets Discovered by Method",
        labels={'discovery_method': 'Discovery Method', 'method_frequency': 'Number of Exoplanet Discoveries'},
        color_discrete_sequence=["#011BAE"]
        )
    fig.update_layout(
        yaxis=dict(showgrid=False)
    )
    st.plotly_chart(fig)

