import { describe, expect, test } from "vitest";
import { cn, formatBytes } from "../../src/lib/utils";

describe("cn", () => {
  test("merges simple class names", () => {
    const result = cn("btn", "btn-primary", "rounded");
    expect(result).toBe("btn btn-primary rounded");
  });

  test("handles conditional class names", () => {
    const isActive = true;
    const result = cn("btn", isActive && "active");
    expect(result).toBe("btn active");
  });

  test("resolves conflicting Tailwind classes with tailwind-merge", () => {
    const result = cn("text-sm", "text-lg");
    expect(result).toBe("text-lg"); // tailwind-merge prioritizes the last one
  });
});

describe("formatBytes", () => {
  test('returns "0 Byte" when input is 0', () => {
    expect(formatBytes(0)).toBe("0 Byte");
  });

  test("formats 1024 bytes as 1 KB (default sizeType)", () => {
    expect(formatBytes(1024)).toBe("1 KB");
  });

  test("formats 1048576 bytes as 1.00 MB with 2 decimals", () => {
    expect(formatBytes(1048576, { decimals: 2 })).toBe("1.00 MB");
  });

  test('uses "accurate" sizeType for 1024 bytes', () => {
    expect(formatBytes(1024, { sizeType: "accurate" })).toBe("1 KiB");
  });

  test("handles large byte values (1 TB)", () => {
    expect(formatBytes(1099511627776)).toBe("1 TB");
    expect(formatBytes(1099511627776, { sizeType: "accurate" })).toBe("1 TiB");
  });

  test('falls back to "Bytes" if index is out of bounds', () => {
    const large = Math.pow(1024, 10);
    expect(formatBytes(large)).toMatch(/Bytes$/);
  });
});
