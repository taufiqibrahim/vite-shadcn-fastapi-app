import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Calendar, Filter, ChevronDown, Plus, ShoppingBag } from "lucide-react";
import { motion } from "motion/react";

export interface DemoEmptyStateProps {
  title?: string;
}

export default function DemoEmptyState({
  title = "Order",
}: DemoEmptyStateProps) {
  const [isHoveringOrder, setIsHoveringOrder] = useState(false);

  return (
    <div>
      {/* Orders Empty State */}
      <div>
        <h1 className="text-2xl font-bold mb-6">{title}</h1>

        {/* Controls */}
        <div className="flex flex-wrap items-center justify-between mb-8 gap-4">
          <div className="w-full md:w-auto">
            <Input
              placeholder="Find order..."
              className="h-10 w-full md:w-[300px]"
            />
          </div>

          <div className="flex flex-wrap justify-end items-center gap-3">
            <div className="flex flex-wrap gap-3 mr-2">
              <Button variant="outline" size="sm" className="h-10 gap-1">
                <Filter className="h-4 w-4" />
                Status
                <ChevronDown className="h-3 w-3 opacity-50" />
              </Button>
              <Button variant="outline" size="sm" className="h-10 gap-1">
                <Calendar className="h-4 w-4" />
                Order date
                <ChevronDown className="h-3 w-3 opacity-50" />
              </Button>
            </div>

            <Button variant="outline" size="sm" className="h-10">
              View
              <ChevronDown className="ml-1 h-3 w-3 opacity-50" />
            </Button>

            <Button className="h-10 bg-[#0B2B0B] hover:bg-[#0B2B0B]/90 text-white gap-1">
              <Plus className="h-4 w-4" />
              New Order
            </Button>
          </div>
        </div>

        {/* Empty State */}
        <motion.div
          className="relative border border-dashed border-gray-200 dark:border-gray-800 rounded-xl p-10 flex flex-col items-center justify-center min-h-[350px] bg-gray-50 dark:bg-gray-900/50"
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.4 }}
        >
          {/* Decorative Elements - Minimalistic */}
          <div className="absolute top-0 left-0 w-full h-full overflow-hidden pointer-events-none">
            <div className="absolute -top-4 -right-4 w-16 h-16 bg-primary/5 rounded-full" />
            <div className="absolute bottom-10 -left-6 w-10 h-10 bg-primary/5 rounded-full" />
          </div>

          {/* Main Content */}
          <div className="relative z-4 flex flex-col items-center text-center max-h-[360px]">
            <motion.div
              className="relative mb-6 p-4"
              animate={{
                y: isHoveringOrder ? -5 : 0,
                rotate: isHoveringOrder ? [0, -2, 2, -2, 0] : 0,
              }}
              transition={{ duration: 0.5 }}
              onMouseEnter={() => setIsHoveringOrder(true)}
              onMouseLeave={() => setIsHoveringOrder(false)}
            >
              <div className="absolute inset-0 bg-primary/10 rounded-xl -rotate-6 scale-90 transform-gpu" />
              <div className="absolute inset-0 bg-primary/5 rounded-xl rotate-3 scale-95 transform-gpu" />
              <div className="relative bg-white dark:bg-gray-800 shadow-lg rounded-xl p-6 flex items-center justify-center">
                <ShoppingBag className="h-16 w-16 text-primary" />
              </div>
            </motion.div>

            <h2 className="text-2xl font-bold mb-2">No Orders Yet</h2>
            <p className="text-gray-500 dark:text-gray-400 mb-6 max-w-md">
              Your orders will appear here once customers start placing them.
            </p>

            <Button
              className="h-10 bg-[#0B2B0B] hover:bg-[#0B2B0B]/90 text-white gap-1"
              onMouseEnter={() => setIsHoveringOrder(true)}
              onMouseLeave={() => setIsHoveringOrder(false)}
            >
              <Plus className="h-4 w-4" />
              Create New Order
            </Button>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
