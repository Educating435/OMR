import { useEffect, useState } from "react";
import { apiRequest } from "../../lib/api";
import { getUserRole } from "../../lib/auth";

type ReviewAttempt = {
  id: string;
  student_identifier: string;
  score: number;
  max_score: number;
  review_status: string;
  needs_review: boolean;
};

export function ReviewPage() {
  const [items, setItems] = useState<ReviewAttempt[]>([]);
  const role = getUserRole();

  async function load() {
    const data = await apiRequest<ReviewAttempt[]>("/review/flagged");
    setItems(data);
  }

  async function markReviewed(id: string) {
    await apiRequest(`/review/${id}`, {
      method: "PATCH",
      body: JSON.stringify({
        needs_review: false,
        review_status: "reviewed",
        remarks: "Reviewed from admin panel"
      })
    });
    await load();
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="space-y-4">
      {items.map((item) => (
        <article key={item.id} className="panel flex flex-col gap-4 p-6 md:flex-row md:items-center md:justify-between">
          <div>
            <h3 className="text-xl font-bold">{item.student_identifier}</h3>
            <p className="text-sm text-slate-600">
              Score {item.score}/{item.max_score} · Status {item.review_status}
            </p>
          </div>
          {role === "viewer" ? null : (
            <button className="button-primary" onClick={() => void markReviewed(item.id)}>
              Mark Reviewed
            </button>
          )}
        </article>
      ))}
      {items.length === 0 ? <div className="panel p-6">No flagged scans right now.</div> : null}
    </section>
  );
}

