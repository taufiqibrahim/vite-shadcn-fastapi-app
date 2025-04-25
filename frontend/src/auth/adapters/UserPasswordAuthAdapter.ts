import { request } from "@/lib/api";
import {
  AuthAdapter,
  LoginCredentials,
  LoginResponse,
  SignupCredentials,
  SignupResponse,
  UserMe,
} from "./AuthAdapter";
import { ACCESS_TOKEN_KEY } from "@/constants";

export class UserPasswordAuthAdapter implements AuthAdapter {
  private async handleAuthRequest(
    endpoint: string,
    credentials: SignupCredentials | LoginCredentials,
  ): Promise<{ token: string | null; message: string }> {
    try {
      const form = new URLSearchParams();

      if (endpoint === "/auth/signup") {
        form.append("email", credentials.email);
      } else {
        form.append("username", credentials.email);
      }

      form.append("password", credentials.password);

      // Only append full_name if exists
      if ("full_name" in credentials && credentials.full_name) {
        form.append("full_name", credentials.full_name);
      }

      const data = await request(endpoint, "POST", form, {
        "Content-Type": "application/x-www-form-urlencoded",
      });

      if (data.access_token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
      }

      return {
        token: data.access_token,
        message: data.message ?? "Success",
      };
    } catch (err: any) {
      console.error(`${endpoint} error:`, err);

      let errorMessage = "Authentication failed";
      if (typeof err === "string") errorMessage = err;
      else if (err?.message) errorMessage = err.message;
      else if (err?.detail) errorMessage = err.detail;

      return {
        token: null,
        message: errorMessage,
      };
    }
  }

  async signup(credentials: SignupCredentials): Promise<SignupResponse> {
    return this.handleAuthRequest("/auth/signup", credentials);
  }

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    return this.handleAuthRequest("/auth/login", credentials);
  }

  logout() {}

  async getUser(): Promise<UserMe> {
    return await request("/users/me", "GET");
  }

  async refreshToken(): Promise<any> {}
}
