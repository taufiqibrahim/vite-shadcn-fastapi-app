import { request } from "@/lib/api";
import { useQuery } from "@tanstack/react-query";

export const useDatasetTable = (uid?: string) => {
  return useQuery({
    queryKey: ["geospatial-mapping/datasets", uid, "content"],
    queryFn: () => request(`/geospatial-mapping/datasets/${uid}/table`, "GET"),
    enabled: !!uid,
    refetchOnWindowFocus: false,
    retry: false,
  });
};

export const useDatasetFeatures = (
  uid?: string,
  bbox?: [number, number, number, number] | null,
) => {
  const bboxQuery = bbox?.join(",");
  return useQuery({
    queryKey: ["geospatial-mapping/datasets", uid, "features", bboxQuery],
    queryFn: () =>
      request(`/geospatial-mapping/datasets/${uid}/features`, "GET", {
        bbox: bboxQuery,
      }),
    enabled: !!uid && !!bbox,
    refetchOnWindowFocus: false,
    retry: false,
  });
};

// export const useDatasetMVT = (uid?: string,) => {
//   return useQuery({
//     queryKey: ["geospatial-mapping/datasets", uid, 'features', bbox],
//     queryFn: () => request(`/geospatial-mapping/datasets/${uid}/tiles/{z}/{x}/{y}.pbf`, "GET", { bbox }),
//     enabled: !!uid,
//     refetchOnWindowFocus: false,
//   });
// };
