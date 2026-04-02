import { useState } from "react";
import { apiRequest } from "../../lib/api";

type ResultRow = {
  id: string;
  student_identifier: string;
  score: number;
  max_score: number;
  review_status: string;
};

export function ResultsPage() {
  const [page, setPage] = useState("1");
  const [rows, setRows] = useState<ResultRow[]>([]);

  async function load() {
    const data = await apiRequest<{ items: ResultRow[]; meta: { total: number } }>(`/results?page=${page}&page_size=20`);
    setRows(data.items);
  }

  return (
    <section className="space-y-6">
      <div className="panel flex flex-col gap-4 p-6 md:flex-row">
        <input
          className="input"
          value={page}
          onChange={(e) => setPage(e.target.value)}
          placeholder="Page number"
        />
        <button className="button-primary" onClick={() => void load()}>
          Load Results
        </button>
      </div>

      <div className="panel overflow-hidden">
        <table className="w-full border-collapse">
          <thead className="bg-ink text-left text-sm uppercase tracking-[0.2em] text-white">
            <tr>
              <th className="px-4 py-3">Student</th>
              <th className="px-4 py-3">Score</th>
              <th className="px-4 py-3">Max</th>
              <th className="px-4 py-3">Status</th>
            </tr>
          </thead>
          <tbody>
            {rows.map((row) => (
              <tr key={row.id} className="border-t border-slate-200">
                <td className="px-4 py-3">{row.student_identifier}</td>
                <td className="px-4 py-3">{row.score}</td>
                <td className="px-4 py-3">{row.max_score}</td>
                <td className="px-4 py-3">{row.review_status}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
