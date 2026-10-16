"""Shared base for all MapLibre wrappers.

Every component in this package renders against the ``react-map-gl/maplibre``
entry point and the browser-only ``maplibre-gl`` engine. Two cross-cutting
concerns are handled here (see ``specs/technical/architecture.md``):

* **DD-002 SSR:** the engine touches ``window``/WebGL, so components are rendered
  client-only by subclassing :class:`~reflex.components.component.NoSSRComponent`.
* **DD-004 CSS:** ``maplibre-gl/dist/maplibre-gl.css`` is injected automatically
  via :meth:`add_imports` (empty import key → side-effect stylesheet import).
"""

from __future__ import annotations

from reflex.components.component import NoSSRComponent

# Pinned npm versions (see specs §"Compatibility & Versioning").
LIBRARY = "react-map-gl/maplibre"
MAPLIBRE_PKG = "maplibre-gl@^6.14.0"
REACT_MAP_GL_PKG = "react-map-gl@^8.1.3"
MAPLIBRE_CSS = "maplibre-gl/dist/maplibre-gl.css"


class MapLibreComponent(NoSSRComponent):
    """Base class for every ``react-map-gl/maplibre`` wrapper.

    Subclasses set ``tag`` (and ``is_default`` for the root ``Map``). The npm
    package ``react-map-gl`` and the engine ``maplibre-gl`` are declared as
    dependencies so Reflex installs them, while the import path stays the
    ``/maplibre`` subpath.
    """

    # Import specifier (the /maplibre subpath export).
    library = LIBRARY

    # Ensure the actual packages land in package.json with pinned versions.
    lib_dependencies: list[str] = [REACT_MAP_GL_PKG, MAPLIBRE_PKG]

    def add_imports(self) -> dict:
        """Inject the MapLibre base stylesheet (DD-004)."""
        return {"": MAPLIBRE_CSS}
