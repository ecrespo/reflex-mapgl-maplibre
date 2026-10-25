# Implementation Plan — `reflex-mapgl-maplibre`

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |
| **Related** | [phases.md](phases.md) · [tasks.md](tasks.md) · ../prd/reflex-mapgl-maplibre.md |

---

## 1. Strategy

Build bottom-up: a shared base component (library + CSS + SSR) first, then the
declarative primitives (`Map`, `Marker`, `Popup`, `Source`, `Layer`, controls),
then interaction and imperative camera control, then multi-map and the optional
heavy overlays, and finally packaging/release. Each phase is demonstrated by one
or more demo pages mapped to the upstream examples gallery.

Detail is proportional to risk: this is a library wrapper (medium feature), so we
ship PRD + API spec + Tech Design + Phases + Plan + Tasks, but no Data Model
(N/A, no persistence).

## 2. Dependency graph

```
base.py ──► map.py ──► markers.py
   │           │           │
   │           ├──► controls.py
   │           └──► sources.py ──► (layers via Layer)
   │
   ├──► provider.py (needs map.py)
   └──► advanced.py (needs map.py + optional npm deps)

demo app ──► depends on the public package exports
tests ──► depend on each wrapper module
CI ──► depends on tests + packaging
```

## 3. Work breakdown by phase

### Phase 0 — Foundation
1. Repo + git `main`, `.gitignore`, MIT `LICENSE`, `pyproject.toml`, `.python-version`.
2. SDD artifacts under `specs/` (PRD, API, architecture, phases, plan, tasks, analysis).
3. `base.py` `MapLibreComponent` (library, CSS via `add_imports`, `NoSSRComponent`).
4. `map.py` minimal `Map` + public exports; `__init__.py` namespace.
5. Demo skeleton (`rxconfig.py`, app, basic-map page), README, CI workflow.
6. `scripts/create_github_repo.sh`; push to GitHub.

### Phase 1 — Core map & primitives
1. Flesh out `Map` props/events (`map.py`).
2. `markers.py`: `Marker` (+ events), `Popup` (+ events).
3. `controls.py`: navigation/geolocate/fullscreen/scale/attribution.
4. Demo pages: controls, markers & popups.

### Phase 2 — Data sources & layers
1. `sources.py`: `Source` (geojson/cluster/tiles) + `Layer` (all types,
   `paint`/`layout`/`filter`, `_rename_props` for `source-layer`).
2. Demo pages: geojson layers, clusters, heatmap, data-driven styling, 3D extrusion.

### Phase 3 — Interaction & imperative camera
1. Event specs for `lng_lat`/`features`/`view_state` (`base.py`/`map.py`).
2. Imperative helpers `fly_to`/`ease_to`/`jump_to`/`fit_bounds` (`map.py`).
3. Demo pages: interaction (hover/click), viewport animation, zoom to bounds.

### Phase 4 — Multi-map & advanced
1. `provider.py`: `MapProvider`; synced side-by-side demo.
2. `advanced.py`: `deckgl_overlay`, `draw_control` (optional `lib_dependencies`).
3. Demo pages: side-by-side, deck.gl overlay, draw polygon, custom overlay.

### Phase 5 — Packaging, tests & release
1. Tests to >80% wrapper coverage; CI matrix.
2. Generate stubs (`reflex_base.utils.pyi_generator`); `uv build`; publish to PyPI.
3. README polish + examples gallery + CHANGELOG; tag v0.1.0.

## 4. Definition of Done (per item)
- Compiles and renders in `reflex run` (no console/hydration errors).
- Props/events match the API spec; reserved words renamed.
- Unit/compile test added and green.
- Documented (docstring + README snippet where user-facing).

## 5. Risks to sequencing
- If `NoSSRComponent` alone is insufficient, add dynamic-import guards (P1 spike).
- If the ref bridge for `fly_to` is fragile, fall back to controlled view state
  (P3); RF-008 is `SHOULD`, so it can slip without blocking v0.1.0.
- deck.gl/draw bundle size or API changes can defer P4 advanced examples; they are
  `COULD` and isolated.

## 6. Milestones

| Milestone | Phase | Exit signal |
|---|---|---|
| M0 Repo live | P0 | GitHub repo + basic-map demo |
| M1 Primitives | P1 | controls/markers/popups demos |
| M2 Data viz | P2 | clusters/heatmap demos |
| M3 Interactive | P3 | animation + feature picking demos |
| M4 Advanced | P4 | synced + deck.gl + draw demos |
| M5 Release | P5 | v0.1.0 on PyPI |
