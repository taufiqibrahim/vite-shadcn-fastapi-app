import { ACCESS_TOKEN_KEY, API_BASE_URL } from "@/constants";
import axios from "axios";

// Base API instance
export const api = axios.create({
  baseURL: API_BASE_URL,
  withCredentials: true,
});

// Request interceptor
api.interceptors.request.use((config) => {
  const token = localStorage.getItem(ACCESS_TOKEN_KEY);
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem(ACCESS_TOKEN_KEY);
      return Promise.reject(error);
    }
    return Promise.reject(error);
  },
);

// API request wrapper
export const request = async (
  url: string,
  method: "GET" | "POST" | "OPTION" | "PUT" | "PATCH" | "DELETE",
  data?: any,
  headers: Record<string, string> = {},
) => {
  const isForm = data instanceof URLSearchParams;

  try {
    const response = await api.request({
      url,
      method,
      headers: {
        ...(isForm
          ? { "Content-Type": "application/x-www-form-urlencoded" }
          : {}),
        ...headers,
      },
      ...(method === "GET" ? { params: data } : { data }),
    });

    return response.data;
  } catch (error: any) {
    // Axios error object shape
    const message =
      error.response?.data?.detail || error.message || "Request failed";

    // Optionally re-throw with a better message
    throw new Error(JSON.stringify(message));
  }
};
