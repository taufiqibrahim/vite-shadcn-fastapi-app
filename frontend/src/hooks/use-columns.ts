import { useMemo } from "react";

export function useColumns(data: any[]) {
  return useMemo(() => {
    if (!data || data.length === 0) return [];

    const sample = data[0];

    return Object.keys(sample).map((key) => ({
      accessorKey: key,
      header: key.charAt(0).toUpperCase() + key.slice(1),
    }));
  }, [data]);
}
