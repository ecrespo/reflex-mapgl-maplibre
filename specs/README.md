# Specs — reflex-mapgl-maplibre

Spec-Driven Design (SDD) documents for this project. Specs are the primary
artifact: written and reviewed **before** implementation, and kept in version
control.

## Flow

```
PRD (what) → Component API Spec (contract) → Technical Design (how)
          → Phases → Implementation Plan → Tasks
```

| Document | File | Purpose |
|---|---|---|
| PRD | [prd/reflex-mapgl-maplibre.md](prd/reflex-mapgl-maplibre.md) | What we build, for whom, scope, requirements, risks |
| Component API Spec | [api/component-api-v1.md](api/component-api-v1.md) | Contract of the Python API and mapping to the React components |
| Technical Design | [technical/architecture.md](technical/architecture.md) | Architecture, design decisions (SSR, CSS, imperative refs, events), structure |
| Phases | [plans/phases.md](plans/phases.md) | Delivery phases, entry/exit criteria, examples unlocked |
| Implementation Plan | [plans/implementation-plan.md](plans/implementation-plan.md) | Strategy, dependency graph, work breakdown, milestones |
| Tasks | [plans/tasks.md](plans/tasks.md) | Task list per phase with priorities and traceability |
| Upstream Analysis | [analysis/react-map-gl-upstream.md](analysis/react-map-gl-upstream.md) | Analysis of `visgl/react-map-gl` (`/maplibre`) + examples catalog |

## Notes

- **Data Model:** N/A. This is a UI component library with no persistence, so the
  SDD data-model document does not apply.
- Detail is proportional to risk: a library wrapper (medium feature), hence PRD +
  API + Tech Design + Phases + Plan + Tasks, but no Data Model.
- Upstream is **MIT** (`react-map-gl`, `maplibre-gl`); this package is published
  under **MIT** with attribution.
