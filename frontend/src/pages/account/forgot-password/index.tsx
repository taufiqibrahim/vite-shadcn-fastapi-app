import { AccountAuthContainer } from "@/components/account/account-container";
import { ForgotPasswordForm } from "@/components/account/forgot-password-form";
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
  const [requestSubmitted, setRequestSubmitted] = useState<boolean>(false);

  return (
    <AccountAuthContainer>
      <div className="flex flex-col space-y-2 text-center mb-8">
        <div className="flex justify-center lg:hidden mb-4">
          <div className="flex items-center justify-center rounded-full bg-primary p-2">
            <KeyRoundIcon className="h-6 w-6 text-primary-foreground" />
          </div>
        </div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Forgot password
        </h1>
        <p className="text-sm text-muted-foreground">
          {requestSubmitted
            ? "Email has been sent. Please check your inbox for reset password link."
            : "Enter your email address and we'll send you a link to reset your password."}
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
          <ForgotPasswordForm
            requestSubmitted={requestSubmitted}
            setRequestSubmitted={setRequestSubmitted}
          />
        </motion.div>
      </AnimatePresence>
    </AccountAuthContainer>
  );
}
