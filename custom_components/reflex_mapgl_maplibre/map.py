"""Root ``Map`` component and imperative camera helpers.

``Map`` is the **default export** of ``react-map-gl/maplibre`` (hence
``is_default = True``). It controls the camera/view state, the basemap style and
the map-level events, and acts as the parent for ``Marker``/``Popup``/``Source``/
``Layer``/control children.

Imperative camera control (``fly_to``/``ease_to``/``jump_to``/``fit_bounds``)
and the style global-state setter (``set_global_state``) follow DD-003:
``react-map-gl`` forwards a ``MapRef`` exposing the underlying MapLibre methods;
Reflex registers that ref in the global ``refs`` map when the component has an
``id``. From an event handler we reach ``refs["ref_<id>"].current`` and call the
method. Optional chaining makes the call
a no-op before the engine has loaded.
"""

from __future__ import annotations

import json

import reflex as rx
from reflex.event import EventSpec
from reflex.utils.imports import ImportVar
from reflex.vars import VarData

from .base import MAPLIBRE_WORKER, MapLibreComponent

# Vite-bundled worker URL (default ``worker_url``; see ``base`` module docstring).
_WORKER_URL_VAR = rx.Var(
    "maplibreWorkerUrl",
    _var_data=VarData(
        imports={
            MAPLIBRE_WORKER: ImportVar(
                tag="maplibreWorkerUrl", is_default=True, install=False
            )
        }
    ),
).to(str)


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
    min_pitch: rx.Var[float]
    max_pitch: rx.Var[float]
    render_world_copies: rx.Var[bool]
    projection: rx.Var[str | dict]  # "mercator" | "globe" | ProjectionSpecification
    style_diffing: rx.Var[bool]

    # --- 3D: terrain, sky & light (style-spec objects) ----------------- #
    # terrain={"source": "<raster-dem source id>", "exaggeration": 1.5}
    terrain: rx.Var[dict]
    sky: rx.Var[dict]
    light: rx.Var[dict]
    # "auto" hides terrain skirts on transparent backgrounds (MapLibre 6).
    terrain_skirt_length: rx.Var[str]
    center_clamped_to_ground: rx.Var[bool]

    # --- Style global state (read via ["global-state", name]) --------- #
    # Initial values only (MapLibre 6.14 `MapOptions.globalState`); change them
    # at runtime with :meth:`set_global_state`.
    global_state: rx.Var[dict]

    # --- Interaction & chrome ----------------------------------------- #
    interactive_layer_ids: rx.Var[list[str]]
    cursor: rx.Var[str]
    attribution_control: rx.Var[bool | dict]
    reuse_maps: rx.Var[bool]
    maplibre_logo: rx.Var[bool]
    # Degrees of bearing/pitch change per pixel dragged (MapLibre 6.1).
    rotate_speed: rx.Var[float]
    pitch_speed: rx.Var[float]

    # --- Engine globals (applied once, before the first map is created) - #
    # Defaults to the Vite-bundled MapLibre 6 worker; override for a self-hosted
    # worker file (e.g. under a strict CSP).
    worker_url: rx.Var[str]
    worker_count: rx.Var[int]
    max_parallel_image_requests: rx.Var[int]

    # Upstream uses `mapStyle`; Reflex would emit `map_style` → rename it.
    _rename_props: dict[str, str] = {"map_style": "mapStyle"}

    @classmethod
    def create(cls, *children, **props):
        """Default ``worker_url`` and forward sizing to the React ``style`` prop.

        MapLibre 6 cannot locate its worker inside Vite's pre-bundled deps, so
        unless the caller sets ``worker_url`` we pass the ``?worker&url`` import.

        react-map-gl sizes its container from a real React ``style`` prop and
        ignores Reflex's emotion ``css`` prop. If we let Reflex handle ``style=``
        / ``width`` / ``height`` natively (→ ``css``), react-map-gl falls back to
        its default ``height:100%``, which collapses to 0px against an
        auto-height parent — i.e. an invisible map. So we route the requested
        ``style`` dict (and ``width``/``height`` shorthands) through
        ``custom_attrs``, which Reflex emits verbatim as the ``style`` prop.
        """
        props.setdefault("worker_url", _WORKER_URL_VAR)
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
    on_drag_start: rx.EventHandler[_view_state_spec]
    on_drag_end: rx.EventHandler[_view_state_spec]
    on_zoom_start: rx.EventHandler[_view_state_spec]
    on_zoom: rx.EventHandler[_view_state_spec]
    on_zoom_end: rx.EventHandler[_view_state_spec]
    on_rotate: rx.EventHandler[_view_state_spec]
    on_rotate_end: rx.EventHandler[_view_state_spec]
    on_pitch: rx.EventHandler[_view_state_spec]
    on_pitch_end: rx.EventHandler[_view_state_spec]
    on_click: rx.EventHandler[_mouse_spec]
    on_dbl_click: rx.EventHandler[_mouse_spec]
    on_mouse_move: rx.EventHandler[_mouse_spec]
    on_mouse_enter: rx.EventHandler[_mouse_spec]
    on_mouse_leave: rx.EventHandler[rx.event.no_args_event_spec]
    # Also fires on touch long-press since MapLibre 6.11.
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

    def fit_bounds(
        self,
        bounds: list,
        padding: int = 40,
        absolute_padding: bool | None = None,
        **options,
    ) -> EventSpec:
        """Fit the camera to ``[[w, s], [e, n]]`` bounds (``MapRef.fitBounds``).

        ``absolute_padding=True`` (MapLibre 6.12) treats ``padding`` as the map's
        persistent padding instead of adding it to the current one.
        """
        ref = self._require_ref()
        opts = {"padding": padding, **options}
        if absolute_padding is not None:
            opts["absolutePadding"] = absolute_padding
        return rx.call_script(
            f'refs["{ref}"]?.current?.fitBounds({json.dumps(bounds)}, {json.dumps(opts)})'
        )

    def set_global_state(self, name: str, value) -> EventSpec:
        """Set a style global-state property (``Map#setGlobalStateProperty``).

        Layers whose ``paint``/``layout``/``filter`` read ``["global-state", name]``
        re-evaluate without rebuilding the style.
        """
        ref = self._require_ref()
        return rx.call_script(
            f'refs["{ref}"]?.current?.setGlobalStateProperty'
            f"({json.dumps(name)}, {json.dumps(value)})"
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
                "(fly_to/ease_to/jump_to/fit_bounds/set_global_state)."
            )
        return ref


map = Map.create
