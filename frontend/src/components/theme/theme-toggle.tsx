import { Moon, Sun } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { useTheme } from "next-themes";
import { useFont } from "@/hooks/use-fonts";

export function ThemeToggle() {
  const { setTheme } = useTheme();
  const { setFont } = useFont();

  const handleThemeChange = (theme: string, font?: string) => {
    setTheme(theme);
    if (font) {
      setFont(font);
    }
  };

  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button variant="ghost" size="icon" className="h-8 w-8">
          <Sun className="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => handleThemeChange("light")}>
          Light
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleThemeChange("dark")}>
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => handleThemeChange("system")}>
          System
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={() => {
            handleThemeChange("theme-facebook");
            setFont("font-helvetica");
          }}
        >
          Facebook
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => {
            handleThemeChange("theme-instagram");
            setFont("font-sf-pro");
          }}
        >
          Instagram
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => {
            handleThemeChange("theme-airbnb");
            setFont("font-circular");
          }}
        >
          Airbnb
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
