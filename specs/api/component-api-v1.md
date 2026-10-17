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
    terrain_control,
    globe_control,
    logo_control,
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
| `min_pitch` / `max_pitch` | `minPitch` / `maxPitch` | `float` | Defaults 0 / 85 |
| `render_world_copies` | `renderWorldCopies` | `bool` | |
| `projection` | `projection` | `str \| dict` | e.g. `"globe"`, `"mercator"` |
| `style_diffing` | `styleDiffing` | `bool` | Diff style changes (default `true`) |
| `terrain` | `terrain` | `dict` | `{source: <raster-dem id>, exaggeration}`; omit to remove |
| `sky` | `sky` | `dict` | Sky spec (`sky-color`, `atmosphere-blend`, …) |
| `light` | `light` | `dict` | Light spec |
| `terrain_skirt_length` | `terrainSkirtLength` | `str` | `"auto"` \| `"none"` (MapLibre 6, init only) |
| `center_clamped_to_ground` | `centerClampedToGround` | `bool` | Init only |
| `global_state` | `globalState` | `dict` | Initial style global state (MapLibre 6.14, init only) |
| `interactive_layer_ids` | `interactiveLayerIds` | `list[str]` | Layers eligible for picking |
| `cursor` | `cursor` | `str` | CSS cursor |
| `attribution_control` | `attributionControl` | `bool \| dict` | |
| `reuse_maps` | `reuseMaps` | `bool` | Reuse engine instances |
| `maplibre_logo` | `maplibreLogo` | `bool` | Show MapLibre logo |
| `worker_url` | `workerUrl` | `str` | Defaults to the Vite `?worker&url` import of `maplibre-gl-worker.mjs` (MapLibre 6) |
| `worker_count` / `max_parallel_image_requests` | `workerCount` / `maxParallelImageRequests` | `int` | Engine globals |
| `rotate_speed` / `pitch_speed` | `rotateSpeed` / `pitchSpeed` | `float` | Degrees per dragged pixel (MapLibre 6.1, init only) |
| `id` | `id` | `str` | Required for imperative helpers / multi-map |
| `style` | `style` | `dict` | Container CSS (width/height) |

### Events

| Python event | Upstream | Payload to handler |
|---|---|---|
| `on_load` | `onLoad` | `()` |
| `on_move` | `onMove` | `view_state: dict` |
| `on_move_end` | `onMoveEnd` | `view_state: dict` |
| `on_drag_start` / `on_drag_end` | `onDragStart` / `onDragEnd` | `view_state: dict` |
| `on_zoom_start` / `on_zoom` / `on_zoom_end` | `onZoomStart` / `onZoom` / `onZoomEnd` | `view_state: dict` |
| `on_rotate` / `on_rotate_end` | `onRotate` / `onRotateEnd` | `view_state: dict` |
| `on_pitch` / `on_pitch_end` | `onPitch` / `onPitchEnd` | `view_state: dict` |
| `on_click` | `onClick` | `(lng_lat: dict, features: list)` |
| `on_dbl_click` | `onDblClick` | `(lng_lat, features)` |
| `on_mouse_move` | `onMouseMove` | `(lng_lat, features)` |
| `on_mouse_enter` | `onMouseEnter` | `(lng_lat, features)` |
| `on_mouse_leave` | `onMouseLeave` | `()` |
| `on_context_menu` | `onContextMenu` | `(lng_lat, features)`; also on touch long-press (MapLibre 6.11) |
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
| `m.fit_bounds(bounds, padding=40, absolute_padding=None, **opts)` | `MapRef.fitBounds` | `[[w,s],[e,n]]`; `absolute_padding` → `absolutePadding` (MapLibre 6.12) |
| `m.set_global_state(name, value)` | `MapRef.setGlobalStateProperty` | Updates layers reading `["global-state", name]` |

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
| `type` | `type` | `str` (`geojson`,`vector`,`raster`,`raster-dem`,`image`, …) |
| `data` | `data` | `str \| dict` | GeoJSON URL or object |
| `cluster` | `cluster` | `bool` |
| `cluster_max_zoom` | `clusterMaxZoom` | `int` |
| `cluster_radius` | `clusterRadius` | `int` |
| `cluster_min_points` | `clusterMinPoints` | `int` |
| `max_zoom` | `maxzoom` | `int` |
| `tiles` | `tiles` | `list[str]` |
| `url` | `url` | `str` |
| `tile_size` | `tileSize` | `int` | raster / raster-dem |
| `encoding` | `encoding` | `str` | raster-dem: `mapbox`,`terrarium`,`custom` |
| `attribution` | `attribution` | `str` |

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
`scale_control`, `attribution_control`, `terrain_control`, `globe_control` and
`logo_control` wrap the matching named exports.

Common prop: `position` → `position` (`top-left`,`top-right`,`bottom-left`,
`bottom-right`). Extras: navigation `show_compass`/`show_zoom`/`visualize_pitch`;
geolocate `track_user_location`/`show_user_location`/`show_accuracy_circle`/
`position_options`/`fit_bounds_options`/`zoom_to_user_accuracy` (MapLibre 6.12);
scale `max_width`/`unit` (`metric`,`imperial`,`nautical`); terrain `source`
(raster-dem source id)/`exaggeration`; logo `compact`. `globe_control` toggles
the `mercator` ↔ `globe` projection.

`geolocate_control` events: `on_geolocate` / `on_out_of_max_bounds` →
`(coords: dict)`, `on_track_user_location_start` / `on_track_user_location_end`
→ `()`.

## 8. `map_provider`

Wraps `MapProvider`. Place around multiple `map`s (each with a unique `id`) to
enable synchronization. Sync logic is expressed in Reflex via the imperative
helpers reading one map's view state in `on_move` and driving the other.

## 9. Advanced module (`reflex_mapgl_maplibre.advanced`)

- `deckgl_overlay(layers=..., get_tooltip=..., interleaved=False)` — wraps a
  child that mounts a deck.gl `MapboxOverlay` via `useControl`. Requires
  `@deck.gl/mapbox@^9.4.0`. On MapLibre 6 the bridge shims the removed
  `map.transform` (`elevation`, `height`, `_nearZ`, `_farZ`) that deck.gl 9.4
  reads with terrain and in interleaved mode.
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
