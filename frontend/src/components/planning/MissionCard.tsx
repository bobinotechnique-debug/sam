import { Mission } from "../../api/types";
import { computeBlockPosition, TimeRange } from "../../utils/planning";

interface MissionCardProps {
  mission: Mission;
  assignments: string[];
  range: TimeRange;
  index: number;
  onSelect: (mission: Mission) => void;
}

export function MissionCard({ mission, assignments, range, index, onSelect }: MissionCardProps) {
  const { offsetPercent, widthPercent } = computeBlockPosition(mission, range);
  const statusColor = mission.status === "cancelled" ? "bg-red-500/80" : mission.status === "published" ? "bg-emerald-500/80" : "bg-indigo-500/80";

  return (
    <button
      type="button"
      className="absolute overflow-hidden rounded-lg border border-slate-700 bg-indigo-500/20 text-left shadow hover:border-indigo-400"
      style={{
        left: `${offsetPercent}%`,
        width: `${widthPercent}%`,
        top: `${index * 72}px`,
        minHeight: "64px",
      }}
      onClick={() => onSelect(mission)}
    >
      <div className={`flex items-center gap-2 px-3 py-2 text-xs uppercase tracking-wide text-white ${statusColor}`}>
        <span>Mission #{mission.id}</span>
        <span className="rounded bg-white/10 px-2 py-1 text-[10px] capitalize">{mission.status}</span>
      </div>
      <div className="space-y-1 px-3 py-2 text-sm text-slate-100">
        <p className="truncate">{new Date(mission.start_utc).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })} → {new Date(mission.end_utc).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}</p>
        <p className="truncate text-xs text-indigo-100">Site #{mission.site_id}</p>
        {assignments.length > 0 ? (
          <p className="truncate text-xs text-emerald-100">{assignments.join(", ")}</p>
        ) : (
          <p className="truncate text-xs text-amber-100">Aucun collaborateur</p>
        )}
      </div>
    </button>
  );
}
