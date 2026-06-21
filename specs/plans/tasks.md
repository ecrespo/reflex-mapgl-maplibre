# Tasks — `reflex-mapgl-maplibre`

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |
| **Related** | [phases.md](phases.md) · [implementation-plan.md](implementation-plan.md) |

Status legend: ☐ todo · ◐ in progress · ☑ done. IDs are stable references.
Priority follows the PRD (`MUST`/`SHOULD`/`COULD`).

## Phase 0 — Foundation

| ID | Task | Pri | Status |
|---|---|---|---|
| T0.1 | Init repo, `main` branch, `.gitignore`, MIT `LICENSE` | MUST | ☑ |
| T0.2 | `pyproject.toml` (setuptools, packages=`custom_components`) | MUST | ☑ |
| T0.3 | Write SDD artifacts (PRD, API, architecture, phases, plan, tasks, analysis) | MUST | ☑ |
| T0.4 | `base.py` `MapLibreComponent` (library, CSS, `NoSSRComponent`) | MUST | ☑ |
| T0.5 | Minimal `Map` + public exports + `mapgl` namespace | MUST | ☑ |
| T0.6 | Demo skeleton + basic-map page | MUST | ☑ |
| T0.7 | `README.md` (install, quickstart, examples table) | MUST | ☑ |
| T0.8 | CI workflow (ruff + pytest) | MUST | ☑ |
| T0.9 | `scripts/create_github_repo.sh`; create public GitHub repo & push | MUST | ☑ |

## Phase 1 — Core map & primitives

| ID | Task | Pri | Status |
|---|---|---|---|
| T1.1 | Complete `Map` props (view state, style, projection, limits, cursor) | MUST | ☑ |
| T1.2 | `Map` events (`on_load`, `on_move*`, `on_zoom`) | MUST | ☑ |
| T1.3 | `Marker` (props + `on_click`/`on_drag*`) | MUST | ☑ |
| T1.4 | `Popup` (props + `on_close`/`on_open`) | MUST | ☑ |
| T1.5 | Controls: navigation/geolocate/fullscreen/scale/attribution | MUST | ☑ |
| T1.6 | Demo: controls page; markers & popups page | MUST | ☑ |
| T1.7 | Tests: library/tag/is_default, children render | MUST | ☑ |

## Phase 2 — Data sources & layers

| ID | Task | Pri | Status |
|---|---|---|---|
| T2.1 | `Source` (geojson, cluster, tiles, url) | MUST | ☑ |
| T2.2 | `Layer` (all types; `paint`/`layout`/`filter`; `source-layer` rename) | MUST | ☑ |
| T2.3 | Demo: geojson layers; clusters; heatmap | MUST | ☑ |
| T2.4 | Demo: data-driven styling; 3D fill-extrusion | SHOULD | ☐ |
| T2.5 | Tests: source/layer nesting compiles | MUST | ☑ |

## Phase 3 — Interaction & imperative camera

| ID | Task | Pri | Status |
|---|---|---|---|
| T3.1 | Event specs: `lng_lat`, `features`, `view_state` | SHOULD | ☑ |
| T3.2 | `on_click`/`on_mouse_move` deliver features w/ `interactive_layer_ids` | SHOULD | ☑ |
| T3.3 | Imperative `fly_to`/`ease_to`/`jump_to`/`fit_bounds` via ref + `id` | SHOULD | ☑ |
| T3.4 | Demo: interaction (hover/click); viewport animation; zoom to bounds | SHOULD | ◐ |
| T3.5 | Tests: helpers raise without `id`; event-spec shapes | SHOULD | ☑ |

## Phase 4 — Multi-map & advanced overlays

| ID | Task | Pri | Status |
|---|---|---|---|
| T4.1 | `MapProvider` wrapper | SHOULD | ☑ |
| T4.2 | Demo: side-by-side synced maps | SHOULD | ☑ |
| T4.3 | `advanced.deckgl_overlay` (`@deck.gl/mapbox` via `useControl`) | COULD | ☑ |
| T4.4 | `advanced.draw_control` (`@mapbox/mapbox-gl-draw` via `useControl`) | COULD | ☑ |
| T4.5 | Demo: deck.gl overlay; draw polygon; custom overlay/cursor | COULD | ☐ |

## Phase 5 — Packaging, tests & release

| ID | Task | Pri | Status |
|---|---|---|---|
| T5.1 | Wrapper test coverage > 80% | MUST | ☑ (100%, 58 tests) |
| T5.2 | CI matrix (Python 3.10–3.13) | SHOULD | ☑ |
| T5.3 | `reflex component build` + `uv build` artifacts | MUST | ◐ (wheel builds via `python -m build`) |
| T5.4 | Publish v0.1.0 to PyPI | MUST | ☐ |
| T5.5 | README gallery + CHANGELOG + tag `v0.1.0` | MUST | ◐ (CHANGELOG added) |
| T5.6 | Demo: localization page | COULD | ☐ |

## Traceability (requirement → tasks)

| Requirement | Tasks |
|---|---|
| RF-001 Basic map | T0.4, T0.5, T1.1 |
| RF-002 Camera config | T1.1 |
| RF-003 CSS injection | T0.4 |
| RF-004 Markers/popups | T1.3, T1.4 |
| RF-005 Sources/layers | T2.1, T2.2 |
| RF-006 Controls | T1.5 |
| RF-007 Feature interaction | T3.1, T3.2 |
| RF-008 Imperative camera | T3.3 |
| RF-009 Multi-map | T4.1, T4.2 |
| RF-010 Advanced overlays | T4.3, T4.4 |
| RF-011 Demo & docs | T0.6, T0.7, T1.6, T2.3, T3.4, T5.5 |
