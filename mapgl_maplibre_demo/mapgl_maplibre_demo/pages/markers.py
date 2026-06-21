"""Example 3 — Markers & Popups."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import MAP_BOX, STYLE_POSITRON, DemoState, shell

CITIES = [
    ("San Francisco", -122.4194, 37.7749),
    ("Oakland", -122.2711, 37.8044),
    ("Berkeley", -122.2730, 37.8715),
]


def markers_page() -> rx.Component:
    markers = [
        mapgl.marker(
            longitude=lng,
            latitude=lat,
            color="#ef4444",
            on_click=DemoState.select_city(name, lng, lat),
        )
        for name, lng, lat in CITIES
    ]
    popup = rx.cond(
        DemoState.popup_open,
        mapgl.popup(
            rx.text(DemoState.selected_name, weight="bold"),
            longitude=DemoState.selected_lng,
            latitude=DemoState.selected_lat,
            anchor="bottom",
            offset=25,
            on_close=DemoState.close_popup,
        ),
    )
    return shell(
        "Markers & Popups",
        "Colored markers; clicking one opens a popup bound to Reflex state.",
        mapgl.map(
            *markers,
            popup,
            initial_view_state={"longitude": -122.32, "latitude": 37.82, "zoom": 10},
            map_style=STYLE_POSITRON,
            style=MAP_BOX,
        ),
    )
