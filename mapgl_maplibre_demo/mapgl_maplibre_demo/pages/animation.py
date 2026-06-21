"""Example 9 & 10 — Viewport animation (fly_to) and zoom to bounds (fit_bounds)."""

import reflex as rx
import reflex_mapgl_maplibre as mapgl

from ..shared import MAP_BOX, STYLE_VOYAGER, shell

CITIES = [
    ("Paris", 2.3522, 48.8566, 11),
    ("New York", -74.006, 40.7128, 11),
    ("Tokyo", 139.6917, 35.6895, 11),
]


def animation_page() -> rx.Component:
    # The map needs an id so imperative camera helpers can find its ref.
    m = mapgl.map(
        mapgl.navigation_control(position="top-right"),
        id="anim-map",
        initial_view_state={"longitude": 2.35, "latitude": 48.85, "zoom": 4},
        map_style=STYLE_VOYAGER,
        style=MAP_BOX,
    )
    buttons = rx.hstack(
        *[
            rx.button(name, on_click=m.fly_to(lng, lat, zoom=z))
            for name, lng, lat, z in CITIES
        ],
        rx.button(
            "Fit Europe",
            variant="soft",
            on_click=m.fit_bounds([[-10.0, 36.0], [30.0, 60.0]], padding=40),
        ),
        spacing="3",
        wrap="wrap",
    )
    return shell(
        "Viewport animation",
        "Imperative camera control from Python: fly_to a city or fit_bounds to a box.",
        buttons,
        m,
    )
