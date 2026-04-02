import { useEffect, useState } from "react";
import { api, Exam, Result } from "../../lib/api";

export function ResultsPage() {
  const [results, setResults] = useState<Result[]>([]);
  const [exams, setExams] = useState<Exam[]>([]);
  const [selectedExamId, setSelectedExamId] = useState("");

  async function refresh(examId?: string) {
    setResults(await api.listResults({ examId }));
  }

  useEffect(() => {
    api.listExams().then((items) => {
      setExams(items);
      if (items[0]) {
        setSelectedExamId(items[0].id);
        refresh(items[0].id);
      }
    });
  }, []);

  return (
    <section className="panel p-6">
      <div className="flex flex-wrap items-center gap-4">
        <h2 className="text-2xl font-semibold">Results</h2>
        <select
          className="input max-w-xs"
          value={selectedExamId}
          onChange={(event) => {
            setSelectedExamId(event.target.value);
            refresh(event.target.value);
          }}
        >
          {exams.map((exam) => (
            <option key={exam.id} value={exam.id}>
              {exam.title}
            </option>
          ))}
        </select>
        <button className="button-secondary" onClick={() => refresh(selectedExamId)} type="button">
          Refresh
        </button>
      </div>

      <div className="mt-6 overflow-x-auto">
        <table className="min-w-full text-left text-sm">
          <thead className="text-slate-500">
            <tr>
              <th className="pb-3">Roll</th>
              <th className="pb-3">Set</th>
              <th className="pb-3">Score</th>
              <th className="pb-3">Correct</th>
              <th className="pb-3">Review</th>
            </tr>
          </thead>
          <tbody>
            {results.map((result) => (
              <tr key={result.id} className="border-t border-slate-200/70">
                <td className="py-4 font-medium">{result.roll_number}</td>
                <td>{result.set_code}</td>
                <td>
                  {result.score} / {result.max_score}
                </td>
                <td>{result.correct_count}</td>
                <td>{result.needs_review ? "Flagged" : "Clear"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  );
}
