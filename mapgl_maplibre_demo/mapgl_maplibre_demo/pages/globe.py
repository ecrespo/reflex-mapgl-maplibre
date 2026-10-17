"""Example 12 — Globe projection and style global state (MapLibre 6)."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import EARTHQUAKES, MAP_BOX, STYLE_DARK, shell

MAGNITUDES = [0, 3, 4.5, 6]

ATMOSPHERE = {"atmosphere-blend": ["interpolate", ["linear"], ["zoom"], 0, 1, 5, 1, 7, 0]}


def globe_page() -> rx.Component:
    # The map needs an id so set_global_state can find its ref.
    m = mapgl.map(
        mapgl.source(
            mapgl.layer(
                id="quakes",
                type="circle",
                # Re-evaluated in place when the "minMag" global state changes.
                filter=[">=", ["get", "mag"], ["global-state", "minMag"]],
                paint={
                    "circle-radius": ["interpolate", ["linear"], ["get", "mag"], 1, 2, 7, 12],
                    "circle-color": [
                        "interpolate", ["linear"], ["get", "mag"],
                        1, "#facc15", 4, "#f97316", 6, "#dc2626",
                    ],
                    "circle-opacity": 0.75,
                    "circle-stroke-width": 0.5,
                    "circle-stroke-color": "#fff",
                },
            ),
            id="earthquakes",
            type="geojson",
            data=EARTHQUAKES,
        ),
        mapgl.navigation_control(position="top-right"),
        mapgl.globe_control(position="top-right"),
        mapgl.logo_control(position="bottom-left", compact=True),
        id="globe-map",
        initial_view_state={"longitude": -150, "latitude": 30, "zoom": 1.6},
        projection="globe",
        sky=ATMOSPHERE,
        global_state={"minMag": 0},
        maplibre_logo=False,
        map_style=STYLE_DARK,
        style=MAP_BOX,
    )
    buttons = rx.hstack(
        rx.text("Minimum magnitude:", weight="medium"),
        *[
            rx.button(f"≥ {mag}", variant="soft", on_click=m.set_global_state("minMag", mag))
            for mag in MAGNITUDES
        ],
        spacing="3",
        align="center",
        wrap="wrap",
    )
    return shell(
        "Globe & global state",
        "Globe projection with atmosphere, a globe_control toggle and a compact "
        "logo_control. The magnitude filter reads a style global state that "
        "set_global_state updates without rebuilding the layer.",
        buttons,
        m,
    )
