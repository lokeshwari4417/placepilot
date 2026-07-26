import { render, screen } from "@testing-library/react";
import { describe, it, expect, vi } from "vitest";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { BrowserRouter } from "react-router-dom";
import CodingPage from "./CodingPage";

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
});

vi.mock("../features/coding/hooks", () => ({
  useProblem: () => ({
    data: {
      id: "1",
      title: "Two Sum",
      description: "Given an array of integers...",
      difficulty: "easy",
      time_limit: 2,
      memory_limit: 256,
      test_cases: [
        { id: "tc1", input_data: "2 7 11 15\n9", expected_output: "0 1", is_hidden: false, order: 1 },
      ],
    },
    isLoading: false,
    error: null,
  }),
  useSubmitSolution: () => ({ mutate: vi.fn(), isPending: false, data: null }),
}));

describe("CodingPage", () => {
  it("renders problem details", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <CodingPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText("Two Sum")).toBeInTheDocument();
  });

  it("displays problem description", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <CodingPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText("Given an array of integers...")).toBeInTheDocument();
  });

  it("shows sample test cases", () => {
    render(
      <QueryClientProvider client={queryClient}>
        <BrowserRouter>
          <CodingPage />
        </BrowserRouter>
      </QueryClientProvider>
    );
    expect(screen.getByText("Sample Test Cases")).toBeInTheDocument();
  });
});
