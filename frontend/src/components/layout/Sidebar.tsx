import {
  Blocks,
  Boxes,
  ChartAreaIcon,
  CreditCardIcon,
  Settings,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { APP_NAME, LOGIN_SUCCESS_REDIRECT_URL } from "@/constants";

export function AppSidebar() {
  const items = [
    {
      title: "Apps",
      url: "/apps",
      icon: Boxes,
    },
    {
      title: "Billing",
      url: "/billing",
      icon: CreditCardIcon,
    },
    {
      title: "Usage",
      url: "/usage",
      icon: ChartAreaIcon,
    },
    {
      title: "Settings",
      url: "/settings",
      icon: Settings,
    },
  ];

  return (
    <Sidebar>
      <SidebarHeader className="p-0 max-h-12">
        <SidebarMenu>
          <SidebarMenuButton size="lg" asChild>
            <a href={LOGIN_SUCCESS_REDIRECT_URL}>
              <div className="flex size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <Blocks className="size-4" />
              </div>
              <div className="flex flex-col gap-0 leading-none">
                <span className="font-semibold">{APP_NAME}</span>
                <span className="text-xs text-zinc-500">v0.0.0</span>
              </div>
            </a>
          </SidebarMenuButton>
        </SidebarMenu>
      </SidebarHeader>

      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupContent>
            <SidebarMenu>
              {items.map((item) => (
                <SidebarMenuItem key={item.title}>
                  <SidebarMenuButton asChild>
                    <a href={item.url}>
                      <item.icon />
                      <span>{item.title}</span>
                    </a>
                  </SidebarMenuButton>
                </SidebarMenuItem>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
