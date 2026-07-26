import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { codingApi } from "./api";

export function useProblems() {
  return useQuery({
    queryKey: ["problems"],
    queryFn: () => codingApi.getProblems().then((res) => res.data),
  });
}

export function useProblem(id) {
  return useQuery({
    queryKey: ["problem", id],
    queryFn: () => codingApi.getProblem(id).then((res) => res.data),
    enabled: !!id,
  });
}

export function useSubmissions() {
  return useQuery({
    queryKey: ["submissions"],
    queryFn: () => codingApi.getSubmissions().then((res) => res.data),
  });
}

export function useSubmitSolution() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ problemId, code, language }) => 
      codingApi.submitSolution(problemId, code, language).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries(["submissions"]);
      queryClient.invalidateQueries(["readinessScore"]);
    },
  });
}
