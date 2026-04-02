import { FormEvent, useEffect, useState } from "react";
import { apiRequest } from "../../lib/api";

type Exam = {
  id: string;
  title: string;
  subject: string;
  total_questions: number;
  options_per_question: number;
  positive_marks: number;
  negative_marks: number;
  answer_key: Record<string, string>;
};

type ExamPageResponse = {
  items: Exam[];
  meta: { page: number; page_size: number; total: number };
};

export function ExamsPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [title, setTitle] = useState("Mock Test 1");
  const [subject, setSubject] = useState("Physics");
  const [questions, setQuestions] = useState(50);

  async function load() {
    const data = await apiRequest<ExamPageResponse>("/exams");
    setExams(data.items);
  }

  useEffect(() => {
    void load();
  }, []);

  async function createExam(event: FormEvent) {
    event.preventDefault();
    const answerKey = Object.fromEntries(Array.from({ length: questions }, (_, i) => [`${i + 1}`, "A"]));
    await apiRequest("/exams", {
      method: "POST",
      body: JSON.stringify({
        title,
        subject,
        total_questions: questions,
        options_per_question: 4,
        positive_marks: 1,
        negative_marks: 0,
        answer_key: answerKey
      })
    });
    await load();
  }

  async function generateTemplate(examId: string) {
    await apiRequest(`/templates/generate`, { method: "POST", body: JSON.stringify({ exam_id: examId }) });
    alert("Template generated on backend storage.");
  }

  return (
    <section className="grid gap-6 lg:grid-cols-[360px_1fr]">
      <form className="panel space-y-4 p-6" onSubmit={createExam}>
        <h2 className="text-2xl font-black">Create Exam</h2>
        <input className="input" value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Exam title" />
        <input className="input" value={subject} onChange={(e) => setSubject(e.target.value)} placeholder="Subject" />
        <input
          className="input"
          value={questions}
          onChange={(e) => setQuestions(Number(e.target.value))}
          type="number"
          min={1}
          max={300}
          placeholder="Questions"
        />
        <button className="button-primary w-full" type="submit">
          Save Exam
        </button>
      </form>

      <div className="space-y-4">
        {exams.map((exam) => (
          <article key={exam.id} className="panel flex flex-col gap-4 p-6 md:flex-row md:items-center md:justify-between">
            <div>
              <h3 className="text-xl font-bold">{exam.title}</h3>
              <p className="text-sm text-slate-600">
                {exam.subject} · {exam.total_questions} questions
              </p>
            </div>
            <button className="button-secondary" onClick={() => void generateTemplate(exam.id)}>
              Generate Template PDF
            </button>
          </article>
        ))}
      </div>
    </section>
  );
}
