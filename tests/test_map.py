"""Contract tests for the root ``Map`` (API spec §2)."""

import pytest
from reflex.vars import Var

import reflex_mapgl_maplibre as mapgl
from reflex_mapgl_maplibre.map import Map, _mouse_spec, _view_state_spec


def _call_script_js(spec) -> str:
    """Extract the literal JS string from a ``rx.call_script`` EventSpec."""
    return spec.args[0][1]._var_value


# --- props ----------------------------------------------------------------- #
def test_map_declares_all_camera_and_style_props():
    props = set(mapgl.map().get_props())
    expected = {
        "initial_view_state",
        "longitude",
        "latitude",
        "zoom",
        "pitch",
        "bearing",
        "map_style",
        "min_zoom",
        "max_zoom",
        "max_bounds",
        "projection",
        "interactive_layer_ids",
        "cursor",
        "attribution_control",
        "reuse_maps",
        "maplibre_logo",
    }
    assert expected <= props


def test_map_style_renamed_to_camelcase():
    assert Map._rename_props.get("map_style") == "mapStyle"


# --- container sizing (react-map-gl reads a real `style` prop, not css) ----- #
def _react_style_props(component) -> list[str]:
    return [p for p in component.render()["props"] if p.startswith("style:")]


def test_style_dict_forwarded_to_react_style_prop():
    """``style=`` must reach react-map-gl as a real ``style`` prop.

    Reflex would otherwise serialize it as the emotion ``css`` prop, which
    react-map-gl ignores — the container then defaults to ``height:100%`` and
    collapses to 0px (an invisible map).
    """
    m = mapgl.map(style={"height": "70vh", "width": "100%"})
    style_props = _react_style_props(m)
    assert style_props, f"no react `style` prop emitted: {m.render()['props']}"
    assert "70vh" in style_props[0]


def test_width_height_shorthand_forwarded_to_react_style_prop():
    m = mapgl.map(width="100%", height="400px")
    style_props = _react_style_props(m)
    assert any("400px" in p for p in style_props), m.render()["props"]


# --- events ---------------------------------------------------------------- #
def test_map_declares_events():
    triggers = set(mapgl.map().get_event_triggers())
    expected = {
        "on_load",
        "on_move",
        "on_move_end",
        "on_zoom",
        "on_click",
        "on_dbl_click",
        "on_mouse_move",
        "on_mouse_enter",
        "on_mouse_leave",
        "on_context_menu",
        "on_error",
    }
    assert expected <= triggers


def test_mouse_spec_extracts_lnglat_and_features():
    event = Var(_js_expr="_e").to(dict)
    lng_lat, features = _mouse_spec(event)
    assert "lngLat" in str(lng_lat)
    assert "features" in str(features)


def test_view_state_spec_extracts_view_state():
    event = Var(_js_expr="_e").to(dict)
    (view_state,) = _view_state_spec(event)
    assert "viewState" in str(view_state)


# --- imperative camera helpers (DD-003) ----------------------------------- #
def test_fly_to_emits_flyto_with_center_and_zoom():
    m = mapgl.map(id="cam")
    js = _call_script_js(m.fly_to(2.35, 48.85, zoom=11))
    assert 'refs["ref_cam"]?.current?.flyTo(' in js
    assert '"center": [2.35, 48.85]' in js
    assert '"zoom": 11' in js


def test_fly_to_without_zoom_omits_zoom():
    m = mapgl.map(id="cam")
    js = _call_script_js(m.fly_to(2.35, 48.85))
    assert "zoom" not in js
    assert '"center": [2.35, 48.85]' in js


@pytest.mark.parametrize(
    "method, js_name",
    [("ease_to", "easeTo"), ("jump_to", "jumpTo")],
)
def test_other_camera_methods(method, js_name):
    m = mapgl.map(id="cam")
    js = _call_script_js(getattr(m, method)(1.0, 2.0, zoom=5))
    assert f"?.current?.{js_name}(" in js


def test_fit_bounds_emits_bounds_and_padding():
    m = mapgl.map(id="cam")
    js = _call_script_js(m.fit_bounds([[-5, 40], [10, 52]], padding=60))
    assert "?.current?.fitBounds(" in js
    assert "[[-5, 40], [10, 52]]" in js
    assert '"padding": 60' in js


def test_imperative_helpers_require_id():
    m = mapgl.map()
    with pytest.raises(ValueError):
        m.fly_to(2.35, 48.85)
    with pytest.raises(ValueError):
        m.fit_bounds([[-5, 40], [10, 52]])
