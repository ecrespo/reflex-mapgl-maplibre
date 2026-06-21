"""Integration smoke test: every demo page builds a valid component tree.

This exercises the wrappers exactly as an app uses them (nested Map/Source/Layer/
Marker/controls + event handlers), catching contract regressions a unit test of a
single wrapper would miss.
"""

import sys
from pathlib import Path

import pytest
import reflex as rx

# Put the demo Reflex project on the path so its package is importable.
_DEMO_ROOT = Path(__file__).resolve().parent.parent / "mapgl_maplibre_demo"
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))


@pytest.fixture(scope="module")
def page_builders():
    from mapgl_maplibre_demo import pages

    return {name: getattr(pages, name) for name in pages.__all__}


def test_all_pages_exported(page_builders):
    assert len(page_builders) == 9


def test_each_page_builds_a_component(page_builders):
    for name, builder in page_builders.items():
        component = builder()
        assert isinstance(component, rx.Component), f"{name} did not return a Component"
