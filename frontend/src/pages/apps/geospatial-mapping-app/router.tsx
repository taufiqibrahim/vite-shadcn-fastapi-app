import { Navigate, RouteObject } from "react-router";

export const GeospatialMappingAppRoutes: RouteObject = {
  path: "geospatial-mapping-app",
  children: [
    { index: true, element: <Navigate to="datasets" replace /> },
    {
      path: "datasets",
      lazy: async () => ({
        Component: (
          await import("@/pages/apps/geospatial-mapping-app/pages/datasets")
        ).default,
      }),
    },
  ],
};
