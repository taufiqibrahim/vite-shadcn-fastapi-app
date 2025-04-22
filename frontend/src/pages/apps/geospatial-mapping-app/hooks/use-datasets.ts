import { request } from "@/lib/api";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export interface BBox {
  xmin: number;
  ymin: number;
  xmax: number;
  ymax: number;
}

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
  bbox: BBox;
  primary_key_column: string;
  created_at?: string;
  updated_at?: string;
}

export const useDatasetList = () => {
  return useQuery<Dataset[]>({
    queryKey: ["geospatial-mapping/datasets"],
    queryFn: () => request("/geospatial-mapping/datasets", "GET"),
    staleTime: 1000 * 60 * 5,
    refetchOnWindowFocus: false,
  });
};

export const useDatasetDetail = (uid?: string) => {
  return useQuery<Dataset>({
    queryKey: ["geospatial-mapping/datasets", uid],
    queryFn: () => request(`/geospatial-mapping/datasets/${uid}`, "GET"),
    enabled: !!uid, // Only fetch if id exists
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
