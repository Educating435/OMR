import { useEffect, useState } from "react";
import { api, Result } from "../../lib/api";

export function ReviewPage() {
  const [results, setResults] = useState<Result[]>([]);

  async function refresh() {
    const all = await api.listResults();
    setResults(all.filter((item) => item.needs_review));
  }

  useEffect(() => {
    refresh();
  }, []);

  return (
    <section className="panel p-6">
      <div className="flex items-center justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Flagged review queue</h2>
          <p className="mt-1 text-sm text-slate-600">IMPLEMENTED: review status is driven by backend result records, not local browser state.</p>
        </div>
        <button className="button-secondary" onClick={refresh} type="button">
          Refresh
        </button>
      </div>

      <div className="mt-6 space-y-4">
        {results.map((result) => (
          <article key={result.id} className="rounded-3xl border border-slate-200 bg-white/70 p-5">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-sm text-slate-500">Roll number</p>
                <h3 className="text-xl font-semibold">{result.roll_number}</h3>
              </div>
              <button
                className="button-primary"
                type="button"
                onClick={async () => {
                  await api.markResultReviewed(result.id);
                  refresh();
                }}
              >
                Mark reviewed
              </button>
            </div>
            <p className="mt-3 text-sm text-slate-600">Attempt {result.local_attempt_id}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
