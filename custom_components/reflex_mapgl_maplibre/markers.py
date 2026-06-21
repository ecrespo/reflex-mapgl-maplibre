"""``Marker`` and ``Popup`` wrappers (named exports of ``react-map-gl/maplibre``)."""

from __future__ import annotations

import reflex as rx

from .base import MapLibreComponent


def _lng_lat_spec(event: rx.Var[dict]) -> tuple[rx.Var]:
    """Drag events → ``lng_lat`` dict (event carries ``.lngLat``)."""
    return (event["lngLat"],)


class Marker(MapLibreComponent):
    """A DOM marker pinned to a longitude/latitude.

    Pass children to replace the default pin with custom content.
    """

    tag = "Marker"
    is_default = False

    longitude: rx.Var[float]
    latitude: rx.Var[float]
    color: rx.Var[str]
    anchor: rx.Var[str]
    offset: rx.Var[list]
    rotation: rx.Var[float]
    rotation_alignment: rx.Var[str]
    pitch_alignment: rx.Var[str]
    scale: rx.Var[float]
    draggable: rx.Var[bool]

    on_click: rx.EventHandler[rx.event.no_args_event_spec]
    on_drag: rx.EventHandler[_lng_lat_spec]
    on_drag_start: rx.EventHandler[_lng_lat_spec]
    on_drag_end: rx.EventHandler[_lng_lat_spec]


class Popup(MapLibreComponent):
    """A floating popup pinned to a longitude/latitude. Children are its content."""

    tag = "Popup"
    is_default = False

    longitude: rx.Var[float]
    latitude: rx.Var[float]
    anchor: rx.Var[str]
    offset: rx.Var[int | list]
    close_button: rx.Var[bool]
    close_on_click: rx.Var[bool]
    close_on_move: rx.Var[bool]
    focus_after_open: rx.Var[bool]
    max_width: rx.Var[str]

    on_close: rx.EventHandler[rx.event.no_args_event_spec]
    on_open: rx.EventHandler[rx.event.no_args_event_spec]


marker = Marker.create
popup = Popup.create
