import { FormEvent, useState } from "react";
import { apiRequest } from "../../lib/api";

type AnswerKeyRow = {
  question_no: number;
  correct_option: string;
  set_code: string;
};

export function AnswerKeysPage() {
  const [examId, setExamId] = useState("");
  const [rows, setRows] = useState<AnswerKeyRow[]>([]);

  async function load() {
    if (!examId) return;
    const data = await apiRequest<AnswerKeyRow[]>(`/exams/${examId}/answer-keys`);
    setRows(data);
  }

  async function save(event: FormEvent) {
    event.preventDefault();
    if (!examId) return;
    await apiRequest(`/exams/${examId}/answer-keys`, {
      method: "PUT",
      body: JSON.stringify({ items: rows })
    });
    await load();
  }

  function seedRows() {
    setRows(Array.from({ length: 50 }, (_, i) => ({ question_no: i + 1, correct_option: "A", set_code: "A" })));
  }

  return (
    <section className="space-y-6">
      <div className="panel flex flex-col gap-4 p-6 md:flex-row">
        <input className="input" value={examId} onChange={(e) => setExamId(e.target.value)} placeholder="Exam ID" />
        <button className="button-secondary" onClick={() => void load()}>
          Load Answer Keys
        </button>
        <button className="button-primary" onClick={seedRows}>
          Seed 50 Questions
        </button>
      </div>

      <form className="panel p-6" onSubmit={save}>
        <div className="grid gap-3 md:grid-cols-4">
          {rows.slice(0, 20).map((row, index) => (
            <div key={row.question_no} className="rounded-2xl border border-slate-200 p-3">
              <p className="text-sm font-semibold">Q{row.question_no}</p>
              <select
                className="input mt-2"
                value={row.correct_option}
                onChange={(e) =>
                  setRows((current) =>
                    current.map((item, itemIndex) =>
                      itemIndex === index ? { ...item, correct_option: e.target.value } : item
                    )
                  )
                }
              >
                <option value="A">A</option>
                <option value="B">B</option>
                <option value="C">C</option>
                <option value="D">D</option>
              </select>
            </div>
          ))}
        </div>
        <button className="button-primary mt-6" type="submit">
          Save Answer Keys
        </button>
      </form>
    </section>
  );
}

