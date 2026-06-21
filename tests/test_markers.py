"""Contract tests for ``Marker`` and ``Popup`` (API spec §3, §4)."""

from reflex.vars import Var

import reflex_mapgl_maplibre as mapgl
from reflex_mapgl_maplibre.markers import Marker, Popup, _lng_lat_spec


def test_marker_props():
    props = set(mapgl.marker().get_props())
    assert {"longitude", "latitude", "color", "anchor", "offset", "rotation",
            "draggable", "scale"} <= props


def test_marker_drag_events():
    triggers = set(mapgl.marker().get_event_triggers())
    assert {"on_click", "on_drag", "on_drag_start", "on_drag_end"} <= triggers


def test_lng_lat_spec_extracts_lnglat():
    event = Var(_js_expr="_e").to(dict)
    (lng_lat,) = _lng_lat_spec(event)
    assert "lngLat" in str(lng_lat)


def test_marker_renders_children():
    m = mapgl.marker(mapgl.popup(longitude=0, latitude=0))
    assert len(m.children) == 1


def test_popup_props():
    props = set(mapgl.popup().get_props())
    assert {"longitude", "latitude", "anchor", "offset", "close_button",
            "close_on_click", "close_on_move", "max_width"} <= props


def test_popup_events():
    triggers = set(mapgl.popup().get_event_triggers())
    assert {"on_close", "on_open"} <= triggers


def test_identity():
    assert Marker.tag == "Marker" and Marker.is_default is False
    assert Popup.tag == "Popup" and Popup.is_default is False
