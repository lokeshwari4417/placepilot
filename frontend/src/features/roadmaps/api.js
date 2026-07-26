import { apiClient } from "../../api/client";

export const roadmapsApi = {
  getRoadmaps: () => apiClient.get("/roadmaps/"),
  getRoadmap: (id) => apiClient.get(`/roadmaps/${id}/`),
  getProgress: () => apiClient.get("/roadmaps/progress/"),
  getRoadmapProgress: (roadmapId) => apiClient.get(`/roadmaps/progress/${roadmapId}/`),
  startRoadmap: (roadmapId) => apiClient.post("/roadmaps/progress/", { roadmap_id: roadmapId }),
  completeTopic: (roadmapId, topicId) => apiClient.post(`/roadmaps/progress/${roadmapId}/complete/`, { topic_id: topicId }),
  uncompleteTopic: (roadmapId, topicId) => apiClient.post(`/roadmaps/progress/${roadmapId}/uncomplete/`, { topic_id: topicId }),
};
