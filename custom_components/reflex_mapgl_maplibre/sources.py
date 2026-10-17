"""``Source`` and ``Layer`` wrappers (named exports of ``react-map-gl/maplibre``).

``Source`` declares data (GeoJSON, vector/raster tiles, image), optionally with
clustering. ``Layer`` declares a MapLibre style layer that draws from a source.
``paint``/``layout``/``filter`` accept MapLibre expressions as plain Python
dicts/lists.
"""

from __future__ import annotations

import reflex as rx


from .base import MapLibreComponent


class Source(MapLibreComponent):
    """A MapLibre data source. Holds ``Layer`` children."""

    tag = "Source"
    is_default = False

    id: rx.Var[str]
    type: rx.Var[str]  # "geojson" | "vector" | "raster" | "raster-dem" | "image" | ...
    data: rx.Var[str | dict]  # GeoJSON URL or object
    url: rx.Var[str]
    tiles: rx.Var[list[str]]
    min_zoom: rx.Var[int]
    max_zoom: rx.Var[int]
    attribution: rx.Var[str]

    # Raster / raster-dem tiles (terrain & hillshade).
    tile_size: rx.Var[int]
    encoding: rx.Var[str]  # "mapbox" | "terrarium" | "custom"

    # Clustering (geojson sources).
    cluster: rx.Var[bool]
    cluster_max_zoom: rx.Var[int]
    cluster_radius: rx.Var[int]
    cluster_min_points: rx.Var[int]

    _rename_props: dict[str, str] = {
        "min_zoom": "minzoom",
        "max_zoom": "maxzoom",
    }


class Layer(MapLibreComponent):
    """A MapLibre style layer (circle, line, fill, symbol, heatmap, ...)."""

    tag = "Layer"
    is_default = False

    id: rx.Var[str]
    type: rx.Var[str]
    source: rx.Var[str]
    source_layer: rx.Var[str]
    paint: rx.Var[dict]
    layout: rx.Var[dict]
    filter: rx.Var[list]
    min_zoom: rx.Var[int]
    max_zoom: rx.Var[int]
    before_id: rx.Var[str]

    _rename_props: dict[str, str] = {
        "source_layer": "source-layer",
        "min_zoom": "minzoom",
        "max_zoom": "maxzoom",
        "before_id": "beforeId",
    }


source = Source.create
layer = Layer.create
