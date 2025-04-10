import { Separator } from "@/components/ui/separator";
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
import { ArrowLeftCircle, Blocks, Boxes, StepBack } from "lucide-react";

const APP_NAME = "Geospatial Mapping App";
const APP_VERSION = "0.0.1";

export function GeospatialMappingAppSidebar() {
  const items = [
    {
      title: "Datasets",
      url: "/apps/geospatial-mapping-app/datasets",
      icon: Boxes,
    },
  ];

  return (
    <Sidebar>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuButton size="sm" asChild>
            <a href="/apps">
              <div className="flex aspect-square size-8 items-center justify-center">
                <ArrowLeftCircle className="size-4" />
              </div>
              Back to Apps
            </a>
          </SidebarMenuButton>
          <Separator />
          <SidebarMenuButton size="lg" asChild>
            <div>
              <div className="flex aspect-square size-8 items-center justify-center rounded-lg bg-sidebar-primary text-sidebar-primary-foreground">
                <Blocks className="size-4" />
              </div>
              <div className="flex flex-col gap-0.5 leading-none">
                <span className="font-semibold">{APP_NAME}</span>
                <span className="text-xs text-zinc-500">{APP_VERSION}</span>
              </div>
            </div>
          </SidebarMenuButton>
        </SidebarMenu>
      </SidebarHeader>
      <Separator />
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
