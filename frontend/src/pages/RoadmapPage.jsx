import { useParams } from "react-router-dom";
import { Card } from "../components/ui/Card";
import { Button } from "../components/ui/Button";
import { ProgressBar } from "../components/ui/ProgressBar";
import { EmptyState } from "../components/ui/EmptyState";
import { useRoadmap, useRoadmapProgressById, useCompleteTopic, useUncompleteTopic, useStartRoadmap } from "../features/roadmaps/hooks";

export default function RoadmapPage() {
  const { id } = useParams();
  const { data: roadmap, isLoading: roadmapLoading, error: roadmapError } = useRoadmap(id);
  const { data: progress, isLoading: progressLoading } = useRoadmapProgressById(id);
  const completeTopic = useCompleteTopic();
  const uncompleteTopic = useUncompleteTopic();
  const startRoadmap = useStartRoadmap();

  if (roadmapLoading || progressLoading) {
    return (
      <div className="space-y-6">
        <div className="animate-pulse">
          <div className="h-6 bg-slate-200 rounded w-48 mb-2"></div>
          <div className="h-4 bg-slate-200 rounded w-64"></div>
        </div>
      </div>
    );
  }

  if (roadmapError || !roadmap) {
    return (
      <Card>
        <EmptyState
          title="Roadmap not found"
          description="The roadmap you're looking for doesn't exist."
        />
      </Card>
    );
  }

  const isTopicCompleted = (topicId) => {
    return progress?.completed_topics?.some((t) => t.id === topicId);
  };

  const handleTopicToggle = (topicId) => {
    if (isTopicCompleted(topicId)) {
      uncompleteTopic.mutate({ roadmapId: id, topicId });
    } else {
      completeTopic.mutate({ roadmapId: id, topicId });
    }
  };

  const handleStartRoadmap = () => {
    startRoadmap.mutate(id);
  };

  const hasStarted = progress?.status !== "not_started";

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-xl font-semibold text-ink">{roadmap.title}</h1>
        <p className="text-sm text-muted mt-1">{roadmap.description}</p>
        <div className="flex items-center gap-4 mt-2 text-xs text-muted">
          <span>Target: {roadmap.target_role}</span>
          <span>•</span>
          <span>{roadmap.estimated_weeks} weeks</span>
        </div>
      </div>

      {hasStarted && progress && (
        <Card>
          <div className="space-y-4">
            <div className="flex items-center justify-between">
              <h3 className="text-sm font-medium text-ink">Progress</h3>
              <span className="text-sm text-accent-600 font-medium">{progress.completion_percentage}%</span>
            </div>
            <ProgressBar value={progress.completion_percentage} label="Completion" />
            <div className="text-xs text-muted">
              {progress.completed_topics?.length || 0} of {roadmap.topics?.length || 0} topics completed
            </div>
          </div>
        </Card>
      )}

      {!hasStarted && (
        <Card>
          <div className="text-center space-y-4">
            <p className="text-sm text-muted">Start this roadmap to track your progress</p>
            <Button onClick={handleStartRoadmap} disabled={startRoadmap.isPending}>
              {startRoadmap.isPending ? "Starting..." : "Start Roadmap"}
            </Button>
          </div>
        </Card>
      )}

      <Card>
        <div className="space-y-4">
          <h3 className="text-sm font-medium text-ink">Topics</h3>
          {roadmap.topics?.length === 0 ? (
            <EmptyState title="No topics yet" description="Topics will be added soon." />
          ) : (
            <div className="space-y-3">
              {roadmap.topics.map((topic) => (
                <div
                  key={topic.id}
                  className={`p-4 rounded-lg border-2 transition-colors ${
                    isTopicCompleted(topic.id)
                      ? "border-green-200 bg-green-50"
                      : "border-slate-200 bg-white"
                  }`}
                >
                  <div className="flex items-start gap-3">
                    <input
                      type="checkbox"
                      checked={isTopicCompleted(topic.id)}
                      onChange={() => handleTopicToggle(topic.id)}
                      disabled={!hasStarted || completeTopic.isPending || uncompleteTopic.isPending}
                      className="mt-1 h-4 w-4 rounded border-slate-300 text-accent-600 focus:ring-accent-500"
                    />
                    <div className="flex-1">
                      <h4 className="text-sm font-medium text-ink">{topic.title}</h4>
                      {topic.description && (
                        <p className="text-xs text-muted mt-1">{topic.description}</p>
                      )}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </Card>
    </div>
  );
}
