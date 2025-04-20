import * as React from "react";
import { toast } from "sonner";
import { getErrorMessage } from "@/lib/handle-error";
import type { UploadedFile } from "@/lib/uploader";
import { useUploader } from "@/lib/uploader/context";

interface UseUploadFileOptions {
  defaultUploadedFiles?: UploadedFile[];
  headers?: Record<string, string>;
  onUploadBegin?: () => void;
  onUploadProgress?: (info: { file: File; progress: number }) => void;
}

export function useUploadFile({
  defaultUploadedFiles = [],
  onUploadBegin,
  onUploadProgress,
  headers,
}: UseUploadFileOptions = {}) {
  const uploader = useUploader();

  const [uploadedFiles, setUploadedFiles] =
    React.useState(defaultUploadedFiles);
  const [progresses, setProgresses] = React.useState<Record<string, number>>(
    {},
  );
  const [isUploading, setIsUploading] = React.useState(false);

  const onUpload = async (files: File[]) => {
    setIsUploading(true);
    onUploadBegin?.();

    try {
      const res = await uploader(files, {
        headers,
        onProgress: (file, progress) => {
          setProgresses((prev) => ({ ...prev, [file.name]: progress }));
          onUploadProgress?.({ file, progress });
        },
      });
      setUploadedFiles((prev) => [...prev, ...res]);
    } catch (err) {
      toast.error(getErrorMessage(err));
    } finally {
      setIsUploading(false);
      setProgresses({});
    }
  };

  const resetUploadedFiles = () => setUploadedFiles([]);

  return {
    onUpload,
    uploadedFiles,
    progresses,
    isUploading,
    resetUploadedFiles,
  };
}
