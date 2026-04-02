import { useState } from "react";
import { apiRequest } from "../../lib/api";

type Template = {
  id: string;
  exam_id: string;
  revision: number;
  pdf_path: string;
};

type TemplatePageResponse = {
  items: Template[];
  meta: { page: number; page_size: number; total: number };
};

export function TemplatesPage() {
  const [examId, setExamId] = useState("");
  const [templates, setTemplates] = useState<Template[]>([]);

  async function loadAll() {
    const response = await apiRequest<TemplatePageResponse>("/templates");
    setTemplates(response.items);
  }

  async function generate() {
    if (!examId) return;
    await apiRequest("/templates/generate", {
      method: "POST",
      body: JSON.stringify({ exam_id: examId })
    });
    await loadAll();
  }

  return (
    <section className="space-y-6">
      <div className="panel flex flex-col gap-4 p-6 md:flex-row">
        <input className="input" value={examId} onChange={(e) => setExamId(e.target.value)} placeholder="Exam ID for generation" />
        <button className="button-primary" onClick={() => void generate()}>
          Generate Template
        </button>
        <button className="button-secondary" onClick={() => void loadAll()}>
          Refresh List
        </button>
      </div>

      <div className="space-y-4">
        {templates.map((template) => (
          <article key={template.id} className="panel p-6">
            <h3 className="text-xl font-bold">Template Revision {template.revision}</h3>
            <p className="text-sm text-slate-600">Exam {template.exam_id}</p>
            <p className="mt-2 text-sm text-slate-500">{template.pdf_path}</p>
          </article>
        ))}
      </div>
    </section>
  );
}
