import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { NavUser } from "@/components/nav-user";
import { ComponentType, ReactNode } from "react";
import { Toaster } from "sonner";

interface LayoutProps {
  children: ReactNode;
  SidebarComponent?: ComponentType;
}

export default function Layout({ children, SidebarComponent }: LayoutProps) {
  const user = {
    name: "Demo",
    email: "demo@example.com",
    avatar: "/avatars/shadcn.jpg",
    initials: "D",
  };

  // Fallback to AppSidebar if none is passed
  const RenderedSidebar = SidebarComponent || AppSidebar;

  return (
    <SidebarProvider>
      <RenderedSidebar />
      <SidebarInset>
        <div>
          <header className="w-full sticky top-0 flex w-full h-12 items-center justify-between gap-2 border-b bg-background px-1">
            <div className="flex items-center gap-2">
              <SidebarTrigger />
              <div>
                <h1>TODO:Breadcrumb</h1>
              </div>
            </div>
            <div className="ml-auto px-3">
              <NavUser
                user={{
                  name: user?.name,
                  email: user?.email,
                  avatar: user?.avatar ?? "/avatars/shadcn.jpg",
                  initials: user?.initials ?? "IC",
                }}
              />
            </div>
          </header>
        </div>
        <div className="p-2">{children}</div>
        <Toaster />
      </SidebarInset>
    </SidebarProvider>
  );
}
