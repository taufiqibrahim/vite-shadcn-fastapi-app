import DemoEmptyState from "@/components/demo/EmptyStateDemo";
import { Layout } from "@/components/layout/Layout";

export default function Page() {
  return (
    <Layout>
      <div className="w-full max-w-6xl space-y-12">
        <DemoEmptyState />
      </div>
    </Layout>
  );
}
