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

interface ThemeToggleProps {
  isOpen?: boolean;
  onOpenChange?: (open: boolean) => void;
}

export function ThemeToggle({ isOpen, onOpenChange }: ThemeToggleProps) {
  const { setTheme } = useTheme();
  const { setFont } = useFont();

  // an array of all possible custom themes
  const customThemes = [
    { label: "Facebook", theme: "theme-facebook", font: "font-helvetica" },
    { label: "Instagram", theme: "theme-instagram", font: "font-sf-pro" },
    { label: "Airbnb", theme: "theme-airbnb", font: "font-circular" },
  ];
  const THEME_CLASSES = customThemes.map((t) => t.theme);

  const handleThemeChange = (theme: string, font?: string) => {
    /**
     * Every time the user selects a new custom theme:
     * It removes all previous custom themes safely (html.classList.remove(...THEME_CLASSES)).
     * It adds the selected custom theme (html.classList.add(themeClass)).
     * It does NOT touch any other classes (like dark, light, system, etc.).
     */
    const html = document.documentElement;

    // Remove any previous custom theme classes
    html.classList.remove(...THEME_CLASSES);

    // Add the new custom theme
    html.classList.add(theme);

    setTheme(theme);
    if (font) {
      setFont(font);
    }
  };

  return (
    <DropdownMenu open={isOpen} onOpenChange={onOpenChange}>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="relative h-8 w-8 rounded-full border border-input text-xs font-semibold uppercase"
          data-dropdown-trigger
        >
          <Sun className="h-8 w-8 rotate-0 scale-120 transition-all dark:-rotate-90 dark:scale-0" />
          <Moon className="absolute h-8 w-8 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-120" />
          <span className="sr-only">Toggle theme</span>
        </Button>
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem
          onClick={() => handleThemeChange("light", "font-sans")}
        >
          Light
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => handleThemeChange("dark", "font-opensans")}
        >
          Dark
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => handleThemeChange("system", "font-sans")}
        >
          System
        </DropdownMenuItem>
        <DropdownMenuSeparator />
        <DropdownMenuItem
          onClick={() => handleThemeChange("theme-facebook", "font-helvetica")}
        >
          Facebook
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => handleThemeChange("theme-instagram", "font-sf-pro")}
        >
          Instagram
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() => handleThemeChange("theme-airbnb", "font-circular")}
        >
          Airbnb
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}
