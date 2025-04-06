import { createContext } from "react";
import { LoginResponse } from "./adapters/AuthAdapter";

// Defines the shape of the authentication context
interface AuthContextType {
  accessToken?: string | null;
  user: any; // TODO: Consider typing `user` if available
  login: (credentials: any) => Promise<LoginResponse>;
  logout: () => void;
}

// Create a context with an initial null value
export const AuthContext = createContext<AuthContextType | null>(null);
