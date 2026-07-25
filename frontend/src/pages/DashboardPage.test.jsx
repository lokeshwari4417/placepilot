import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import DashboardPage from "./DashboardPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

vi.mock("../features/analytics/hooks", () => ({
  useReadinessScore: () => ({
    data: {
      overall_score: 75,
      coding_score: 80,
      aptitude_score: 70,
      resume_score: 85,
      interview_score: 75,
      roadmap_progress: 50,
      streak_days: 5,
    },
    isLoading: false,
    error: null,
  }),
}));

describe("DashboardPage", () => {
  it("renders dashboard", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <DashboardPage />
      </QueryClientProvider>
    );
    expect(screen.getByText("Your Placement Readiness")).toBeInTheDocument();
  });

  it("displays sub-score categories", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <DashboardPage />
      </QueryClientProvider>
    );
    expect(screen.getByText("Coding")).toBeInTheDocument();
    expect(screen.getByText("Aptitude")).toBeInTheDocument();
    expect(screen.getByText("Resume")).toBeInTheDocument();
    expect(screen.getByText("Interview Readiness")).toBeInTheDocument();
  });

  it("displays streak counter", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <DashboardPage />
      </QueryClientProvider>
    );
    expect(screen.getByText("5")).toBeInTheDocument();
    expect(screen.getByText("Day Streak")).toBeInTheDocument();
  });
});
