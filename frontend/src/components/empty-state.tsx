import { InboxIcon } from "lucide-react";

export const BasicEmptyState = () => {
  return (
    <div className="flex flex-col items-center justify-center h-[50vh] gap-6">
      <div className="flex items-center justify-center w-20 h-20 bg-gray-100 rounded-full dark:bg-gray-800">
        <InboxIcon size={40} strokeWidth={1} />
      </div>
      <div className="space-y-2 text-center">
        <h2 className="text-2xl font-bold tracking-tight">
          No data to display
        </h2>
        <p className="text-gray-500 dark:text-gray-400">
          It looks like there's no data available yet. Try adding some new
          items.
        </p>
      </div>
    </div>
  );
};
