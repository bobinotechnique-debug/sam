import { Collaborator, Site } from "../../../api/types";
import { PlanningFilters } from "../types";

interface FiltersProps {
  places: Site[];
  people: Collaborator[];
  filters: PlanningFilters;
  onChange: (next: PlanningFilters) => void;
  onReset: () => void;
}

const statusOptions = ["draft", "published", "locked", "archived"];

function toggleValue(list: number[], value: number): number[] {
  return list.includes(value) ? list.filter((item) => item !== value) : [...list, value];
}

function toggleString(list: string[], value: string): string[] {
  return list.includes(value) ? list.filter((item) => item !== value) : [...list, value];
}

export function Filters({ places, people, filters, onChange, onReset }: FiltersProps) {
  return (
    <div className="flex flex-col gap-4 rounded-lg border border-slate-800 bg-slate-950/60 p-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-xs uppercase tracking-[0.2em] text-indigo-300">Filters</p>
          <p className="text-sm text-slate-300">Client side filters until API supports them.</p>
        </div>
        <button
          type="button"
          className="rounded-md border border-slate-800 px-3 py-2 text-xs font-semibold text-slate-200 hover:border-indigo-400 hover:text-white"
          onClick={onReset}
        >
          Reset
        </button>
      </div>

      <label className="flex flex-col gap-1 text-sm text-slate-200">
        Search
        <input
          className="rounded border border-slate-800 bg-slate-900 px-3 py-2 text-sm text-white"
          placeholder="Search shift id or source"
          value={filters.search}
          onChange={(event) => onChange({ ...filters, search: event.target.value })}
        />
      </label>

      <div className="grid gap-4 md:grid-cols-3">
        <div className="space-y-2 rounded-md border border-slate-800 bg-slate-900/60 p-3 text-sm text-slate-200">
          <div className="flex items-center justify-between">
            <span className="font-semibold">Places</span>
            <span className="text-xs text-slate-400">{filters.placeIds.length} selected</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {places.map((place) => {
              const selected = filters.placeIds.includes(place.id);
              return (
                <button
                  key={place.id}
                  type="button"
                  className={`rounded border px-3 py-1 text-xs font-semibold ${
                    selected
                      ? "border-indigo-400 bg-indigo-500/20 text-indigo-100"
                      : "border-slate-800 bg-slate-900 text-slate-200 hover:border-slate-700"
                  }`}
                  onClick={() => onChange({ ...filters, placeIds: toggleValue(filters.placeIds, place.id) })}
                >
                  {place.name}
                </button>
              );
            })}
          </div>
        </div>

        <div className="space-y-2 rounded-md border border-slate-800 bg-slate-900/60 p-3 text-sm text-slate-200">
          <div className="flex items-center justify-between">
            <span className="font-semibold">People</span>
            <span className="text-xs text-slate-400">{filters.personIds.length} selected</span>
          </div>
          <div className="grid grid-cols-2 gap-2 text-xs">
            {people.map((person) => {
              const selected = filters.personIds.includes(person.id);
              return (
                <label
                  key={person.id}
                  className="flex items-center gap-2 rounded border border-slate-800 bg-slate-900 px-2 py-1 hover:border-indigo-500"
                >
                  <input
                    type="checkbox"
                    checked={selected}
                    onChange={() => onChange({ ...filters, personIds: toggleValue(filters.personIds, person.id) })}
                    className="rounded border-slate-700 bg-slate-900 text-indigo-500"
                  />
                  <span className="truncate text-slate-100">{person.full_name}</span>
                </label>
              );
            })}
          </div>
        </div>

        <div className="space-y-2 rounded-md border border-slate-800 bg-slate-900/60 p-3 text-sm text-slate-200">
          <div className="flex items-center justify-between">
            <span className="font-semibold">Status</span>
            <span className="text-xs text-slate-400">{filters.status.length} selected</span>
          </div>
          <div className="flex flex-wrap gap-2">
            {statusOptions.map((option) => {
              const selected = filters.status.includes(option);
              return (
                <button
                  key={option}
                  type="button"
                  className={`rounded border px-3 py-1 text-xs font-semibold capitalize ${
                    selected
                      ? "border-indigo-400 bg-indigo-500/20 text-indigo-100"
                      : "border-slate-800 bg-slate-900 text-slate-200 hover:border-slate-700"
                  }`}
                  onClick={() => onChange({ ...filters, status: toggleString(filters.status, option) })}
                >
                  {option}
                </button>
              );
            })}
          </div>
        </div>
      </div>
    </div>
  );
}

