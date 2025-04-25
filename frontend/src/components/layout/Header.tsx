import { User } from "@/auth/types";
import { cn } from "@/lib/utils";
import { useEffect, useState } from "react";
import UserNav from "./UserNav";
import { SidebarTrigger } from "@/components/ui/sidebar";
import { Separator } from "@/components/ui/separator";

export interface HeaderProps {
  user: User;
  fixed?: boolean;
  onMenuClick?: () => void;
}

export default function Header({ user, fixed = false }: HeaderProps) {
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
        "flex h-14 shrink-0 justify-between items-center gap-2 bg-background z-5 border-b bg-background/96 backdrop-blur supports-[backdrop-filter]:bg-background/60 z-5 transition-all duration-200",
        fixed ? "sticky top-0" : "relative",
        scrolled ? "shadow-xs" : "",
      )}
    >
      <div className="flex items-center gap-2 px-2">
        <SidebarTrigger />
        <Separator orientation="vertical" />
        <div>[Breadcrumb]</div>
      </div>
      <div className="px-4">
        <UserNav user={user} />
      </div>
    </header>
  );
}
