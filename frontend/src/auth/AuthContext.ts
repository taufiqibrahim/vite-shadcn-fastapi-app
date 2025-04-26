import { createContext } from "react";
import {
  ResetPasswordCredentials,
  LoginResponse,
  ResetPasswordResponse,
  SignupResponse,
  UserMe,
} from "./AuthAdapter";

// Defines the shape of the authentication context
interface AuthContextType {
  accessToken?: string | null;
  getUser: () => Promise<UserMe>;
  user?: UserMe;
  signup: (credentials: any) => Promise<SignupResponse>;
  login: (credentials: any) => Promise<LoginResponse>;
  logout: () => void;
  requestResetPassword: (credentials: any) => Promise<any>;
  confirmResetPassword: (
    credentials: ResetPasswordCredentials,
  ) => Promise<ResetPasswordResponse>;
}

// Create a context with an initial null value
export const AuthContext = createContext<AuthContextType | null>(null);
