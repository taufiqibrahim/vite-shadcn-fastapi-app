export const APP_NAME = import.meta.env.VITE_APP_NAME || "vite-shadcn-fastapi";
export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
export const ACCESS_TOKEN_KEY = "accessToken";
export const LOGIN_URL = "/login";
export const LOGIN_SUCCESS_REDIRECT_URL =
  import.meta.env.LOGIN_SUCCESS_REDIRECT_URL || "/apps";
export const STORAGE_BACKEND = import.meta.env.VITE_STORAGE_BACKEND || "minio";
export const DEFAULT_TOASTER_DURATION_MS = 5000;
export const DEMO_USERNAME = import.meta.env.VITE_DEMO_USERNAME;
export const DEMO_PASSWORD = import.meta.env.VITE_DEMO_PASSWORD;
export const DEFAULT_ERROR_MESSAGE = "Oops, something wrong on our side";
