import { ColumnDef } from "@tanstack/react-table";
import { Dataset } from "@/pages/apps/geospatial-mapping-app/hooks/use-datasets";

export const columns: ColumnDef<Dataset>[] = [
  {
    accessorKey: "name",
    header: "Name",
    cell: ({ row }) => {
      return (
        <a
          href={`/apps/geospatial-mapping-app/datasets/${row.original.uid}`}
          className="text-sm font-medium text-primary hover:underline hover:text-primary/80 transition-colors"
        >
          {row.original.name}
        </a>
      );
    },
  },
];
