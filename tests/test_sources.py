"""Contract tests for ``Source`` and ``Layer`` (API spec §5, §6)."""

import reflex_mapgl_maplibre as mapgl
from reflex_mapgl_maplibre.sources import Layer, Source


def test_source_props():
    props = set(mapgl.source().get_props())
    assert {"id", "type", "data", "url", "tiles", "cluster",
            "cluster_max_zoom", "cluster_radius", "cluster_min_points"} <= props


def test_source_zoom_renames():
    assert Source._rename_props.get("min_zoom") == "minzoom"
    assert Source._rename_props.get("max_zoom") == "maxzoom"


def test_layer_props():
    props = set(mapgl.layer().get_props())
    assert {"id", "type", "source", "source_layer", "paint", "layout",
            "filter", "min_zoom", "max_zoom", "before_id"} <= props


def test_layer_renames():
    renames = Layer._rename_props
    assert renames.get("source_layer") == "source-layer"
    assert renames.get("min_zoom") == "minzoom"
    assert renames.get("max_zoom") == "maxzoom"
    assert renames.get("before_id") == "beforeId"


def test_source_holds_layer_children():
    s = mapgl.source(
        mapgl.layer(id="pts", type="circle"),
        id="src",
        type="geojson",
        data="https://example.com/data.geojson",
    )
    assert len(s.children) == 1
    assert s.children[0].tag == "Layer"


def test_source_raster_dem_props_render_style_spec_names():
    s = mapgl.source(
        id="dem",
        type="raster-dem",
        url="https://example.com/tiles.json",
        tile_size=256,
        encoding="terrarium",
    )
    assert {"tile_size", "encoding", "attribution"} <= set(s.get_props())
    rendered = " ".join(s.render()["props"])
    assert "tileSize:" in rendered
    assert "encoding:" in rendered
