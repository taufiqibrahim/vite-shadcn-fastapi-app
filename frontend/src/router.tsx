import {
  createBrowserRouter,
  Navigate,
  Outlet,
  RouteObject,
} from "react-router";
import { useAuth } from "./auth/use-auth";
import { GeospatialMappingAppRoutes } from "@/pages/apps/geospatial-mapping-app/router";

const ProtectedRoute = () => {
  console.log("router.ProtectedRoute");
  const { accessToken } = useAuth();
  return accessToken ? <Outlet /> : <Navigate to="/login" replace />;
};

export const routes: RouteObject[] = [
  {
    path: "/",
    children: [
      { index: true, element: <Navigate to="/apps" replace /> },
      {
        id: "Login",
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
      {
        path: "apps",
        children: [
          {
            path: "",
            lazy: async () => ({
              Component: (await import("@/pages/apps")).default,
            }),
          },
          GeospatialMappingAppRoutes,
        ],
      },
      {
        path: "billing",
        children: [
          {
            path: "",
            lazy: async () => ({
              Component: (await import("@/pages/billing")).default,
            }),
          },
        ],
      },
      {
        path: "usage",
        handle: { breadcrumb: "Usage" },
        children: [
          {
            path: "",
            lazy: async () => ({
              Component: (await import("@/pages/usage")).default,
            }),
          },
        ],
      },
      {
        path: "settings",
        handle: { breadcrumb: "Settings" },
        children: [
          {
            path: "",
            lazy: async () => ({
              Component: (await import("@/pages/settings")).default,
            }),
          },
          {
            path: "api-keys",
            handle: { breadcrumb: "API Keys" },
            lazy: async () => ({
              Component: (await import("@/pages/settings/api-keys")).default,
            }),
          },
        ],
      },
    ],
  },
];

export const router = createBrowserRouter(routes);
