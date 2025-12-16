import { useMemo } from "react";

import { Collaborator } from "../../../api/types";
import { PlanningShift } from "../types";
import { calculatePosition } from "../utils";
import { AvatarStack } from "./AvatarStack";

interface ShiftCardProps {
  shift: PlanningShift;
  peopleMap: Record<number, Collaborator>;
  dayStartHour: number;
  dayEndHour: number;
  onSelect: (shift: PlanningShift) => void;
}

function formatTime(value: string) {
  return new Date(value).toISOString().substring(11, 16);
}

export function ShiftCard({ shift, peopleMap, dayStartHour, dayEndHour, onSelect }: ShiftCardProps) {
  const { offsetPercent, widthPercent } = useMemo(
    () => calculatePosition(shift.startUtc, shift.endUtc, dayStartHour, dayEndHour),
    [dayEndHour, dayStartHour, shift.endUtc, shift.startUtc],
  );

  const assignedPeople = shift.assignments
    .map((assignment) => peopleMap[assignment.collaborator_id])
    .filter(Boolean) as Collaborator[];

  return (
    <button
      type="button"
      className="absolute top-1 flex flex-col gap-1 rounded-lg border border-slate-800 bg-slate-900/80 px-3 py-2 text-left shadow hover:border-indigo-400 hover:shadow-indigo-500/20"
      style={{ left: `${offsetPercent}%`, width: `${widthPercent}%` }}
      onClick={() => onSelect(shift)}
    >
      <div className="flex items-center justify-between text-xs text-slate-300">
        <span className="font-semibold text-slate-100">Shift #{shift.id}</span>
        <span className="rounded bg-slate-800 px-2 py-0.5 text-[11px] uppercase tracking-wide text-slate-200">
          {shift.status}
        </span>
      </div>
      <p className="text-xs text-indigo-100">
        {formatTime(shift.startUtc)} - {formatTime(shift.endUtc)}
      </p>
      <div className="flex items-center justify-between text-xs text-slate-400">
        <span>Capacity {shift.capacity}</span>
        {shift.conflicts.length > 0 && (
          <span className="rounded bg-amber-500/20 px-2 py-0.5 text-[11px] font-semibold text-amber-300">
            {shift.conflicts.length} conflict(s)
          </span>
        )}
      </div>
      <AvatarStack people={assignedPeople} />
    </button>
  );
}

