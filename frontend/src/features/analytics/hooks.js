import { useQuery } from "@tanstack/react-query";
import { analyticsApi } from "./api";

export function useReadinessScore() {
  return useQuery({
    queryKey: ["readinessScore"],
    queryFn: () => analyticsApi.getReadinessScore().then((res) => res.data),
  });
}
