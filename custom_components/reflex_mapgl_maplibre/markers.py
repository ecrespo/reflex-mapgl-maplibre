"""``Marker`` and ``Popup`` wrappers (named exports of ``react-map-gl/maplibre``)."""

from __future__ import annotations

import reflex as rx
from reflex.vars import Var

from .base import MapLibreComponent


def _lng_lat_spec(event: Var[dict]) -> tuple[Var]:
    """Drag events → ``lng_lat`` dict (event carries ``.lngLat``)."""
    return (event["lngLat"],)


class Marker(MapLibreComponent):
    """A DOM marker pinned to a longitude/latitude.

    Pass children to replace the default pin with custom content.
    """

    tag = "Marker"
    is_default = False

    longitude: Var[float]
    latitude: Var[float]
    color: Var[str]
    anchor: Var[str]
    offset: Var[list]
    rotation: Var[float]
    rotation_alignment: Var[str]
    pitch_alignment: Var[str]
    scale: Var[float]
    draggable: Var[bool]

    on_click: rx.EventHandler[rx.event.no_args_event_spec]
    on_drag: rx.EventHandler[_lng_lat_spec]
    on_drag_start: rx.EventHandler[_lng_lat_spec]
    on_drag_end: rx.EventHandler[_lng_lat_spec]


class Popup(MapLibreComponent):
    """A floating popup pinned to a longitude/latitude. Children are its content."""

    tag = "Popup"
    is_default = False

    longitude: Var[float]
    latitude: Var[float]
    anchor: Var[str]
    offset: Var[int | list]
    close_button: Var[bool]
    close_on_click: Var[bool]
    close_on_move: Var[bool]
    focus_after_open: Var[bool]
    max_width: Var[str]

    on_close: rx.EventHandler[rx.event.no_args_event_spec]
    on_open: rx.EventHandler[rx.event.no_args_event_spec]


marker = Marker.create
popup = Popup.create
