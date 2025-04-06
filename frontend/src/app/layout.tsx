import {
  SidebarInset,
  SidebarProvider,
  SidebarTrigger,
} from "@/components/ui/sidebar";
import { AppSidebar } from "@/components/app-sidebar";
import { NavUser } from "@/components/nav-user";

export default function Layout({ children }: { children: React.ReactNode }) {
  const user = {
    name: "Demo",
    email: "demo@example.com",
    avatar: "/avatars/shadcn.jpg",
    initials: "D",
  };
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <div>
          <header className="w-full sticky top-0 flex w-full h-12 items-center justify-between gap-2 border-b bg-background px-1">
            <div className="flex items-center gap-2">
              <SidebarTrigger />
              <div>
                <h1>App</h1>
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
        <div className="px-2">{children}</div>
      </SidebarInset>
    </SidebarProvider>
  );
}
