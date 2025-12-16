import { useState } from "react";

import { Collaborator, Site } from "../../../api/types";
import { PlanningShift } from "../types";

interface ShiftEditorProps {
  shift: PlanningShift;
  places: Site[];
  people: Collaborator[];
  onClose: () => void;
  onSave: (payload: { start_utc: string; end_utc: string; site_id: number }) => void;
  onAssign: (collaboratorId: number) => void;
}

function toDateTimeLocal(value: string) {
  const date = new Date(value);
  const iso = new Date(date.getTime() - date.getTimezoneOffset() * 60000).toISOString();
  return iso.substring(0, 16);
}

export function ShiftEditor({ shift, places, people, onClose, onSave, onAssign }: ShiftEditorProps) {
  const [start, setStart] = useState(toDateTimeLocal(shift.startUtc));
  const [end, setEnd] = useState(toDateTimeLocal(shift.endUtc));
  const [siteId, setSiteId] = useState<number>(shift.siteId);
  const [assignee, setAssignee] = useState<number | "">("");

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSave({ start_utc: new Date(start).toISOString(), end_utc: new Date(end).toISOString(), site_id: siteId });
  };

  return (
    <div className="fixed inset-0 z-20 flex items-center justify-center bg-black/70 p-4">
      <div className="w-full max-w-lg rounded-lg border border-slate-800 bg-slate-950 p-6 shadow-xl">
        <div className="flex items-center justify-between">
          <h3 className="text-lg font-semibold text-white">Edit shift #{shift.id}</h3>
          <button
            type="button"
            className="rounded border border-slate-800 px-3 py-1 text-xs font-semibold text-slate-200 hover:border-indigo-400 hover:text-white"
            onClick={onClose}
          >
            Close
          </button>
        </div>

        <form className="mt-4 space-y-4" onSubmit={handleSubmit}>
          <label className="flex flex-col gap-1 text-sm text-slate-200">
            Start
            <input
              type="datetime-local"
              className="rounded border border-slate-800 bg-slate-900 px-3 py-2 text-white"
              value={start}
              onChange={(event) => setStart(event.target.value)}
              required
            />
          </label>
          <label className="flex flex-col gap-1 text-sm text-slate-200">
            End
            <input
              type="datetime-local"
              className="rounded border border-slate-800 bg-slate-900 px-3 py-2 text-white"
              value={end}
              onChange={(event) => setEnd(event.target.value)}
              required
            />
          </label>
          <label className="flex flex-col gap-1 text-sm text-slate-200">
            Place
            <select
              className="rounded border border-slate-800 bg-slate-900 px-3 py-2 text-white"
              value={siteId}
              onChange={(event) => setSiteId(Number(event.target.value))}
            >
              {places.map((place) => (
                <option key={place.id} value={place.id}>
                  {place.name}
                </option>
              ))}
            </select>
          </label>

          <div className="flex flex-col gap-2 rounded-md border border-slate-800 bg-slate-900/70 p-3">
            <p className="text-sm font-semibold text-slate-100">Assign collaborator</p>
            <div className="flex items-center gap-2">
              <select
                className="flex-1 rounded border border-slate-800 bg-slate-900 px-3 py-2 text-white"
                value={assignee}
                onChange={(event) => setAssignee(event.target.value === "" ? "" : Number(event.target.value))}
              >
                <option value="">Select collaborator</option>
                {people.map((person) => (
                  <option key={person.id} value={person.id}>
                    {person.full_name}
                  </option>
                ))}
              </select>
              <button
                type="button"
                className="rounded bg-indigo-600 px-3 py-2 text-xs font-semibold text-white hover:bg-indigo-500 disabled:opacity-50"
                onClick={() => assignee !== "" && onAssign(Number(assignee))}
                disabled={assignee === ""}
              >
                Assign
              </button>
            </div>
          </div>

          <div className="flex justify-end gap-2">
            <button
              type="button"
              className="rounded border border-slate-800 px-4 py-2 text-sm font-semibold text-slate-200 hover:border-indigo-400"
              onClick={onClose}
            >
              Cancel
            </button>
            <button
              type="submit"
              className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
            >
              Save
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

