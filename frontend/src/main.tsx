import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import { RouterProvider } from "react-router";
import { router } from "./router";
import { AuthProvider } from "./auth/AuthProvider";
import { UserPasswordAuthAdapter } from "./auth/adapters/UserPasswordAuthAdapter";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { UploadProvider } from "./lib/uploader/context";
import { uploadthingUploader } from "./lib/uploader/uploadthing";

const authAdapter = new UserPasswordAuthAdapter();
const queryClient = new QueryClient();

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <QueryClientProvider client={queryClient}>
      <AuthProvider adapter={authAdapter}>
        <UploadProvider uploader={uploadthingUploader}>
          <RouterProvider router={router} />
        </UploadProvider>
      </AuthProvider>
    </QueryClientProvider>
  </StrictMode>,
);
