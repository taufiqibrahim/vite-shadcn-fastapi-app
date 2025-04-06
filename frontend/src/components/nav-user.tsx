import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { SidebarMenu, SidebarMenuButton } from "@/components/ui/sidebar";
import { ACCESS_TOKEN_KEY } from "@/constants";
import { LogOut } from "lucide-react";

export function NavUser({
  user,
}: {
  user: {
    name: string;
    email: string;
    avatar: string;
    initials: string;
  };
}) {
  const handleLogout = (event: any) => {
    event.preventDefault();
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    window.location.reload();
  };

  return (
    <SidebarMenu>
      <DropdownMenu>
        <DropdownMenuTrigger asChild>
          <SidebarMenuButton
            size="lg"
            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground md:h-8 w-8 rounded-full p-0"
          >
            <Avatar className="h-8 w-8 rounded-full border-2 border-primary">
              <AvatarImage src={user.avatar} alt={user.name} />
              {/* <AvatarImage src="https://github.com/shadcn.png" /> */}
              <AvatarFallback className="rounded-lg">
                {user.initials}
              </AvatarFallback>
            </Avatar>
          </SidebarMenuButton>
        </DropdownMenuTrigger>
        <DropdownMenuContent
          className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
          side="bottom"
          align="end"
        >
          <DropdownMenuLabel className="p-0 font-normal">
            <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
              <Avatar className="h-8 w-8 rounded-lg">
                <AvatarImage src={user.avatar} alt={user.name} />
                <AvatarFallback className="rounded-lg">
                  {user.initials}
                </AvatarFallback>
              </Avatar>
              <div className="grid flex-1 text-left text-sm leading-tight">
                <span className="truncate font-semibold">{user.name}</span>
                <span className="truncate text-xs">{user.email}</span>
              </div>
            </div>
          </DropdownMenuLabel>
          <DropdownMenuItem onClick={(e: any) => handleLogout(e)}>
            <LogOut />
            Log out
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
    </SidebarMenu>
  );
}
