import { create } from "zustand";
import { persist } from "zustand/middleware";

interface FontStore {
  font: string;
  setFont: (font: string) => void;
}

export const useFont = create<FontStore>()(
  persist(
    (set) => ({
      font: "font-sans",
      setFont: (font: string) => set({ font }),
    }),
    {
      name: "font-storage",
    },
  ),
);
