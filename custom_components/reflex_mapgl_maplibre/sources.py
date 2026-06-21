"""``Source`` and ``Layer`` wrappers (named exports of ``react-map-gl/maplibre``).

``Source`` declares data (GeoJSON, vector/raster tiles, image), optionally with
clustering. ``Layer`` declares a MapLibre style layer that draws from a source.
``paint``/``layout``/``filter`` accept MapLibre expressions as plain Python
dicts/lists.
"""

from __future__ import annotations

from reflex.vars import Var

from .base import MapLibreComponent


class Source(MapLibreComponent):
    """A MapLibre data source. Holds ``Layer`` children."""

    tag = "Source"
    is_default = False

    id: Var[str]
    type: Var[str]  # "geojson" | "vector" | "raster" | "image" | ...
    data: Var[str | dict]  # GeoJSON URL or object
    url: Var[str]
    tiles: Var[list[str]]
    min_zoom: Var[int]
    max_zoom: Var[int]

    # Clustering (geojson sources).
    cluster: Var[bool]
    cluster_max_zoom: Var[int]
    cluster_radius: Var[int]
    cluster_min_points: Var[int]

    _rename_props: dict[str, str] = {
        "min_zoom": "minzoom",
        "max_zoom": "maxzoom",
    }


class Layer(MapLibreComponent):
    """A MapLibre style layer (circle, line, fill, symbol, heatmap, ...)."""

    tag = "Layer"
    is_default = False

    id: Var[str]
    type: Var[str]
    source: Var[str]
    source_layer: Var[str]
    paint: Var[dict]
    layout: Var[dict]
    filter: Var[list]
    min_zoom: Var[int]
    max_zoom: Var[int]
    before_id: Var[str]

    _rename_props: dict[str, str] = {
        "source_layer": "source-layer",
        "min_zoom": "minzoom",
        "max_zoom": "maxzoom",
        "before_id": "beforeId",
    }


source = Source.create
layer = Layer.create
