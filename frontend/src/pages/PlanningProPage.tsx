import { useMemo } from "react";
import { useQuery } from "@tanstack/react-query";

import { listShiftInstances, getPlanningProConfig } from "../api/entities";
import type { PlanningShift } from "../api/types";
import { PlanningTimelineV2, type TimelineRow } from "../components/planning-pro/TimelineV2";

function toTimeLabel(value: string): string {
  return new Date(value).toISOString().substring(11, 16);
}

function mapShiftsToRows(shifts: PlanningShift[]): TimelineRow[] {
  const rows = new Map<number, TimelineRow>();
  shifts.forEach((item) => {
    const { shift, assignments, conflicts } = item;
    const row = rows.get(shift.site_id) ?? {
      id: `site-${shift.site_id}`,
      title: `Site ${shift.site_id}`,
      subtitle: `Role ${shift.role_id}`,
      items: [],
    };
    row.items.push({
      id: `shift-${shift.id}`,
      label: `Shift ${shift.id}`,
      role: `Role ${shift.role_id}`,
      start: toTimeLabel(shift.start_utc),
      end: toTimeLabel(shift.end_utc),
      status: shift.status,
      assignments: assignments.map((assignment) => ({
        id: assignment.id,
        collaboratorId: assignment.collaborator_id,
        status: assignment.status,
        source: assignment.source,
      })),
      conflicts: conflicts.map((conflict) => ({
        rule: conflict.rule,
        type: conflict.type,
      })),
    });
    rows.set(shift.site_id, row);
  });
  return Array.from(rows.values());
}

export function PlanningProPage() {
  const { data: shifts, isLoading: loadingShifts } = useQuery({
    queryKey: ["planning", "shifts"],
    queryFn: listShiftInstances,
  });
  const { data: rules } = useQuery({ queryKey: ["planning", "rules"], queryFn: getPlanningProConfig });

  const rows = useMemo(() => mapShiftsToRows(shifts ?? []), [shifts]);

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-2 lg:flex-row lg:items-center lg:justify-between">
        <div>
          <p className="text-xs uppercase tracking-widest text-indigo-300">Planning PRO V2</p>
          <h2 className="text-2xl font-semibold text-slate-100">Timeline avancée connectée</h2>
          <p className="text-sm text-slate-300">
            Timeline V2 branchée sur l'API Planning PRO : shifts, assignments, conflits et statuts réels.
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
            <p className="text-xs uppercase tracking-wide text-indigo-300">Règles actives</p>
            <p className="text-sm text-slate-300">
              {rules?.hr_rules.length || 0} règles HR · {rules?.conflict_rules.length || 0} règles de conflit.
            </p>
          </div>
          <div className="rounded-md border border-dashed border-slate-800 p-3 text-sm text-slate-400">
            Filtres à venir (site, équipe, statut) et liste des collaborateurs.
          </div>
        </aside>

        <section className="space-y-3">
          {loadingShifts ? (
            <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4 text-slate-300">Chargement du planning...</div>
          ) : (
            <PlanningTimelineV2 rows={rows} />
          )}
          <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-xs uppercase tracking-wide text-indigo-300">Conflits & règles</p>
                <p className="text-sm text-slate-300">Conflicts détectés côté API (hard vs soft) visibles dans la timeline.</p>
              </div>
              <button className="rounded-md bg-slate-800 px-3 py-1 text-sm text-indigo-100 hover:bg-slate-700">
                Export CSV
              </button>
            </div>
            <div className="mt-3 rounded-md border border-dashed border-slate-800 p-3 text-sm text-slate-400">
              Les conflits hard sont surlignés en rouge, les soft en ambre dans la timeline ci-dessus.
            </div>
          </div>
        </section>
      </div>
    </div>
  );
}
