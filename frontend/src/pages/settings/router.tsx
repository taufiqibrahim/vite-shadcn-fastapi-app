import { RouteObject } from "react-router";

export const SettingRoutes: RouteObject = {
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
      path: "organizations",
      handle: { breadcrumb: "Organizations" },
      children: [
        {
          path: "",
          handle: { breadcrumb: "" },
          lazy: async () => ({
            Component: (await import("@/pages/settings/organizations/general"))
              .default,
          }),
        },
        {
          path: "billing",
          handle: { breadcrumb: "Billing" },
          lazy: async () => ({
            Component: (await import("@/pages/settings/organizations/billing"))
              .default,
          }),
        },
      ],
    },
    {
      path: "api-keys",
      handle: { breadcrumb: "API Keys" },
      lazy: async () => ({
        Component: (await import("@/pages/settings/organizations/api-keys"))
          .default,
      }),
    },
  ],
};
