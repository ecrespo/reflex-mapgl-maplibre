"""Map control wrappers (named exports of ``react-map-gl/maplibre``).

All controls accept a ``position`` prop:
``"top-left" | "top-right" | "bottom-left" | "bottom-right"``.
"""

from __future__ import annotations

import reflex as rx

from .base import MapLibreComponent


def _geolocate_spec(event: rx.Var[dict]) -> tuple[rx.Var]:
    """Map ``onGeolocate`` → ``coords`` dict (event is a ``GeolocationPosition``)."""
    return (event["coords"],)


class NavigationControl(MapLibreComponent):
    """Zoom in/out buttons and a compass."""

    tag = "NavigationControl"
    is_default = False

    position: rx.Var[str]
    show_compass: rx.Var[bool]
    show_zoom: rx.Var[bool]
    visualize_pitch: rx.Var[bool]


class GeolocateControl(MapLibreComponent):
    """A "find my location" button."""

    tag = "GeolocateControl"
    is_default = False

    position: rx.Var[str]
    track_user_location: rx.Var[bool]
    show_user_location: rx.Var[bool]
    show_accuracy_circle: rx.Var[bool]
    position_options: rx.Var[dict]
    fit_bounds_options: rx.Var[dict]
    # Zoom in line with each position's accuracy while tracking (MapLibre 6.12).
    zoom_to_user_accuracy: rx.Var[bool]

    on_geolocate: rx.EventHandler[_geolocate_spec]
    on_error: rx.EventHandler[rx.event.no_args_event_spec]
    on_out_of_max_bounds: rx.EventHandler[_geolocate_spec]
    on_track_user_location_start: rx.EventHandler[rx.event.no_args_event_spec]
    on_track_user_location_end: rx.EventHandler[rx.event.no_args_event_spec]


class FullscreenControl(MapLibreComponent):
    """A fullscreen toggle button."""

    tag = "FullscreenControl"
    is_default = False

    position: rx.Var[str]


class ScaleControl(MapLibreComponent):
    """A distance scale bar."""

    tag = "ScaleControl"
    is_default = False

    position: rx.Var[str]
    max_width: rx.Var[int]
    unit: rx.Var[str]  # "metric" | "imperial" | "nautical"


class AttributionControl(MapLibreComponent):
    """An attribution box."""

    tag = "AttributionControl"
    is_default = False

    position: rx.Var[str]
    compact: rx.Var[bool]
    custom_attribution: rx.Var[str | list]


class TerrainControl(MapLibreComponent):
    """A button toggling 3D terrain from a ``raster-dem`` source."""

    tag = "TerrainControl"
    is_default = False

    position: rx.Var[str]
    source: rx.Var[str]  # id of a raster-dem Source
    exaggeration: rx.Var[float]


class GlobeControl(MapLibreComponent):
    """A button toggling between the ``mercator`` and ``globe`` projections."""

    tag = "GlobeControl"
    is_default = False

    position: rx.Var[str]


class LogoControl(MapLibreComponent):
    """The MapLibre logo watermark as a positionable control."""

    tag = "LogoControl"
    is_default = False

    position: rx.Var[str]
    compact: rx.Var[bool]


navigation_control = NavigationControl.create
geolocate_control = GeolocateControl.create
fullscreen_control = FullscreenControl.create
scale_control = ScaleControl.create
attribution_control = AttributionControl.create
terrain_control = TerrainControl.create
globe_control = GlobeControl.create
logo_control = LogoControl.create
