import streamlit as st
import plotly.express as px
import base64
import os
from src.analytics import count_exoplanets_discovered, count_exoplanets_discovered_2026, count_exoplanets_discovered_by_year, top_exoplanet_discovery_methods, exoplanet_radius_by_discovery_method

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
    st.caption("Transit photometry dominates exoplanet detection, accounting for over 70% of all confirmed discoveries due to the Kepler and TESS space telescopes.")

with c2:
    size_dist = exoplanet_radius_by_discovery_method()
    fig = px.bar(
        size_dist,
        x='planet_count',
        y='discovery_method',
        color='size_category',
        orientation='h',  
        barmode='stack',
        custom_data=['planet_count'],
        color_discrete_map={
            "Small (<2 Earth Radius)": "#0B1D51",
            "Medium (2-6 Earth Radius)": "#2D7FF9",
            "Large (6-15 Earth Radius)": "#6FA8FF",
            "Giant (>15 Earth Radius)": "#A6C8FF"
        },
        category_orders={"size_category": [
            "Giant (>15 Earth Radius)",
            "Large (6-15 Earth Radius)",
            "Medium (2-6 Earth Radius)",
            "Small (<2 Earth Radius)"
        ]},
        title="Exoplanet Size Breakdown by Discovery Method (%)",
        labels={
            "planet_count": "Percentage of Discoveries (%)",
            "discovery_method": "Discovery Method",
            "size_category": "Planet Size"
        }
    )
    fig.update_layout(
        barnorm='percent',
        xaxis=dict(showgrid=False), 
        yaxis=dict(showgrid=False)
    )
    fig.update_traces(
        hovertemplate="<b>%{fullData.name}</b><br>Number of Exoplanets Discovered: %{customdata[0]}<br>Percentage: %{x:.1f}%<extra></extra>"
    )
    st.plotly_chart(fig)
    st.caption("Direct imaging finds mostly giant and large exoplanets. It primarily captures young, massive gas giants far from their star, as these bright planets are the easiest to photograph.")

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