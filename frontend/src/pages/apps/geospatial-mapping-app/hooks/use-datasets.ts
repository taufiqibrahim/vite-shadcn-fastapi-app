import { useQuery } from "@tanstack/react-query";

export interface Dataset {
  id: string;
  name: string;
  status: "active" | "draft" | "archived"; // expand as needed
}

export const useDatasetList = () => {
  return useQuery<Dataset[]>({
    queryKey: ["geospatial-mapping-apps/datasets"],
    queryFn: async () => {
      // TODO: Replace with `request("/apps", "GET")` later
      return [
        { id: "1", name: "Map Editor", status: "active" },
        { id: "2", name: "GeoAnalytics", status: "draft" },
      ];
    },
    //   API
    // queryFn: () => request("/apps", "GET"),
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
  });
};
