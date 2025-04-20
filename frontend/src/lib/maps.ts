import { ACCESS_TOKEN_KEY, API_BASE_URL } from "@/constants";
import maplibregl from "maplibre-gl";

export const transformRequest: maplibregl.RequestTransformFunction = (
  url: any,
  resourceType: any,
) => {
  if (resourceType === "Tile" && url.indexOf(API_BASE_URL) > -1) {
    const token = localStorage.getItem(ACCESS_TOKEN_KEY);
    return {
      url: url,
      headers: { Authorization: `Bearer ${token}` },
      credentials: "include",
    };
  }
};

export function debounce<F extends (...args: any[]) => void>(
  func: F,
  wait: number,
) {
  let timeoutId: ReturnType<typeof setTimeout> | null;

  const debounced = (...args: Parameters<F>) => {
    if (timeoutId) clearTimeout(timeoutId);
    timeoutId = setTimeout(() => func(...args), wait);
  };

  debounced.cancel = () => {
    if (timeoutId) {
      clearTimeout(timeoutId);
      timeoutId = null;
    }
  };

  return debounced as F & { cancel: () => void };
}
