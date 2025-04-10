import Layout from "@/app/layout";
import { Loading } from "@/components/app-loading";
import { FileUploader } from "@/components/file-uploader";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { useUploadFile } from "@/hooks/use-upload-file";
// import { UploadDropzone } from "@/lib/uploadthing";
import { GeospatialMappingAppSidebar } from "@/pages/apps/geospatial-mapping-app/components/app-sidebar";
import { useDatasetList } from "@/pages/apps/geospatial-mapping-app/hooks/use-datasets";

export default function Page() {
  const { data: datasets, isFetching } = useDatasetList();
  const { onUpload, uploadedFiles, isUploading, progresses } = useUploadFile();

  return (
    <Layout SidebarComponent={GeospatialMappingAppSidebar}>
      <div className="flex flex-col p-2 gap-2">
        <div className="flex justify-between gap-6">
          <h1 className="scroll-m-20 text-2xl font-bold">Datasets</h1>

          {/* New dataset dialogue */}
          <Dialog open={true}>
            <DialogTrigger asChild>
              <Button size="sm" className="text-xs">
                New dataset
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>New Dataset</DialogTitle>
              </DialogHeader>

              <FileUploader
                // accept={{
                //   "image/*": [],
                //   "application/*": [],
                //   "text/*": ["geojson"],
                // }}
                maxFileCount={1}
                maxSize={10 * 1024 * 1024}
                progresses={progresses}
                onUpload={onUpload}
                disabled={isUploading}
              />
              {/* <UploadedFilesCard uploadedFiles={uploadedFiles} /> */}
            </DialogContent>
          </Dialog>
        </div>

        <Loading isLoading={isFetching}>
          {datasets && datasets.length > 0 ? (
            <div>Datasets here...</div>
          ) : (
            <div>Empty</div>
          )}
        </Loading>
      </div>
    </Layout>
  );
}
