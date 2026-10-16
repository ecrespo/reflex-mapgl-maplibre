# Component API Spec — `reflex-mapgl-maplibre` v1

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |
| **Related PRD** | ../prd/reflex-mapgl-maplibre.md |
| **Related Tech Design** | ../technical/architecture.md |

---

This document is the **contract** of the Python API and its mapping to the
`react-map-gl/maplibre` React components. Prop names use Reflex `snake_case`;
Reflex compiles them to the upstream `camelCase`. Reserved words use a trailing
underscore and are renamed via `_rename_props`.

## 1. Public Python API

```python
from reflex_mapgl_maplibre import (
    map as mapgl_map,        # root Map (default export)
    marker,
    popup,
    source,
    layer,
    navigation_control,
    geolocate_control,
    fullscreen_control,
    scale_control,
    attribution_control,
    map_provider,
)
# Advanced (optional) modules:
from reflex_mapgl_maplibre.advanced import deckgl_overlay, draw_control
```

A convenience namespace is also exported:

```python
import reflex_mapgl_maplibre as mapgl
mapgl.map(...)          # mapgl.marker(...), mapgl.layer(...), etc.
```

## 2. `map` (root)

Wraps `react-map-gl/maplibre` **default export** `Map`. Rendered client-only
(`NoSSRComponent`). Injects `maplibre-gl/dist/maplibre-gl.css`.

### Props

| Python prop | Upstream prop | Type | Notes |
|---|---|---|---|
| `initial_view_state` | `initialViewState` | `dict` | `{longitude, latitude, zoom, pitch, bearing}` (uncontrolled) |
| `longitude` | `longitude` | `float` | Controlled camera |
| `latitude` | `latitude` | `float` | Controlled camera |
| `zoom` | `zoom` | `float` | Controlled camera |
| `pitch` | `pitch` | `float` | |
| `bearing` | `bearing` | `float` | |
| `map_style` | `mapStyle` | `str \| dict` | Style URL or style JSON |
| `min_zoom` / `max_zoom` | `minZoom` / `maxZoom` | `float` | |
| `max_bounds` | `maxBounds` | `list` | `[[w,s],[e,n]]` |
| `projection` | `projection` | `str \| dict` | e.g. `"globe"`, `"mercator"` |
| `interactive_layer_ids` | `interactiveLayerIds` | `list[str]` | Layers eligible for picking |
| `cursor` | `cursor` | `str` | CSS cursor |
| `attribution_control` | `attributionControl` | `bool \| dict` | |
| `reuse_maps` | `reuseMaps` | `bool` | Reuse engine instances |
| `maplibre_logo` | `maplibreLogo` | `bool` | Show MapLibre logo |
| `id` | `id` | `str` | Required for imperative helpers / multi-map |
| `style` | `style` | `dict` | Container CSS (width/height) |

### Events

| Python event | Upstream | Payload to handler |
|---|---|---|
| `on_load` | `onLoad` | `()` |
| `on_move` | `onMove` | `view_state: dict` |
| `on_move_end` | `onMoveEnd` | `view_state: dict` |
| `on_zoom` | `onZoom` | `view_state: dict` |
| `on_click` | `onClick` | `(lng_lat: dict, features: list)` |
| `on_dbl_click` | `onDblClick` | `(lng_lat, features)` |
| `on_mouse_move` | `onMouseMove` | `(lng_lat, features)` |
| `on_mouse_enter` | `onMouseEnter` | `(lng_lat, features)` |
| `on_mouse_leave` | `onMouseLeave` | `()` |
| `on_context_menu` | `onContextMenu` | `(lng_lat, features)` |
| `on_error` | `onError` | `()` |

> Mouse-event `features` is only populated for layers listed in
> `interactive_layer_ids`.

### Imperative helpers (camera control)

Methods on a created `map` instance return an `EventSpec` that calls the
forwarded `MapRef` method through `refs["ref_<id>"].current`. They require `id`.

| Method | Calls | Args |
|---|---|---|
| `m.fly_to(longitude, latitude, zoom=None, **opts)` | `MapRef.flyTo` | smooth fly |
| `m.ease_to(longitude, latitude, zoom=None, **opts)` | `MapRef.easeTo` | eased move |
| `m.jump_to(longitude, latitude, zoom=None, **opts)` | `MapRef.jumpTo` | instant |
| `m.fit_bounds(bounds, padding=40, **opts)` | `MapRef.fitBounds` | `[[w,s],[e,n]]` |

```python
m = mapgl.map(id="main", initial_view_state={...}, map_style=STYLE)
rx.button("Paris", on_click=m.fly_to(2.35, 48.85, zoom=11))
```

## 3. `marker`

Wraps named export `Marker`.

| Python prop | Upstream | Type |
|---|---|---|
| `longitude` | `longitude` | `float` (required) |
| `latitude` | `latitude` | `float` (required) |
| `color` | `color` | `str` |
| `anchor` | `anchor` | `str` (`center`,`top`,`bottom`,`left`,`right`, …) |
| `offset` | `offset` | `list[int]` |
| `rotation` | `rotation` | `float` |
| `draggable` | `draggable` | `bool` |
| `scale` | `scale` | `float` |

Events: `on_click` → `()`, `on_drag` / `on_drag_start` / `on_drag_end` →
`(lng_lat: dict)`. Children replace the default pin.

## 4. `popup`

Wraps named export `Popup`.

| Python prop | Upstream | Type |
|---|---|---|
| `longitude` | `longitude` | `float` (required) |
| `latitude` | `latitude` | `float` (required) |
| `anchor` | `anchor` | `str` |
| `offset` | `offset` | `int \| list` |
| `close_button` | `closeButton` | `bool` |
| `close_on_click` | `closeOnClick` | `bool` |
| `close_on_move` | `closeOnMove` | `bool` |
| `max_width` | `maxWidth` | `str` |

Events: `on_close` → `()`, `on_open` → `()`. Children are the popup content.

## 5. `source`

Wraps named export `Source`. Holds `layer` children.

| Python prop | Upstream | Type |
|---|---|---|
| `id` | `id` | `str` |
| `type` | `type` | `str` (`geojson`,`vector`,`raster`,`image`, …) |
| `data` | `data` | `str \| dict` | GeoJSON URL or object |
| `cluster` | `cluster` | `bool` |
| `cluster_max_zoom` | `clusterMaxZoom` | `int` |
| `cluster_radius` | `clusterRadius` | `int` |
| `cluster_min_points` | `clusterMinPoints` | `int` |
| `max_zoom` | `maxzoom` | `int` |
| `tiles` | `tiles` | `list[str]` |
| `url` | `url` | `str` |

## 6. `layer`

Wraps named export `Layer`.

| Python prop | Upstream | Type |
|---|---|---|
| `id` | `id` | `str` |
| `type` | `type` | `str` (`circle`,`line`,`fill`,`symbol`,`heatmap`,`fill-extrusion`,`raster`) |
| `source` | `source` | `str` |
| `source_layer` | `source-layer` | `str` |
| `paint` | `paint` | `dict` (MapLibre expressions allowed) |
| `layout` | `layout` | `dict` |
| `filter` | `filter` | `list` |
| `min_zoom` / `max_zoom` | `minzoom` / `maxzoom` | `int` |
| `before_id` | `beforeId` | `str` |

`source_layer` is renamed to `source-layer` via `_rename_props`.

## 7. Controls

`navigation_control`, `geolocate_control`, `fullscreen_control`,
`scale_control`, `attribution_control` wrap the matching named exports.

Common prop: `position` → `position` (`top-left`,`top-right`,`bottom-left`,
`bottom-right`). Extras: navigation `show_compass`/`show_zoom`/`visualize_pitch`;
geolocate `track_user_location`/`show_user_location`/`position_options`;
scale `max_width`/`unit` (`metric`,`imperial`,`nautical`).

`geolocate_control` event: `on_geolocate` → `(coords: dict)`.

## 8. `map_provider`

Wraps `MapProvider`. Place around multiple `map`s (each with a unique `id`) to
enable synchronization. Sync logic is expressed in Reflex via the imperative
helpers reading one map's view state in `on_move` and driving the other.

## 9. Advanced module (`reflex_mapgl_maplibre.advanced`)

- `deckgl_overlay(layers=..., get_tooltip=...)` — wraps a child that mounts a
  deck.gl `MapboxOverlay` via `useControl`. Requires `@deck.gl/mapbox`.
- `draw_control(position=..., controls=..., on_create=..., on_update=...,
  on_delete=...)` — wraps `@mapbox/mapbox-gl-draw` via `useControl`.

These pull heavy optional npm deps and are **not** imported by the core package.

## 10. Versioning & compatibility

- npm pins: `react-map-gl@^8.1.3`, `maplibre-gl@^6.14.0`.
- Python: `reflex>=0.9`, `python>=3.10`.
- The package version tracks its own SemVer; the upstream npm range is documented
  per release. Breaking upstream prop/event changes bump the wrapper minor.

## 11. Minimal example (contract sanity check)

```python
import reflex as rx
import reflex_mapgl_maplibre as mapgl

STYLE = "https://demotiles.maplibre.org/style.json"

def index() -> rx.Component:
    return mapgl.map(
        mapgl.navigation_control(position="top-right"),
        mapgl.marker(longitude=-122.4, latitude=37.8, color="#ef4444"),
        initial_view_state={"longitude": -122.4, "latitude": 37.8, "zoom": 11},
        map_style=STYLE,
        style={"width": "100%", "height": "100vh"},
    )
```
