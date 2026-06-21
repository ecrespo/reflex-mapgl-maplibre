# reflex-mapgl-maplibre

Interactive **MapLibre GL JS** maps for [Reflex](https://reflex.dev), in pure
Python. A thin, idiomatic wrapper around
[`react-map-gl`](https://github.com/visgl/react-map-gl) via its
`react-map-gl/maplibre` endpoint — markers, popups, GeoJSON sources & layers,
clustering, heatmaps, controls, feature interaction and imperative camera
control, with **no JavaScript or React required**.

> Status: **early scaffold (Phase 0).** The component API and SDD artifacts are
> in place and the demo app is structured around the upstream examples gallery.
> See [`specs/`](specs/) for the full design.

## Why

Reflex has no built-in map component. `react-map-gl/maplibre` is the standard
React wrapper for MapLibre, but it is unreachable from Python without a wrapper.
This package exposes it as Reflex components and ships a demo app that reproduces
the upstream examples.

## Install

```bash
pip install reflex-mapgl-maplibre
```

It pulls the npm packages `react-map-gl` and `maplibre-gl` into the compiled
frontend automatically, and injects `maplibre-gl/dist/maplibre-gl.css` for you.

## Quickstart

```python
import reflex as rx
import reflex_mapgl_maplibre as mapgl

STYLE = "https://demotiles.maplibre.org/style.json"  # key-less basemap

def index() -> rx.Component:
    return mapgl.map(
        mapgl.navigation_control(position="top-right"),
        mapgl.marker(longitude=-122.4, latitude=37.8, color="#ef4444"),
        initial_view_state={"longitude": -122.4, "latitude": 37.8, "zoom": 11},
        map_style=STYLE,
        style={"width": "100%", "height": "100vh"},
    )

app = rx.App()
app.add_page(index)
```

## Components

| Factory | Wraps | Purpose |
|---|---|---|
| `mapgl.map(...)` | `Map` (default export) | Root map canvas, camera, style, events |
| `mapgl.marker(...)` | `Marker` | DOM marker at a lng/lat |
| `mapgl.popup(...)` | `Popup` | Floating info bubble |
| `mapgl.source(...)` | `Source` | Data source (GeoJSON, tiles, clustering) |
| `mapgl.layer(...)` | `Layer` | Style layer (circle/line/fill/symbol/heatmap/…) |
| `mapgl.navigation_control(...)` | `NavigationControl` | Zoom + compass |
| `mapgl.geolocate_control(...)` | `GeolocateControl` | Find my location |
| `mapgl.fullscreen_control(...)` | `FullscreenControl` | Fullscreen toggle |
| `mapgl.scale_control(...)` | `ScaleControl` | Scale bar |
| `mapgl.attribution_control(...)` | `AttributionControl` | Attribution box |
| `mapgl.map_provider(...)` | `MapProvider` | Multi-map / synced maps |

Optional, heavier overlays live in `reflex_mapgl_maplibre.advanced`
(`deckgl_overlay`, `draw_control`) and pull extra npm dependencies on demand.

Full contract: [`specs/api/component-api-v1.md`](specs/api/component-api-v1.md).

## Imperative camera control

`map(...)` returns an instance whose camera helpers produce event specs you can
attach to any handler. The map needs an `id`:

```python
m = mapgl.map(id="main", initial_view_state={...}, map_style=STYLE)

rx.button("Paris",    on_click=m.fly_to(2.35, 48.85, zoom=11))
rx.button("Fit area", on_click=m.fit_bounds([[-10, 36], [30, 60]], padding=40))
```

`fly_to`, `ease_to`, `jump_to`, `fit_bounds` are forwarded to the MapLibre
`MapRef` (see Technical Design DD-003).

## Examples (demo app)

The `mapgl_maplibre_demo/` app maps the upstream examples gallery to one page
each:

| Page | Example |
|---|---|
| `/` | Basic map |
| `/controls` | Controls |
| `/markers` | Markers & Popups |
| `/geojson` | GeoJSON sources & layers |
| `/clusters` | Clustering |
| `/heatmap` | Heatmap |
| `/interaction` | Click features → Reflex state |
| `/animation` | Viewport animation (`fly_to` / `fit_bounds`) |
| `/side-by-side` | Two maps under a `MapProvider` |

Run it:

```bash
cd mapgl_maplibre_demo
pip install -e ..          # install the local wrapper
reflex init                # if needed
reflex run
```

> Basemaps use key-less styles (MapLibre demotiles, CARTO). For MapTiler styles,
> pass `map_style="https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY"`.

## Project layout

```
reflex-mapgl-maplibre/
├── custom_components/reflex_mapgl_maplibre/   # the wrapper package
│   ├── base.py        # shared base: library, CSS, NoSSR
│   ├── map.py         # Map root + imperative camera helpers
│   ├── markers.py     # Marker, Popup
│   ├── sources.py     # Source, Layer
│   ├── controls.py    # Navigation/Geolocate/Fullscreen/Scale/Attribution
│   ├── provider.py    # MapProvider
│   └── advanced.py    # deck.gl overlay & draw control (optional deps)
├── mapgl_maplibre_demo/                       # demo Reflex app
├── specs/                                     # SDD artifacts (see specs/README.md)
├── tests/                                     # compile/contract tests
└── scripts/create_github_repo.sh
```

## Design docs (SDD)

This project is spec-driven. See [`specs/README.md`](specs/README.md):
PRD · Component API Spec · Technical Design · Phases · Implementation Plan ·
Tasks · Upstream Analysis (examples catalog).

## Compatibility

- Python ≥ 3.10, Reflex ≥ 0.9
- Frontend: `react-map-gl@^8.1.1`, `maplibre-gl@^5`

## License

[MIT](LICENSE). Upstream `react-map-gl` and `maplibre-gl` are MIT-licensed;
this wrapper is published with attribution.

## Credits

- [react-map-gl](https://github.com/visgl/react-map-gl) by vis.gl
- [MapLibre GL JS](https://maplibre.org/)
- Wrapper by Ernesto Crespo
