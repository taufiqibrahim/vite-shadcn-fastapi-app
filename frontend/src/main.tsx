import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { RouterProvider } from "react-router";
import { router } from "./router";
import { AuthProvider } from "./auth/AuthProvider";
import { UserPasswordAuthAdapter } from "./auth/adapters/UserPasswordAuthAdapter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "./components/theme-provider";
import { Toaster } from "./components/ui/sonner";

const authAdapter = new UserPasswordAuthAdapter();
const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <QueryClientProvider client={queryClient}>
        <AuthProvider adapter={authAdapter}>
          <RouterProvider router={router} />
          <Toaster
            position="bottom-center"
            closeButton
            duration={3000}
            toastOptions={{}}
          />
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  </StrictMode>,
);
