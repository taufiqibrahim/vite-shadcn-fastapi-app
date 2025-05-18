import { AccountAuthContainer } from "@/components/account/account-container";
import { SignupForm } from "@/components/account/signup-form";
import { KeyRoundIcon } from "lucide-react";
import { AnimatePresence, motion } from "motion/react";
import { useNavigate } from "react-router";

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

export default function SignupPage() {
  const nav = useNavigate();

  return (
    <AccountAuthContainer>
      <div className="flex flex-col space-y-2 text-center mb-8">
        <div className="flex justify-center lg:hidden mb-4">
          <div className="flex items-center justify-center rounded-full bg-primary p-2">
            <KeyRoundIcon className="h-6 w-6 text-primary-foreground" />
          </div>
        </div>
        <h1 className="text-2xl font-semibold tracking-tight">
          Create an account
        </h1>
        <p className="text-sm text-muted-foreground">
          Enter your information to create an account"
        </p>
      </div>

      <AnimatePresence mode="wait">
        <motion.div
          key="signup"
          variants={formContainerVariants}
          initial="hidden"
          animate="visible"
          exit="exit"
        >
          <SignupForm onLoginClick={() => nav("/login")} />
        </motion.div>
      </AnimatePresence>
    </AccountAuthContainer>
  );
}
