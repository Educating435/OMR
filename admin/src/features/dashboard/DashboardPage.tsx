import { useEffect, useState } from "react";
import { api, Exam, Result, Template, User } from "../../lib/api";

export function DashboardPage() {
  const [stats, setStats] = useState<{ exams: Exam[]; templates: Template[]; results: Result[]; users: User[] } | null>(null);

  useEffect(() => {
    Promise.all([api.listExams(), api.listTemplates(), api.listResults(), api.listUsers()]).then(([exams, templates, results, users]) =>
      setStats({ exams, templates, results, users }),
    );
  }, []);

  const cards = [
    { label: "Exams", value: stats?.exams.length ?? "-" },
    { label: "Official Templates", value: stats?.templates.length ?? "-" },
    { label: "Synced Results", value: stats?.results.length ?? "-" },
    { label: "Operators & Admins", value: stats?.users.length ?? "-" },
  ];

  return (
    <>
      <section className="panel p-8">
        <p className="text-xs font-semibold uppercase tracking-[0.35em] text-emerald-700">System status</p>
        <h2 className="mt-3 text-3xl font-semibold">Controlled-template OMR operations</h2>
        <p className="mt-3 max-w-3xl text-sm text-slate-600">
          IMPLEMENTED: admin exam setup, answer keys, official A4 template generation, offline-first Android result sync, and review/export
          endpoints.
        </p>
      </section>

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        {cards.map((card) => (
          <article key={card.label} className="panel p-6">
            <p className="text-sm text-slate-500">{card.label}</p>
            <p className="mt-4 text-4xl font-semibold text-slate-900">{card.value}</p>
          </article>
        ))}
      </section>
    </>
  );
}
