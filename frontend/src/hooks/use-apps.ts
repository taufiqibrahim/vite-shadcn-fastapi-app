import { useQuery } from "@tanstack/react-query";
import { request } from "@/lib/api";

export const useAppList = () => {
  return useQuery({
    queryKey: ["apps"],
    queryFn: () => request("/apps", "GET"),
    staleTime: 1000 * 60 * 5, // Cache for 5 minutes
    enabled: true,
    refetchOnWindowFocus: false,
  });
};
