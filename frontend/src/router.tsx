import { createBrowserRouter, Navigate, Outlet, useParams } from "react-router";
import { useAuth } from "./auth/use-auth";
import { lazy, Suspense } from "react";

const ProtectedRoute = () => {
  const { accessToken } = useAuth();
  return accessToken ? <Outlet /> : <Navigate to="/login" replace />;
};

const DynamicAppLoader = () => {
  const pages = import.meta.glob("/src/pages/apps/**/index.tsx");
  const { name } = useParams();

  const pagePath = `/src/pages/apps/${name}/index.tsx`;
  const importPage = pages[pagePath];

  const loadComponent = async () => {
    try {
      if (!importPage) {
        const notFound = await import("@/pages/not-found.tsx");
        return { default: notFound.default } as {
          default: React.ComponentType;
        };
      }

      const mod = (await importPage()) as { default: React.ComponentType };
      return { default: mod.default };
    } catch (err) {
      const notFound = await import("@/pages/not-found.tsx");
      return { default: notFound.default } as { default: React.ComponentType };
    }
  };

  const LazyComponent = lazy(loadComponent);

  return (
    <Suspense fallback={<div>Loading...</div>}>
      <LazyComponent />
    </Suspense>
  );
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
          {
            path: ":name",
            lazy: async () => ({
              Component: DynamicAppLoader,
            }),
          },
        ],
      },
    ],
  },
]);
