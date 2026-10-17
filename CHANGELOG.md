# Changelog

All notable changes to `reflex-mapgl-maplibre` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres
to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **MapLibre 6 / react-map-gl 8.1.3 surface:**
  - New controls `terrain_control` (`source`, `exaggeration`), `globe_control`
    and `logo_control` (`compact`), exported with their classes.
  - `map` props `min_pitch`, `max_pitch`, `render_world_copies`,
    `style_diffing`, `terrain`, `sky`, `light`, `terrain_skirt_length`,
    `center_clamped_to_ground`, `global_state` (6.14), and `rotate_speed` /
    `pitch_speed` (6.1).
  - `map` camera events `on_drag_start`/`on_drag_end`, `on_zoom_start`/
    `on_zoom_end`, `on_rotate`/`on_rotate_end` and `on_pitch`/`on_pitch_end`
    (all deliver `view_state`).
  - `Map.set_global_state(name, value)` imperative helper
    (`setGlobalStateProperty`), and `fit_bounds(..., absolute_padding=...)` (6.12).
  - `geolocate_control` props `zoom_to_user_accuracy` (6.12) and
    `fit_bounds_options`, and events `on_out_of_max_bounds`,
    `on_track_user_location_start` and `on_track_user_location_end`.
  - `source` props `tile_size`, `encoding` and `attribution` for `raster-dem`
    terrain/hillshade sources.
  - Demo pages `/terrain` (3D terrain, hillshade, sky, terrain control) and
    `/globe` (globe projection, globe/logo controls, global-state magnitude
    filter); the `/controls` page now uses `logo_control` and
    `zoom_to_user_accuracy`.
- Comprehensive TDD contract test suite (58 tests, 100% wrapper coverage):
  `test_base`, `test_map`, `test_markers`, `test_sources`, `test_controls`,
  `test_advanced` and a `test_demo_pages` integration smoke test that builds every
  demo page's component tree.
- `tests` and `custom_components` wired into pytest via `pythonpath` so the suite
  runs without manual `PYTHONPATH`.
- **Packaging as a publishable Reflex custom component (uv):** uv-managed
  environment (`uv.lock`, `[dependency-groups].dev`), generated `.pyi` type stubs
  and a `py.typed` marker shipped in the wheel (PEP 561), expanded PyPI
  classifiers (license, Python 3.10–3.13, GIS topic, `Framework :: Reflex`), and a
  README "Development & publishing" section documenting the `uv` + `reflex
  component build` workflow. `twine check` passes on both artifacts.

### Changed
- **Bumped the frontend engine to MapLibre GL JS 6:** `maplibre-gl` `^5.0.0` →
  `^6.14.0` and `react-map-gl` `^8.1.1` → `^8.1.3` (its `/maplibre` endpoint
  loads MapLibre 6's ESM-only namespace and no longer relies on the removed
  `map.transform`). MapLibre 6 requires WebGL2 and changes some defaults (e.g.
  `zoomLevelsToOverscale`, nested GeoJSON properties); no wrapper prop or
  event was removed upstream, so the Python API is unchanged. The CSS path
  `maplibre-gl/dist/maplibre-gl.css` is unchanged.
- `map` now passes `workerUrl` (new `worker_url` prop, plus `worker_count` and
  `max_parallel_image_requests`) defaulting to Vite's
  `maplibre-gl/dist/maplibre-gl-worker.mjs?worker&url` import, as the MapLibre
  v5→v6 migration guide requires for bundlers.
- Known limitation: `@deck.gl/mapbox` 9.4 still reads `map.transform` when the
  map has terrain or when the overlay is `interleaved`; `deckgl_overlay`'s
  default overlaid mode is unaffected.
- Wrapper modules annotate props with `rx.Var` instead of `from reflex.vars import
  Var`, which removes a duplicate-import lint error from the generated `.pyi`
  stubs (no behavior change).

### Fixed
- MapLibre 6 maps no longer fail with `Worker failed to load` under Reflex's
  Vite dev server: the ESM engine looked for its worker next to Vite's
  pre-bundled `node_modules/.vite/deps` chunk (404), so no tiles were
  rendered. The bundled worker URL fixes both `reflex run` and the production
  export.
- `geolocate_control`'s `on_geolocate` now delivers the position `coords` dict to
  the handler (API spec §7), replacing the previous no-arg event spec.

## [0.1.0] - 2026-06-21

### Added
- Initial scaffold: `Map`, `Marker`, `Popup`, `Source`, `Layer`, the five map
  controls, `MapProvider`, and the optional `advanced` overlays (`deckgl_overlay`,
  `draw_control`).
- Automatic MapLibre CSS injection and client-only (`NoSSRComponent`) rendering.
- Imperative camera helpers (`fly_to`/`ease_to`/`jump_to`/`fit_bounds`) via the
  forwarded `MapRef`.
- Demo app with one page per upstream `react-map-gl` example.
- SDD artifacts under `specs/` and CI (ruff + pytest on Python 3.10–3.13).
