# Maps

## Using react-map-gl and maplibre-gl
```bash
pnpm add react-map-gl maplibre-gl
```

Initialize the map:
```tsx
import { Map } from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
// ...
    <Map
      initialViewState={{
        longitude: -122.4,
        latitude: 37.8,
        zoom: 14,
      }}
      style={{ width: "100%", height: "100%" }}
      mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
    ></Map>
// ...
```