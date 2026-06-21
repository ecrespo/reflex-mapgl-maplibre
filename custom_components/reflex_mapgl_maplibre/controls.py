"""Map control wrappers (named exports of ``react-map-gl/maplibre``).

All controls accept a ``position`` prop:
``"top-left" | "top-right" | "bottom-left" | "bottom-right"``.
"""

from __future__ import annotations

import reflex as rx
from reflex.vars import Var

from .base import MapLibreComponent


class NavigationControl(MapLibreComponent):
    """Zoom in/out buttons and a compass."""

    tag = "NavigationControl"
    is_default = False

    position: Var[str]
    show_compass: Var[bool]
    show_zoom: Var[bool]
    visualize_pitch: Var[bool]


class GeolocateControl(MapLibreComponent):
    """A "find my location" button."""

    tag = "GeolocateControl"
    is_default = False

    position: Var[str]
    track_user_location: Var[bool]
    show_user_location: Var[bool]
    show_accuracy_circle: Var[bool]
    position_options: Var[dict]

    on_geolocate: rx.EventHandler[rx.event.no_args_event_spec]
    on_error: rx.EventHandler[rx.event.no_args_event_spec]


class FullscreenControl(MapLibreComponent):
    """A fullscreen toggle button."""

    tag = "FullscreenControl"
    is_default = False

    position: Var[str]


class ScaleControl(MapLibreComponent):
    """A distance scale bar."""

    tag = "ScaleControl"
    is_default = False

    position: Var[str]
    max_width: Var[int]
    unit: Var[str]  # "metric" | "imperial" | "nautical"


class AttributionControl(MapLibreComponent):
    """An attribution box."""

    tag = "AttributionControl"
    is_default = False

    position: Var[str]
    compact: Var[bool]
    custom_attribution: Var[str | list]


navigation_control = NavigationControl.create
geolocate_control = GeolocateControl.create
fullscreen_control = FullscreenControl.create
scale_control = ScaleControl.create
attribution_control = AttributionControl.create
