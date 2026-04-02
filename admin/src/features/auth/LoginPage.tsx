import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { api } from "../../lib/api";
import { saveSession } from "../../lib/auth";

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("change-me");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();
    setIsLoading(true);
    setError(null);
    try {
      const session = await api.login({ email, password });
      saveSession(session.access_token, session.role);
      navigate("/", { replace: true });
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed");
    } finally {
      setIsLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center bg-[linear-gradient(135deg,_#132623,_#2f5d50_45%,_#e4d8bf)] p-6">
      <div className="grid w-full max-w-5xl overflow-hidden rounded-[32px] bg-white shadow-2xl shadow-slate-950/20 lg:grid-cols-[1.1fr_0.9fr]">
        <section className="hidden bg-[radial-gradient(circle_at_top,_rgba(255,255,255,0.28),_transparent_35%),linear-gradient(180deg,_#133a35,_#0b1e1c)] p-10 text-white lg:block">
          <p className="text-xs font-semibold uppercase tracking-[0.4em] text-amber-200">Production flow</p>
          <h1 className="mt-5 text-4xl font-semibold leading-tight">Admin Panel and Android clients only ever talk to FastAPI.</h1>
          <ul className="mt-8 space-y-4 text-sm text-emerald-50/90">
            <li>IMPLEMENTED: exam, answer key, template, result, export, and user workflows are API-backed.</li>
            <li>IMPLEMENTED: Hostinger MySQL is the only server database target.</li>
            <li>TODO NEXT: role-specific dashboards and richer review evidence previews.</li>
          </ul>
        </section>

        <section className="p-8 lg:p-10">
          <p className="text-xs font-semibold uppercase tracking-[0.35em] text-emerald-700">Admin sign-in</p>
          <h2 className="mt-3 text-3xl font-semibold text-slate-900">OMR Scanner Console</h2>
          <p className="mt-2 text-sm text-slate-600">Use an admin account from the FastAPI backend. This UI never touches MySQL directly.</p>

          <form className="mt-8 space-y-4" onSubmit={handleSubmit}>
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-700">Email</span>
              <input className="input" value={email} onChange={(event) => setEmail(event.target.value)} />
            </label>
            <label className="block">
              <span className="mb-2 block text-sm font-medium text-slate-700">Password</span>
              <input className="input" type="password" value={password} onChange={(event) => setPassword(event.target.value)} />
            </label>
            {error ? <p className="rounded-2xl bg-rose-50 px-4 py-3 text-sm text-rose-700">{error}</p> : null}
            <button className="button-primary w-full" disabled={isLoading} type="submit">
              {isLoading ? "Signing in..." : "Sign in"}
            </button>
          </form>
        </section>
      </div>
    </div>
  );
}
