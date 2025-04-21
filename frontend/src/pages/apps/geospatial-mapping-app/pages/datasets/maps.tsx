import { useCallback, useMemo, useRef, useState } from "react";
import {
  Layer,
  Map,
  MapLayerMouseEvent,
  MapRef,
  Popup,
  Source,
} from "react-map-gl/maplibre";
import "maplibre-gl/dist/maplibre-gl.css";
import { DatasetMapsProps } from "@/pages/apps/geospatial-mapping-app/types";
import { API_BASE_URL } from "@/constants";
import { debounce, transformRequest } from "@/lib/maps";

export default function DatasetMaps({ datasetUid, bbox }: DatasetMapsProps) {
  const mapRef = useRef<MapRef>(null);
  const [hoverInfo, setHoverInfo] = useState<any>(null);
  const [hoveredId, setHoveredId] = useState<number | null>(null);

  /**
   * Fit the maps to the bounding box from parent component
   */
  if (mapRef && mapRef?.current) {
    if (bbox && bbox[0] && bbox[1] && bbox[2] && bbox[3]) {
      mapRef.current.fitBounds(
        [
          [bbox[0], bbox[1]],
          [bbox[2], bbox[3]],
        ],
        { padding: 20, duration: 1000 },
      );
    }
  }

  // const handleOnMoveEnd = () => {
  //   const bounds = mapRef.current?.getBounds();
  //   if (bounds) {
  //     const bbox: [number, number, number, number] = [
  //       bounds.getWest(),
  //       bounds.getSouth(),
  //       bounds.getEast(),
  //       bounds.getNorth(),
  //     ];
  //     setBBox(bbox);
  //   }
  // };

  /**
   * Use debouncing to avoid "laggy" during fast movement on hover
   */
  const debouncedSetHoveredFeature = useMemo(() => {
    return debounce((feature: any, lngLat: any) => {
      setHoveredId(feature.id as number);
      setHoverInfo({
        lngLat,
        properties: feature.properties,
      });
    }, 5);
  }, []);

  /* Original without debouncing */
  // const handleOnHover = useCallback((e: MapLayerMouseEvent) => {
  //   if (e.features && e.features[0]) {
  //     const feature = e.features[0];
  //     setHoveredId(feature.id as number);
  //     setHoverInfo({
  //       lngLat: e.lngLat,
  //       properties: feature.properties,
  //     });
  //   } else {
  //     setHoveredId(null);
  //     setHoverInfo(null);
  //   }
  // }, []);

  /** With debounce */
  const handleOnHover = useCallback(
    (e: MapLayerMouseEvent) => {
      if (e.features && e.features[0]) {
        const feature = e.features[0];
        debouncedSetHoveredFeature(feature, e.lngLat);
      } else {
        debouncedSetHoveredFeature.cancel();
        setHoveredId(null);
        setHoverInfo(null);
      }
    },
    [debouncedSetHoveredFeature],
  );

  /**
   * Handle onclick on features
   * TODO: render component
   */
  const handleOnClick = useCallback((e: MapLayerMouseEvent) => {
    if (e.features && e.features[0]) {
      console.log("Clicked feature properties:", e.features[0].properties);
    }
  }, []);

  const tileURL = `${API_BASE_URL}geospatial-mapping/datasets/${datasetUid}/tiles/{z}/{x}/{y}.pbf`;
  return (
    <Map
      ref={mapRef}
      initialViewState={{
        longitude: -122.631425,
        latitude: 38.96543,
        zoom: 14,
      }}
      style={{ width: "100%", height: "100%" }}
      mapStyle="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json"
      // onMoveEnd={handleOnMoveEnd}
      onMouseMove={handleOnHover}
      onMouseDown={handleOnClick}
      transformRequest={transformRequest}
      interactiveLayerIds={[
        "dataset-points",
        "dataset-lines",
        "dataset-polygon",
      ]}
    >
      {datasetUid && (
        <Source id="dataset" type="vector" tiles={[tileURL]}>
          <Layer
            id="dataset-polygon"
            source-layer="dataset"
            type="fill"
            paint={{
              "fill-color": "#007cbf",
            }}
            filter={["==", "$type", "Polygon"]}
          />
          <Layer
            id="dataset-points"
            source-layer="dataset"
            type="circle"
            paint={{
              "circle-radius": 5,
              "circle-color": "#007cbf",
            }}
            filter={["==", "$type", "Point"]}
          />
          <Layer
            id="dataset-lines"
            source-layer="dataset"
            type="line"
            paint={{
              "line-width": 3,
              "line-color": "#007cbf",
            }}
            filter={["==", "$type", "LineString"]}
          />
          <Layer
            id="dataset-polygon-hover"
            source-layer="dataset"
            type="fill"
            paint={{
              "fill-color": "red",
            }}
            filter={
              hoveredId !== null
                ? [
                    "all",
                    ["==", "$type", "Polygon"],
                    ["==", "ogc_fid", hoveredId],
                  ]
                : ["==", "ogc_fid", -1]
            }
          />
          <Layer
            id="dataset-hover-points"
            source-layer="dataset"
            type="circle"
            paint={{
              "circle-radius": 7,
              "circle-color": "#ff6600",
            }}
            filter={
              hoveredId !== null
                ? [
                    "all",
                    ["==", "$type", "Point"],
                    ["==", "ogc_fid", hoveredId],
                  ]
                : ["==", "ogc_fid", -1]
            }
          />
          <Layer
            id="dataset-lines-hover"
            source-layer="dataset"
            type="line"
            paint={{
              "line-width": 5,
              "line-color": "red",
            }}
            filter={
              hoveredId !== null
                ? [
                    "all",
                    ["==", "$type", "LineString"],
                    ["==", "ogc_fid", hoveredId],
                  ]
                : ["==", "ogc_fid", -1]
            }
          />
        </Source>
      )}

      {hoverInfo && hoverInfo.lngLat && (
        <div className="z-[9999] text-sm">
          <Popup
            className="opacity-90"
            longitude={hoverInfo.lngLat.lng}
            latitude={hoverInfo.lngLat.lat}
            closeButton={false}
            closeOnClick={false}
          >
            <div style={{ fontSize: "12px" }}>
              {Object.entries(hoverInfo.properties)
                .filter(([key]) => key !== "geom")
                .map(([key, value]) => (
                  <div key={key}>
                    <strong>{key}</strong>: {String(value)}
                  </div>
                ))}
            </div>
          </Popup>
        </div>
      )}
    </Map>
  );
}
