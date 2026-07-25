import { apiClient } from "../../api/client";

export const analyticsApi = {
  getReadinessScore: () => apiClient.get("/analytics/readiness-score/"),
};
