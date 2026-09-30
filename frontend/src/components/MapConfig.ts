export const DARK_CANVAS_STYLE = {
  version: 8 as const,
  sources: {
    "esri-dark-base": {
      type: "raster" as const,
      tiles: [
        "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Base/MapServer/tile/{z}/{y}/{x}"
      ],
      tileSize: 256,
      attribution: "&copy; Esri, DeLorme, NAVTEQ"
    },
    "esri-dark-reference": {
      type: "raster" as const,
      tiles: [
        "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/World_Dark_Gray_Reference/MapServer/tile/{z}/{y}/{x}"
      ],
      tileSize: 256,
      attribution: ""
    }
  },
  layers: [
    {
      id: "esri-dark-base-layer",
      type: "raster" as const,
      source: "esri-dark-base",
      minzoom: 0,
      maxzoom: 18
    },
    {
      id: "esri-dark-reference-layer",
      type: "raster" as const,
      source: "esri-dark-reference",
      minzoom: 0,
      maxzoom: 18
    }
  ]
};

// Backwards-compatible export
export const CARTO_DARK_RASTER_STYLE = DARK_CANVAS_STYLE;

export const INITIAL_VIEW_STATE = {
  longitude: 86.05,
  latitude: 19.92,
  zoom: 8.6,
  pitch: 38,
  bearing: -6,
  maxPitch: 60,
  minZoom: 6,
  maxZoom: 16
};
