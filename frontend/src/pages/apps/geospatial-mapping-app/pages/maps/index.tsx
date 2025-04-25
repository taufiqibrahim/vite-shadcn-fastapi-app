import { Layout } from "@/components/layout/Layout";
import { GeospatialMappingAppSidebar } from "@/pages/apps/geospatial-mapping-app/components/app-sidebar";
import { useDatasetList } from "@/pages/apps/geospatial-mapping-app/hooks/use-datasets";

export default function Page() {
  const { data: datasets } = useDatasetList();
  console.debug(datasets);
  return (
    <Layout SidebarComponent={GeospatialMappingAppSidebar}>
      <h1 className="scroll-m-20 text-2xl font-bold tracking-tight">Maps</h1>

      {datasets && datasets.length > 0 ? (
        <div>TODO: Maps</div>
      ) : (
        <div>Empty</div>
      )}
    </Layout>
  );
}
