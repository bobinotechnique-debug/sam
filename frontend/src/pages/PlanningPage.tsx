import { useMemo, useState } from "react";

import { AssignmentPayload } from "../api/types";
import { Filters } from "../features/planning/components/Filters";
import { ShiftEditor } from "../features/planning/components/ShiftEditor";
import { Timeline } from "../features/planning/components/Timeline";
import { Toolbar } from "../features/planning/components/Toolbar";
import {
  defaultFilters,
  filterPlanningShifts,
  useCreateAssignment,
  usePlanningDataset,
  useUpdateShift,
} from "../features/planning/hooks";
import { PlanningFilters, PlanningShift } from "../features/planning/types";
import { daysInRange, getWeekRange } from "../features/planning/utils";

export function PlanningPage() {
  const [range, setRange] = useState(getWeekRange(new Date()));
  const [filters, setFilters] = useState<PlanningFilters>(defaultFilters);
  const [selectedShift, setSelectedShift] = useState<PlanningShift | null>(null);

  const { data, isLoading, error, refetch } = usePlanningDataset(range, filters);
  const updateShift = useUpdateShift();
  const createAssignment = useCreateAssignment();

  const days = useMemo(() => daysInRange(range), [range]);
  const peopleMap = useMemo(
    () => Object.fromEntries((data?.people ?? []).map((person) => [person.id, person])),
    [data?.people],
  );

  const handleSaveShift = (payload: { start_utc: string; end_utc: string; site_id: number }) => {
    if (!selectedShift) return;
    updateShift.mutate({ id: selectedShift.id, payload }, { onSuccess: () => setSelectedShift(null) });
  };

  const handleAssign = (collaboratorId: number) => {
    if (!selectedShift) return;
    const assignment: AssignmentPayload = {
      shift_instance_id: selectedShift.id,
      collaborator_id: collaboratorId,
      role_id: selectedShift.roleId,
      status: "pending",
      source: "manual",
      note: null,
      is_locked: false,
    };
    createAssignment.mutate(assignment, { onSuccess: () => setSelectedShift(null) });
  };

  const selectedPeople = selectedShift?.assignments
    .map((assignment) => peopleMap[assignment.collaborator_id])
    .filter(Boolean);

  const shifts = useMemo(() => data?.shifts ?? [], [data?.shifts]);
  const visibleShifts = useMemo(() => filterPlanningShifts(shifts, filters), [filters, shifts]);

  return (
    <div className="flex flex-col gap-4">
      <Toolbar range={range} onRangeChange={setRange} onRefresh={refetch} />

      {data ? (
        <Filters
          places={data.places}
          people={data.people}
          filters={filters}
          onChange={setFilters}
          onReset={() => setFilters(defaultFilters)}
        />
      ) : null}

      {error && (
        <p className="rounded border border-red-900/50 bg-red-900/20 px-3 py-2 text-sm text-red-100">
          {(error as Error).message}
        </p>
      )}

      {isLoading && <p className="text-sm text-slate-300">Loading planning data...</p>}

      {!isLoading && data && (
        <Timeline
          places={data.places}
          days={days}
          shifts={visibleShifts}
          peopleMap={peopleMap}
          onSelectShift={setSelectedShift}
        />
      )}

      {selectedShift && data && (
        <ShiftEditor
          shift={selectedShift}
          places={data.places}
          people={data.people}
          onClose={() => setSelectedShift(null)}
          onSave={handleSaveShift}
          onAssign={handleAssign}
        />
      )}

      {selectedPeople && selectedPeople.length > 0 && (
        <p className="text-xs text-slate-400">Selected collaborators: {selectedPeople.map((p) => p.full_name).join(", ")}</p>
      )}
    </div>
  );
}

