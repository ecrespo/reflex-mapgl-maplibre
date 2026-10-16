# reflex-mapgl-maplibre

Interactive **MapLibre GL JS** maps for [Reflex](https://reflex.dev), in pure
Python. A thin, idiomatic wrapper around
[`react-map-gl`](https://github.com/visgl/react-map-gl) via its
`react-map-gl/maplibre` endpoint — markers, popups, GeoJSON sources & layers,
clustering, heatmaps, controls, feature interaction and imperative camera
control, with **no JavaScript or React required**.

> Status: **beta (0.1.0).** Core map, markers/popups, sources/layers, controls,
> multi-map provider and optional deck.gl/draw overlays are implemented, with a
> 58-test contract suite (100% wrapper coverage) and a demo app mapped to the
> upstream examples gallery. See [`specs/`](specs/) for the full design.

## Why

Reflex has no built-in map component. `react-map-gl/maplibre` is the standard
React wrapper for MapLibre, but it is unreachable from Python without a wrapper.
This package exposes it as Reflex components and ships a demo app that reproduces
the upstream examples.

## Install

```bash
uv add reflex-mapgl-maplibre      # or: pip install reflex-mapgl-maplibre
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

> **deck.gl + MapLibre 6:** `deckgl_overlay` uses `MapboxOverlay` in its default
> overlaid mode, which only reads public camera getters. `@deck.gl/mapbox` 9.4 still
> reads the internal `map.transform` (removed in MapLibre 6) when the map has
> 3D terrain or when `interleaved=True`, so avoid those two setups with the overlay
> until deck.gl ships a fix.

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
uv sync                       # create .venv with the wrapper + dev tools
cd mapgl_maplibre_demo
uv run reflex run             # the local wrapper is installed in editable mode
```

> Basemaps use key-less styles (MapLibre demotiles, CARTO). For MapTiler styles,
> pass `map_style="https://api.maptiler.com/maps/streets/style.json?key=YOUR_KEY"`.

## Development & publishing (Reflex custom component, uv)

This repo follows the [Reflex custom-components](https://reflex.dev/docs/custom-components/overview/)
layout (`custom_components/`, a demo app, and a publishable `pyproject.toml`) and
uses **uv** as the package manager.

```bash
# 1. Set up the dev environment (creates .venv, installs the wrapper editable
#    plus the dev group: build, twine, pytest, pytest-cov, ruff).
uv sync

# 2. Quality gates.
uv run ruff check custom_components tests
uv run pytest                      # 58 tests, 100% wrapper coverage

# 3. Build the component (regenerates the .pyi type stubs and the dist/ artifacts:
#    .whl + .tar.gz). `python -m reflex` keeps the repo root importable so the
#    stub generator can resolve `custom_components.*`.
uv run python -m reflex component build

# 4. Validate the distribution metadata for PyPI.
uv run twine check dist/*

# 5. Publish (requires a PyPI account + API token; see prerequisites docs).
uv publish                         # or: uv run twine upload dist/*
#   TestPyPI first:  uv publish --publish-url https://test.pypi.org/legacy/
```

> `reflex component build` produces the same `dist/` artifacts; `uv build` works
> too (both invoke the setuptools backend). The published wheel ships the `.pyi`
> stubs and a `py.typed` marker (PEP 561) for IDE autocomplete.

To list the component on the Reflex gallery after publishing: `reflex component share`.

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
- Frontend: `react-map-gl@^8.1.3`, `maplibre-gl@^6.14.0` (ESM-only, WebGL2 required)

## License

[MIT](LICENSE). Upstream `react-map-gl` and `maplibre-gl` are MIT-licensed;
this wrapper is published with attribution.

## Credits

- [react-map-gl](https://github.com/visgl/react-map-gl) by vis.gl
- [MapLibre GL JS](https://maplibre.org/)
- Wrapper by Ernesto Crespo
