import { request } from "@/lib/api";
import { AuthAdapter, LoginCredentials, LoginResponse } from "./AuthAdapter";
import { ACCESS_TOKEN_KEY } from "@/constants";

export class UserPasswordAuthAdapter implements AuthAdapter {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    try {
      // Prepare form data for FastAPI OAuth2 login
      const form = new URLSearchParams();
      form.append("username", credentials.email);
      form.append("password", credentials.password);

      // Send the request using your global API handler
      const data = await request("/auth/login", "POST", form, {
        "Content-Type": "application/x-www-form-urlencoded",
      });

      // Store token
      if (data.access_token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
      }

      return {
        token: data.access_token,
        message: data.message ?? "Login successful",
      };
    } catch (err: any) {
      console.error("Login error:", err);

      let errorMessage = "Login failed";
      if (typeof err === "string") errorMessage = err;
      else if (err?.message) errorMessage = err.message;
      else if (err?.detail) errorMessage = err.detail;

      return {
        token: null,
        message: errorMessage,
      };
      // return {
      //   token: null,
      //   message: err?.message || err?.detail || "Login failed",
      // };
    }
  }

  logout() {}

  async getUser(): Promise<any> {}

  async refreshToken(): Promise<any> {}
}
