import { FormEvent, useEffect, useState } from "react";
import { apiRequest } from "../../lib/api";

type User = {
  id: string;
  email: string;
  full_name: string;
  role: string;
  is_active: boolean;
};

export function UsersPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [email, setEmail] = useState("staff@example.com");
  const [fullName, setFullName] = useState("Scanner Staff");
  const [password, setPassword] = useState("staff123");
  const [role, setRole] = useState("staff");

  async function load() {
    const data = await apiRequest<User[]>("/auth/users");
    setUsers(data);
  }

  async function createUser(event: FormEvent) {
    event.preventDefault();
    await apiRequest("/auth/users", {
      method: "POST",
      body: JSON.stringify({
        email,
        full_name: fullName,
        password,
        role
      })
    });
    await load();
  }

  useEffect(() => {
    void load();
  }, []);

  return (
    <section className="grid gap-6 lg:grid-cols-[360px_1fr]">
      <form className="panel space-y-4 p-6" onSubmit={createUser}>
        <h2 className="text-2xl font-black">Create User</h2>
        <input className="input" value={fullName} onChange={(e) => setFullName(e.target.value)} placeholder="Full name" />
        <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input className="input" value={password} onChange={(e) => setPassword(e.target.value)} type="password" placeholder="Password" />
        <select className="input" value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="staff">Staff / Scanner Operator</option>
          <option value="viewer">Read-only Viewer</option>
          <option value="super_admin">Super Admin</option>
        </select>
        <button className="button-primary w-full" type="submit">
          Add User
        </button>
      </form>

      <div className="space-y-4">
        {users.map((user) => (
          <article key={user.id} className="panel p-6">
            <h3 className="text-xl font-bold">{user.full_name}</h3>
            <p className="text-sm text-slate-600">
              {user.email} · {user.role} · {user.is_active ? "active" : "disabled"}
            </p>
          </article>
        ))}
      </div>
    </section>
  );
}
