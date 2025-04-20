import { Navigate, RouteObject } from "react-router";

export const GeospatialMappingAppRoutes: RouteObject = {
  path: "geospatial-mapping-app",
  children: [
    { index: true, element: <Navigate to="datasets" replace /> },
    {
      path: "datasets",
      children: [
        {
          index: true,
          lazy: async () => ({
            Component: (
              await import("@/pages/apps/geospatial-mapping-app/pages/datasets")
            ).default,
          }),
        },
        {
          path: ":uid",
          lazy: async () => ({
            Component: (
              await import(
                "@/pages/apps/geospatial-mapping-app/pages/datasets/details"
              )
            ).default,
          }),
        },
      ],
    },
    {
      path: "maps",
      lazy: async () => ({
        Component: (
          await import("@/pages/apps/geospatial-mapping-app/pages/maps")
        ).default,
      }),
    },
    {
      path: "workflows",
      lazy: async () => ({
        Component: (
          await import("@/pages/apps/geospatial-mapping-app/pages/workflows")
        ).default,
      }),
    },
  ],
};
