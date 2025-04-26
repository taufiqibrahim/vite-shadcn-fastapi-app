import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { MailIcon } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useNavigate } from "react-router";
import { useAuth } from "@/auth/use-auth";

interface ForgotPasswordFormProps {
  requestSubmitted: boolean;
  setRequestSubmitted: React.Dispatch<React.SetStateAction<boolean>>;
}

const formSchema = z.object({
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Please enter a valid email address" }),
});

export function ForgotPasswordForm({
  requestSubmitted,
  setRequestSubmitted,
}: ForgotPasswordFormProps) {
  const nav = useNavigate();

  // Auth adapter
  const { requestResetPassword } = useAuth();

  const [isLoading, setIsLoading] = useState(false);
  // const { toast } = useToast();

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    const email = values.email;

    // Call auth adapter forgot password function with credentials
    const {} = await requestResetPassword({ email });
    setRequestSubmitted(true);
    setIsLoading(false);
  }

  return (
    <>
      {requestSubmitted ? (
        <div></div>
      ) : (
        <div className="w-full">
          <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
              <FormField
                control={form.control}
                name="email"
                render={({ field }) => (
                  <FormItem>
                    <div className="relative">
                      <FormControl>
                        <div className="relative">
                          <Input
                            {...field}
                            placeholder="Email"
                            className="pl-10"
                            autoComplete="email"
                            disabled={isLoading}
                          />
                          <MailIcon className="absolute left-3 top-1/2 -translate-y-1/2 h-5 w-5 text-muted-foreground" />
                        </div>
                      </FormControl>
                    </div>
                    <FormMessage />
                  </FormItem>
                )}
              />

              <Button
                type="submit"
                className="w-full"
                disabled={
                  isLoading ||
                  form.formState.isLoading ||
                  !form.formState.isValid
                }
              >
                {isLoading
                  ? "Sending reset password link..."
                  : "Reset password"}
              </Button>
            </form>
          </Form>

          <div className="mt-6 text-center">
            <p className="text-sm text-muted-foreground">
              Back to{" "}
              <Button
                variant="link"
                className="p-0"
                onClick={() => nav("/login")}
                disabled={isLoading}
              >
                Log in
              </Button>
            </p>
          </div>
        </div>
      )}
    </>
  );
}
