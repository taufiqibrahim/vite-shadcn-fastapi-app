FROM node:23-slim AS builder

ARG API_BASE_URL
ARG DEMO_USERNAME
ARG DEMO_PASSWORD

ENV VITE_API_BASE_URL=${API_BASE_URL}
ENV VITE_DEMO_USERNAME=${DEMO_USERNAME}
ENV VITE_DEMO_PASSWORD=${DEMO_PASSWORD}

WORKDIR /app

RUN npm install -g pnpm

COPY package*.json pnpm-lock.yaml ./
RUN pnpm install

COPY . .
RUN pnpm run build


FROM nginx:stable-alpine AS final

# Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy built app from builder
COPY --from=builder /app/dist /usr/share/nginx/html

COPY nginx.conf /etc/nginx/nginx.conf

EXPOSE 3000

CMD ["nginx", "-g", "daemon off;"]