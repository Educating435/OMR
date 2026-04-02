import { FormEvent, useEffect, useState } from "react";
import { api, Exam } from "../../lib/api";

const initialForm = {
  title: "",
  subject: "",
  exam_date: "",
  total_questions: 50,
  options_per_question: 4,
  roll_number_digits: 6,
  supported_set_codes: ["A", "B", "C", "D"],
  positive_marks: 1,
  negative_marks: 0,
};

export function ExamsPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [form, setForm] = useState(initialForm);

  async function refresh() {
    setExams(await api.listExams());
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await api.createExam({
      ...form,
      exam_date: form.exam_date || null,
    });
    setForm(initialForm);
    refresh();
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[380px_1fr]">
      <section className="panel p-6">
        <h2 className="text-2xl font-semibold">Create exam</h2>
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <input className="input" placeholder="Exam title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          <input className="input" placeholder="Subject" value={form.subject} onChange={(e) => setForm({ ...form, subject: e.target.value })} />
          <input className="input" type="date" value={form.exam_date} onChange={(e) => setForm({ ...form, exam_date: e.target.value })} />
          <div className="grid grid-cols-2 gap-3">
            <input
              className="input"
              type="number"
              value={form.total_questions}
              onChange={(e) => setForm({ ...form, total_questions: Number(e.target.value) })}
            />
            <input
              className="input"
              type="number"
              value={form.roll_number_digits}
              onChange={(e) => setForm({ ...form, roll_number_digits: Number(e.target.value) })}
            />
          </div>
          <button className="button-primary w-full" type="submit">
            Save exam
          </button>
        </form>
      </section>

      <section className="panel p-6">
        <div className="flex items-center justify-between">
          <h2 className="text-2xl font-semibold">Exam registry</h2>
          <button className="button-secondary" onClick={refresh} type="button">
            Refresh
          </button>
        </div>
        <div className="mt-6 overflow-x-auto">
          <table className="min-w-full text-left text-sm">
            <thead className="text-slate-500">
              <tr>
                <th className="pb-3">Title</th>
                <th className="pb-3">Subject</th>
                <th className="pb-3">Questions</th>
                <th className="pb-3">Set codes</th>
              </tr>
            </thead>
            <tbody>
              {exams.map((exam) => (
                <tr key={exam.id} className="border-t border-slate-200/70">
                  <td className="py-4 font-medium">{exam.title}</td>
                  <td>{exam.subject}</td>
                  <td>{exam.total_questions}</td>
                  <td>{exam.supported_set_codes.join(", ")}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}
