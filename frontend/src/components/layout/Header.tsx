import { User } from "@/auth/types";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";

import { SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";
import { AppBreadcrumbs } from "@/components/layout/Breadcrumbs";
import { UserNav } from "@/components/layout/UserNav";

export interface HeaderProps {
  user: User;
  fixed?: boolean;
  onMenuClick?: () => void;
}

export function Header({ user, fixed = false }: HeaderProps) {
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    if (!fixed) return;

    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, [fixed]);

  return (
    <header
      className={cn(
        "flex h-12 shrink-0 justify-between items-center gap-2 bg-background z-5 border-b bg-background/96 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-5 transition-all duration-200",
        fixed ? "sticky top-0" : "relative",
        scrolled ? "shadow-xs" : "",
      )}
    >
      <div className="flex items-center gap-0 px-0">
        <SidebarTrigger />
        <Separator orientation="vertical" />
        <div>
          <AppBreadcrumbs />
        </div>
      </div>
      <div className="px-4">
        <UserNav user={user} />
      </div>
    </header>
  );
}
