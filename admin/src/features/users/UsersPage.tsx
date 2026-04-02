import { FormEvent, useEffect, useState } from "react";
import { api, User } from "../../lib/api";

export function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [form, setForm] = useState({ full_name: "", email: "", password: "", role: "admin" });

  async function refresh() {
    setUsers(await api.listUsers());
  }

  useEffect(() => {
    refresh();
  }, []);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    await api.createUser(form);
    setForm({ full_name: "", email: "", password: "", role: "admin" });
    refresh();
  }

  return (
    <div className="grid gap-6 xl:grid-cols-[340px_1fr]">
      <section className="panel p-6">
        <h2 className="text-2xl font-semibold">Create user</h2>
        <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
          <input className="input" placeholder="Full name" value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          <input className="input" placeholder="Email" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
          <input
            className="input"
            type="password"
            placeholder="Temporary password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <select className="input" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
            <option value="admin">admin</option>
            <option value="operator">operator</option>
            <option value="reviewer">reviewer</option>
          </select>
          <button className="button-primary w-full" type="submit">
            Create user
          </button>
        </form>
      </section>

      <section className="panel p-6">
        <h2 className="text-2xl font-semibold">Users</h2>
        <div className="mt-6 space-y-3">
          {users.map((user) => (
            <article key={user.id} className="rounded-2xl border border-slate-200 bg-white/70 px-4 py-4">
              <div className="flex items-center justify-between gap-4">
                <div>
                  <h3 className="font-semibold">{user.full_name}</h3>
                  <p className="text-sm text-slate-600">{user.email}</p>
                </div>
                <span className="rounded-full bg-slate-900 px-3 py-1 text-xs font-semibold uppercase tracking-[0.25em] text-white">{user.role}</span>
              </div>
            </article>
          ))}
        </div>
      </section>
    </div>
  );
}
