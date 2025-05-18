import { Layout } from "@/components/layout/Layout";
import EntityListLayout from "@/components/layout/EntityListLayout";
import { KeyRoundIcon } from "lucide-react";
import { useTranslation } from "react-i18next";

export default function Page() {
  const { t } = useTranslation();
  const apiKeys = []
  return (
    <Layout>
      <div className="w-full max-w-7xl space-y-12">
        {/* <DemoEmptyState title="API Keys" /> */}
        <EntityListLayout
          title="API Keys"
          searchPlaceholder={t("settings.org.apiKeys.list.searchPlaceholder")}
          emptyTitle={t("settings.org.apiKeys.list.emptyTitle")}
          // filters={
          //   <>
          //     <Button variant="outline" size="sm" className="h-10 gap-1">
          //       <Filter className="h-4 w-4" />
          //       Status
          //       <ChevronDown className="h-3 w-3 opacity-50" />
          //     </Button>
          //     <Button variant="outline" size="sm" className="h-10 gap-1">
          //       <Calendar className="h-4 w-4" />
          //       Order Date
          //       <ChevronDown className="h-3 w-3 opacity-50" />
          //     </Button>
          //   </>
          // }
          // viewOptions={
          //   <Button variant="outline" size="sm" className="h-10">
          //     View
          //     <ChevronDown className="ml-1 h-3 w-3 opacity-50" />
          //   </Button>
          // }
          icon={<KeyRoundIcon className="h-16 w-16 text-primary" />}
          ctaLabel="New API Key"
          onCreate={() => console.log("Create new")}
        >
          {apiKeys.length > 0 ? (
            <div>
              {/* Your actual list rendering (e.g., table or grid of orders) */}
              <p>Render your orders here...</p>
            </div>
          ) : null}
        </EntityListLayout>
      </div>
    </Layout>
  );
}
