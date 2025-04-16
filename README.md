# Fullstack App – Vite + shadcn/ui + FastAPI

A modern, fullstack web application built to showcase real-world architecture, clean code practices, and a seamless developer experience. Powered by **Vite** and **shadcn/ui** on the frontend, and a **FastAPI** backend, this app is designed for rapid development, performance, and scalability.

---

## Quickstart (Docker Compose)
Run this command (make sure `docker` is installed)
```bash
docker compose build
docker compose up -d
```

## 🚀 Features

### 🔐 Authentication

- ✅ **Basic Auth**: Standard email & password authentication with hashed credentials and JWT-based session management.
- 🛠️ **Magic Link Login** *(in progress)*: Email-based login without the need for passwords.
- 🔒 **2FA Support** *(planned)*: Time-based One-Time Passwords (TOTP) with QR code setup.
- ❌ **OAuth2** *(planned)*

### 🎨 Frontend (Vite + shadcn/ui + Tailwind)

- ⚡ Ultra-fast dev experience with Vite HMR
- 💅 Beautiful, accessible UI components via [shadcn/ui](https://ui.shadcn.com/)
- 🎨 Fully themed with TailwindCSS & dark mode support
- 🧹 Auto-formatting with [Prettier](https://prettier.io/)
- 🧪 Unit-tested components using Vitest & Testing Library

### 🧠 Backend (FastAPI + SQLModel)

- ⚡ High-performance Python backend with FastAPI
- 🔐 Auth system with JWT, dependency overrides, and secure password hashing
- 📄 RESTful APIs and OpenAPI docs auto-generated
- 🧰 Database modeling with SQLModel (SQLite/PostgreSQL)
- 📬 Email sending capabilities via SendGrid (mocked in dev)
- 🔄 Background tasks using Celery (with Redis broker)
- 🧪 Pytest test suite with coverage reports

---

### 🧰 Dev Setup

This app is built with a **Docker-first** mindset, but runs perfectly natively too. Preconfigured for:

- `docker-compose` for local dev (frontend + backend + db)
- `.env` and `.env.example` for quick environment configuration
- Pre-commit hooks for linting and formatting

---

Let me know if you want badges, deployment info (like Vercel + Railway), or a demo login setup.
### Frontend

- [prettier](https://prettier.io/) for code formatter.

### Backend

### File Upload
This repository includes file uploader as React Context.

