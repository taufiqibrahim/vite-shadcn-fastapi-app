export type LoginCredentials = { email: string; password: string };
export type SignupCredentials = {
  email: string;
  password: string;
  full_name?: string | null | undefined;
};

export type LoginResponse = {
  token: string | null;
  message: string | null;
};

export type SignupResponse = {
  token: string | null;
  message: string | null;
};

export interface UserMe {
  id: number;
  uid: string;
  account_id: number;
  full_name: string;
}

export interface AuthAdapter {
  signup: (credentials: SignupCredentials) => Promise<SignupResponse>;
  login: (credentials: LoginCredentials) => Promise<LoginResponse>;
  logout: () => void;
  forgotPassword?: () => void;
  getUser: () => Promise<UserMe>;
  refreshToken?: () => Promise<string>;
}
