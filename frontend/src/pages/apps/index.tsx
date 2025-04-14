import Layout from "@/app/layout";
import { Button } from "@/components/ui/button";
import {
  Card,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { useAppList } from "@/hooks/use-apps";
import { Rocket } from "lucide-react";
import { useNavigate } from "react-router";

export default function Page() {
  const { data } = useAppList();
  const navigate = useNavigate();

  return (
    <Layout>
      <div className="*:data-[slot=card]:shadow-sm grid sm:grid-cols-1 sm:grid-cols-2 lg:grid-cols-2 xl:grid-cols-4 @5xl/main:grid-cols-4 gap-4 p-4">
        {data?.map((app: any, idx: number) => (
          <Card
            key={idx}
            className="@container/card max-w-100 h-96 max-h-96 overflow-hidden py-4 gap-4"
          >
            <CardHeader className="relative">
              <CardTitle className="@[250px]/card:text-2xl text-xl font-semibold line-clamp-1">
                {app.name}
              </CardTitle>
              <CardDescription className="text-sm line-clamp-3">
                {app.description}
              </CardDescription>
            </CardHeader>
            <CardFooter className="flex justify-start gap-4 mt-auto">
              <Button
                className="w-full rounded-lg"
                size="sm"
                onClick={() => navigate(`/apps/${app.name}`)}
              >
                <span className="flex gap-2 items-center">
                  <Rocket />
                  Launch Demo
                </span>
              </Button>
            </CardFooter>
          </Card>
        ))}
      </div>
    </Layout>
  );
}
