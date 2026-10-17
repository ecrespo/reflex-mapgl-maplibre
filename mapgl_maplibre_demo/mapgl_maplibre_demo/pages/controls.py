"""Example 2 — Controls."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import MAP_BOX, STYLE_POSITRON, shell


def controls_page() -> rx.Component:
    return shell(
        "Controls",
        "Navigation, geolocate, fullscreen, scale and logo controls placed by "
        "position. Geolocate tracking zooms to the fix accuracy (MapLibre 6.12).",
        mapgl.map(
            mapgl.navigation_control(position="top-right", visualize_pitch=True),
            mapgl.geolocate_control(
                position="top-right",
                track_user_location=True,
                zoom_to_user_accuracy=True,
            ),
            mapgl.fullscreen_control(position="top-right"),
            mapgl.scale_control(position="bottom-left", unit="metric"),
            mapgl.logo_control(position="bottom-right", compact=False),
            initial_view_state={"longitude": 2.35, "latitude": 48.85, "zoom": 11},
            maplibre_logo=False,
            map_style=STYLE_POSITRON,
            style=MAP_BOX,
        ),
    )
