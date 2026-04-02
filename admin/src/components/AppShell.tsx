import { NavLink, Outlet } from "react-router-dom";
import { getUserRole } from "../lib/auth";

export function AppShell() {
  const role = getUserRole();
  const navItems = [
    { label: "Dashboard", to: "/", roles: ["super_admin", "staff", "viewer"] },
    { label: "Exams", to: "/exams", roles: ["super_admin"] },
    { label: "Answer Keys", to: "/answer-keys", roles: ["super_admin"] },
    { label: "Templates", to: "/templates", roles: ["super_admin"] },
    { label: "Review", to: "/review", roles: ["super_admin", "staff", "viewer"] },
    { label: "Results", to: "/results", roles: ["super_admin", "staff", "viewer"] },
    { label: "Users", to: "/users", roles: ["super_admin"] }
  ].filter((item) => item.roles.includes(role));

  return (
    <div className="min-h-screen px-6 py-8 text-ink">
      <div className="mx-auto grid max-w-7xl gap-6 lg:grid-cols-[260px_1fr]">
        <aside className="panel p-6">
          <div className="mb-8">
            <p className="text-sm uppercase tracking-[0.3em] text-brand">Institute Ops</p>
            <h1 className="mt-3 text-3xl font-black">OMR Control</h1>
            <p className="mt-2 text-sm text-slate-600">Role: {role.replace("_", " ")}</p>
          </div>

          <nav className="space-y-2">
            {navItems.map((item) => (
              <NavLink
                key={item.to}
                to={item.to}
                end={item.to === "/"}
                className={({ isActive }) =>
                  `block rounded-2xl px-4 py-3 font-medium transition ${
                    isActive ? "bg-brand text-white" : "hover:bg-slate-100"
                  }`
                }
              >
                {item.label}
              </NavLink>
            ))}
          </nav>
        </aside>

        <main className="space-y-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
}
