import { User } from "@/auth/types";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { ACCESS_TOKEN_KEY } from "@/constants";
import { LogOut } from "lucide-react";

export interface UserNavProps {
  user: User;
  isOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function UserNav({ user, isOpen, onOpenChange }: UserNavProps) {
  const handleLogout = (event: any) => {
    event.preventDefault();
    localStorage.removeItem(ACCESS_TOKEN_KEY);
    window.location.reload();
  };

  return (
    <DropdownMenu open={isOpen} onOpenChange={onOpenChange}>
      <DropdownMenuTrigger asChild>
        <Avatar className="h-8 w-8 border cursor-pointer shadow-xs">
          <AvatarImage src={user.avatar} alt={user.fullName} />
          <AvatarFallback className="rounded-lg bg-background hover:bg-accent hover:text-accent-foreground">
            {user.initials}
          </AvatarFallback>
        </Avatar>
      </DropdownMenuTrigger>
      <DropdownMenuContent
        className="w-[--radix-dropdown-menu-trigger-width] min-w-56 rounded-lg"
        side="bottom"
        align="end"
      >
        <DropdownMenuLabel className="p-0 font-normal">
          <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
            <Avatar className="h-8 w-8 rounded-lg">
              <AvatarImage src={user.avatar} alt={user.fullName} />
              <AvatarFallback className="rounded-lg">
                {user.initials}
              </AvatarFallback>
            </Avatar>
            <div className="grid flex-1 text-left text-sm leading-tight">
              <span className="truncate font-semibold">{user.fullName}</span>
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
  );
}
