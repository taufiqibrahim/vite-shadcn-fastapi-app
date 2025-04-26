import { ForgotPasswordForm } from "@/components/auth/forgot-password-form";
import { LoginForm } from "@/components/auth/login-form";
import { SignupForm } from "@/components/auth/signup-form";
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
  const { font } = useFont();

  return (
    <div
      className={`flex min-h-screen flex-col justify-center lg:flex-row ${font}`}
    >
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
              Reset password
            </h1>
            <p className="text-sm text-muted-foreground">
              Enter your new password
            </p>
          </div>

          <AnimatePresence mode="wait">
            <motion.div
              key="reset-password"
              variants={formContainerVariants}
              initial="hidden"
              animate="visible"
              exit="exit"
            >
              <ResetPasswordForm />
            </motion.div>
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
