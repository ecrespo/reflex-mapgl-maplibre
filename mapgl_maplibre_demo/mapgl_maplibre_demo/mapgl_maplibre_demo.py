"""Demo app showcasing reflex-mapgl-maplibre — one page per upstream example."""

import reflex as rx

from .pages import (
    animation_page,
    basic_page,
    clusters_page,
    controls_page,
    geojson_page,
    globe_page,
    heatmap_page,
    interaction_page,
    markers_page,
    side_by_side_page,
    terrain_page,
)

app = rx.App()

app.add_page(basic_page, route="/", title="Basic map")
app.add_page(controls_page, route="/controls", title="Controls")
app.add_page(markers_page, route="/markers", title="Markers & Popups")
app.add_page(geojson_page, route="/geojson", title="GeoJSON layers")
app.add_page(clusters_page, route="/clusters", title="Clusters")
app.add_page(heatmap_page, route="/heatmap", title="Heatmap")
app.add_page(interaction_page, route="/interaction", title="Interaction")
app.add_page(animation_page, route="/animation", title="Viewport animation")
app.add_page(side_by_side_page, route="/side-by-side", title="Side-by-side")
app.add_page(terrain_page, route="/terrain", title="3D terrain & sky")
app.add_page(globe_page, route="/globe", title="Globe & global state")
