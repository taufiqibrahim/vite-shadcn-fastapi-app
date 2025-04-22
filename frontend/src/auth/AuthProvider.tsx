import { ReactNode, useState } from "react";
import { AuthAdapter, LoginResponse, UserMe } from "./adapters/AuthAdapter";
import { AuthContext } from "./AuthContext";
import { ACCESS_TOKEN_KEY } from "@/constants";
import { useQuery } from "@tanstack/react-query";

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

  const { data: user } = useQuery<UserMe>({
    queryKey: ["auth", "user"],
    queryFn: () => adapter.getUser(),
    enabled: !!accessToken, // only run query if accessToken is set
    retry: false, // disable retries if needed
    refetchOnWindowFocus: false,
  });

  // Logs out the user and clears authentication state
  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setAccessToken(null);
    adapter.logout(); // Optional: call adapter logic if needed
  };

  // Provide authentication state and actions to child components
  return (
    <AuthContext.Provider value={{ accessToken, user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
