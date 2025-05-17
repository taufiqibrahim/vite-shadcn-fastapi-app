import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { RouterProvider } from "react-router";
import { router } from "./router";
import { AuthProvider } from "./auth/AuthProvider";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { ThemeProvider } from "./components/theme-provider";
import { Toaster } from "./components/ui/sonner";
import { DEFAULT_TOASTER_DURATION_MS } from "./constants";

const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <QueryClientProvider client={queryClient}>
        <AuthProvider>
          <RouterProvider router={router} />
          <Toaster
            position="bottom-center"
            closeButton
            duration={DEFAULT_TOASTER_DURATION_MS}
            toastOptions={{
              classNames: {
                description: "!text-red-900",
                closeButton:
                  "!absolute !top-0 !bg-gray-100 !right-[-12px] !left-auto rounded p-1",
              },
            }}
          />
        </AuthProvider>
      </QueryClientProvider>
    </ThemeProvider>
  </StrictMode>,
);
