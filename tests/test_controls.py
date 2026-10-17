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
        (mapgl.terrain_control, "TerrainControl"),
        (mapgl.globe_control, "GlobeControl"),
        (mapgl.logo_control, "LogoControl"),
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
        mapgl.terrain_control,
        mapgl.globe_control,
        mapgl.logo_control,
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


def test_geolocate_control_maplibre6_props_and_events():
    comp = mapgl.geolocate_control()
    assert {"zoom_to_user_accuracy", "fit_bounds_options"} <= set(comp.get_props())
    assert {
        "on_out_of_max_bounds",
        "on_track_user_location_start",
        "on_track_user_location_end",
    } <= set(comp.get_event_triggers())


def test_terrain_control_props():
    comp = mapgl.terrain_control(source="dem", exaggeration=1.5)
    assert {"source", "exaggeration"} <= set(comp.get_props())


def test_logo_control_compact():
    assert "compact" in set(mapgl.logo_control(compact=True).get_props())
