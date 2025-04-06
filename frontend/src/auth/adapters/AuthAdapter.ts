export type UserPasswordLoginCredentials = { email: string; password: string };
export type LoginCredentials = UserPasswordLoginCredentials;

export type SimpleLoginResponse = {
  token: string | null;
  message: string | null;
};
export type LoginResponse = SimpleLoginResponse;

export interface AuthAdapter {
  login: (credentials: LoginCredentials) => Promise<LoginResponse>;
  logout: () => void;
  getUser: () => Promise<any>;
  refreshToken?: () => Promise<string>;
}
