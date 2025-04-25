import { useAuth } from "@/auth/use-auth";
import { Loading } from "@/components/app-loading";
import { DataTable } from "@/components/data-table";
import { FileUploader } from "@/components/file-uploader";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { STORAGE_BACKEND } from "@/constants";
import { useUploadFile } from "@/hooks/use-upload-file";
import { backendApiUploader } from "@/lib/uploader/backend-uploader";
import { UploadProvider } from "@/lib/uploader/context";
import { GeospatialMappingAppSidebar } from "@/pages/apps/geospatial-mapping-app/components/app-sidebar";
import {
  useCreateDataset,
  useDatasetList,
} from "@/pages/apps/geospatial-mapping-app/hooks/use-datasets";
import { useEffect, useRef, useState } from "react";
import { columns } from "./columns";
import { Layout } from "@/components/layout/Layout";

export default function Page() {
  return (
    <UploadProvider uploader={backendApiUploader}>
      <PageContent />
    </UploadProvider>
  );
}

function PageContent() {
  const { user } = useAuth();
  const { data: datasets, isFetching } = useDatasetList();
  const { mutate: createDataset } = useCreateDataset();
  const {
    onUpload,
    uploadedFiles,
    isUploading,
    progresses,
    resetUploadedFiles,
  } = useUploadFile();
  const prevIsUploading = useRef(isUploading);
  const [dialogOpen, setDialogOpen] = useState(false);

  useEffect(() => {
    if (prevIsUploading.current === true && isUploading === false) {
      setDialogOpen(false);

      resetUploadedFiles();

      uploadedFiles.map((item) => {
        const newDataset = {
          uid: item.uid,
          name: item.name,
          account_id: user.account_id,
          file_name: item.name,
          status: "uploaded" as const,
          storage_backend: STORAGE_BACKEND,
          storage_uri: item.storage_uri,
        };

        createDataset(newDataset);
      });
    }
    prevIsUploading.current = isUploading;
  }, [isUploading]);

  return (
    <Layout SidebarComponent={GeospatialMappingAppSidebar}>
      <div className="flex flex-col p-2 gap-2">
        <div className="flex justify-between gap-6">
          <h1 className="scroll-m-20 text-2xl font-bold">Datasets</h1>

          {/* New dataset dialogue */}
          <Dialog open={dialogOpen} onOpenChange={setDialogOpen}>
            <DialogTrigger asChild>
              <Button
                size="sm"
                className="text-xs"
                onClick={() => setDialogOpen(true)}
              >
                New dataset
              </Button>
            </DialogTrigger>
            <DialogContent className="sm:max-w-[425px]">
              <DialogHeader>
                <DialogTitle>New Dataset</DialogTitle>
              </DialogHeader>

              <FileUploader
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
          <DataTable data={datasets ?? []} columns={columns} />
        </Loading>
      </div>
    </Layout>
  );
}
