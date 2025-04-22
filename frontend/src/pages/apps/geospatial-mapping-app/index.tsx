import Layout from "@/app/layout";
import { GeospatialMappingAppSidebar } from "./components/app-sidebar";

export default function Page() {
  return (
    <Layout SidebarComponent={GeospatialMappingAppSidebar}>
      <div>geospatial</div>
    </Layout>
  );
}
