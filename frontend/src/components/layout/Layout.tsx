import { ComponentType, ReactNode } from "react";
import { Header } from "@/components/layout/Header";
import { SidebarInset, SidebarProvider } from "@/components/ui/sidebar";
import { AppSidebar } from "./Sidebar";
import { useAuth } from "@/auth/use-auth";
import { getInitials } from "@/lib/utils";
import { useFont } from "@/hooks/use-fonts";

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
  const { font } = useFont();
  const { user: userData } = useAuth();

  return (
    <div className={`${font}`}>
      {sidebarEnabled && (
        <SidebarProvider>
          <SidebarComponent />
          <SidebarInset>
            {headerEnabled && (
              <Header
                user={{
                  email: userData?.email,
                  avatar: userData?.avatar,
                  fullName: userData?.full_name,
                  initials: getInitials(userData?.email),
                }}
                fixed={fixedHeader}
              />
            )}
            <div className="flex flex-1 flex-col gap-4 px-6 p-4">
              {children}
            </div>
          </SidebarInset>
        </SidebarProvider>
      )}
    </div>
  );
}
