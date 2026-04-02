import { FormEvent, useEffect, useState } from "react";
import { api, AnswerKeyRow, Exam } from "../../lib/api";

function buildRows(setCode: string): AnswerKeyRow[] {
  return Array.from({ length: 50 }, (_, index) => ({
    set_code: setCode,
    question_number: index + 1,
    correct_option: "A",
  }));
}

export function AnswerKeysPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [selectedExamId, setSelectedExamId] = useState("");
  const [setCode, setSetCode] = useState("A");
  const [rows, setRows] = useState<AnswerKeyRow[]>(buildRows("A"));

  useEffect(() => {
    api.listExams().then((items) => {
      setExams(items);
      if (items[0]) setSelectedExamId(items[0].id);
    });
  }, []);

  useEffect(() => {
    setRows(buildRows(setCode));
  }, [setCode]);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await api.replaceAnswerKeys({ exam_id: selectedExamId, rows });
  }

  return (
    <section className="panel p-6">
      <div className="flex flex-wrap items-center gap-4">
        <h2 className="text-2xl font-semibold">Answer keys</h2>
        <select className="input max-w-xs" value={selectedExamId} onChange={(event) => setSelectedExamId(event.target.value)}>
          {exams.map((exam) => (
            <option key={exam.id} value={exam.id}>
              {exam.title}
            </option>
          ))}
        </select>
        <select className="input max-w-[100px]" value={setCode} onChange={(event) => setSetCode(event.target.value)}>
          {["A", "B", "C", "D"].map((code) => (
            <option key={code}>{code}</option>
          ))}
        </select>
      </div>

      <form className="mt-6" onSubmit={handleSubmit}>
        <div className="grid gap-2 md:grid-cols-2 xl:grid-cols-5">
          {rows.map((row, index) => (
            <label key={row.question_number} className="rounded-2xl border border-slate-200 bg-white/70 p-3">
              <span className="mb-2 block text-sm font-medium">Q{row.question_number}</span>
              <select
                className="input"
                value={row.correct_option}
                onChange={(event) =>
                  setRows((current) =>
                    current.map((item, itemIndex) =>
                      itemIndex === index ? { ...item, correct_option: event.target.value } : item,
                    ),
                  )
                }
              >
                {["A", "B", "C", "D"].map((option) => (
                  <option key={option}>{option}</option>
                ))}
              </select>
            </label>
          ))}
        </div>
        <button className="button-primary mt-6" type="submit">
          Replace answer key
        </button>
      </form>
    </section>
  );
}
