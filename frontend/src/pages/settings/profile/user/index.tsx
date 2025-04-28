
import { Layout } from "@/components/layout/Layout";
import { ProfileForm } from "@/components/settings/profile-form";
import { Button } from "@/components/ui/button";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useFont } from "@/hooks/use-fonts";
import { Copy } from "lucide-react";

export default function Page() {
  const { font } = useFont();
  const tabs = [
    {
      name: "pnpm",
      value: "pnpm",
      content: "pnpm dlx shadcn@latest add tabs",
    },
  ]
  return (
    <Layout>
      <div className="w-full max-w-7xl space-y-12">
        <div>
          <div>
            <h1 className="text-2xl font-bold mb-6">{"Profile"}</h1>

            {/* <Tabs defaultValue={tabs[0].value} className="max-w-xs w-full">
              <TabsList className="w-full p-0 bg-background justify-start border-b rounded-none">
                {tabs.map((tab) => (
                  <TabsTrigger
                    key={tab.value}
                    value={tab.value}
                    className="rounded-none bg-background h-full data-[state=active]:shadow-none border-b-2 border-transparent data-[state=active]:border-b-4"
                  >
                    <code className="text-[13px]">{tab.name}</code>
                  </TabsTrigger>
                ))}
              </TabsList>

              {tabs.map((tab) => (
                <TabsContent key={tab.value} value={tab.value}>
                  <div className="h-10 flex items-center justify-between border gap-2 rounded-md pl-3 pr-1.5">
                    <code className="text-[13px]">{tab.content}</code>
                    <Button size="icon" variant="secondary" className="h-7 w-7">
                      <Copy className="!h-3.5 !w-3.5" />
                    </Button>
                  </div>
                </TabsContent>
              ))}
            </Tabs> */}

            <div
              className={`flex flex-col justify-center lg:flex-row ${font}`}
            >
              <div className="flex flex-1 flex-col justify-start py-4 ">
                <div className="w-full max-w-md sm:w-[400px]">
                  <ProfileForm />
                </div>
              </div>
            </div>

          </div>
        </div>
      </div>
    </Layout>
  );
}
