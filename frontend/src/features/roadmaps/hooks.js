import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { roadmapsApi } from "./api";

export function useRoadmaps() {
  return useQuery({
    queryKey: ["roadmaps"],
    queryFn: () => roadmapsApi.getRoadmaps().then((res) => res.data),
  });
}

export function useRoadmap(id) {
  return useQuery({
    queryKey: ["roadmap", id],
    queryFn: () => roadmapsApi.getRoadmap(id).then((res) => res.data),
    enabled: !!id,
  });
}

export function useRoadmapProgress() {
  return useQuery({
    queryKey: ["roadmapProgress"],
    queryFn: () => roadmapsApi.getProgress().then((res) => res.data),
  });
}

export function useRoadmapProgressById(roadmapId) {
  return useQuery({
    queryKey: ["roadmapProgress", roadmapId],
    queryFn: () => roadmapsApi.getRoadmapProgress(roadmapId).then((res) => res.data),
    enabled: !!roadmapId,
  });
}

export function useStartRoadmap() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: (roadmapId) => roadmapsApi.startRoadmap(roadmapId).then((res) => res.data),
    onSuccess: () => {
      queryClient.invalidateQueries(["roadmapProgress"]);
    },
  });
}

export function useCompleteTopic() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ roadmapId, topicId }) => 
      roadmapsApi.completeTopic(roadmapId, topicId).then((res) => res.data),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries(["roadmapProgress", variables.roadmapId]);
      queryClient.invalidateQueries(["readinessScore"]);
    },
  });
}

export function useUncompleteTopic() {
  const queryClient = useQueryClient();
  
  return useMutation({
    mutationFn: ({ roadmapId, topicId }) => 
      roadmapsApi.uncompleteTopic(roadmapId, topicId).then((res) => res.data),
    onSuccess: (data, variables) => {
      queryClient.invalidateQueries(["roadmapProgress", variables.roadmapId]);
      queryClient.invalidateQueries(["readinessScore"]);
    },
  });
}
