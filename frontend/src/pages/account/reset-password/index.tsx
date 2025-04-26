import { JwtPayload } from "@/auth/types";
import { ResetPasswordForm } from "@/components/account/reset-password-form";
import { Button } from "@/components/ui/button";
import { useFont } from "@/hooks/use-fonts";
import { jwtDecode } from "jwt-decode";
import { KeyRoundIcon } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import { useLocation, useNavigate } from "react-router";

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
  const nav = useNavigate();
  const { font } = useFont();
  const [isTokenExpired, setIsTokenExpired] = useState(false);
  const token = new URLSearchParams(useLocation().search).get("token");

  useEffect(() => {
    if (token) {
      const decoded = jwtDecode<JwtPayload>(token);
      const isExpired = decoded.exp * 1000 < Date.now();
      setIsTokenExpired(isExpired);
    }
  }, [token]);

  return (
    <div
      className={`flex min-h-screen flex-col justify-center lg:flex-row ${font}`}
    >
      <div className="flex flex-1 flex-col justify-start px-5 py-24 sm:px-6 lg:px-8 xl:px-12">
        <div className="mx-auto w-full max-w-md sm:w-[400px] border rounded shadow p-4">
          <div className="flex flex-col space-y-2 text-center mb-8">
            <div className="flex justify-center lg:hidden mb-4">
              <div className="flex items-center justify-center rounded-full bg-primary p-2">
                <KeyRoundIcon className="h-6 w-6 text-primary-foreground" />
              </div>
            </div>
            <h1 className="text-2xl font-semibold tracking-tight">
              {isTokenExpired ? "Link expired!" : "Reset password"}
            </h1>
            <p className="text-sm text-muted-foreground">
              {isTokenExpired
                ? "The reset password link has been expired. Please request a new one"
                : "Enter your new password"}
            </p>
          </div>

          {isTokenExpired ? (
            <div className="mt-2 text-center">
              <Button
                type="button"
                className="w-max"
                onClick={() => nav("/account/forgot-password")}
              >
                Request password reset
              </Button>
            </div>
          ) : (
            <AnimatePresence mode="wait">
              <motion.div
                key="reset-password"
                variants={formContainerVariants}
                initial="hidden"
                animate="visible"
                exit="exit"
              >
                <ResetPasswordForm resetToken={token as string} />
              </motion.div>
            </AnimatePresence>
          )}
        </div>
      </div>
    </div>
  );
}
