import { Card } from "../components/ui/Card";
import { ProgressBar } from "../components/ui/ProgressBar";
import { EmptyState } from "../components/ui/EmptyState";

const STATS = [
  { label: "Coding", value: 0 },
  { label: "Aptitude", value: 0 },
  { label: "Resume", value: 0 },
  { label: "Interview Readiness", value: 0 },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-ink">Your Placement Readiness</h1>
        <p className="text-sm text-muted">Overall score updates as you practice.</p>
      </div>

      <Card>
        <ProgressBar value={0} label="Overall Placement Ready" />
      </Card>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {STATS.map((stat) => (
          <Card key={stat.label}>
            <ProgressBar value={stat.value} label={stat.label} />
          </Card>
        ))}
      </div>

      <Card>
        <EmptyState
          title="No recent activity yet"
          description="Solve a problem, take a quiz, or update your resume to see it here."
        />
      </Card>
    </div>
  );
}
