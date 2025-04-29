import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
// import {
//   EyeIcon,
//   EyeOffIcon,
//   MailIcon,
//   LockIcon,
//   UserIcon,
// } from "lucide-react";

import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormDescription,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/auth/use-auth";
// import { Checkbox } from "@/components/ui/checkbox";
// import { useNavigate } from "react-router";
// import { useAuth } from "@/auth/use-auth";
// import { toast } from "sonner";
// import {
//   DEMO_PASSWORD,
//   DEMO_USERNAME,
//   LOGIN_SUCCESS_REDIRECT_URL,
// } from "@/constants";
// import { renderMessage } from "@/lib/utils";

const formSchema = z.object({
  full_name: z
    .string()
    .min(2, { message: "Name must be at least 2 characters" })
    .max(50, { message: "Name cannot exceed 50 characters" }),
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Please enter a valid email address" }),
  // password: z
  //   .string()
  //   .min(8, { message: "Password must be at least 8 characters" })
  //   .regex(/[a-z]/, {
  //     message: "Password must contain at least one lowercase letter",
  //   })
  //   .regex(/[A-Z]/, {
  //     message: "Password must contain at least one uppercase letter",
  //   })
  //   .regex(/[0-9]/, { message: "Password must contain at least one number" }),
  // termsAccepted: z.literal(true, {
  //   errorMap: () => ({ message: "You must accept the terms and conditions" }),
  // }),
});

export function ProfileForm() {
  // Hook for navigation (React Router)
  // const nav = useNavigate();

  // Auth adapter
  const { user } = useAuth();
  const [isLoading, setIsLoading] = useState(false);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      full_name: user?.full_name,
      email: user?.email,
      // password: DEMO_PASSWORD,
      // termsAccepted: true as const,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    console.log(values);
    // const email = values.email;
    // const password = values.password;
    // const full_name = values.name;
    // // Call auth adapter signup function with credentials
    // const { token, message } = await signup({ email, password, full_name });

    // if (token) {
    //   // If login successful, navigate to dashboard
    //   nav(LOGIN_SUCCESS_REDIRECT_URL);
    // } else {
    //   // If login fails, show error message
    //   const data = message ? JSON.parse(message) : "";
    //   toast.error("Signup Failed", { description: renderMessage(data) });
    // }

    setIsLoading(false);
  }

  return (
    <div className="w-full">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="full_name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Full name</FormLabel>
                <FormDescription>
                  The name associated with this account
                </FormDescription>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Full Name"
                    autoComplete="full_name"
                    disabled={isLoading}
                  />
                </FormControl>

                <FormMessage />
              </FormItem>
            )}
          />

          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email address</FormLabel>
                <FormDescription>
                  The email address associated with this account
                </FormDescription>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Email"
                    autoComplete="email"
                    disabled
                    className="bg-muted"
                  />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />

          <Button type="submit" className="w-max" disabled={isLoading}>
            {isLoading ? "Saving..." : "Save"}
          </Button>
        </form>
      </Form>
    </div>
  );
}
