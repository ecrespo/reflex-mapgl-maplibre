# Reflex MapGL MapLibre — Technical Design Document

## Metadata

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |
| **Related PRD** | ../prd/reflex-mapgl-maplibre.md |
| **Related API Spec** | ../api/component-api-v1.md |
| **Reviewers** | — |

---

## 1. Context

Reflex lets you wrap React components and expose them as Python components by
subclassing `rx.Component`, declaring `library` (npm import specifier), `tag`
(component name) and typed `Var`s for props. On compile, Reflex generates a
React + Vite frontend and translates `snake_case` → `camelCase`.

`react-map-gl` (v8) exposes a dedicated `react-map-gl/maplibre` entry point whose
**default export** is `Map` and whose **named exports** are `Marker`, `Popup`,
`Source`, `Layer`, the control components, plus the `useControl` / `useMap`
hooks and `MapProvider`. The engine, `maplibre-gl`, is browser/WebGL-only and
ships a required stylesheet.

Three technical challenges drive the design: (1) load the MapLibre CSS, (2) avoid
SSR/hydration problems, and (3) translate imperative camera control (`flyTo`,
`fitBounds`) and event payloads (`lngLat`, `features`) into Reflex's model.

The central decision is to **wrap the `react-map-gl/maplibre` React components**
directly — they already handle the MapLibre lifecycle, SSR guards and a forwarded
imperative ref — minimizing the code we maintain.

## 2. Technical Goals

- **Correctness:** Components compile and render without hydration errors; props
  and events map faithfully to upstream.
- **Performance:** Preserve client-only dynamic loading; do not block first paint.
- **Maintainability:** Small, typed wrappers grouped by concern; compile tests;
  pinned npm version ranges.
- **Operability:** Reproducible build/publish with `uv` + `reflex component build`;
  CI with tests.

## 3. Proposed Architecture

### 3.1 High-level diagram

```
┌──────────────────────────┐   compiles   ┌─────────────────────────────────┐
│  Reflex App (Python)      │ ───────────▶ │  React/Vite frontend             │
│  mapgl.map(... children)  │              │  <Map> <Marker/> <Source>...     │
└───────────┬──────────────┘              └───────────────┬─────────────────┘
            │ uses                                          │ imports (client-only)
            ▼                                               ▼
┌──────────────────────────┐  library/tag  ┌─────────────────────────────────┐
│ reflex_mapgl_maplibre     │ ────────────▶ │ react-map-gl/maplibre            │
│  rx.Component wrappers     │ lib_deps      │  + maplibre-gl (+ maplibre css)  │
│  (Map, Marker, Layer, …)   │ ────────────▶ │  [+ deck.gl / mapbox-gl-draw]    │
└──────────────────────────┘               └─────────────────────────────────┘
```

### 3.2 Components

| Component | Technology | Responsibility |
|---|---|---|
| `reflex_mapgl_maplibre` (wrappers) | Python / Reflex `rx.Component` | Declare library/tag/props/events, inject CSS, handle SSR & imperative helpers |
| `react-map-gl/maplibre` | npm / React | Official reactive wrapper over MapLibre |
| `maplibre-gl` | npm / TS + CSS | WebGL engine + base stylesheet |
| `@deck.gl/mapbox`, `@mapbox/mapbox-gl-draw` | npm (optional) | deck.gl overlay & draw control |
| `mapgl_maplibre_demo` | Reflex app | Reproduces upstream examples |
| Packaging | `uv` + setuptools + `reflex component build` | Build & publish |

### 3.3 Module layout (wrapper package)

```
custom_components/reflex_mapgl_maplibre/
├── __init__.py        # public exports + mapgl namespace
├── base.py            # shared MapLibreComponent base (library/css/SSR)
├── map.py             # Map root + imperative helpers
├── markers.py         # Marker, Popup
├── sources.py         # Source, Layer
├── controls.py        # Navigation/Geolocate/Fullscreen/Scale/Attribution
├── provider.py        # MapProvider
└── advanced.py        # deckgl_overlay, draw_control (optional deps)
```

### 3.4 Data flow

**Render + interaction**
```
1. Python: mapgl.map(*children, initial_view_state, map_style, interactive_layer_ids)
2. Reflex compiles to <Map ...> with nested <Source>/<Layer>/<Marker> children
3. Reflex injects `import "maplibre-gl/dist/maplibre-gl.css"`
4. On client, react-map-gl dynamically loads maplibre-gl and creates the engine
5. onClick/onMouseMove → Reflex EventHandler receives {lngLat, features}
```

**Imperative camera (fly_to / fit_bounds)**
```
1. on_click of a button emits an EventSpec running client JS
2. JS reads refs["ref_<map id>"].current (the forwarded MapRef)
3. It calls flyTo/fitBounds → MapLibre animates the camera
```

## 4. Design Decisions

### DD-001: Wrap `react-map-gl/maplibre` (not raw `maplibre-gl`, not Mapbox)

- **Decision:** Wrap the `react-map-gl/maplibre` endpoint.
- **Alternatives:**

| Option | Pros | Cons |
|---|---|---|
| **A. `react-map-gl/maplibre` (chosen)** | Declarative React API; SSR guard + ref handled upstream; matches Reflex model | Extra npm layer; tied to its API |
| B. Wrap raw `maplibre-gl` | No React layer | Must reimplement lifecycle/refs/reconciliation in hooks; large surface |
| C. `@vis.gl/react-maplibre` standalone | Same API, MapLibre-only package | User asked for `react-map-gl/maplibre`; keep as documented alternative |

- **Rationale:** Least code and risk; upstream maintains the hard parts.
- **Consequences:** Wrapper is a thin prop/event translation; versioning follows
  `react-map-gl`.

### DD-002: SSR handling via `NoSSRComponent`

- **Decision:** Base all map wrappers on `NoSSRComponent` so the engine is
  imported and rendered **client-only**.
- **Context:** `maplibre-gl` touches `window`/`document`/WebGL; rendering it on
  the server crashes or causes hydration mismatches.
- **Alternatives:** plain `rx.Component` (risks hydration errors) vs
  `NoSSRComponent` (safe, slight first-paint flash).
- **Rationale:** Safety and correctness outweigh the SSR markup benefit for a
  WebGL canvas.
- **Consequences:** Map shell is not server-rendered; acceptable for a canvas.

### DD-003: Imperative camera control via forwarded `MapRef` + `id`

- **Decision:** Expose `fly_to`/`ease_to`/`jump_to`/`fit_bounds` as methods that
  return an `EventSpec` calling `refs["ref_<id>"]?.current?.<method>(...)`.
- **Context:** `react-map-gl` forwards a `MapRef` exposing the MapLibre methods.
  Reflex registers a component's ref in the global `refs` map when it has an `id`.
- **Alternatives:** controlled view-state via state Vars (more re-renders, no
  smooth animation) vs ref bridge (clean DX, smooth animation).
- **Rationale:** Mirrors the proven approach used in `reflex-blossom-carousel`
  (prev/next). Optional chaining makes calls a no-op before load.
- **Consequences:** Imperative helpers require the map to have an `id`.

### DD-004: Automatic MapLibre CSS injection

- **Decision:** Inject `maplibre-gl/dist/maplibre-gl.css` from the base component
  via `add_imports` (empty key → side-effect CSS import).
- **Rationale:** Guarantees correct rendering with zero manual steps (RF-003).
- **Consequences:** CSS included once per page using the component.

### DD-005: Event payload mapping with custom event specs

- **Decision:** Map upstream events to Reflex `EventHandler`s using custom event
  specs that extract `event.lngLat` and `event.features` into serializable dicts/
  lists; view events extract `event.viewState`.
- **Rationale:** Upstream event objects are not directly serializable; we forward
  only the fields apps need (RF-007).
- **Consequences:** A small JS event-spec function per payload shape.

### DD-006: Optional heavy deps isolated in `advanced.py`

- **Decision:** Keep deck.gl and mapbox-gl-draw wrappers in a separate module
  with their own `lib_dependencies`; never import them from the core package.
- **Rationale:** Core stays light; users opt in to large bundles.
- **Consequences:** Advanced examples require the extra npm packages (documented).

### DD-007: Packaging with `uv` over the `reflex component` scaffold

- **Decision:** Use the standard `custom_components/` publishable layout and a
  demo app, manage env/deps/lock with `uv`, keep the setuptools `pyproject.toml`.
- **Rationale:** Combines the gallery-ready layout with reproducible tooling.

## 5. Compatibility & Versioning

- npm: `react-map-gl@^8.1.3`, `maplibre-gl@^6.14.0`; optional `@deck.gl/mapbox`,
  `@mapbox/mapbox-gl-draw`.
- Python: `reflex>=0.9`, `python>=3.10`.
- SemVer on the package; upstream npm range documented per release; breaking
  upstream prop/event changes bump the wrapper minor.

## 6. Testing & CI

- Unit/compile tests assert each wrapper sets the right `library`/`tag`/
  `is_default`, renders children, and that imperative helpers raise without `id`.
- `reflex run` smoke test of the demo app (manual / CI with a headless build).
- GitHub Actions: lint (ruff) + pytest on push/PR.

## 7. Data Model

N/A — this is a UI component library with no persistence. The SDD data-model
artifact does not apply (detail proportional to risk).
