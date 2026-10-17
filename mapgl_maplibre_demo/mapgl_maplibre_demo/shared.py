"""Shared constants, state and layout shell for the demo pages."""

from __future__ import annotations

import reflex as rx

# Key-less basemap styles (no API token required).
STYLE_DEMO = "https://demotiles.maplibre.org/style.json"
STYLE_POSITRON = "https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
STYLE_DARK = "https://basemaps.cartocdn.com/gl/dark-matter-gl-style/style.json"
STYLE_VOYAGER = "https://basemaps.cartocdn.com/gl/voyager-gl-style/style.json"

# Public earthquake dataset used by the cluster/heatmap demos.
EARTHQUAKES = "https://maplibre.org/maplibre-gl-js/docs/assets/earthquakes.geojson"

# Key-less raster-dem TileJSON (Alps around Innsbruck) for the terrain demo.
TERRAIN_TILES = "https://demotiles.maplibre.org/terrain-tiles/tiles.json"

MAP_BOX = {"width": "100%", "height": "70vh", "borderRadius": "12px"}

# (label, route) for each example page.
EXAMPLES = [
    ("Basic map", "/"),
    ("Controls", "/controls"),
    ("Markers & Popups", "/markers"),
    ("GeoJSON layers", "/geojson"),
    ("Clusters", "/clusters"),
    ("Heatmap", "/heatmap"),
    ("Interaction", "/interaction"),
    ("Viewport animation", "/animation"),
    ("Side-by-side", "/side-by-side"),
    ("3D terrain & sky", "/terrain"),
    ("Globe & global state", "/globe"),
]


class DemoState(rx.State):
    """State shared by the interactive demo pages."""

    # Markers & popups page.
    selected_name: str = ""
    selected_lng: float = 0.0
    selected_lat: float = 0.0
    popup_open: bool = False

    # Interaction page (hovered feature label).
    hovered: str = ""

    @rx.event
    def select_city(self, name: str, lng: float, lat: float):
        self.selected_name = name
        self.selected_lng = lng
        self.selected_lat = lat
        self.popup_open = True

    @rx.event
    def close_popup(self):
        self.popup_open = False

    @rx.event
    def on_map_click(self, lng_lat, features):
        """Receive the (lng_lat, features) payload from the map on_click event."""
        lng = lng_lat.get("lng") if isinstance(lng_lat, dict) else None
        lat = lng_lat.get("lat") if isinstance(lng_lat, dict) else None
        count = len(features) if isinstance(features, list) else 0
        self.hovered = f"lng={lng}, lat={lat}, features={count}"


def shell(title: str, description: str, *content: rx.Component) -> rx.Component:
    """Wrap a demo page with a header and an example navigation bar."""
    nav = rx.hstack(
        *[
            rx.link(
                label,
                href=route,
                padding="0.35rem 0.7rem",
                border_radius="8px",
                background_color=rx.color("gray", 3),
                _hover={"background_color": rx.color("accent", 4)},
                font_size="0.85rem",
            )
            for label, route in EXAMPLES
        ],
        wrap="wrap",
        spacing="2",
        width="100%",
    )
    return rx.container(
        rx.vstack(
            rx.heading("reflex-mapgl-maplibre — demo", size="6"),
            nav,
            rx.divider(),
            rx.heading(title, size="8"),
            rx.text(description, color_scheme="gray", size="4"),
            *content,
            spacing="5",
            width="100%",
        ),
        size="4",
        padding_y="2rem",
    )
