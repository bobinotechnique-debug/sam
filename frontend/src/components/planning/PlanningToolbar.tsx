interface PlanningToolbarProps {
  mode: "day" | "week";
  date: Date;
  onModeChange: (mode: "day" | "week") => void;
  onDateChange: (date: Date) => void;
  onRefresh: () => void;
}

export function PlanningToolbar({ mode, date, onModeChange, onDateChange, onRefresh }: PlanningToolbarProps) {
  const changeDate = (delta: number) => {
    const next = new Date(date);
    next.setDate(date.getDate() + delta);
    onDateChange(next);
  };

  const formattedDate = new Intl.DateTimeFormat(undefined, {
    weekday: "long",
    day: "2-digit",
    month: "short",
  }).format(date);

  return (
    <div className="flex flex-col gap-3 rounded-lg border border-slate-800 bg-slate-900/70 p-4 md:flex-row md:items-center md:justify-between">
      <div className="flex items-center gap-3">
        <button
          className={`rounded px-4 py-2 text-sm font-semibold ${mode === "day" ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-100"}`}
          onClick={() => onModeChange("day")}
        >
          Jour
        </button>
        <button
          className={`rounded px-4 py-2 text-sm font-semibold ${mode === "week" ? "bg-indigo-600 text-white" : "bg-slate-800 text-slate-100"}`}
          onClick={() => onModeChange("week")}
        >
          Semaine
        </button>
      </div>
      <div className="flex flex-wrap items-center gap-3">
        <div className="flex items-center gap-2 rounded border border-slate-800 bg-slate-950 px-3 py-2 text-sm">
          <button className="rounded bg-slate-800 px-2 py-1" onClick={() => changeDate(mode === "day" ? -1 : -7)}>
            ◀
          </button>
          <span className="font-semibold text-slate-100">{formattedDate}</span>
          <button className="rounded bg-slate-800 px-2 py-1" onClick={() => changeDate(mode === "day" ? 1 : 7)}>
            ▶
          </button>
        </div>
        <button
          className="rounded border border-indigo-500 px-4 py-2 text-sm font-semibold text-indigo-200 hover:bg-indigo-500/10"
          onClick={onRefresh}
        >
          Rafraîchir
        </button>
      </div>
    </div>
  );
}
