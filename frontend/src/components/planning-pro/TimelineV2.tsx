import type { ReactNode } from "react";

export interface TimelineItem {
  id: string;
  label: string;
  start: string;
  end: string;
  role: string;
  status: "draft" | "published" | "warning" | "error";
  teamColor?: string;
}

export interface TimelineRow {
  id: string;
  title: string;
  subtitle?: string;
  items: TimelineItem[];
}

interface PlanningTimelineV2Props {
  rows: TimelineRow[];
  headerSlot?: ReactNode;
}

export function PlanningTimelineV2({ rows, headerSlot }: PlanningTimelineV2Props) {
  return (
    <div className="rounded-lg border border-slate-800 bg-slate-950/60">
      <div className="flex items-center justify-between border-b border-slate-800 px-4 py-3">
        <div>
          <p className="text-xs uppercase tracking-wide text-indigo-300">Timeline V2</p>
          <p className="text-sm text-slate-200">Zoom jour/semaine avec groupes dynamiques</p>
        </div>
        {headerSlot}
      </div>
      <div className="divide-y divide-slate-900">
        {rows.map((row) => (
          <div key={row.id} className="px-4 py-3">
            <div className="mb-2 flex items-center justify-between">
              <div>
                <p className="font-medium text-slate-100">{row.title}</p>
                {row.subtitle ? <p className="text-xs text-slate-400">{row.subtitle}</p> : null}
              </div>
              <div className="text-xs text-slate-400">{row.items.length} shifts</div>
            </div>
            <div className="flex flex-wrap gap-2">
              {row.items.map((item) => (
                <div
                  key={item.id}
                  className={`relative flex min-w-[180px] flex-col rounded-md border px-3 py-2 text-xs shadow-sm ${resolveStatus(item.status)}`}
                  style={{ borderColor: item.teamColor ?? "#6366f1" }}
                >
                  <div className="flex items-center justify-between gap-2">
                    <span className="font-semibold text-slate-100">{item.label}</span>
                    <span className="rounded bg-slate-800 px-2 py-0.5 text-[10px] uppercase tracking-wide text-slate-200">
                      {item.role}
                    </span>
                  </div>
                  <div className="mt-1 text-slate-300">
                    <span className="font-mono text-[11px] text-indigo-200">{item.start}</span>
                    <span className="text-slate-500"> → </span>
                    <span className="font-mono text-[11px] text-indigo-200">{item.end}</span>
                  </div>
                  <div className="mt-2 flex items-center gap-2">
                    <span className="h-2 w-2 rounded-full" style={{ backgroundColor: item.teamColor ?? "#6366f1" }} />
                    <p className="text-[11px] text-slate-300">{describeStatus(item.status)}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function resolveStatus(status: TimelineItem["status"]): string {
  switch (status) {
    case "published":
      return "border-emerald-500/80 bg-emerald-500/10";
    case "warning":
      return "border-amber-400/80 bg-amber-500/10";
    case "error":
      return "border-rose-500/80 bg-rose-500/10";
    default:
      return "border-slate-700 bg-slate-800/80";
  }
}

function describeStatus(status: TimelineItem["status"]): string {
  switch (status) {
    case "published":
      return "Publié";
    case "warning":
      return "Avertissement (contrôle soft)";
    case "error":
      return "Erreur bloquante";
    default:
      return "Brouillon";
  }
}
