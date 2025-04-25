import {
  Breadcrumb,
  BreadcrumbList,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import React from "react";
import { useMatches } from "react-router";

type MatchHandle = {
  breadcrumb: string | ((params: Record<string, string | undefined>) => string);
};

export function AppBreadcrumbs() {
  const matches = useMatches();

  // Filter and map matches with breadcrumbs
  const crumbs = matches
    .filter((m) => m.handle && (m.handle as MatchHandle).breadcrumb)
    .map((m, i, arr) => {
      const handle = m.handle as MatchHandle;
      const label =
        typeof handle.breadcrumb === "function"
          ? handle.breadcrumb(m.params)
          : handle.breadcrumb;

      const isLast = i === arr.length - 1;

      return (
        <React.Fragment key={m.pathname}>
          <BreadcrumbItem>
            {isLast ? (
              <BreadcrumbPage>{label}</BreadcrumbPage>
            ) : (
              <BreadcrumbLink href={m.pathname}>{label}</BreadcrumbLink>
            )}
          </BreadcrumbItem>
          {!isLast && <BreadcrumbSeparator />}
        </React.Fragment>
      );
    });

  return (
    <Breadcrumb>
      <BreadcrumbList>{crumbs}</BreadcrumbList>
    </Breadcrumb>
  );
}
