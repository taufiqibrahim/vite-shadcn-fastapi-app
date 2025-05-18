import { createContext, useContext } from "react";
import { LoginResponse, ResetPasswordCredentials, ResetPasswordResponse, SignupResponse } from "./types";
import { AccountProfileMe } from "@/client";


// Defines the shape of the authentication context
interface AuthContextType {
  accessToken?: string | null;
  user?: AccountProfileMe;
  refetchUser: () => void;
  // isLoading: boolean;
  // error: unknown;
  signup: (credentials: any) => Promise<SignupResponse>;
  login: (credentials: any) => Promise<LoginResponse>;
  logout: () => void;
  requestResetPassword: (credentials: any) => Promise<any>;
  confirmResetPassword: (credentials: ResetPasswordCredentials) => Promise<ResetPasswordResponse>;
}

export const AuthContext = createContext<AuthContextType | null>(null);

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
};
