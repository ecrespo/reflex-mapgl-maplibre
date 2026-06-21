"""Example 4 — GeoJSON sources & layers."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import MAP_BOX, STYLE_DEMO, shell

POINTS = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-122.4, 37.8]}, "properties": {"name": "A"}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [-122.5, 37.75]}, "properties": {"name": "B"}},
    ],
}

POLYGON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[-122.45, 37.78], [-122.42, 37.78], [-122.42, 37.76], [-122.45, 37.76], [-122.45, 37.78]]],
            },
            "properties": {"name": "Area"},
        }
    ],
}


def geojson_page() -> rx.Component:
    return shell(
        "GeoJSON layers",
        "Points (circle layer) plus a polygon fill and outline drawn from GeoJSON.",
        mapgl.map(
            mapgl.source(
                mapgl.layer(
                    id="points",
                    type="circle",
                    paint={"circle-radius": 8, "circle-color": "#007cbf", "circle-stroke-width": 2, "circle-stroke-color": "#fff"},
                ),
                id="points-src",
                type="geojson",
                data=POINTS,
            ),
            mapgl.source(
                mapgl.layer(id="poly-fill", type="fill", paint={"fill-color": "#0a8", "fill-opacity": 0.4}),
                mapgl.layer(id="poly-line", type="line", paint={"line-color": "#0a8", "line-width": 2}),
                id="poly-src",
                type="geojson",
                data=POLYGON,
            ),
            initial_view_state={"longitude": -122.45, "latitude": 37.77, "zoom": 12},
            map_style=STYLE_DEMO,
            style=MAP_BOX,
        ),
    )
