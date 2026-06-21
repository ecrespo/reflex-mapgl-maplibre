# Changelog

All notable changes to `reflex-mapgl-maplibre` are documented here. The format is
based on [Keep a Changelog](https://keepachangelog.com/) and this project adheres
to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
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
- Wrapper modules annotate props with `rx.Var` instead of `from reflex.vars import
  Var`, which removes a duplicate-import lint error from the generated `.pyi`
  stubs (no behavior change).

### Fixed
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
