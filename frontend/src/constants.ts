export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000/api/v1";
export const ACCESS_TOKEN_KEY = "accessToken";
export const LOGIN_URL = "/login";
export const STORAGE_BACKEND = import.meta.env.VITE_STORAGE_BACKEND || "minio";
export const DEMO_USERNAME = import.meta.env.VITE_DEMO_USERNAME;
export const DEMO_PASSWORD = import.meta.env.VITE_DEMO_PASSWORD;
