import React, { createContext, useContext } from "react";
import type { UploaderFn } from ".";

interface UploadContextValue {
  uploader: UploaderFn;
}

const UploadContext = createContext<UploadContextValue | null>(null);

export const UploadProvider = ({
  children,
  uploader,
}: {
  uploader: UploaderFn;
  children: React.ReactNode;
}) => {
  return (
    <UploadContext.Provider value={{ uploader }}>
      {children}
    </UploadContext.Provider>
  );
};

export const useUploader = () => {
  const context = useContext(UploadContext);
  if (!context)
    throw new Error("useUploader must be used within UploadProvider");
  return context.uploader;
};
