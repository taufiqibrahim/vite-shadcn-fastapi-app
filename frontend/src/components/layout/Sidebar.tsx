import {
  Blocks,
  Building2Icon,
  CircleUserRoundIcon,
  KeyIcon,
  Settings,
} from "lucide-react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
} from "@/components/ui/sidebar";
import { APP_NAME, LOGIN_SUCCESS_REDIRECT_URL } from "@/constants";
import { useLocation } from "react-router";
import { Separator } from "../ui/separator";

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { pathname } = useLocation();

  const navMain = [
    // {
    //   title: "Apps",
    //   url: "/apps",
    //   icon: Boxes,
    //   isActive: false,
    // },
    // {
    //   title: "Usage",
    //   url: "/usage",
    //   icon: ChartAreaIcon,
    // },
    {
      title: "SETTINGS",
      url: "/settings",
      icon: Settings,
      items: [
        {
          title: "PROFILE",
          url: "/settings/profile",
          icon: CircleUserRoundIcon,
          items: [
            {
              title: "Your profile",
              url: "/settings/profile/user",
              icon: CircleUserRoundIcon,
              isActive: false,
            },
          ],
        },
        {
          title: "ORGANIZATIONS",
          url: "/settings/organizations",
          icon: Building2Icon,
          isActive: false,
          items: [
            {
              title: "General",
              url: "/settings/organizations/general",
              icon: CircleUserRoundIcon,
              isActive: false,
            },
            {
              title: "API Keys",
              url: "/settings/organizations/api-keys",
              icon: KeyIcon,
              isActive: false,
            },
          ],
        },
      ],
    },
  ];

  // function getItemActiveState(item: { title: string; url: string; icon: ForwardRefExoticComponent<Omit<LucideProps, "ref"> & RefAttributes<SVGSVGElement>>; isActive: boolean; }): boolean | undefined {
  //   throw new Error("Function not implemented.");
  // }

  const getItemActiveState = (url: string) => {
    if (url === pathname) {
      return true;
    }
    return false;
  };

  return (
    <Sidebar {...props}>
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
        {navMain.map((item) => (
          <SidebarGroup key={item.url}>
            <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
            <SidebarGroupContent>
              <SidebarMenu>
                {item.items?.map((item) =>
                  item.items && item.items?.length > 0 ? (
                    <SidebarGroup key={item.url} className="p-0">
                      <SidebarGroupLabel>{item.title}</SidebarGroupLabel>
                      <SidebarGroupContent>
                        <SidebarMenu>
                          {item.items?.map((item) => (
                            <SidebarMenuItem key={item.url}>
                              <SidebarMenuButton
                                asChild
                                isActive={getItemActiveState(item.url)}
                                className={`${getItemActiveState(item.url) ? "bg-accent" : ""}`}
                              >
                                <a
                                  href={item.url}
                                  className={`${getItemActiveState(item.url) ? "!font-bold" : "text-muted-foreground"}`}
                                >
                                  {item.title}
                                </a>
                              </SidebarMenuButton>
                            </SidebarMenuItem>
                          ))}
                        </SidebarMenu>
                      </SidebarGroupContent>
                      <div className="flex h-2 items-end">
                        <Separator />
                      </div>
                    </SidebarGroup>
                  ) : (
                    <SidebarMenuItem key={item.url}>
                      <SidebarMenuButton
                        asChild
                        isActive={getItemActiveState(item.url)}
                        className={`${getItemActiveState(item.url) ? "bg-accent" : ""}`}
                      >
                        <a
                          href={item.url}
                          className={`${getItemActiveState(item.url) ? "!font-bold" : "text-muted-foreground"}`}
                        >
                          {item.title}
                        </a>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  ),
                )}
              </SidebarMenu>
            </SidebarGroupContent>
          </SidebarGroup>
        ))}
      </SidebarContent>
      <SidebarFooter />
    </Sidebar>
  );
}
