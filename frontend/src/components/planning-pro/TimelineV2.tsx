import type { ReactNode } from "react";

export interface TimelineAssignment {
  id: number | string;
  collaboratorId: number;
  status: string;
  source: string;
}

export interface TimelineConflict {
  rule: string;
  type: "hard" | "soft";
}

export interface TimelineItem {
  id: string;
  label: string;
  start: string;
  end: string;
  role: string;
  status: "draft" | "published" | "cancelled";
  teamColor?: string;
  assignments: TimelineAssignment[];
  conflicts: TimelineConflict[];
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
                  className={`relative flex min-w-[200px] flex-col rounded-md border px-3 py-2 text-xs shadow-sm ${resolveStatus(
                    item.status,
                    item.conflicts,
                  )}`}
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
                    <span className="text-slate-500"> -&gt; </span>
                    <span className="font-mono text-[11px] text-indigo-200">{item.end}</span>
                  </div>
                  <div className="mt-2 flex flex-wrap gap-1">
                    {item.assignments.map((assignment) => (
                      <span
                        key={`${item.id}-${assignment.id}`}
                        className="rounded bg-slate-800 px-2 py-0.5 text-[11px] text-indigo-100"
                      >
                        Collab {assignment.collaboratorId} - {assignment.status}
                        {assignment.source === "auto-assign-v1" ? " - proposed" : ""}
                      </span>
                    ))}
                    {item.assignments.length === 0 ? (
                      <span className="rounded bg-slate-800 px-2 py-0.5 text-[11px] text-slate-300">No assignment</span>
                    ) : null}
                  </div>
                  {item.conflicts.length > 0 ? (
                    <div className="mt-2 flex flex-wrap gap-1">
                      {item.conflicts.map((conflict) => (
                        <span
                          key={`${item.id}-${conflict.rule}`}
                          className={`rounded px-2 py-0.5 text-[11px] ${
                            conflict.type === "hard"
                              ? "bg-rose-500/20 text-rose-200"
                              : "bg-amber-400/20 text-amber-100"
                          }`}
                        >
                          {conflict.rule} ({conflict.type})
                        </span>
                      ))}
                    </div>
                  ) : null}
                </div>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

function resolveStatus(status: TimelineItem["status"], conflicts: TimelineConflict[]): string {
  if (conflicts.some((conflict) => conflict.type === "hard")) {
    return "border-rose-500/80 bg-rose-500/10";
  }
  if (conflicts.some((conflict) => conflict.type === "soft")) {
    return "border-amber-400/80 bg-amber-500/10";
  }
  switch (status) {
    case "published":
      return "border-emerald-500/80 bg-emerald-500/10";
    case "cancelled":
      return "border-slate-600 bg-slate-800/60";
    default:
      return "border-slate-700 bg-slate-800/80";
  }
}
