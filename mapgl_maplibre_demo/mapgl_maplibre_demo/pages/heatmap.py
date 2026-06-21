"""Example 6 — Heatmap."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import EARTHQUAKES, MAP_BOX, STYLE_DARK, shell


def heatmap_page() -> rx.Component:
    return shell(
        "Heatmap",
        "A density heat surface that fades into individual points as you zoom in.",
        mapgl.map(
            mapgl.source(
                mapgl.layer(
                    id="quakes-heat",
                    type="heatmap",
                    max_zoom=9,
                    paint={
                        "heatmap-weight": ["interpolate", ["linear"], ["get", "mag"], 0, 0, 6, 1],
                        "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 1, 9, 3],
                        "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 9, 20],
                        "heatmap-opacity": ["interpolate", ["linear"], ["zoom"], 7, 1, 9, 0],
                    },
                ),
                mapgl.layer(
                    id="quakes-point",
                    type="circle",
                    min_zoom=7,
                    paint={
                        "circle-radius": ["interpolate", ["linear"], ["get", "mag"], 1, 4, 6, 14],
                        "circle-color": "#e55e5e",
                        "circle-opacity": ["interpolate", ["linear"], ["zoom"], 7, 0, 8, 1],
                    },
                ),
                id="quakes",
                type="geojson",
                data=EARTHQUAKES,
            ),
            initial_view_state={"longitude": -120, "latitude": 38, "zoom": 4},
            map_style=STYLE_DARK,
            style=MAP_BOX,
        ),
    )
