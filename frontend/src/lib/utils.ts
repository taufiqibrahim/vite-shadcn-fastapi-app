import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export function formatBytes(
  bytes: number,
  opts: {
    decimals?: number;
    sizeType?: "accurate" | "normal";
  } = {},
) {
  const { decimals = 0, sizeType = "normal" } = opts;

  const sizes = ["Bytes", "KB", "MB", "GB", "TB"];
  const accurateSizes = ["Bytes", "KiB", "MiB", "GiB", "TiB"];
  if (bytes === 0) return "0 Byte";
  const i = Math.floor(Math.log(bytes) / Math.log(1024));
  return `${(bytes / Math.pow(1024, i)).toFixed(decimals)} ${
    sizeType === "accurate"
      ? (accurateSizes[i] ?? "Bytes")
      : (sizes[i] ?? "Bytes")
  }`;
}

export const getInitials = (input?: string): string => {
  if (!input) return "";

  // If input contains "@", assume it's an email
  if (input.includes("@")) {
    const namePart = input.split("@")[0]; // Get the part before '@'
    const nameSegments = namePart.split(/[\.\_\-]/); // Split by common separators

    if (nameSegments.length > 1) {
      return (nameSegments[0][0] + nameSegments[1][0]).toUpperCase(); // Use first letters of first two parts
    }

    return nameSegments[0].slice(0, 2).toUpperCase(); // Otherwise, take first two letters
  }

  // If it's a full name
  const words = input.split(" ").filter(Boolean);
  if (words.length > 1) {
    return (words[0][0] + words[1][0]).toUpperCase(); // First letter of first two words
  }
  return words[0].slice(0, 2).toUpperCase(); // First two letters if only one word
};

export const renderMessage = (data: any): string => {
  if (typeof data?.message === "string") {
    return data.message;
  }
  return JSON.stringify(data);
};
