import { Layout } from "@/components/layout/Layout";
import { GeospatialMappingAppSidebar } from "./components/app-sidebar";

export default function Page() {
  return (
    <Layout SidebarComponent={GeospatialMappingAppSidebar}>
      <div>geospatial</div>
    </Layout>
  );
}
