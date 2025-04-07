import Layout from "@/app/layout";
import { Button } from "@/components/ui/button";
import { Card, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { useAppList } from "@/hooks/use-apps";

export default function Page() {

  const { data } = useAppList()
  console.log("data", data)
  return (
    <Layout>
      <div
        className="*:data-[slot=card]:shadow-sm grid sm:grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 xl:grid-cols-4 @5xl/main:grid-cols-4 gap-4 p-4"
      >
        {
          data?.data?.map((app: any, idx: number) => (
              <Card key={idx} className="@container/card h-96 max-h-96 overflow-hidden py-4 gap-4">
                <CardHeader className="relative">
                  <CardTitle className="@[250px]/card:text-2xl text-xl font-semibold line-clamp-1">
                    {app.name}
                  </CardTitle>
                  <CardDescription className="text-sm line-clamp-3">
                    {app.description}
                  </CardDescription>
                </CardHeader>
                <CardFooter className="flex justify-start gap-4 mt-auto">
                  <Button size="sm">Demo</Button>
                  <Button size="sm" variant="link">Cancel</Button>
                </CardFooter>
              </Card>
            ))
        }

      </div>
    </Layout>
  );
}
