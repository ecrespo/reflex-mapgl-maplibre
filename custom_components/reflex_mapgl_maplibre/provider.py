"""``MapProvider`` wrapper for multi-map / synced-map scenarios.

Wrap several ``map(...)`` instances (each with a unique ``id``) in a
``map_provider`` so they can be coordinated. Synchronization is expressed in
Reflex by reading one map's view state in ``on_move`` and driving the other with
the imperative camera helpers (see ``Map.fly_to`` / ``Map.ease_to``).
"""

from __future__ import annotations

from .base import MapLibreComponent


class MapProvider(MapLibreComponent):
    """Context provider sharing map refs across the component tree."""

    tag = "MapProvider"
    is_default = False


map_provider = MapProvider.create
