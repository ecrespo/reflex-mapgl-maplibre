"""Optional, heavyweight overlays kept out of the core package (DD-006).

These wrap local JSX bridges (``deckgl_overlay.jsx``, ``draw_control.jsx``) that
use ``react-map-gl/maplibre``'s ``useControl`` hook. They pull large optional npm
dependencies, so importing this module is opt-in:

    from reflex_mapgl_maplibre.advanced import deckgl_overlay, draw_control

Install the matching extras in your project before using them:

* ``deckgl_overlay`` → ``@deck.gl/mapbox`` (and a deck.gl layers package)
* ``draw_control``   → ``@mapbox/mapbox-gl-draw``
"""

from __future__ import annotations

import reflex as rx
from reflex.components.component import NoSSRComponent

# Copy the local JSX bridges into the compiled frontend's public dir.
_DECK_PATH = rx.asset("./deckgl_overlay.jsx", shared=True)
_DRAW_PATH = rx.asset("./draw_control.jsx", shared=True)

DECK_PKG = "@deck.gl/mapbox@^9.0.0"
DRAW_PKG = "@mapbox/mapbox-gl-draw@^1.4.3"
DRAW_CSS = "@mapbox/mapbox-gl-draw/dist/mapbox-gl-draw.css"


class DeckGLOverlay(NoSSRComponent):
    """deck.gl overlay rendered on top of the map (returns null in the DOM)."""

    library = f"$/public{_DECK_PATH}"
    tag = "DeckGLOverlay"
    is_default = False
    lib_dependencies: list[str] = [DECK_PKG]

    # deck.gl layer instances are constructed in the page module and passed in.
    layers: rx.Var[list]
    get_tooltip: rx.Var


class DrawControl(NoSSRComponent):
    """Polygon/line/point draw control via @mapbox/mapbox-gl-draw."""

    library = f"$/public{_DRAW_PATH}"
    tag = "DrawControl"
    is_default = False
    lib_dependencies: list[str] = [DRAW_PKG]

    position: rx.Var[str]
    display_controls_default: rx.Var[bool]
    controls: rx.Var[dict]
    default_mode: rx.Var[str]

    on_create: rx.EventHandler[rx.event.no_args_event_spec]
    on_update: rx.EventHandler[rx.event.no_args_event_spec]
    on_delete: rx.EventHandler[rx.event.no_args_event_spec]

    def add_imports(self) -> dict:
        """Inject the draw control stylesheet."""
        return {"": DRAW_CSS}


deckgl_overlay = DeckGLOverlay.create
draw_control = DrawControl.create
