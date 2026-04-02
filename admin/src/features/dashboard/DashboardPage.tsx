import { useEffect, useState } from "react";
import { apiRequest } from "../../lib/api";

type AnalyticsSnapshot = {
  total_exams: number;
  total_attempts: number;
  flagged_attempts: number;
  average_score: number;
};

export function DashboardPage() {
  const [analytics, setAnalytics] = useState<AnalyticsSnapshot | null>(null);

  useEffect(() => {
    void apiRequest<AnalyticsSnapshot>("/analytics/summary").then(setAnalytics).catch(() => undefined);
  }, []);

  return (
    <section className="grid gap-6 lg:grid-cols-3">
      <div className="panel p-6 lg:col-span-2">
        <p className="text-sm uppercase tracking-[0.3em] text-brand">Pipeline</p>
        <h2 className="mt-3 text-3xl font-black">Controlled template OMR, tuned for mobile capture.</h2>
        <p className="mt-4 max-w-2xl text-slate-600">
          This admin console manages exam definitions, answer keys, template revisions, and synced scan results.
        </p>
      </div>
      <div className="panel p-6">
        <h3 className="text-xl font-bold">Ready Modules</h3>
        <ul className="mt-4 space-y-3 text-sm text-slate-700">
          <li>JWT auth and bootstrap admin</li>
          <li>Exam creation and answer key storage</li>
          <li>Template PDF generation endpoint</li>
          <li>Result export and review workflow</li>
        </ul>
        {analytics ? (
          <div className="mt-6 space-y-2 text-sm text-slate-700">
            <p>Total exams: {analytics.total_exams}</p>
            <p>Total attempts: {analytics.total_attempts}</p>
            <p>Flagged attempts: {analytics.flagged_attempts}</p>
            <p>Average score: {analytics.average_score}</p>
          </div>
        ) : null}
      </div>
    </section>
  );
}
