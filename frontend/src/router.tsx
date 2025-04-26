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
  return accessToken ? <Outlet /> : <Navigate to="/auth/login" replace />;
};

export const routes: RouteObject[] = [
  {
    path: "/",
    children: [{ index: true, element: <Navigate to="/apps" replace /> }],
  },
  {
    path: "/auth",
    children: [
      {
        path: "login",
        lazy: async () => ({
          Component: (await import("@/pages/auth/login")).default,
        }),
      },
      {
        path: "signup",
        lazy: async () => ({
          Component: (await import("@/pages/auth/signup")).default,
        }),
      },
    ],
  },
  {
    path: "/account",
    children: [
      {
        path: "forgot-password",
        lazy: async () => ({
          Component: (await import("@/pages/account/forgot-password")).default,
        }),
      },
      {
        path: "reset-password",
        lazy: async () => ({
          Component: (await import("@/pages/account/reset-password")).default,
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
