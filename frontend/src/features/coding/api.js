import { apiClient } from "../../api/client";

export const codingApi = {
  getProblems: () => apiClient.get("/coding/problems/"),
  getProblem: (id) => apiClient.get(`/coding/problems/${id}/`),
  getSubmissions: () => apiClient.get("/coding/submissions/"),
  getSubmission: (id) => apiClient.get(`/coding/submissions/${id}/`),
  submitSolution: (problemId, code, language) => 
    apiClient.post(`/coding/problems/${problemId}/submit/`, { code, language }),
};
