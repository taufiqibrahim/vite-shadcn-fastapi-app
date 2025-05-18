import { useState, ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { motion } from "motion/react";
import { Plus } from "lucide-react";

export interface EntityListLayoutProps {
  title?: string;
  searchPlaceholder?: string;
  filters?: ReactNode;
  viewOptions?: ReactNode;
  icon?: ReactNode;
  emptyTitle?: string;
  emptyDescription?: string;
  ctaLabel?: string;
  onCreate?: () => void;
  children?: ReactNode; // list content (table, cards, etc.)
}

export default function EntityListLayout({
  title = "Items",
  searchPlaceholder = "Search...",
  filters,
  viewOptions,
  icon,
  emptyTitle = `No ${title} Yet`,
  emptyDescription = `Your ${title.toLowerCase()} will appear here once created.`,
  ctaLabel = `Create New ${title}`,
  onCreate,
  children,
}: EntityListLayoutProps) {
  const [isHovering, setIsHovering] = useState(false);

  const isEmpty = !children;

  return (
    <div>
      <h1 className="text-2xl font-bold mb-6">{title}</h1>

      {/* Controls */}
      <div className="flex flex-wrap items-center justify-between mb-8 gap-4">
        <div className="w-full md:w-auto">
          <Input
            placeholder={searchPlaceholder}
            className="h-10 w-full md:w-[300px]"
          />
        </div>

        <div className="flex flex-wrap justify-end items-center gap-3">
          <div className="flex flex-wrap gap-3 mr-2">{filters}</div>
          {viewOptions}
          <Button
            className="h-10 bg-[#0B2B0B] hover:bg-[#0B2B0B]/90 text-white gap-1"
            onClick={onCreate}
          >
            <Plus className="h-4 w-4" />
            {ctaLabel}
          </Button>
        </div>
      </div>

      {/* Content or Empty State */}
      {isEmpty ? (
        <motion.div
          className="relative border border-dashed border-gray-200 dark:border-gray-800 rounded-xl p-10 flex flex-col items-center justify-center min-h-[350px] bg-gray-50 dark:bg-gray-900/50"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          {/* Background accents */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
            <div className="absolute -top-4 -right-4 w-16 h-16 bg-primary/5 rounded-full" />
            <div className="absolute bottom-10 -left-6 w-10 h-10 bg-primary/5 rounded-full" />
          </div>

          <div className="relative z-10 flex flex-col items-center text-center max-h-[360px]">
            <motion.div
              className="relative mb-6 p-4"
              animate={{
                y: isHovering ? -5 : 0,
                rotate: isHovering ? [0, -2, 2, -2, 0] : 0,
              }}
              transition={{ duration: 0.5 }}
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
            >
              <div className="absolute inset-0 bg-primary/10 rounded-xl -rotate-6 scale-90 transform-gpu" />
              <div className="absolute inset-0 bg-primary/5 rounded-xl rotate-3 scale-95 transform-gpu" />
              <div className="relative bg-white dark:bg-gray-800 shadow-lg rounded-xl p-6 flex items-center justify-center">
                {icon}
              </div>
            </motion.div>

            <h2 className="text-2xl font-bold mb-2">{emptyTitle}</h2>
            <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-md">
              {emptyDescription}
            </p>

            <Button
              className="h-10 bg-[#0B2B0B] hover:bg-[#0B2B0B]/90 text-white gap-1"
              onClick={onCreate}
              onMouseEnter={() => setIsHovering(true)}
              onMouseLeave={() => setIsHovering(false)}
            >
              <Plus className="h-4 w-4" />
              {ctaLabel}
            </Button>
          </div>
        </motion.div>
      ) : (
        <div>{children}</div>
      )}
    </div>
  );
}
