import { createBrowserRouter, Navigate, Outlet } from "react-router";
import { useAuth } from "./auth/use-auth";
import { GeospatialMappingAppRoutes } from "@/pages/apps/geospatial-mapping-app/router";

const ProtectedRoute = () => {
  const { accessToken } = useAuth();
  return accessToken ? <Outlet /> : <Navigate to="/login" replace />;
};

export const router = createBrowserRouter([
  {
    path: "/",
    children: [
      { index: true, element: <Navigate to="/apps" replace /> },
      {
        path: "login",
        lazy: async () => ({
          Component: (await import("@/pages/auth/login")).default,
        }),
      },
    ],
  },
  {
    path: "/",
    element: <ProtectedRoute />,
    children: [
      // {
      //   path: "dashboard",
      //   // element: <ProtectedRoute />,
      //   children: [
      //     {
      //       path: "",
      //       lazy: async () => ({
      //         Component: (await import("@/pages/dashboard")).default,
      //       }),
      //     },
      //   ],
      // },
      {
        path: "apps",
        // element: <ProtectedRoute />,
        children: [
          {
            path: "",
            lazy: async () => ({
              Component: (await import("@/pages/apps")).default,
            }),
          },
          // {
          //   path: ":name",
          //   lazy: async () => ({
          //     Component: DynamicAppLoader,
          //   }),
          // },
          GeospatialMappingAppRoutes,
        ],
      },
    ],
  },
]);
