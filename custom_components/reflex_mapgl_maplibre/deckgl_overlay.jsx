// Local React component bridging deck.gl into react-map-gl/maplibre via the
// `useControl` hook (see specs/technical/architecture.md DD-006).
// Requires the optional npm dependency `@deck.gl/mapbox`.
import { useControl } from "react-map-gl/maplibre";
import { MapboxOverlay } from "@deck.gl/mapbox";

// MapLibre 6 removed the internal `map.transform`, but `@deck.gl/mapbox` 9.4
// still reads `transform.elevation` (terrain) and `transform.height` /
// `_nearZ` / `_farZ` (interleaved viewport). Re-expose exactly those fields,
// backed by the public API where one exists. No-op on MapLibre <= 5.
export function ensureDeckTransformShim(map) {
  if (!map || "transform" in map) return map;
  const shim = {
    get elevation() {
      return map.getCenterElevation();
    },
    get height() {
      return map._camera?.transform?.height ?? map.getCanvas().clientHeight;
    },
    get _nearZ() {
      return map._camera?.transform?.nearZ;
    },
    get _farZ() {
      return map._camera?.transform?.farZ;
    },
  };
  Object.defineProperty(map, "transform", { value: shim, configurable: true });
  return map;
}

export function DeckGLOverlay(props) {
  const overlay = useControl(({ map }) => {
    // `map` is react-map-gl's MapRef; deck.gl works on the engine instance.
    ensureDeckTransformShim(map.getMap());
    return new MapboxOverlay(props);
  });
  overlay.setProps(props);
  return null;
}
