"""Root ``Map`` component and imperative camera helpers.

``Map`` is the **default export** of ``react-map-gl/maplibre`` (hence
``is_default = True``). It controls the camera/view state, the basemap style and
the map-level events, and acts as the parent for ``Marker``/``Popup``/``Source``/
``Layer``/control children.

Imperative camera control (``fly_to``/``ease_to``/``jump_to``/``fit_bounds``)
follows DD-003: ``react-map-gl`` forwards a ``MapRef`` exposing the underlying
MapLibre methods; Reflex registers that ref in the global ``refs`` map when the
component has an ``id``. From an event handler we reach
``refs["ref_<id>"].current`` and call the method. Optional chaining makes the call
a no-op before the engine has loaded.
"""

from __future__ import annotations

import json

import reflex as rx
from reflex.event import EventSpec

from .base import MapLibreComponent


# --------------------------------------------------------------------------- #
# Event specs — extract only the serializable fields apps need (DD-005).
# --------------------------------------------------------------------------- #
def _view_state_spec(event: rx.Var[dict]) -> tuple[rx.Var]:
    """Map ``onMove``/``onZoom`` → ``view_state`` dict."""
    return (event["viewState"],)


def _mouse_spec(event: rx.Var[dict]) -> tuple[rx.Var, rx.Var]:
    """Map mouse events → ``(lng_lat, features)``."""
    return (event["lngLat"], event["features"])


class Map(MapLibreComponent):
    """Wrapper of the ``react-map-gl/maplibre`` default export ``Map``."""

    tag = "Map"
    is_default = True

    # --- Camera (uncontrolled) ---------------------------------------- #
    initial_view_state: rx.Var[dict]

    # --- Camera (controlled) ------------------------------------------ #
    longitude: rx.Var[float]
    latitude: rx.Var[float]
    zoom: rx.Var[float]
    pitch: rx.Var[float]
    bearing: rx.Var[float]

    # --- Style & limits ----------------------------------------------- #
    map_style: rx.Var[str | dict]
    min_zoom: rx.Var[float]
    max_zoom: rx.Var[float]
    max_bounds: rx.Var[list]
    projection: rx.Var[str | dict]

    # --- Interaction & chrome ----------------------------------------- #
    interactive_layer_ids: rx.Var[list[str]]
    cursor: rx.Var[str]
    attribution_control: rx.Var[bool | dict]
    reuse_maps: rx.Var[bool]
    maplibre_logo: rx.Var[bool]

    # Upstream uses `mapStyle`; Reflex would emit `map_style` → rename it.
    _rename_props: dict[str, str] = {"map_style": "mapStyle"}

    @classmethod
    def create(cls, *children, **props):
        """Forward container sizing to react-map-gl's React ``style`` prop.

        react-map-gl sizes its container from a real React ``style`` prop and
        ignores Reflex's emotion ``css`` prop. If we let Reflex handle ``style=``
        / ``width`` / ``height`` natively (→ ``css``), react-map-gl falls back to
        its default ``height:100%``, which collapses to 0px against an
        auto-height parent — i.e. an invisible map. So we route the requested
        ``style`` dict (and ``width``/``height`` shorthands) through
        ``custom_attrs``, which Reflex emits verbatim as the ``style`` prop.
        """
        style: dict = dict(props.pop("style", None) or {})
        for dim in ("width", "height"):
            if dim in props:
                style[dim] = props.pop(dim)
        if style:
            custom_attrs = dict(props.pop("custom_attrs", None) or {})
            custom_attrs.setdefault("style", style)
            props["custom_attrs"] = custom_attrs
        return super().create(*children, **props)

    # --- Events -------------------------------------------------------- #
    on_load: rx.EventHandler[rx.event.no_args_event_spec]
    on_move: rx.EventHandler[_view_state_spec]
    on_move_start: rx.EventHandler[_view_state_spec]
    on_move_end: rx.EventHandler[_view_state_spec]
    on_zoom: rx.EventHandler[_view_state_spec]
    on_click: rx.EventHandler[_mouse_spec]
    on_dbl_click: rx.EventHandler[_mouse_spec]
    on_mouse_move: rx.EventHandler[_mouse_spec]
    on_mouse_enter: rx.EventHandler[_mouse_spec]
    on_mouse_leave: rx.EventHandler[rx.event.no_args_event_spec]
    on_context_menu: rx.EventHandler[_mouse_spec]
    on_error: rx.EventHandler[rx.event.no_args_event_spec]
    on_idle: rx.EventHandler[rx.event.no_args_event_spec]

    # ------------------------------------------------------------------ #
    # Imperative camera helpers (DD-003). Each returns an EventSpec usable
    # as an on_click handler.
    # ------------------------------------------------------------------ #
    def fly_to(
        self,
        longitude: float,
        latitude: float,
        zoom: float | None = None,
        **options,
    ) -> EventSpec:
        """Smoothly fly the camera to a location (``MapRef.flyTo``)."""
        return self._camera("flyTo", longitude, latitude, zoom, options)

    def ease_to(
        self,
        longitude: float,
        latitude: float,
        zoom: float | None = None,
        **options,
    ) -> EventSpec:
        """Eased move to a location (``MapRef.easeTo``)."""
        return self._camera("easeTo", longitude, latitude, zoom, options)

    def jump_to(
        self,
        longitude: float,
        latitude: float,
        zoom: float | None = None,
        **options,
    ) -> EventSpec:
        """Instantly jump to a location (``MapRef.jumpTo``)."""
        return self._camera("jumpTo", longitude, latitude, zoom, options)

    def fit_bounds(self, bounds: list, padding: int = 40, **options) -> EventSpec:
        """Fit the camera to ``[[w, s], [e, n]]`` bounds (``MapRef.fitBounds``)."""
        ref = self._require_ref()
        opts = {"padding": padding, **options}
        return rx.call_script(
            f'refs["{ref}"]?.current?.fitBounds({json.dumps(bounds)}, {json.dumps(opts)})'
        )

    # -- internals ------------------------------------------------------ #
    def _camera(
        self, method: str, lng: float, lat: float, zoom: float | None, options: dict
    ) -> EventSpec:
        ref = self._require_ref()
        payload: dict = {"center": [lng, lat], **options}
        if zoom is not None:
            payload["zoom"] = zoom
        return rx.call_script(
            f'refs["{ref}"]?.current?.{method}({json.dumps(payload)})'
        )

    def _require_ref(self) -> str:
        ref = self.get_ref()
        if ref is None:
            raise ValueError(
                "map(...) requires an `id` to use imperative camera helpers "
                "(fly_to/ease_to/jump_to/fit_bounds)."
            )
        return ref


map = Map.create
