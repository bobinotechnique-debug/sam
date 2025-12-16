import { Collaborator, Site } from "../../../api/types";
import { PlanningShift } from "../types";
import { DAY_END_HOUR, DAY_START_HOUR, overlapsDay } from "../utils";
import { ShiftCard } from "./ShiftCard";

interface TimelineProps {
  places: Site[];
  days: Date[];
  shifts: PlanningShift[];
  peopleMap: Record<number, Collaborator>;
  onSelectShift: (shift: PlanningShift) => void;
}

function formatDayLabel(value: Date) {
  return value.toLocaleDateString(undefined, { weekday: "short", month: "short", day: "numeric" });
}

const hours = Array.from({ length: DAY_END_HOUR - DAY_START_HOUR + 1 }, (_, index) => DAY_START_HOUR + index);

export function Timeline({ places, days, shifts, peopleMap, onSelectShift }: TimelineProps) {
  return (
    <div className="space-y-6">
      {places.map((place) => (
        <div key={place.id} className="space-y-3 rounded-lg border border-slate-800 bg-slate-900/60 p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-xs uppercase tracking-[0.2em] text-indigo-300">Place</p>
              <p className="text-lg font-semibold text-slate-100">{place.name}</p>
            </div>
            <p className="text-xs text-slate-400">{shifts.filter((shift) => shift.siteId === place.id).length} shift(s)</p>
          </div>

          <div className="grid gap-3 lg:grid-cols-2">
            {days.map((day) => {
              const dayKey = day.toISOString().substring(0, 10);
              const dayShifts = shifts.filter(
                (shift) => shift.siteId === place.id && overlapsDay(shift.startUtc, shift.endUtc, day),
              );
              return (
                <div key={`${place.id}-${dayKey}`} className="space-y-2 rounded-md border border-slate-800 bg-slate-950/40 p-3">
                  <div className="flex items-center justify-between text-sm text-slate-200">
                    <span className="font-semibold">{formatDayLabel(day)}</span>
                    <span className="text-xs text-slate-400">{dayShifts.length} item(s)</span>
                  </div>
                  <div className="relative h-32 overflow-hidden rounded-md border border-slate-800 bg-slate-900">
                    <div className="absolute inset-0 flex text-[10px] text-slate-500">
                      {hours.map((hour) => (
                        <div key={`${dayKey}-${hour}`} className="flex-1 border-l border-slate-800 px-1 pt-1">
                          <span>{hour.toString().padStart(2, "0")}:00</span>
                        </div>
                      ))}
                    </div>
                    <div className="relative h-full">
                      {dayShifts.map((shift) => (
                        <ShiftCard
                          key={shift.id}
                          shift={shift}
                          peopleMap={peopleMap}
                          dayStartHour={DAY_START_HOUR}
                          dayEndHour={DAY_END_HOUR}
                          onSelect={onSelectShift}
                        />
                      ))}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}
    </div>
  );
}

