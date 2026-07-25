import { Card } from "../components/ui/Card";
import { ProgressBar } from "../components/ui/ProgressBar";
import { EmptyState } from "../components/ui/EmptyState";
import { useReadinessScore } from "../features/analytics/hooks";

const STATS = [
  { key: "coding_score", label: "Coding" },
  { key: "aptitude_score", label: "Aptitude" },
  { key: "resume_score", label: "Resume" },
  { key: "interview_score", label: "Interview Readiness" },
];

export default function DashboardPage() {
  const { data: score, isLoading, error } = useReadinessScore();

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

  if (error) {
    return (
      <Card>
        <EmptyState
          title="Failed to load readiness score"
          description="Please try refreshing the page."
        />
      </Card>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-ink">Your Placement Readiness</h1>
        <p className="text-sm text-muted">Overall score updates as you practice.</p>
      </div>

      <Card>
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <ProgressBar value={score?.overall_score || 0} label="Overall Placement Ready" />
          </div>
          <div className="ml-4 text-center">
            <div className="text-2xl font-bold text-accent-600">{score?.streak_days || 0}</div>
            <div className="text-xs text-muted">Day Streak</div>
          </div>
        </div>
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {STATS.map((stat) => (
          <Card key={stat.label}>
            <ProgressBar value={score?.[stat.key] || 0} label={stat.label} />
          </Card>
        ))}
      </div>

      <Card>
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-ink">Roadmap Progress</h3>
          <ProgressBar value={score?.roadmap_progress || 0} label="Learning Roadmap" />
        </div>
      </Card>

      <Card>
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-ink">Recent Activity</h3>
          <EmptyState
            title="No recent activity yet"
            description="Solve a problem, take a quiz, or update your resume to see it here."
          />
        </div>
      </Card>

      <Card>
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-ink">Recommended for You</h3>
          <div className="space-y-3">
            <div className="p-3 bg-slate-50 rounded-lg">
              <p className="text-sm font-medium text-ink">Start your learning roadmap</p>
              <p className="text-xs text-muted mt-1">Begin with the fundamentals of your target role</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <p className="text-sm font-medium text-ink">Practice coding problems</p>
              <p className="text-xs text-muted mt-1">Improve your problem-solving skills</p>
            </div>
            <div className="p-3 bg-slate-50 rounded-lg">
              <p className="text-sm font-medium text-ink">Take an aptitude quiz</p>
              <p className="text-xs text-muted mt-1">Test your quantitative and logical reasoning</p>
            </div>
          </div>
        </div>
      </Card>
    </div>
  );
}
