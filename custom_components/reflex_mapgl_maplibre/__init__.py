"""reflex-mapgl-maplibre.

Reflex component library wrapping ``react-map-gl`` (``react-map-gl/maplibre``
endpoint) to bring the MapLibre GL JS WebGL map engine to pure-Python Reflex apps.

Public API
----------
>>> import reflex_mapgl_maplibre as mapgl
>>> mapgl.map(
...     mapgl.navigation_control(position="top-right"),
...     mapgl.marker(longitude=-122.4, latitude=37.8, color="#ef4444"),
...     initial_view_state={"longitude": -122.4, "latitude": 37.8, "zoom": 11},
...     map_style="https://demotiles.maplibre.org/style.json",
...     style={"width": "100%", "height": "100vh"},
... )

Advanced (optional, heavy deps) live in ``reflex_mapgl_maplibre.advanced``.
"""

from .controls import (
    AttributionControl,
    FullscreenControl,
    GeolocateControl,
    NavigationControl,
    ScaleControl,
    attribution_control,
    fullscreen_control,
    geolocate_control,
    navigation_control,
    scale_control,
)
from .map import Map, map
from .markers import Marker, Popup, marker, popup
from .provider import MapProvider, map_provider
from .sources import Layer, Source, layer, source

__version__ = "0.1.0"

__all__ = [
    # factories (idiomatic, snake_case)
    "map",
    "marker",
    "popup",
    "source",
    "layer",
    "navigation_control",
    "geolocate_control",
    "fullscreen_control",
    "scale_control",
    "attribution_control",
    "map_provider",
    # classes (for typing / subclassing)
    "Map",
    "Marker",
    "Popup",
    "Source",
    "Layer",
    "NavigationControl",
    "GeolocateControl",
    "FullscreenControl",
    "ScaleControl",
    "AttributionControl",
    "MapProvider",
]
