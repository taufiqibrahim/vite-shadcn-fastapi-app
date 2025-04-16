# Generate FastAPI Clients

As FastAPI is based on the OpenAPI specification, you get automatic compatibility with many tools, including the automatic API docs (provided by Swagger UI).

We will use this to generate client-side code required for our frontend Vite app.

## Using openapi-react-query
[openapi-react-query](https://openapi-ts.dev/openapi-react-query/)

### Setup
Install this library along with `openapi-fetch` and `openapi-typescript`:

```bash
pnpm add openapi-react-query openapi-fetch
pnpm add -D openapi-typescript typescript
```

### Configure Frontend
Add command to your `package.json` file.

```json
// ...
  "scripts": {
    // ...
    "generate-client": "npx openapi-typescript http://localhost:8000/openapi.json -o ./src/client.d.ts --client axios"
  },
```

Run `pnpm run generate-client` with FastAPI running.
