import { request } from "@/lib/api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export interface Dataset {
  id?: string;
  uid: string;
  account_id: number;
  name: string;
  description: string;
  file_name: string;
  storage_backend: string;
  storage_uri: string;
  status: "uploaded" | "processing" | "ready" | "failed";
  created_at?: string;
}

export const useDatasetList = () => {
  return useQuery<Dataset[]>({
    queryKey: ["geospatial-mapping/datasets"],
    queryFn: () => request("/geospatial-mapping/datasets", "GET"),
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
  });
};

export const useCreateDataset = () => {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (newDataset: Partial<Dataset>) =>
      request("geospatial-mapping/datasets", "POST", newDataset),
    onSuccess: () => {
      queryClient.invalidateQueries({
        queryKey: ["geospatial-mapping/datasets"],
      });
    },
    retry: false,
  });
};
