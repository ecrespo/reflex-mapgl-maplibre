// Local React component bridging @mapbox/mapbox-gl-draw into
// react-map-gl/maplibre via the `useControl` hook (DD-006).
// Requires the optional npm dependency `@mapbox/mapbox-gl-draw`.
import { useControl } from "react-map-gl/maplibre";
import MapboxDraw from "@mapbox/mapbox-gl-draw";

export function DrawControl(props) {
  useControl(
    () =>
      new MapboxDraw({
        displayControlsDefault: props.displayControlsDefault,
        controls: props.controls,
        defaultMode: props.defaultMode,
      }),
    ({ map }) => {
      if (props.onCreate) map.on("draw.create", props.onCreate);
      if (props.onUpdate) map.on("draw.update", props.onUpdate);
      if (props.onDelete) map.on("draw.delete", props.onDelete);
    },
    ({ map }) => {
      if (props.onCreate) map.off("draw.create", props.onCreate);
      if (props.onUpdate) map.off("draw.update", props.onUpdate);
      if (props.onDelete) map.off("draw.delete", props.onDelete);
    },
    { position: props.position },
  );
  return null;
}
