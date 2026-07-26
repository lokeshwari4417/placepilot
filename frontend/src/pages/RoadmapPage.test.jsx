import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import RoadmapPage from "./RoadmapPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

vi.mock("../features/roadmaps/hooks", () => ({
  useRoadmap: () => ({
    data: {
      id: "1",
      title: "Frontend Developer Roadmap",
      description: "Test description",
      target_role: "frontend",
      estimated_weeks: 12,
      topics: [
        { id: "t1", title: "HTML & CSS", description: "Learn basics", order: 1 },
        { id: "t2", title: "JavaScript", description: "Learn JS", order: 2 },
      ],
    },
    isLoading: false,
    error: null,
  }),
  useRoadmapProgressById: () => ({
    data: {
      status: "in_progress",
      completed_topics: [{ id: "t1", title: "HTML & CSS" }],
      completion_percentage: 50,
    },
    isLoading: false,
  }),
  useCompleteTopic: () => ({ mutate: vi.fn() }),
  useUncompleteTopic: () => ({ mutate: vi.fn() }),
  useStartRoadmap: () => ({ mutate: vi.fn(), isPending: false }),
}));

describe("RoadmapPage", () => {
  it("renders roadmap details", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoadmapPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText("Frontend Developer Roadmap")).toBeInTheDocument();
  });

  it("displays topics", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoadmapPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText("HTML & CSS")).toBeInTheDocument();
    expect(screen.getByText("JavaScript")).toBeInTheDocument();
  });

  it("shows progress when roadmap started", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <RoadmapPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText("Progress")).toBeInTheDocument();
    expect(screen.getByText("1 of 2 topics completed")).toBeInTheDocument();
  });
});
