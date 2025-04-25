import { ForgotPasswordForm } from "@/components/auth/forgot-password-form";
import { LoginForm } from "@/components/auth/login-form";
import { SignupForm } from "@/components/auth/signup-form";
import { ThemeToggle } from "@/components/theme/theme-toggle";
import { useFont } from "@/hooks/use-fonts";
import { KeyRoundIcon } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useState } from "react";

const formContainerVariants = {
  hidden: { opacity: 0, x: -20 },
  visible: {
    opacity: 1,
    x: 0,
    transition: { type: "spring", stiffness: 300, damping: 30 },
  },
  exit: {
    opacity: 0,
    x: 20,
    transition: { duration: 0.2 },
  },
};

export default function Page() {
  const [formType, setFormType] = useState<"login" | "signup" | "forgot">(
    "login",
  );
  const { font } = useFont();
  const showLogin = () => setFormType("login");
  const showSignUp = () => setFormType("signup");
  const showForgot = () => setFormType("forgot");

  return (
    <div
      className={`flex min-h-screen flex-col justify-center lg:flex-row ${font}`}
    >
      {/* Theme and Font Toggles */}
      <div className="fixed top-4 right-4 flex items-center gap-2">
        {/* <FontToggle /> */}
        <ThemeToggle />
      </div>

      {/* Right Side - Form */}
      <div className="flex flex-1 flex-col justify-start px-5 py-24 sm:px-6 lg:px-8 xl:px-12">
        <div className="mx-auto w-full max-w-md sm:w-[400px] border rounded shadow p-4">
          <div className="flex flex-col space-y-2 text-center mb-8">
            <div className="flex justify-center lg:hidden mb-4">
              <div className="flex items-center justify-center rounded-full bg-primary p-2">
                <KeyRoundIcon className="h-6 w-6 text-primary-foreground" />
              </div>
            </div>
            <h1 className="text-2xl font-semibold tracking-tight">
              {formType === "signup" && "Create an account"}
              {formType === "login" && "Welcome back"}
              {formType === "forgot" && "Reset password"}
            </h1>
            <p className="text-sm text-muted-foreground">
              {formType === "signup" &&
                "Enter your information to create an account"}
              {formType === "login" &&
                "Enter your credentials to access your account"}
              {formType === "forgot" &&
                "Enter your email address and we'll send you a link to reset your password."}
            </p>
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key={formType}
              variants={formContainerVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
            >
              {formType === "login" && (
                <LoginForm
                  onSignUpClick={showSignUp}
                  onForgotClick={showForgot}
                />
              )}
              {formType === "signup" && <SignupForm onLoginClick={showLogin} />}
              {formType === "forgot" && (
                <ForgotPasswordForm onLoginClick={showLogin} />
              )}
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
