// Local React component bridging deck.gl into react-map-gl/maplibre via the
// `useControl` hook (see specs/technical/architecture.md DD-006).
// Requires the optional npm dependency `@deck.gl/mapbox`.
import { useControl } from "react-map-gl/maplibre";
import { MapboxOverlay } from "@deck.gl/mapbox";

export function DeckGLOverlay(props) {
  const overlay = useControl(() => new MapboxOverlay(props));
  overlay.setProps(props);
  return null;
}
