"""Contract tests for the control wrappers (API spec §7)."""

import pytest
from reflex.vars import Var

import reflex_mapgl_maplibre as mapgl
from reflex_mapgl_maplibre.base import LIBRARY


@pytest.mark.parametrize(
    "factory, tag",
    [
        (mapgl.navigation_control, "NavigationControl"),
        (mapgl.geolocate_control, "GeolocateControl"),
        (mapgl.fullscreen_control, "FullscreenControl"),
        (mapgl.scale_control, "ScaleControl"),
        (mapgl.attribution_control, "AttributionControl"),
    ],
)
def test_control_identity(factory, tag):
    comp = factory()
    assert comp.tag == tag
    assert comp.is_default is False
    assert comp.library == LIBRARY


def test_controls_accept_position():
    for factory in (
        mapgl.navigation_control,
        mapgl.geolocate_control,
        mapgl.fullscreen_control,
        mapgl.scale_control,
        mapgl.attribution_control,
    ):
        comp = factory(position="bottom-right")
        assert "position" in set(comp.get_props())


def test_navigation_control_extra_props():
    props = set(mapgl.navigation_control().get_props())
    assert {"show_compass", "show_zoom", "visualize_pitch"} <= props


def test_scale_control_props():
    props = set(mapgl.scale_control().get_props())
    assert {"max_width", "unit"} <= props


def test_geolocate_control_delivers_coords():
    """API spec §7: on_geolocate must deliver the position `coords` dict."""
    from reflex_mapgl_maplibre.controls import _geolocate_spec

    event = Var(_js_expr="_e").to(dict)
    (coords,) = _geolocate_spec(event)
    assert "coords" in str(coords)
