import folium
from streamlit_folium import st_folium

def render_map():

    m = folium.Map(
        location=[10.5, 77.5],
        zoom_start=6
    )

    folium.Marker(
        [10.85, 76.27],
        popup="Kerala"
    ).add_to(m)

    st_folium(
        m,
        width=900,
        height=450
    )