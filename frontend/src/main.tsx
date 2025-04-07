import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { RouterProvider } from "react-router";
import { router } from "./router";
import { AuthProvider } from "./auth/AuthProvider";
import { UserPasswordAuthAdapter } from "./auth/adapters/UserPasswordAuthAdapter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";

const authAdapter = new UserPasswordAuthAdapter();
const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider adapter={authAdapter}>
        <RouterProvider router={router} />
      </AuthProvider>
    </QueryClientProvider>
  </StrictMode>,
);
