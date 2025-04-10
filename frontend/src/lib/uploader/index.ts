export interface UploadedFile {
  name: string;
  url: string;
  [key: string]: any;
}

export interface UploadOptions {
  headers?: Record<string, string>;
  onProgress?: (file: File, progress: number) => void;
}

export type UploaderFn = (
  files: File[],
  options?: UploadOptions,
) => Promise<UploadedFile[]>;
