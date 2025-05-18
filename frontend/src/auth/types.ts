// export interface User {
//   email?: string;
//   fullName?: string;
//   avatar?: string | undefined;
//   initials?: string;
// }

export interface JwtPayload {
  sub: string;
  id: number;
  exp: number;
  jti: string;
}

export type LoginCredentials = { email: string; password: string };
export type SignupCredentials = {
  email: string;
  password: string;
  full_name: string;
};
export type RequestResetPasswordCredentials = { email: string };
export type ResetPasswordCredentials = { resetToken: string; password: string };

export type LoginResponse = {
  token: string | null;
  message: string | null;
};

export type SignupResponse = {
  token: string | null;
  message: string | null;
};

export type ResetPasswordResponse = {
  token: string | null;
  message: string | null;
};