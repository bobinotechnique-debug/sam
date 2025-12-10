import { useMemo } from "react";

import { PlanningTimelineV2, type TimelineRow } from "../components/planning-pro/TimelineV2";

const mockRows: TimelineRow[] = [
  {
    id: "site-a",
    title: "Site A — Équipe Nuit",
    subtitle: "UTC · 3 rôles",
    items: [
      {
        id: "shift-1",
        label: "Mission Alpha",
        role: "Technicien",
        start: "08:00",
        end: "12:00",
        status: "draft",
        teamColor: "#4f46e5",
      },
      {
        id: "shift-2",
        label: "Mission Bravo",
        role: "Opérateur",
        start: "12:00",
        end: "18:00",
        status: "warning",
        teamColor: "#f59e0b",
      },
    ],
  },
  {
    id: "site-b",
    title: "Site B — Production",
    subtitle: "UTC · capacité 4",
    items: [
      {
        id: "shift-3",
        label: "Mission Charlie",
        role: "Chef",
        start: "09:00",
        end: "17:00",
        status: "published",
        teamColor: "#22c55e",
      },
      {
        id: "shift-4",
        label: "Mission Delta",
        role: "Logistique",
        start: "14:00",
        end: "20:00",
        status: "error",
        teamColor: "#ef4444",
      },
    ],
  },
];

export function PlanningProPage() {
  const rows = useMemo(() => mockRows, []);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-widest text-indigo-300">Planning PRO V2</p>
          <h2 className="text-2xl font-semibold text-slate-100">Timeline avancée (fondations)</h2>
          <p className="text-sm text-slate-300">
            Structure de page pour la timeline V2 avec filtres, panneau de conflits et publication.
          </p>
        </div>
        <div className="flex gap-2">
          <button className="rounded-md bg-slate-800 px-3 py-2 text-sm text-white hover:bg-slate-700">
            Préparer publication
          </button>
          <button className="rounded-md bg-indigo-600 px-3 py-2 text-sm text-white hover:bg-indigo-500">
            Lancer auto-assign v1
          </button>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-4 lg:grid-cols-[320px,1fr]">
        <aside className="space-y-3 rounded-lg border border-slate-800 bg-slate-950/60 p-4">
          <div>
            <p className="text-xs uppercase tracking-wide text-indigo-300">Filtres & collaborateurs</p>
            <p className="text-sm text-slate-300">Placeholder pour filtres (site, équipe, rôle, statut, conflits).</p>
          </div>
          <div className="rounded-md border border-dashed border-slate-800 p-3 text-sm text-slate-400">
            TODO Step 06 : liste des collaborateurs drag & drop avec états de conflit/disponibilité.
          </div>
        </aside>

        <section className="space-y-3">
          <PlanningTimelineV2 rows={rows} headerSlot={<TimelineHeader />} />
          <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-wide text-indigo-300">Conflits & règles</p>
                <p className="text-sm text-slate-300">Surface dédiée aux erreurs/avertissements + ancres timeline.</p>
              </div>
              <button className="rounded-md bg-slate-800 px-3 py-1 text-sm text-indigo-100 hover:bg-slate-700">
                Export CSV
              </button>
            </div>
            <div className="mt-3 rounded-md border border-dashed border-slate-800 p-3 text-sm text-slate-400">
              TODO Step 07 : liste des conflits détaillés (double booking, capacités, repos, skills) avec filtres.
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}

function TimelineHeader() {
  return (
    <div className="flex items-center gap-2 text-xs text-slate-200">
      <span className="rounded bg-slate-800 px-2 py-1">Zoom jour</span>
      <span className="rounded bg-slate-800 px-2 py-1">Snapping 15 min</span>
      <span className="rounded bg-slate-800 px-2 py-1 text-indigo-200">Mode highlight conflits</span>
    </div>
  );
}
