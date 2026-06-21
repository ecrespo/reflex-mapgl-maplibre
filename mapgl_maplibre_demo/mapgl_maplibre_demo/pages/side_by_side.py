"""Example 13 — Side-by-side maps under a MapProvider."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import STYLE_DARK, STYLE_POSITRON, shell

HALF = {"width": "100%", "height": "70vh", "borderRadius": "12px"}


def side_by_side_page() -> rx.Component:
    return shell(
        "Side-by-side",
        "Two maps sharing a MapProvider. Each has its own id so they can be "
        "synchronized via on_move + the imperative camera helpers.",
        mapgl.map_provider(
            rx.grid(
                mapgl.map(
                    id="left-map",
                    initial_view_state={"longitude": -122.4, "latitude": 37.8, "zoom": 9},
                    map_style=STYLE_POSITRON,
                    style=HALF,
                ),
                mapgl.map(
                    id="right-map",
                    initial_view_state={"longitude": -122.4, "latitude": 37.8, "zoom": 9},
                    map_style=STYLE_DARK,
                    style=HALF,
                ),
                columns="2",
                spacing="3",
                width="100%",
            ),
        ),
    )
