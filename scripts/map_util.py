import folium
from streamlit_folium import st_folium

def display_map(lat, long):
    """Display map centered on the given latitude and longitude with area coverage."""
    map_center = [lat, long]
    m = folium.Map(location=map_center, zoom_start=15)

    # Add a circle to represent the area coverage (without tooltips or popups)
    folium.Circle(
        radius=1000,  # Radius in meters
        location=map_center,
        color='blue',
        fill=True,
        fill_opacity=0.3
    ).add_to(m)

    return st_folium(m, width=700, height=500)
