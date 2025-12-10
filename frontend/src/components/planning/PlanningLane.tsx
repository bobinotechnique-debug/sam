import { Mission } from "../../api/types";
import { PLANNING_END_HOUR, PLANNING_START_HOUR, TimeRange, formatHourLabel } from "../../utils/planning";
import { MissionCard } from "./MissionCard";

interface PlanningLaneProps {
  label: string;
  missions: Mission[];
  assignmentsByMission: Record<number, string[]>;
  range: TimeRange;
  onSelect: (mission: Mission) => void;
}

export function PlanningLane({ label, missions, assignmentsByMission, range, onSelect }: PlanningLaneProps) {
  const hours = Array.from({ length: PLANNING_END_HOUR - PLANNING_START_HOUR + 1 }, (_, index) => PLANNING_START_HOUR + index);
  const height = Math.max(72, missions.length * 72 + 16);

  return (
    <div className="flex gap-4 border-b border-slate-800 pb-6">
      <div className="w-28 pt-4 text-sm font-semibold text-slate-200">{label}</div>
      <div className="flex-1">
        <div className="grid grid-cols-[repeat(auto-fit,minmax(0,1fr))]" style={{ gridTemplateColumns: `repeat(${hours.length}, minmax(0, 1fr))` }}>
          {hours.map((hour) => (
            <div key={hour} className="border-l border-slate-800/60 bg-slate-900/40 px-2 py-1 text-xs text-slate-400 first:border-l-0">
              {formatHourLabel(hour)}
            </div>
          ))}
        </div>
        <div className="relative overflow-hidden rounded-lg border border-slate-800 bg-slate-950/60" style={{ height }}>
          <div className="absolute inset-0 grid" style={{ gridTemplateColumns: `repeat(${hours.length}, minmax(0, 1fr))` }}>
            {hours.map((hour) => (
              <div key={hour} className="border-l border-slate-800/50 first:border-l-0" />
            ))}
          </div>
          <div className="relative">
            {missions.map((mission, index) => (
              <MissionCard
                key={mission.id}
                mission={mission}
                assignments={assignmentsByMission[mission.id] || []}
                range={range}
                index={index}
                onSelect={onSelect}
              />
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
