# Reflex MapGL MapLibre

## Product Requirements Document (PRD)

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |
| **Reviewers** | — |
| **Last updated** | 2026-06-21 |

---

## 1. Executive Summary

`reflex-mapgl-maplibre` is a component library for [Reflex](https://reflex.dev)
that wraps [`react-map-gl`](https://github.com/visgl/react-map-gl) through its
`react-map-gl/maplibre` entry point, exposing the [MapLibre GL JS](https://maplibre.org/)
WebGL map engine as idiomatic Reflex components. The goal is to let developers
who build full-stack apps in **pure Python with Reflex** embed interactive maps —
markers, popups, GeoJSON layers, clustering, heatmaps, controls, camera
animation and more — **without writing any JavaScript or React**.

The package exposes a reactive Python API (`mapgl.map(...)`, `mapgl.marker(...)`,
`mapgl.source(...)`, `mapgl.layer(...)`, control components and imperative camera
helpers) plus a **demo Reflex app that reproduces every upstream example**. It is
distributed as a Python package following Reflex's official *Custom Components*
flow.

## 2. Context & Problem

### 2.1 Current situation
Reflex ships layout primitives and `rx.scroll_area` but has **no map component**.
Developers who need an interactive map must hand-wrap a React mapping library,
which requires understanding Reflex's React-wrapping model, SSR handling, CSS
imports, event-payload mapping and imperative refs.

### 2.2 Problem
- There is no mature, MapLibre-based map component for Reflex.
- `react-map-gl/maplibre` is the standard React wrapper for MapLibre, but it is
  inaccessible from Python without a wrapper.
- Wrapping it from scratch has real friction: SSR (`NoSSRComponent`), CSS
  injection, `camelCase` vs `snake_case` props, nested `Source`/`Layer` trees,
  event payloads (`lngLat`, `features`) and imperative camera control via refs.

### 2.3 Opportunity
`react-map-gl` (MIT) offers a clean, declarative, well-documented surface and a
rich examples gallery. Wrapping it once, correctly, gives the whole Reflex
community a map component, plus visibility in the Reflex custom-components gallery
and on PyPI.

## 3. Target Users

### Persona 1: Full-stack Reflex developer
- **Description:** Python developer building dashboards, data apps or landing
  pages in Reflex who does not want to leave Python.
- **Primary need:** Drop an interactive map with markers/layers driven by Reflex
  state.
- **Frequency:** Per-project, recurring day-to-day.
- **Technical level:** Medium/High in Python, Low/Medium in JS/React.

### Persona 2: Geospatial / data-viz developer
- **Description:** Developer visualizing geospatial datasets (GeoJSON, clusters,
  heatmaps) who wants MapLibre power from Python.
- **Primary need:** Data-driven styling, clustering, feature interaction.
- **Technical level:** High in data, Medium in web.

### Persona 3: Library maintainer (open source)
- **Description:** Author/contributor (Ernesto Crespo).
- **Primary need:** Keep the wrapper aligned with upstream, publish to PyPI,
  document.
- **Technical level:** High.

## 4. Goals & Success Metrics

### 4.1 Project (OSS) goals

| Goal | Metric | Target | Horizon |
|---|---|---|---|
| Publish the package | PyPI release | v0.1.0 available | +3 weeks |
| Feature coverage | Upstream examples reproduced in demo | >= 12 of 16 | v0.1.0 |
| Initial adoption | Downloads / stars | 50 downloads/mo, 10 stars | +3 months |
| Quality | Wrapper test coverage | > 80 % | v0.1.0 |
| Upstream alignment | Version lag vs `react-map-gl` | <= 1 minor | Continuous |

### 4.2 User goals

| User goal | Indicator |
|---|---|
| Add a map in < 5 min | `pip install` + ~10 lines renders a map |
| Add markers/layers from Python | Declarative children + state-driven data |
| Animate the camera from Python | `fly_to` / `fit_bounds` from an event handler |
| No JS/CSS needed to start | MapLibre CSS injected automatically |

## 5. Scope

### 5.1 In scope
- [ ] `Map` component wrapping `react-map-gl/maplibre` default export, with view
      state, `map_style`, projection, interactive layer ids, cursor and events.
- [ ] `Marker` and `Popup` components with their props and events.
- [ ] `Source` (GeoJSON + clustering) and `Layer` (circle, line, fill, symbol,
      heatmap, fill-extrusion, raster) components.
- [ ] Controls: `NavigationControl`, `GeolocateControl`, `FullscreenControl`,
      `ScaleControl`, `AttributionControl`.
- [ ] `MapProvider` for multi-map / synced-map scenarios.
- [ ] Imperative camera helpers (`fly_to`, `ease_to`, `jump_to`, `fit_bounds`)
      reachable from Reflex event handlers via the map `id`.
- [ ] Automatic injection of `maplibre-gl/dist/maplibre-gl.css`.
- [ ] Correct SSR handling (client-only rendering).
- [ ] Optional/advanced wrappers behind their own modules: deck.gl overlay
      (`useControl` + `@deck.gl/mapbox`) and draw control (`@mapbox/mapbox-gl-draw`).
- [ ] Demo Reflex app reproducing the upstream examples (one page each).
- [ ] Wrapper tests + CI, README with copy-paste examples.
- [ ] Packaging and PyPI publication.

### 5.2 Out of scope
- Reimplementing MapLibre rendering — the upstream npm packages are reused as-is.
- Maintaining Mapbox (`react-map-gl/mapbox`) wrappers — MapLibre only.
- A bespoke theming system — styling is via MapLibre style JSON + CSS, as upstream.
- Reflex versions < 0.9.x.

### 5.3 Future considerations
- Surface more events (`on_idle`, `on_style_data`) as typed `EventHandler`s.
- High-level helpers (e.g. `geojson_layer(...)`, marker clustering helpers).
- Built-in geocoder control wrapper.
- Vector/raster tile source helpers and PMTiles support.

## 6. Functional Requirements

### RF-001: Render a basic map
- **Description:** Render a MapLibre canvas filling its container from a style URL
  and an initial view state.
- **Actor:** Reflex developer.
- **Preconditions:** Package installed and imported.
- **Main flow:**
  1. Developer calls `mapgl.map(initial_view_state=..., map_style=...)`.
  2. Reflex compiles the `Map` React component (client-only).
  3. MapLibre CSS is injected automatically; the map renders and is interactive.
- **Postconditions:** Map is pannable/zoomable.
- **Priority:** `MUST`

### RF-002: Configure the camera (controlled & uncontrolled)
- **Description:** Accept `initial_view_state` (uncontrolled) and
  `longitude`/`latitude`/`zoom`/`pitch`/`bearing` (controlled) plus limits.
- **Priority:** `MUST`

### RF-003: Inject MapLibre CSS automatically
- **Description:** Inject `maplibre-gl/dist/maplibre-gl.css` so controls/popups
  and canvas sizing work with no manual step.
- **Priority:** `MUST`

### RF-004: Markers and popups
- **Description:** `marker(longitude, latitude, ...)` and `popup(...)` with
  anchor/offset/close options; marker `on_click` and popup `on_close` reach state.
- **Priority:** `MUST`

### RF-005: Sources and layers (data-driven)
- **Description:** `source(type="geojson", data=..., cluster=...)` containing
  `layer(...)` children with `paint`/`layout`/`filter` dictionaries, supporting
  circle/line/fill/symbol/heatmap/fill-extrusion/raster.
- **Priority:** `MUST`

### RF-006: Map controls
- **Description:** Navigation, geolocate, fullscreen, scale and attribution
  controls placed by `position`.
- **Priority:** `MUST`

### RF-007: Feature interaction
- **Description:** With `interactive_layer_ids` set, `on_click`/`on_mouse_move`
  deliver `lng_lat` and picked `features` to Reflex state.
- **Priority:** `SHOULD`

### RF-008: Imperative camera control from state
- **Description:** From an event handler, invoke `fly_to`/`ease_to`/`jump_to`/
  `fit_bounds` against a map identified by `id`.
- **Priority:** `SHOULD`

### RF-009: Multiple / synced maps
- **Description:** `map_provider(...)` enables several maps with `id`s that can be
  synchronized.
- **Priority:** `SHOULD`

### RF-010: Advanced overlays (deck.gl, draw)
- **Description:** Optional modules wrap a deck.gl overlay and a polygon-draw
  control via `useControl`.
- **Priority:** `COULD`

### RF-011: Demo app & documentation
- **Description:** A demo app with one page per upstream example and a README with
  copy-paste snippets.
- **Priority:** `MUST`

## 7. Non-Functional Requirements

### Performance
- Client-only dynamic import; map init must not block first render.
- Reuse maps where possible (`reuse_maps`) to avoid re-instantiation cost.

### Accessibility
- Preserve MapLibre's built-in keyboard navigation and control ARIA; do not
  regress accessibility in the wrapper.

### Compatibility
- Python >= 3.10. Reflex >= 0.9. `react-map-gl >= 8.1`, `maplibre-gl >= 5`
  (provided in the compiled frontend). Must work under Reflex SSR without
  hydration errors.

### Maintainability
- Wrapper test coverage > 80 %. Typed code. Semantic versioning. Pinned npm
  version ranges.

### Observability
- N/A at runtime (UI component). CI with green tests as the merge gate.

## 8. Constraints & Dependencies

### Technical constraints
- The wrapper depends on the public API of `react-map-gl/maplibre` (component
  props, events, and the forwarded `MapRef` methods).
- MapLibre CSS must be imported separately from the JS.
- `as`/reserved-word collisions and `camelCase` mapping handled via `_rename_props`.

### Business constraints
- Licensing: upstream `react-map-gl` and `maplibre-gl` are **MIT**; this package
  is published under **MIT** with attribution to upstream.

### External dependencies

| Dependency | Type | Owner | Status | Risk |
|---|---|---|---|---|
| `react-map-gl` (`/maplibre`) | npm (frontend runtime) | vis.gl | v8.1.1, MIT | Upstream API drift |
| `maplibre-gl` | npm (engine + CSS) | MapLibre org | v5.x, MIT | API drift |
| `@deck.gl/mapbox` | npm (optional overlay) | vis.gl | optional | Heavy, optional |
| `@mapbox/mapbox-gl-draw` | npm (optional draw) | Mapbox | optional, MIT | Optional |
| Reflex | Python framework | Reflex Labs | >= 0.9 | Wrapping API changes |
| PyPI | Package registry | PSF | Active | Low |
| GitHub + gh CLI | Hosting/repos | GitHub | Active | Requires user auth |

## 9. User Stories

### Epic: MapLibre maps in Reflex

**US-001:** As a Reflex developer, I want `mapgl.map(...)` to render a basemap so
I can show a map without writing JS.
- Acceptance: map compiles and renders; CSS auto-loaded.

**US-002:** As a Reflex developer, I want markers and popups so I can annotate
locations.
- Acceptance: clicking a marker opens a popup bound to state.

**US-003:** As a data-viz developer, I want GeoJSON sources/layers and clustering
so I can visualize datasets.
- Acceptance: cluster example renders and expands on click.

**US-004:** As a Reflex developer, I want `fly_to`/`fit_bounds` from an event
handler so I can animate the camera from Python.
- Acceptance: a button flies the camera to a city.

**US-005:** As a package user, I want a demo app and README so I can copy working
examples.
- Acceptance: demo runs; README has a minimal example.

## 10. Wireframes / Mockups
Textual: a full-bleed map canvas with controls top-right; example pages add
markers, colored layers, cluster bubbles, a heat surface, or two side-by-side
maps. Equivalent to the upstream examples gallery.

## 11. Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|---|---|---|---|
| SSR/hydration errors | Medium | High | `NoSSRComponent`; verify with `reflex run` |
| Upstream API drift (v8 minors) | Medium | High | Pin npm ranges; track CHANGELOG; compile tests |
| Imperative ref bridge fragile | Medium | Medium | Use forwarded `MapRef` via `id` + `call_script`; degrade gracefully |
| Heavy optional deps (deck.gl) | Medium | Medium | Isolate in optional modules; not in core deps |
| Style API key requirement | Low | Medium | Default to key-less styles; document MapTiler usage |

## 12. Estimated Timeline

| Phase | Estimate | Deliverable |
|---|---|---|
| Spec & design | 0.5 week | Approved specs (this doc + API + tech design + plan) |
| Core MVP | 1 week | `Map`/`Marker`/`Popup`/`Source`/`Layer`/controls + CSS + demo basics |
| Interaction & camera | 0.5 week | events + imperative helpers + more demo pages |
| Advanced + publish | 0.5 week | deck.gl/draw modules + tests/CI + v0.1.0 on PyPI |

---

## Change History

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | 2026-06-21 | Ernesto Crespo | Initial version |

## Approvals

| Role | Name | Date | Status |
|---|---|---|---|
| Product Owner | Ernesto Crespo | | ☐ Pending |
| Tech Lead | Ernesto Crespo | | ☐ Pending |
