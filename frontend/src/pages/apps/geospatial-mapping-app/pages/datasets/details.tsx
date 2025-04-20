import { Loading } from "@/components/app-loading";
import {
  ResizableHandle,
  ResizablePanel,
  ResizablePanelGroup,
} from "@/components/ui/resizable";
import DatasetMaps from "./maps";
import { useParams } from "react-router";
import { ArrowLeft, MoreVertical } from "lucide-react";
import { useDatasetDetail } from "../../hooks/use-datasets";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";

export default function Page() {
  const { uid } = useParams<{ uid: string }>();
  const { data: dataset } = useDatasetDetail(uid);
  // const [bbox, setBBox] = useState<[number, number, number, number] | null>();

  // useEffect(() => {
  //   if (
  //     dataset?.bbox?.xmin != null &&
  //     dataset?.bbox?.ymin != null &&
  //     dataset?.bbox?.xmax != null &&
  //     dataset?.bbox?.ymax != null
  //   ) {
  //     setBBox([
  //       dataset.bbox.xmin,
  //       dataset.bbox.ymin,
  //       dataset.bbox.xmax,
  //       dataset.bbox.ymax,
  //     ]);
  //   }
  // }, [dataset]);

  // const columns = useColumns(dataset);
  // const { data: datasetTable } = useDatasetTable(uid);
  // const { data: datasetFeatures } = useDatasetFeatures(uid, bbox);

  return (
    <div className="flex flex-col gap-2">
      <div className="flex justify-between items-end p-1">
        <div className="flex justify-start items-end gap-2">
          <a href="/apps/geospatial-mapping-app/datasets/">
            <div className="flex aspect-square size-8 items-center justify-center">
              <ArrowLeft />
            </div>
          </a>
          <h1 className="scroll-m-20 text-2xl font-bold">{dataset?.name}</h1>
        </div>
        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <Button
              variant="ghost"
              className="flex pt-2 size-8 text-muted-foreground data-[state=open]:bg-muted"
              size="icon"
            >
              <MoreVertical />
              <span className="sr-only">Open menu</span>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent align="end" className="w-32">
            <DropdownMenuItem>Edit</DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem>Delete</DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <div className="flex flex-col gap-2 h-[calc(100vh-4rem)] overflow-hidden">
        <ResizablePanelGroup direction="vertical">
          <ResizablePanel defaultSize={60}>
            <DatasetMaps datasetUID={dataset?.uid} />
          </ResizablePanel>
          <ResizableHandle />
          <ResizablePanel defaultSize={40}>
            <ResizablePanelGroup direction="horizontal">
              <ResizablePanel defaultSize={40}>SQL</ResizablePanel>
              <ResizableHandle />
              <ResizablePanel defaultSize={60}>Table</ResizablePanel>
            </ResizablePanelGroup>
          </ResizablePanel>
        </ResizablePanelGroup>
      </div>

      <Loading isLoading={false}></Loading>
    </div>
  );
}
