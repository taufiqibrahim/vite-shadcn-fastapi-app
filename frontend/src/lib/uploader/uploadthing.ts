import { genUploader } from "uploadthing/client";
import type { UploaderFn, UploadedFile } from "@/lib/uploader";
import { createUploadthing, type FileRouter } from "uploadthing/server";

const f = createUploadthing();

// const auth = (req: Request) => ({ id: "fakeId" }); // Fake auth function

// FileRouter for your app, can contain multiple FileRoutes
export const ourFileRouter = {
  /**
 * For full list of options and defaults, see the File Route API reference
 * @see https://docs.uploadthing.com/file-routes#route-config
 */
  // Define as many FileRoutes as you like, each with a unique routeSlug

  defaultUploader: f({ })
    .onUploadComplete((data) => {
      console.log("Upload complete", data);
    })
    // .onUploadError((err: any) => {console.log(err)}),

} satisfies FileRouter;

export type UploadRouter = typeof ourFileRouter;


const { uploadFiles } = genUploader<UploadRouter>();

export const uploadthingUploader: UploaderFn = async (files, options) => {
  try {
    const uploaded = await uploadFiles("defaultUploader", {
      files,
      onUploadProgress: (progressEvent) => {
        const { loaded, totalLoaded: total } = progressEvent;
        const progress = Math.round((loaded / (total ?? 1)) * 100);
        if (options?.onProgress) {
          options.onProgress(files[0], progress);
        }
      },
    });

    return uploaded.map((file) => ({
      ...file,
    })) satisfies UploadedFile[];
  } catch (error) {
    console.error("UploadThing upload failed", error);
    throw error;
  }
};
