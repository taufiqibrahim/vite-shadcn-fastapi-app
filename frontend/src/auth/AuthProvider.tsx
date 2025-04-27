import { ReactNode, useState } from "react";
import {
  AuthAdapter,
  LoginResponse,
  ResetPasswordResponse,
  SignupResponse,
  UserMe,
} from "./AuthAdapter";
import { AuthContext } from "./AuthContext";
import { ACCESS_TOKEN_KEY } from "@/constants";
import { useQuery } from "@tanstack/react-query";

/**
 *
 * AuthProvider supplies authentication state and logic to the app
 * @param param0
 * @returns
 */
export const AuthProvider: React.FC<{
  adapter: AuthAdapter;
  children: ReactNode;
}> = ({ adapter, children }) => {
  // Initialize token from localStorage for session persistence
  const [accessToken, setAccessToken] = useState<string | null>(() => {
    return localStorage.getItem(ACCESS_TOKEN_KEY);
  });

  // Sign up the user, stores token, and updates state
  const signup = async (credentials: any): Promise<SignupResponse> => {
    const { token, message } = await adapter.signup(credentials);
    if (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token);
      setAccessToken(token);
    }
    return { token, message };
  };

  // Logs in the user, stores token, and updates state
  const login = async (credentials: any): Promise<LoginResponse> => {
    const { token, message } = await adapter.login(credentials);
    if (token) {
      localStorage.setItem(ACCESS_TOKEN_KEY, token);
      setAccessToken(token);
    }
    return { token, message };
  };

  const requestResetPassword = async (credentials: any): Promise<any> => {
    const { data } = await adapter.requestResetPassword(credentials);
    return { data };
  };

  const confirmResetPassword = async (
    credentials: any,
  ): Promise<ResetPasswordResponse> => {
    const { token, message } = await adapter.confirmResetPassword(credentials);
    return { token, message };
  };

  const { data: user } = useQuery<UserMe>({
    queryKey: ["auth", "user"],
    queryFn: () => adapter.getUser(),
    enabled: !!accessToken, // only run query if accessToken is set
    retry: false, // disable retries if needed
    refetchOnWindowFocus: false,
    staleTime: 5 * 60000,
  });

  const getUser = async (): Promise<UserMe> => {
    const data = await adapter.getUser();
    return data;
  };

  // Logs out the user and clears authentication state
  const logout = () => {
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    setAccessToken(null);
    adapter.logout(); // Optional: call adapter logic if needed
  };

  // Provide authentication state and actions to child components
  return (
    <AuthContext.Provider
      value={{
        accessToken,
        user,
        getUser,
        signup,
        login,
        logout,
        requestResetPassword,
        confirmResetPassword,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};
