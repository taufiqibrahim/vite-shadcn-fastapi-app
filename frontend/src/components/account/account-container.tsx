import { useFont } from "@/hooks/use-fonts";
import { ThemeToggle } from "../theme/theme-toggle";

interface AccountAuthContainerProps {
  children?: React.ReactNode;
}

export function AccountAuthContainer({ children }: AccountAuthContainerProps) {
  const { font } = useFont();
  return (
    <div
      className={`flex min-h-screen flex-col justify-center lg:flex-row ${font}`}
    >
      <div className="fixed top-4 right-4 flex items-center gap-2">
        {/* <FontToggle /> */}
        <ThemeToggle />
      </div>
      <div className="flex flex-1 flex-col justify-start px-5 py-24 sm:px-6 lg:px-8 xl:px-12">
        <div className="mx-auto w-full max-w-md sm:w-[400px] border rounded shadow p-4">
          {children}
        </div>
      </div>
    </div>
  );
}
