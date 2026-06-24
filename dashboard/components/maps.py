import folium
from streamlit_folium import st_folium


def render_india_map():
    m = folium.Map(
        location=[20.59, 78.96],
        zoom_start=5
    )

    folium.Marker(
        [10.85, 76.27],
        popup="Kerala"
    ).add_to(m)

    st_folium(m, width=900, height=450)