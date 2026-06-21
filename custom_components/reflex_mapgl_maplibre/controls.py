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

    on_geolocate: rx.EventHandler[_geolocate_spec]
    on_error: rx.EventHandler[rx.event.no_args_event_spec]


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


navigation_control = NavigationControl.create
geolocate_control = GeolocateControl.create
fullscreen_control = FullscreenControl.create
scale_control = ScaleControl.create
attribution_control = AttributionControl.create
