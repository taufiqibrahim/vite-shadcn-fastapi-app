export interface User {
  email?: string;
  fullName?: string;
  avatar?: string | undefined;
  initials?: string;
}

export interface JwtPayload {
  sub: string;
  id: number;
  exp: number;
  jti: string;
}
