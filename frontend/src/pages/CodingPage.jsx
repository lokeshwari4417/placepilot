import { useState } from "react";
import { useParams } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { EmptyState } from "../components/ui/EmptyState";
import { useProblem, useSubmitSolution } from "../features/coding/hooks";

export default function CodingPage() {
  const { id } = useParams();
  const { data: problem, isLoading, error } = useProblem(id);
  const submitSolution = useSubmitSolution();
  const [code, setCode] = useState("");
  const [language, setLanguage] = useState("python");

  if (isLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-6 bg-slate-200 rounded w-48 mb-2"></div>
          <div className="h-4 bg-slate-200 rounded w-64"></div>
        </div>
      </div>
    );
  }

  if (error || !problem) {
    return (
      <Card>
        <EmptyState
          title="Problem not found"
          description="The coding problem you're looking for doesn't exist."
        />
      </Card>
    );
  }

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!code.trim()) return;
    submitSolution.mutate({ problemId: id, code, language });
  };

  const getStatusColor = (status) => {
    switch (status) {
      case "accepted": return "text-green-600";
      case "wrong_answer": return "text-red-600";
      case "tle": return "text-orange-600";
      default: return "text-muted";
    }
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-ink">{problem.title}</h1>
        <div className="flex items-center gap-3 mt-2 text-xs text-muted">
          <span className="px-2 py-1 bg-slate-100 rounded capitalize">{problem.difficulty}</span>
          <span>•</span>
          <span>Time: {problem.time_limit}s</span>
          <span>•</span>
          <span>Memory: {problem.memory_limit}MB</span>
        </div>
      </div>

      <Card>
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-ink">Description</h3>
          <p className="text-sm text-muted whitespace-pre-wrap">{problem.description}</p>
          
          {problem.test_cases && problem.test_cases.length > 0 && (
            <div className="space-y-3">
              <h3 className="text-sm font-medium text-ink">Sample Test Cases</h3>
              {problem.test_cases.filter(tc => !tc.is_hidden).map((tc) => (
                <div key={tc.id} className="p-3 bg-slate-50 rounded-lg space-y-2">
                  <div className="text-xs">
                    <span className="font-medium text-ink">Input:</span>
                    <pre className="mt-1 text-xs bg-white p-2 rounded">{tc.input_data}</pre>
                  </div>
                  <div className="text-xs">
                    <span className="font-medium text-ink">Output:</span>
                    <pre className="mt-1 text-xs bg-white p-2 rounded">{tc.expected_output}</pre>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>

      <Card>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div className="flex items-center justify-between">
            <h3 className="text-sm font-medium text-ink">Solution</h3>
            <select
              value={language}
              onChange={(e) => setLanguage(e.target.value)}
              className="text-xs px-2 py-1 border border-slate-200 rounded"
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
              <option value="java">Java</option>
              <option value="cpp">C++</option>
            </select>
          </div>
          
          <textarea
            value={code}
            onChange={(e) => setCode(e.target.value)}
            placeholder="Write your solution here..."
            className="w-full h-64 p-3 text-sm font-mono border border-slate-200 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-accent-500"
            disabled={submitSolution.isPending}
          />
          
          <Button 
            type="submit" 
            className="w-full" 
            disabled={!code.trim() || submitSolution.isPending}
          >
            {submitSolution.isPending ? "Running..." : "Submit Solution"}
          </Button>
        </form>
      </Card>

      {submitSolution.data && (
        <Card>
          <div className="space-y-3">
            <h3 className="text-sm font-medium text-ink">Submission Result</h3>
            <div className="p-4 bg-slate-50 rounded-lg">
              <div className="flex items-center justify-between mb-2">
                <span className="text-sm text-muted">Status:</span>
                <span className={`text-sm font-medium capitalize ${getStatusColor(submitSolution.data.status)}`}>
                  {submitSolution.data.status.replace('_', ' ')}
                </span>
              </div>
              {submitSolution.data.passed_test_cases !== undefined && (
                <div className="text-xs text-muted">
                  Passed: {submitSolution.data.passed_test_cases} / {submitSolution.data.total_test_cases}
                </div>
              )}
              {submitSolution.data.error_message && (
                <div className="mt-2 text-xs text-red-600">{submitSolution.data.error_message}</div>
              )}
            </div>
          </div>
        </Card>
      )}
    </div>
  );
}
