# Phases — `reflex-mapgl-maplibre`

| Field | Value |
|---|---|
| **Author** | Ernesto Crespo |
| **Status** | `DRAFT` |
| **Version** | 1.0 |
| **Date** | 2026-06-21 |

This document defines the delivery **phases**. Each phase has an objective, the
requirements it satisfies (see PRD), entry/exit criteria and the demo examples it
unlocks. Tasks per phase live in [tasks.md](tasks.md); sequencing in
[implementation-plan.md](implementation-plan.md).

```
P0 Foundation → P1 Core map → P2 Data layers → P3 Interaction & camera
             → P4 Multi-map & advanced → P5 Packaging & release
```

## Phase 0 — Foundation (this scaffold)
- **Objective:** Repo, SDD artifacts, package skeleton, base component, demo
  skeleton, README, LICENSE, CI config, git `main`.
- **Requirements:** project setup; RF-011 (docs base).
- **Entry:** approved specs.
- **Exit:** repo builds importable package; `index` demo page renders a basic map;
  pushed to GitHub.
- **Examples unlocked:** #1 Basic map.

## Phase 1 — Core map & primitives
- **Objective:** Production-ready `Map`, `Marker`, `Popup` and all controls;
  automatic CSS; SSR-safe.
- **Requirements:** RF-001, RF-002, RF-003, RF-004, RF-006.
- **Entry:** P0 done.
- **Exit:** controls, markers and popups work in the demo; no hydration errors.
- **Examples unlocked:** #2 Controls, #3 Markers & Popups.

## Phase 2 — Data sources & layers
- **Objective:** `Source` (incl. clustering) + `Layer` for all common types;
  data-driven styling with expressions.
- **Requirements:** RF-005.
- **Entry:** P1 done.
- **Exit:** GeoJSON, cluster and heatmap demos render correctly.
- **Examples unlocked:** #4 GeoJSON layers, #5 Clusters, #6 Heatmap, #7 Data-driven styling, #16 3D / extrusion.

## Phase 3 — Interaction & imperative camera
- **Objective:** Event payloads (`lng_lat`, `features`) to state; imperative
  `fly_to`/`ease_to`/`jump_to`/`fit_bounds`.
- **Requirements:** RF-007, RF-008.
- **Entry:** P2 done.
- **Exit:** hover/click feature demos and camera-animation demos work.
- **Examples unlocked:** #8 Interaction, #9 Viewport animation, #10 Zoom to bounds.

## Phase 4 — Multi-map & advanced overlays
- **Objective:** `MapProvider` synced maps; optional deck.gl overlay and draw
  control modules.
- **Requirements:** RF-009, RF-010.
- **Entry:** P3 done.
- **Exit:** side-by-side demo syncs; deck.gl and draw demos work with optional deps.
- **Examples unlocked:** #11 Draw polygon, #12 deck.gl overlay, #13 Side-by-side, #14 Custom overlay/cursor.

## Phase 5 — Packaging, tests & release
- **Objective:** >80% wrapper coverage, CI green, build & publish to PyPI, polished
  README and docs.
- **Requirements:** all NFRs; RF-011.
- **Entry:** P1–P4 features complete.
- **Exit:** v0.1.0 on PyPI; README and examples gallery complete.
- **Examples unlocked:** #15 Localization + full gallery.

## Phase gate checklist (every phase)
- [ ] Code compiles; demo page(s) render in `reflex run`.
- [ ] Tests added and green.
- [ ] Specs updated if the contract changed.
- [ ] README example added for the new capability.
