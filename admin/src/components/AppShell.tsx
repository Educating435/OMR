import { NavLink, Outlet, useNavigate } from "react-router-dom";
import { clearSession } from "../lib/auth";

const links = [
  { to: "/", label: "Dashboard" },
  { to: "/exams", label: "Exams" },
  { to: "/answer-keys", label: "Answer Keys" },
  { to: "/templates", label: "Templates" },
  { to: "/results", label: "Results" },
  { to: "/review", label: "Review" },
  { to: "/users", label: "Users" },
];

export function AppShell() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-[radial-gradient(circle_at_top_left,_rgba(20,88,78,0.18),_transparent_28%),linear-gradient(180deg,_#f4efe7,_#edf6f2)] text-slate-900">
      <div className="mx-auto grid min-h-screen max-w-7xl grid-cols-1 gap-6 p-6 lg:grid-cols-[260px_1fr]">
        <aside className="panel flex flex-col gap-6 p-6">
          <div>
            <p className="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-700">OMR Scanner</p>
            <h1 className="mt-2 text-3xl font-semibold text-slate-900">Admin Control</h1>
            <p className="mt-2 text-sm text-slate-600">Render-hosted API, Hostinger MySQL source of truth, Android sync clients.</p>
          </div>

          <nav className="space-y-2">
            {links.map((link) => (
              <NavLink
                key={link.to}
                to={link.to}
                end={link.to === "/"}
                className={({ isActive }) =>
                  `block rounded-2xl px-4 py-3 text-sm font-medium transition ${
                    isActive ? "bg-slate-900 text-white" : "bg-white/60 text-slate-700 hover:bg-white"
                  }`
                }
              >
                {link.label}
              </NavLink>
            ))}
          </nav>

          <button
            type="button"
            className="button-secondary mt-auto"
            onClick={() => {
              clearSession();
              navigate("/login", { replace: true });
            }}
          >
            Sign out
          </button>
        </aside>

        <main className="space-y-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
