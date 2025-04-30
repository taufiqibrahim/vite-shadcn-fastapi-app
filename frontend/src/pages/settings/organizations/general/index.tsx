import { Layout } from "@/components/layout/Layout";
import { OrganizationForm } from "@/components/settings/organization-form";
import { useFont } from "@/hooks/use-fonts";

export default function Page() {
  const { font } = useFont();

  return (
    <Layout>
      <div className="w-full max-w-7xl space-y-12">
        <h1 className="text-2xl font-bold mb-6">{"Organization"}</h1>
        <div className={`flex flex-col justify-center lg:flex-row ${font}`}>
          <div className="flex flex-1 flex-col justify-start py-4 ">
            <div className="w-full sm:w-[480px]">
              <OrganizationForm />
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}
