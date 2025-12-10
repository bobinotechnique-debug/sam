import { useEffect, useState } from "react";

interface HealthResponse {
  status: string;
}

const apiBaseUrl = typeof __API_BASE_URL__ !== "undefined" ? __API_BASE_URL__ : "http://localhost:8000";

function App() {
  const [health, setHealth] = useState<HealthResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetch(`${apiBaseUrl}/api/v1/health`)
      .then(async (response) => {
        if (!response.ok) {
          throw new Error(`Unexpected status ${response.status}`);
        }
        return response.json();
      })
      .then((body: HealthResponse) => setHealth(body))
      .catch((err: Error) => setError(err.message));
  }, []);

  return (
    <main className="min-h-screen bg-slate-950 text-slate-100">
      <div className="mx-auto flex max-w-5xl flex-col gap-6 px-6 py-16">
        <header className="flex flex-col gap-2">
          <p className="text-sm uppercase tracking-wide text-indigo-300">Codex Starter</p>
          <h1 className="text-3xl font-semibold">FastAPI + React + Tailwind</h1>
          <p className="text-slate-300">
            Enterprise-ready bootstrap with CI, Docker Compose, and strict quality gates.
          </p>
        </header>

        <section className="rounded-lg border border-slate-800 bg-slate-900/60 p-6 shadow-lg">
          <h2 className="text-xl font-semibold text-indigo-200">Backend status</h2>
          {health && !error && (
            <p className="mt-2 text-green-300">API healthy: {health.status}</p>
          )}
          {error && <p className="mt-2 text-red-300">Failed to reach API: {error}</p>}
          {!health && !error && <p className="mt-2 text-slate-300">Checking health...</p>}
          <p className="mt-4 text-sm text-slate-400">API base URL: {apiBaseUrl}</p>
        </section>

        <section className="grid gap-4 md:grid-cols-3">
          <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
            <h3 className="font-semibold text-indigo-200">Backend</h3>
            <ul className="mt-2 list-disc space-y-1 pl-4 text-slate-200">
              <li>FastAPI with layered structure</li>
              <li>In-memory CRUD service ready for DB swap</li>
              <li>Strict typing, ruff, mypy, pytest</li>
            </ul>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
            <h3 className="font-semibold text-indigo-200">Frontend</h3>
            <ul className="mt-2 list-disc space-y-1 pl-4 text-slate-200">
              <li>React + Vite + Tailwind</li>
              <li>API health indicator</li>
              <li>ESLint + Vitest baseline</li>
            </ul>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-900/50 p-4">
            <h3 className="font-semibold text-indigo-200">DevOps</h3>
            <ul className="mt-2 list-disc space-y-1 pl-4 text-slate-200">
              <li>Docker Compose for local stack</li>
              <li>GitHub Actions with lint + tests</li>
              <li>.env.example for config</li>
            </ul>
          </div>
        </section>
      </div>
    </main>
  );
}

export default App;
