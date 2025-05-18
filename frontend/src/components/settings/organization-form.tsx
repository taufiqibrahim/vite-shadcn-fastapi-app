import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";

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

const formSchema = z.object({
  organization_name: z
    .string()
    .min(2, { message: "Name must be at least 2 characters" })
    .max(50, { message: "Name cannot exceed 50 characters" }),
  email: z
    .string()
    .min(1, { message: "Email is required" })
    .email({ message: "Please enter a valid email address" }),
});

export function OrganizationForm() {
  const { user: userData } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const defaultOrg = userData?.organizations.find(org => org.is_default_org);

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      organization_name: defaultOrg?.name,
      email: userData?.email,
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setIsLoading(true);
    // Logic here
    setIsLoading(false);
  }

  return (
    <div className="w-full">
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
          <FormField
            control={form.control}
            name="organization_name"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Organization name</FormLabel>
                <FormDescription>
                  Human-friendly label for your organization, shown in user
                  interfaces
                </FormDescription>
                <FormControl>
                  <Input
                    {...field}
                    placeholder="Organization Name"
                    autoComplete="organization_name"
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

          <Button
            type="submit"
            className="w-max"
            disabled={
              isLoading ||
              form.formState.isLoading ||
              !form.formState.isValid ||
              !form.formState.isDirty
            }
          >
            {isLoading ? "Saving..." : "Save"}
          </Button>
        </form>
      </Form>
    </div>
  );
}
