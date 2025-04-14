# Frontend

## Quickstart

Install dependencies

```bash
pnpm install
```

Run development server

```bash
pnpm run dev
  ➜  Local:   http://localhost:5173/
```

## Testing

- Using [vitest](https://vitest.dev/)

### How it initialized

The test framework was initialized using following command:

```bash
pnpm add -D vitest jsdom @vitest/coverage-istanbul
```

Then we update the `vite.config.ts`.

```ts
/// <reference types="vitest" />
import path from "path";
import tailwindcss from "@tailwindcss/vite";
import react from "@vitejs/plugin-react";
import { defineConfig } from "vite";

export default defineConfig({
  plugins: [react(), tailwindcss()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  // ++ added
  test: {
    environment: "jsdom",
    coverage: {
      reporter: ["text", "json", "html"],
      exclude: ["node_modules/", "src/mocks/", "**/*.test.tsx"],
    },
  },
});
```

`/// <reference types="vitest" />` must be at the top of `vite.config.ts`.

Also update `package.json` scripts:

```json
  "scripts": {
    "dev": "vite",
    "build": "tsc -b && vite build",
    "lint": "eslint .",
    "preview": "vite preview",
    "test": "vitest",
    "coverage": "vitest run --coverage"
  }
```
