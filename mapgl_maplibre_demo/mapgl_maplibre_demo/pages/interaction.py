"""Example 8 — Interaction (click features → state)."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import EARTHQUAKES, MAP_BOX, STYLE_DARK, DemoState, shell


def interaction_page() -> rx.Component:
    return shell(
        "Interaction",
        "With interactive_layer_ids set, clicks deliver lng_lat and picked features "
        "to Reflex state. Click a point to see its coordinates.",
        rx.text("Last click: ", rx.code(DemoState.hovered), size="3"),
        mapgl.map(
            mapgl.source(
                mapgl.layer(
                    id="quakes",
                    type="circle",
                    paint={"circle-radius": 5, "circle-color": "#f59e0b"},
                ),
                id="quakes-src",
                type="geojson",
                data=EARTHQUAKES,
            ),
            initial_view_state={"longitude": -103.59, "latitude": 40.67, "zoom": 3},
            map_style=STYLE_DARK,
            interactive_layer_ids=["quakes"],
            cursor="pointer",
            on_click=DemoState.on_map_click,
            style=MAP_BOX,
        ),
    )
