import { ReactNode, useState } from "react";
import { AuthContext } from "@/auth/use-auth";
import { ACCESS_TOKEN_KEY } from "@/constants";
import { LoginCredentials, ResetPasswordResponse, SignupCredentials } from "./types";
import { request } from "@/lib/api";
import { useQuery } from "@tanstack/react-query";

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {

  // Initialize token from localStorage for session persistence
  const [accessToken, setAccessToken] = useState<string | null>(() => {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  });

  const isLoading = false;

  // Sign up the user, stores token, and update state
  const signup = async (credentials: SignupCredentials) => {
    try {
      const form = new URLSearchParams();
      form.append("email", credentials.email);
      form.append("full_name", credentials.full_name);
      form.append("password", credentials.password);

      const data = await request("/accounts/signup", "POST", form, {
        "Content-Type": "application/x-www-form-urlencoded",
      });

      if (data.access_token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
        setAccessToken(data.access_token);
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
    }
  };

  // Log in the user, stores token, and update state
  const login = async (credentials: LoginCredentials) => {
    try {
      const form = new URLSearchParams();
      form.append("username", credentials.email);
      form.append("password", credentials.password);

      const data = await request("/accounts/login", "POST", form, {
        "Content-Type": "application/x-www-form-urlencoded",
      });

      if (data.access_token) {
        localStorage.setItem(ACCESS_TOKEN_KEY, data.access_token);
        setAccessToken(data.access_token);
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
    }
  };

  const requestResetPassword = async (credentials: any): Promise<any> => {
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
  };

  const confirmResetPassword = async (
    credentials: any,
  ): Promise<ResetPasswordResponse> => {
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
  };

  // Logs out the user and clears authentication state
  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setAccessToken(null);
  };

  // Get user data
  const { data: user, refetch: refetchUser } = useQuery({
    queryKey: ["apps"],
    queryFn: () => request("/accounts/profile/me", "GET"),
    staleTime: 1000 * 60 * 5, // Cache for 5 minutes
    enabled: !!accessToken,
    retry: false,
    refetchOnWindowFocus: false,
  })

  // Provide authentication state and actions to child components
  return (
    <AuthContext.Provider
      value={{
        accessToken,
        user,
        refetchUser,
        // isLoading,
        // error,
        signup,
        login,
        logout,
        requestResetPassword,
        confirmResetPassword,
      }}
    >
      <div className="relative">
        {isLoading ? (
          <div className="absolute inset-0 bg-white/60 backdrop-blur-sm flex items-center justify-center z-50">
            {/* <Spinner className="w-12 h-12" /> */}
          </div>
        ) : (children)}
      </div>
    </AuthContext.Provider>
  );
}
