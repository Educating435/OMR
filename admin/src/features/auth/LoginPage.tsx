import { FormEvent, useState } from "react";
import { useNavigate } from "react-router-dom";
import { apiRequest } from "../../lib/api";
import { saveAccessToken, saveUserRole } from "../../lib/auth";

type TokenResponse = {
  access_token: string;
  refresh_token: string;
  user_role: string;
};

export function LoginPage() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("admin@example.com");
  const [password, setPassword] = useState("admin123");
  const [error, setError] = useState("");

  async function onSubmit(event: FormEvent) {
    event.preventDefault();
    setError("");

    try {
      const response = await apiRequest<TokenResponse>("/auth/login", {
        method: "POST",
        body: JSON.stringify({ email, password })
      });
      saveAccessToken(response.access_token);
      saveUserRole(response.user_role);
      navigate("/");
    } catch {
      try {
        const response = await apiRequest<TokenResponse>("/auth/bootstrap-admin", {
          method: "POST",
          body: JSON.stringify({ email, password })
        });
        saveAccessToken(response.access_token);
        saveUserRole(response.user_role);
        navigate("/");
      } catch (bootstrapError) {
        setError(bootstrapError instanceof Error ? bootstrapError.message : "Unable to sign in");
      }
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center p-6">
      <form className="panel w-full max-w-md space-y-5 p-8" onSubmit={onSubmit}>
        <div>
          <p className="text-sm uppercase tracking-[0.3em] text-brand">Secure Access</p>
          <h1 className="mt-3 text-3xl font-black">OMR Admin Panel</h1>
        </div>
        <input className="input" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" />
        <input
          className="input"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          type="password"
          placeholder="Password"
        />
        {error ? <p className="text-sm text-red-600">{error}</p> : null}
        <button className="button-primary w-full" type="submit">
          Continue
        </button>
      </form>
    </div>
  );
}
