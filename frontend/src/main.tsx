import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { RouterProvider } from "react-router";
import { router } from "./router";
import { AuthProvider } from "./auth/AuthProvider";
import { UserPasswordAuthAdapter } from "./auth/adapters/UserPasswordAuthAdapter";

const authAdapter = new UserPasswordAuthAdapter();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider adapter={authAdapter}>
      <RouterProvider router={router} />
    </AuthProvider>
  </StrictMode>,
);
