import { ComponentType, ReactNode } from "react";
import Header from "./Header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "./Sidebar";

export interface LayoutProps {
  children: ReactNode;
  sidebarEnabled?: boolean;
  headerEnabled?: boolean;
  fixedHeader?: boolean;
  // showHelpButton?: boolean;
  SidebarComponent?: ComponentType;
}

export function Layout({
  children,
  sidebarEnabled = true,
  SidebarComponent = AppSidebar,
  headerEnabled = true,
  fixedHeader = true,
  // showHelpButton = false,
}: LayoutProps) {
  const user = {
    name: "Demo",
    email: "demo@example.com",
    avatar: "https://github.com/shadcn.png",
    initials: "D",
  };

  // const RenderedSidebar = SidebarComponent || AppSidebar;

  return (
    <div className="">
      {sidebarEnabled && (
        <SidebarProvider>
          <SidebarComponent />
          <SidebarInset>
            {headerEnabled && <Header user={user} fixed={fixedHeader} />}
            <div className="flex flex-1 flex-col gap-4 p-4">{children}</div>
          </SidebarInset>
        </SidebarProvider>
      )}
    </div>
  );
}
