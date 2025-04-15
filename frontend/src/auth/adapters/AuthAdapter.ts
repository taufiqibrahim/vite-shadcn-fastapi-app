export type UserPasswordLoginCredentials = { email: string; password: string };
export type LoginCredentials = UserPasswordLoginCredentials;

export type SimpleLoginResponse = {
  token: string | null;
  message: string | null;
};

export interface UserMe {
  id: number;
  uid: string;
  account_id: number
  full_name: string
}

export type LoginResponse = SimpleLoginResponse;

export interface AuthAdapter {
  login: (credentials: LoginCredentials) => Promise<LoginResponse>;
  logout: () => void;
  getUser: () => Promise<UserMe>;
  refreshToken?: () => Promise<string>;
}
