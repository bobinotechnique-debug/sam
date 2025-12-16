import { DateRange } from "../types";
import { getWeekRange, startOfDay } from "../utils";

interface ToolbarProps {
  range: DateRange;
  onRangeChange: (range: DateRange) => void;
  onRefresh: () => void;
}

function formatRange(range: DateRange): string {
  const formatter = new Intl.DateTimeFormat(undefined, { month: "short", day: "numeric" });
  return `${formatter.format(range.start)} - ${formatter.format(range.end)}`;
}

export function Toolbar({ range, onRangeChange, onRefresh }: ToolbarProps) {
  const moveDays = (delta: number) => {
    const nextStart = new Date(range.start);
    nextStart.setDate(nextStart.getDate() + delta);
    const nextEnd = new Date(range.end);
    nextEnd.setDate(nextEnd.getDate() + delta);
    onRangeChange({ start: nextStart, end: nextEnd });
  };

  const handleDateChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    if (!value) return;
    const picked = startOfDay(new Date(value));
    onRangeChange(getWeekRange(picked));
  };

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-slate-800 bg-slate-950/60 p-4 md:flex-row md:items-center md:justify-between">
      <div>
        <p className="text-xs uppercase tracking-[0.2em] text-indigo-300">Planning</p>
        <p className="text-sm text-slate-200">Week window aligned on Monday. Adjust before loading shifts.</p>
      </div>
      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          className="rounded border border-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 hover:border-indigo-400 hover:text-white"
          onClick={() => moveDays(-7)}
        >
          Prev week
        </button>
        <button
          type="button"
          className="rounded border border-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 hover:border-indigo-400 hover:text-white"
          onClick={() => moveDays(7)}
        >
          Next week
        </button>
        <button
          type="button"
          className="rounded border border-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 hover:border-indigo-400 hover:text-white"
          onClick={() => onRangeChange(getWeekRange(startOfDay(new Date())))}
        >
          Today
        </button>
        <label className="flex items-center gap-2 rounded border border-slate-800 bg-slate-900 px-2 py-1 text-xs text-slate-200">
          <span>Select start</span>
          <input
            type="date"
            className="rounded border border-slate-700 bg-slate-900 px-2 py-1 text-white"
            value={range.start.toISOString().substring(0, 10)}
            onChange={handleDateChange}
          />
        </label>
        <span className="rounded bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-100">{formatRange(range)}</span>
        <button
          type="button"
          className="rounded bg-indigo-600 px-3 py-2 text-xs font-semibold text-white hover:bg-indigo-500"
          onClick={onRefresh}
        >
          Refresh
        </button>
      </div>
    </div>
  );
}

