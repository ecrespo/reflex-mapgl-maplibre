"""Contract tests for the shared base component (DD-002 SSR, DD-004 CSS)."""

from reflex.components.component import NoSSRComponent

import reflex_mapgl_maplibre as mapgl
from reflex_mapgl_maplibre.base import (
    LIBRARY,
    MAPLIBRE_CSS,
    MAPLIBRE_PKG,
    REACT_MAP_GL_PKG,
    MapLibreComponent,
)


def test_base_is_no_ssr():
    """DD-002: map wrappers must render client-only."""
    assert issubclass(MapLibreComponent, NoSSRComponent)


def test_library_is_maplibre_endpoint():
    assert LIBRARY == "react-map-gl/maplibre"


def test_lib_dependencies_pin_npm_packages():
    deps = MapLibreComponent.lib_dependencies
    assert REACT_MAP_GL_PKG in deps
    assert MAPLIBRE_PKG in deps
    assert any(d.startswith("react-map-gl@") for d in deps)
    assert any(d.startswith("maplibre-gl@") for d in deps)


def test_css_injected_as_side_effect_import():
    """DD-004: stylesheet injected under the empty import key."""
    imports = mapgl.map().add_imports()
    assert imports[""] == MAPLIBRE_CSS
    assert MAPLIBRE_CSS.endswith("maplibre-gl.css")
