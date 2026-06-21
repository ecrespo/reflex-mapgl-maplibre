"""Example 1 — Basic map."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import MAP_BOX, STYLE_DEMO, shell


def basic_page() -> rx.Component:
    return shell(
        "Basic map",
        "A pannable, zoomable MapLibre basemap. MapLibre CSS is injected automatically.",
        mapgl.map(
            initial_view_state={"longitude": -122.4, "latitude": 37.8, "zoom": 11},
            map_style=STYLE_DEMO,
            style=MAP_BOX,
        ),
    )
