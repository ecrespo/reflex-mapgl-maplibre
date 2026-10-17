"""Example 11 — 3D terrain, hillshade and sky (MapLibre 6)."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import MAP_BOX, STYLE_VOYAGER, TERRAIN_TILES, shell

SKY = {
    "sky-color": "#7dbbf0",
    "horizon-color": "#e6f0fa",
    "fog-color": "#ffffff",
    "sky-horizon-blend": 0.5,
    "horizon-fog-blend": 0.6,
    "fog-ground-blend": 0.4,
}


def terrain_page() -> rx.Component:
    return shell(
        "3D terrain & sky",
        "A raster-dem source drives terrain (toggle it with terrain_control) and a "
        "hillshade layer; the sky fills the horizon at high pitch.",
        mapgl.map(
            mapgl.source(
                id="terrain-dem",
                type="raster-dem",
                url=TERRAIN_TILES,
                tile_size=256,
            ),
            mapgl.source(
                mapgl.layer(
                    id="hillshade",
                    type="hillshade",
                    paint={"hillshade-shadow-color": "#473B24"},
                ),
                id="hillshade-dem",
                type="raster-dem",
                url=TERRAIN_TILES,
                tile_size=256,
            ),
            mapgl.navigation_control(position="top-right", visualize_pitch=True),
            mapgl.terrain_control(
                position="top-right", source="terrain-dem", exaggeration=1.5
            ),
            initial_view_state={
                "longitude": 11.39085,
                "latitude": 47.27574,
                "zoom": 12,
                "pitch": 70,
                "bearing": -20,
            },
            terrain={"source": "terrain-dem", "exaggeration": 1.5},
            sky=SKY,
            max_pitch=85,
            terrain_skirt_length="auto",
            map_style=STYLE_VOYAGER,
            style=MAP_BOX,
        ),
    )
