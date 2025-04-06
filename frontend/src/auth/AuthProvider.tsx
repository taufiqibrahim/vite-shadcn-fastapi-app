import { ReactNode, useState } from "react";
import { AuthAdapter, LoginResponse } from "./adapters/AuthAdapter";
import { AuthContext } from "./AuthContext";
import { ACCESS_TOKEN_KEY } from "@/constants";

// AuthProvider supplies authentication state and logic to the app
export const AuthProvider: React.FC<{
  adapter: AuthAdapter;
  children: ReactNode;
}> = ({ adapter, children }) => {
  // Initialize token from localStorage for session persistence
  const [accessToken, setAccessToken] = useState<string | null>(() => {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  });

  // Logs in the user, stores token, and updates state
  const login = async (credentials: any): Promise<LoginResponse> => {
    const { token, message } = await adapter.login(credentials);
    if (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token);
      setAccessToken(token);
    }
    return { token, message };
  };

  // Logs out the user and clears authentication state
  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setAccessToken(null);
    adapter.logout(); // Optional: call adapter logic if needed
  };

  // Provide authentication state and actions to child components
  return (
    <AuthContext.Provider value={{ accessToken, user: null, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
