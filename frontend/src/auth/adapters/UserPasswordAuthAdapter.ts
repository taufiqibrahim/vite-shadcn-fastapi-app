import { AuthAdapter, LoginCredentials, LoginResponse } from "./AuthAdapter";

const demoEmail = import.meta.env.VITE_DEMO_USERNAME;
const demoPassword = import.meta.env.VITE_DEMO_PASSWORD;

export class UserPasswordAuthAdapter implements AuthAdapter {
  async login(credentials: LoginCredentials): Promise<LoginResponse> {
    if (
      credentials.email === demoEmail &&
      credentials.password === demoPassword
    ) {
      return { token: "dummytoken", message: "Login successful" };
    } else return { token: null, message: "Invalid username or password" };
  }

  logout() {}

  async getUser(): Promise<any> {}

  async refreshToken(): Promise<any> {}
}
