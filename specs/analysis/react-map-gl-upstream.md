# Upstream Analysis — react-map-gl (`react-map-gl/maplibre`)

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |
| **Upstream repo** | https://github.com/visgl/react-map-gl |
| **Docs** | https://visgl.github.io/react-map-gl |
| **Examples** | https://visgl.github.io/react-map-gl/examples |
| **License** | MIT |

---

## 1. What is react-map-gl?

`react-map-gl` is a suite of React components by the vis.gl / Urban Computing
Foundation team that provides a **fully reactive React API** over the imperative
[MapLibre GL JS](https://maplibre.org/) and [Mapbox GL JS](https://www.mapbox.com/)
WebGL map engines. Instead of manually calling `map.addSource(...)`,
`map.addLayer(...)`, `marker.setLngLat(...)`, the developer declares the desired
map state with JSX and the library reconciles it against the underlying engine.

As of this analysis the latest release is **v8.1.1**. Version 8 split the package
into three entry points so each map engine is typed and bundled independently:

| Entry point | Engine | Notes |
|---|---|---|
| `react-map-gl/mapbox` | `mapbox-gl >= 3.5.0` | Official Mapbox types |
| `react-map-gl/maplibre` | `maplibre-gl >= 4` (supports v5) | **Target of this project** — no Mapbox dependency needed |
| `react-map-gl/mapbox-legacy` | `mapbox-gl` v1.x / v2.x | Backwards compatibility |

A dedicated standalone package, `@vis.gl/react-maplibre`, mirrors the
`react-map-gl/maplibre` endpoint. We wrap the `react-map-gl/maplibre` endpoint
because the user explicitly requested it; `@vis.gl/react-maplibre` is documented
as a drop-in alternative (see architecture DD-001).

## 2. Installation & basic usage (upstream)

```bash
npm install react-map-gl maplibre-gl
```

```jsx
import Map from 'react-map-gl/maplibre';
import 'maplibre-gl/dist/maplibre-gl.css';

<Map
  initialViewState={{ longitude: -122.4, latitude: 37.8, zoom: 14 }}
  style={{ width: 600, height: 400 }}
  mapStyle="https://demotiles.maplibre.org/style.json"
/>
```

Two things are mandatory and drive the wrapper design:

1. **CSS** — `maplibre-gl/dist/maplibre-gl.css` must be imported or controls,
   popups and the canvas size break.
2. **Client-only rendering** — the engine touches `window`/`document` and WebGL,
   so the component is **not SSR-safe** and must be dynamically imported on the
   client (`NoSSRComponent` in Reflex terms).

`mapStyle` requires a style JSON. Free, key-less styles used across the demo:
`https://demotiles.maplibre.org/style.json` and the CARTO basemaps
(`positron`, `dark-matter`, `voyager`). MapTiler styles need an API key.

## 3. Component & hook surface (`react-map-gl/maplibre`)

| Export | Kind | Purpose |
|---|---|---|
| `Map` | **default** export | Root map canvas; controls view state and events |
| `Marker` | named | DOM marker pinned to a lng/lat |
| `Popup` | named | Floating info bubble pinned to a lng/lat |
| `Source` | named | Data source (GeoJSON, vector, raster, image, clustering) |
| `Layer` | named | Style layer (circle, line, fill, symbol, heatmap, fill-extrusion, raster) |
| `NavigationControl` | named | Zoom + compass buttons |
| `GeolocateControl` | named | "Find my location" button |
| `FullscreenControl` | named | Fullscreen toggle |
| `ScaleControl` | named | Distance scale bar |
| `AttributionControl` | named | Attribution box |
| `useControl` | hook | Mount any `IControl` (deck.gl overlay, MapboxDraw, geocoder) |
| `useMap` | hook | Access map instances by `id` from descendants |
| `MapProvider` | provider | Share map refs across the tree (multi-map / sync) |

`Map` ref (`MapRef`) forwards the imperative MapLibre methods — `flyTo`,
`easeTo`, `jumpTo`, `fitBounds`, `getCenter`, `getZoom`, `getSource`, `project`,
`queryRenderedFeatures`, etc. This forwarded ref is the mechanism the Reflex
wrapper uses for imperative camera control (see architecture DD-003).

### Key `Map` props

`initialViewState` (uncontrolled camera), `longitude`/`latitude`/`zoom`/`pitch`/`bearing`
(controlled camera), `mapStyle`, `interactiveLayerIds`, `cursor`, `projection`,
`maxZoom`/`minZoom`, `maxBounds`, `attributionControl`, `reuseMaps`, `maplibreLogo`.

### Key `Map` events

`onLoad`, `onMove`/`onMoveStart`/`onMoveEnd`, `onZoom`, `onClick`, `onDblClick`,
`onMouseMove`, `onMouseEnter`, `onMouseLeave`, `onContextMenu`, `onError`,
`onIdle`, `onStyleData`, `onSourceData`. Mouse events carry `lngLat`, `point`,
and (when `interactiveLayerIds` is set) the picked `features`.

## 4. Examples catalog (what each one renders)

The upstream examples gallery is the de-facto feature checklist. Each row below
maps an upstream example to the feature it exercises and the visual it produces.
These map 1:1 to the demo pages this project ships (see the implementation plan).

| # | Upstream example | What it renders (the "graphic") | Components / APIs exercised |
|---|---|---|---|
| 1 | **Get started / Basic** | A pannable, zoomable basemap filling its container | `Map`, `mapStyle`, `initialViewState` |
| 2 | **Controls** | Navigation, geolocate, fullscreen, scale & attribution widgets on the map | `NavigationControl`, `GeolocateControl`, `FullscreenControl`, `ScaleControl`, `AttributionControl` |
| 3 | **Markers & Popups** | Colored pins at cities; clicking a pin opens a popup card | `Marker`, `Popup`, marker `onClick` |
| 4 | **GeoJSON layers** | Points (circles), a polygon fill and its outline drawn from GeoJSON | `Source` (geojson), `Layer` (circle/fill/line) |
| 5 | **Clusters** | Earthquake points aggregated into sized/colored bubbles with counts; click expands | `Source` clustering, `Layer` (circle/symbol), `interactiveLayerIds`, `easeTo` |
| 6 | **Heatmap** | A density heat surface that fades into individual points as you zoom in | `Source` (geojson), `Layer` (heatmap + circle), zoom interpolation |
| 7 | **GeoJSON / variable-size & data-driven styling** | Features styled by a property (size/color ramps via expressions) | `Layer` paint expressions (`interpolate`, `step`, `get`) |
| 8 | **Interaction (hover / click features)** | Hovering a feature highlights it and shows a tooltip with its properties | `interactiveLayerIds`, `onMouseMove`, `onClick`, feature-state |
| 9 | **Viewport animation** | Camera flies smoothly between cities on button press | `MapRef.flyTo` / controlled view state |
| 10 | **Zoom to bounds** | Camera fits a bounding box around a set of features | `MapRef.fitBounds` |
| 11 | **Draw polygon** | User draws/edits polygons and the live area is computed | `useControl` + `@mapbox/mapbox-gl-draw`, draw events |
| 12 | **deck.gl overlay** | Animated arcs / scatterplot rendered on top of the basemap | `useControl` + `@deck.gl/mapbox` `MapboxOverlay` |
| 13 | **Side-by-side (synced maps)** | Two maps; moving one drives the other | `MapProvider`, `useMap`, multiple `Map` ids |
| 14 | **Custom cursor / custom overlay** | Cursor changes over interactive layers; custom HTML overlay | `cursor` prop, `useControl` custom `IControl` |
| 15 | **Localization / language** | Same map with labels in a chosen language | style `setLayoutProperty('text-field', ...)` |
| 16 | **3D buildings / terrain (MapLibre)** | Extruded buildings / hillshade + sky | `Layer` (fill-extrusion), terrain & sky via style |

### Reflex feasibility per example

- **Pure-declarative examples (1–7, 16)** wrap cleanly: they are just nested
  `Map` / `Source` / `Layer` / control components with prop dictionaries.
- **Imperative-camera examples (9, 10)** are supported through `MapRef`-forwarded
  methods reached from event handlers via `rx.call_script` on the map's `id`.
- **Interaction examples (5, 8)** need event payloads (`lngLat`, `features`)
  surfaced to Reflex state through typed `EventHandler` specs.
- **Third-party-control examples (11, 12)** depend on `useControl` with external
  npm packages (`@mapbox/mapbox-gl-draw`, `@deck.gl/mapbox`). They are scoped as
  optional/advanced wrappers and shipped behind their own modules so the core
  package stays dependency-light.
- **Multi-map example (13)** needs `MapProvider`; the wrapper exposes a provider
  component and per-map `id`s.

## 5. Risks inherited from upstream

| Risk | Notes / mitigation |
|---|---|
| SSR / hydration crashes | Engine is browser-only → wrap as `NoSSRComponent`; verify with `reflex run` |
| CSS not loaded | Always inject `maplibre-gl/dist/maplibre-gl.css` from the component |
| API drift across v8 minors | Pin `react-map-gl@^8.1.1`, `maplibre-gl@^5`; follow CHANGELOG |
| Style key requirement | Default to key-less demotiles/CARTO styles; document MapTiler key usage |
| `interactiveLayerIds` required for picking | Document that click/hover features only arrive for listed layers |

## 6. References

- react-map-gl docs — https://visgl.github.io/react-map-gl/docs
- Upgrade guide (v8 endpoints) — https://visgl.github.io/react-map-gl/docs/upgrade-guide
- Examples gallery — https://visgl.github.io/react-map-gl/examples
- MapLibre GL JS — https://maplibre.org/maplibre-gl-js/docs/
- npm `react-map-gl` — https://www.npmjs.com/package/react-map-gl
- npm `@vis.gl/react-maplibre` — https://www.npmjs.com/package/@vis.gl/react-maplibre
