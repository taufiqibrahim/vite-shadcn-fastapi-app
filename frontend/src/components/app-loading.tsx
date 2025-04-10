import React from "react";

type LoadingProps = {
  isLoading: boolean;
  children?: React.ReactNode;
};

export const Loading: React.FC<LoadingProps> = ({ isLoading, children }) => {
  if (isLoading) {
    return (
      <div className="flex items-center justify-center h-64">
        <span className="animate-spin inline-block w-8 h-8 border-4 border-t-transparent border-black rounded-full" />
      </div>
    );
  }

  return <>{children}</>;
};
