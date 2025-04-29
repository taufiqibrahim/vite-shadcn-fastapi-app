import { ACCESS_TOKEN_KEY } from "@/constants";
import { request } from "@/lib/api";

export type LoginCredentials = { email: string; password: string };
export type SignupCredentials = {
  email: string;
  password: string;
  full_name?: string | null | undefined;
};
export type RequestResetPasswordCredentials = { email: string };
export type ResetPasswordCredentials = { resetToken: string; password: string };

export type LoginResponse = {
  token: string | null;
  message: string | null;
};

export type SignupResponse = {
  token: string | null;
  message: string | null;
};

export type ResetPasswordResponse = {
  token: string | null;
  message: string | null;
};

export interface AccountProfile {
  id: number;
  uid: string;
  account_id: number;
  account_type: string;
  avatar?: string;
  full_name: string;
  created_at: string;
  disabled: boolean;
  email: string;
  updated_at: string;
}

export interface AuthAdapter {
  signup: (credentials: SignupCredentials) => Promise<SignupResponse>;
  login: (credentials: LoginCredentials) => Promise<LoginResponse>;
  logout: () => void;
  requestResetPassword: (
    credentials: RequestResetPasswordCredentials,
  ) => Promise<any>;
  confirmResetPassword: (
    credentials: ResetPasswordCredentials,
  ) => Promise<ResetPasswordResponse>;
  getUser: () => Promise<AccountProfile>;
  refreshToken?: () => Promise<string>;
}

export class UserAuthAdapter implements AuthAdapter {
  private async handleAuthRequest(
    endpoint: string,
    credentials: SignupCredentials | LoginCredentials,
  ): Promise<{ token: string | null; message: string }> {
    try {
      const form = new URLSearchParams();

      if (endpoint === "/accounts/signup") {
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
    return this.handleAuthRequest("/accounts/signup", credentials);
  }

  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    return this.handleAuthRequest("/accounts/login", credentials);
  }

  logout() {}

  async getUser(): Promise<AccountProfile> {
    return await request("/accounts/profile/me", "GET");
  }

  async refreshToken(): Promise<any> {
    console.debug("refreshToken");
  }

  async requestResetPassword(
    credentials: RequestResetPasswordCredentials,
  ): Promise<any> {
    try {
      const form = new URLSearchParams();
      form.append("email", credentials.email);
      const data = await request("/accounts/reset-password", "POST", form, {
        "Content-Type": "application/x-www-form-urlencoded",
      });
      return { data };
    } catch (err) {
      console.error(`Error:`, err);
      return { err };
    }
  }

  async confirmResetPassword(
    credentials: ResetPasswordCredentials,
  ): Promise<ResetPasswordResponse> {
    try {
      const form = new URLSearchParams();
      form.append("password", credentials.password);
      const data = await request(
        "/accounts/confirm-reset-password",
        "POST",
        form,
        {
          Authorization: `Bearer ${credentials.resetToken}`,
          "Content-Type": "application/x-www-form-urlencoded",
        },
      );

      if (data.access_token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
      }

      return { token: data.access_token, message: data.message ?? "Success" };
    } catch (err) {
      console.error(`Error:`, err);
      return {
        token: null,
        message: String(err),
      };
    }
  }
}
