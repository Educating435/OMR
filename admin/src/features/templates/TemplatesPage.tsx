import { useEffect, useState } from "react";
import { api, Exam, Template } from "../../lib/api";

export function TemplatesPage() {
  const [exams, setExams] = useState<Exam[]>([]);
  const [templates, setTemplates] = useState<Template[]>([]);
  const [selectedExamId, setSelectedExamId] = useState("");

  async function refresh(examId?: string) {
    setTemplates(await api.listTemplates(examId));
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
        <h2 className="text-2xl font-semibold">Official templates</h2>
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
        <button
          className="button-primary"
          type="button"
          onClick={async () => {
            await api.generateTemplate(selectedExamId);
            refresh(selectedExamId);
          }}
        >
          Generate A4 PDF template
        </button>
      </div>

      <div className="mt-6 grid gap-4 lg:grid-cols-2">
        {templates.map((template) => (
          <article key={template.id} className="rounded-3xl border border-slate-200 bg-white/70 p-5">
            <p className="text-xs font-semibold uppercase tracking-[0.35em] text-emerald-700">{template.template_code}</p>
            <h3 className="mt-2 text-xl font-semibold">Version {template.template_version}</h3>
            <p className="mt-2 text-sm text-slate-600">PDF path: {template.pdf_storage_path}</p>
            <p className="mt-2 text-sm text-slate-600">QR exam id: {String(template.qr_payload.exam_id)}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
