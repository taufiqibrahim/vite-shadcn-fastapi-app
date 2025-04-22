import type { UploadedFile, UploaderFn } from "@/lib/uploader";
import { api } from "@/lib/api";

export const backendApiUploader: UploaderFn = async (
  files,
  { headers = {}, onProgress } = {},
) => {
  const uploaded: UploadedFile[] = [];

  for (const file of files) {
    const form = new FormData();
    form.append("files", file);

    const res = await api.post<UploadedFile>("files/upload", form, {
      headers: {
        "Content-Type": "multipart/form-data",
        ...headers,
      },
      onUploadProgress: (e) => {
        if (e.total) {
          const progress = (e.loaded / e.total) * 100;
          onProgress?.(file, progress);
        }
      },
    });

    uploaded.push(res.data);
  }

  return uploaded;
};
