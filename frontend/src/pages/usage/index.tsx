import DemoEmptyState from "@/components/demo/EmptyStateDemo";
import { Layout } from "@/components/layout/Layout";

export default function Page() {
  return (
    <Layout>
      <div className="w-full max-w-7xl space-y-12">
        <DemoEmptyState title="Usage" />
      </div>
    </Layout>
  );
}
