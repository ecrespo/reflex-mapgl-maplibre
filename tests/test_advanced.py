"""Contract tests for the optional advanced overlays (API spec §9, DD-006)."""

from reflex.components.component import NoSSRComponent


def test_deckgl_overlay_identity_and_deps():
    from reflex_mapgl_maplibre.advanced import DeckGLOverlay, DECK_PKG

    assert DeckGLOverlay.tag == "DeckGLOverlay"
    assert DeckGLOverlay.is_default is False
    assert issubclass(DeckGLOverlay, NoSSRComponent)
    assert DECK_PKG in DeckGLOverlay.lib_dependencies
    assert {"layers", "get_tooltip"} <= set(DeckGLOverlay().get_props())


def test_draw_control_identity_and_deps():
    from reflex_mapgl_maplibre.advanced import DrawControl, DRAW_PKG

    assert DrawControl.tag == "DrawControl"
    assert DrawControl.is_default is False
    assert issubclass(DrawControl, NoSSRComponent)
    assert DRAW_PKG in DrawControl.lib_dependencies


def test_draw_control_injects_css_and_events():
    from reflex_mapgl_maplibre.advanced import DRAW_CSS, draw_control

    assert draw_control().add_imports()[""] == DRAW_CSS
    triggers = set(draw_control().get_event_triggers())
    assert {"on_create", "on_update", "on_delete"} <= triggers


def test_advanced_not_imported_by_core():
    """DD-006: heavy deps must not leak into the core public namespace."""
    import reflex_mapgl_maplibre as mapgl

    assert not hasattr(mapgl, "deckgl_overlay")
    assert not hasattr(mapgl, "draw_control")
