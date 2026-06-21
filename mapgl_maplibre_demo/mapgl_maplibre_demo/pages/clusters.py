"""Example 5 — Clusters."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import EARTHQUAKES, MAP_BOX, STYLE_DARK, shell


def clusters_page() -> rx.Component:
    return shell(
        "Clusters",
        "Earthquake points aggregated into sized/colored bubbles with counts.",
        mapgl.map(
            mapgl.source(
                mapgl.layer(
                    id="clusters",
                    type="circle",
                    filter=["has", "point_count"],
                    paint={
                        "circle-color": ["step", ["get", "point_count"], "#51bbd6", 100, "#f1f075", 750, "#f28cb1"],
                        "circle-radius": ["step", ["get", "point_count"], 20, 100, 30, 750, 40],
                    },
                ),
                mapgl.layer(
                    id="cluster-count",
                    type="symbol",
                    filter=["has", "point_count"],
                    layout={"text-field": "{point_count_abbreviated}", "text-size": 12},
                ),
                mapgl.layer(
                    id="unclustered",
                    type="circle",
                    filter=["!", ["has", "point_count"]],
                    paint={"circle-color": "#11b4da", "circle-radius": 6, "circle-stroke-width": 1, "circle-stroke-color": "#fff"},
                ),
                id="earthquakes",
                type="geojson",
                data=EARTHQUAKES,
                cluster=True,
                cluster_max_zoom=14,
                cluster_radius=50,
            ),
            initial_view_state={"longitude": -103.59, "latitude": 40.67, "zoom": 3},
            map_style=STYLE_DARK,
            interactive_layer_ids=["clusters"],
            style=MAP_BOX,
        ),
    )
