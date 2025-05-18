import {
  createBrowserRouter,
  Navigate,
  Outlet,
  RouteObject,
} from "react-router";
import { useAuth } from "./auth/use-auth";

const ProtectedRoute = () => {
  const { accessToken } = useAuth();
  return accessToken ? <Outlet /> : <Navigate to="/login" replace />;
};

export const routes: RouteObject[] = [
  {
    path: "/",
    children: [
      { index: true, element: <Navigate to="/apps" replace /> },
      {
        path: "login",
        lazy: async () => ({
          Component: (await import("@/pages/account/login")).default,
        }),
      },
      {
        path: "signup",
        lazy: async () => ({
          Component: (await import("@/pages/account/signup")).default,
        }),
      },
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
            path: "profile",
            handle: { breadcrumb: "Profile" },
            children: [
              {
                path: "user",
                handle: { breadcrumb: "" },
                lazy: async () => ({
                  Component: (await import("@/pages/settings/profile/user")).default,
                }),
              },
            ],
          },
          {
            path: "organizations",
            handle: { breadcrumb: "Organizations" },
            children: [
              {
                path: "general",
                handle: { breadcrumb: "" },
                lazy: async () => ({
                  Component: (await import("@/pages/settings/organizations/general")).default,
                }),
              },
              {
                path: "billing",
                handle: { breadcrumb: "Billing" },
                lazy: async () => ({
                  Component: (await import("@/pages/settings/organizations/billing")).default,
                }),
              },
              {
                path: "api-keys",
                handle: { breadcrumb: "API Keys" },
                lazy: async () => ({
                  Component: (await import("@/pages/settings/organizations/api-keys")).default,
                }),
              },
            ],
          },
        ],
      },
    ],
  },
];

export const router = createBrowserRouter(routes);
