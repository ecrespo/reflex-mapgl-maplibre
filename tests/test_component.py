"""Compile/contract tests for the reflex-mapgl-maplibre wrappers.

These do not boot a browser; they assert the wrappers declare the correct
library/tag/export shape, render children, and that imperative helpers enforce
the ``id`` requirement (see specs/api/component-api-v1.md).
"""

import pytest

import reflex_mapgl_maplibre as mapgl
from reflex_mapgl_maplibre.base import LIBRARY


def test_map_is_default_export():
    m = mapgl.map(initial_view_state={"longitude": 0, "latitude": 0, "zoom": 1})
    assert m.tag == "Map"
    assert m.is_default is True
    assert m.library == LIBRARY


@pytest.mark.parametrize(
    "factory, tag",
    [
        (mapgl.marker, "Marker"),
        (mapgl.popup, "Popup"),
        (mapgl.source, "Source"),
        (mapgl.layer, "Layer"),
        (mapgl.navigation_control, "NavigationControl"),
        (mapgl.geolocate_control, "GeolocateControl"),
        (mapgl.fullscreen_control, "FullscreenControl"),
        (mapgl.scale_control, "ScaleControl"),
        (mapgl.attribution_control, "AttributionControl"),
        (mapgl.map_provider, "MapProvider"),
    ],
)
def test_named_exports(factory, tag):
    comp = factory()
    assert comp.tag == tag
    assert comp.is_default is False
    assert comp.library == LIBRARY


def test_map_renders_children():
    m = mapgl.map(
        mapgl.navigation_control(position="top-right"),
        mapgl.marker(longitude=-122.4, latitude=37.8),
        id="main",
        map_style="https://demotiles.maplibre.org/style.json",
    )
    assert len(m.children) == 2


def test_layer_renames_source_layer():
    assert Layer_rename().get("source_layer") == "source-layer"


def Layer_rename():
    from reflex_mapgl_maplibre.sources import Layer

    return Layer._rename_props


def test_map_style_renamed():
    from reflex_mapgl_maplibre.map import Map

    assert Map._rename_props.get("map_style") == "mapStyle"


def test_imperative_helpers_require_id():
    m = mapgl.map(map_style="https://demotiles.maplibre.org/style.json")
    with pytest.raises(ValueError):
        m.fly_to(2.35, 48.85, zoom=11)
    with pytest.raises(ValueError):
        m.fit_bounds([[-5, 40], [10, 52]])


def test_imperative_helpers_with_id_return_eventspec():
    m = mapgl.map(id="cam", map_style="https://demotiles.maplibre.org/style.json")
    # Should not raise; returns an event spec object.
    assert m.fly_to(2.35, 48.85, zoom=11) is not None
    assert m.fit_bounds([[-5, 40], [10, 52]]) is not None
