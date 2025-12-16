import { Assignment, Collaborator, ConflictEntry, ShiftInstance, Site } from "../../api/types";

export interface PlanningShift {
  id: number;
  siteId: number;
  roleId: number;
  missionId: number;
  startUtc: string;
  endUtc: string;
  status: string;
  source: string;
  capacity: number;
  assignments: Assignment[];
  conflicts: ConflictEntry[];
}

export interface DateRange {
  start: Date;
  end: Date;
}

export interface PlanningFilters {
  placeIds: number[];
  personIds: number[];
  status: string[];
  search: string;
}

export interface PlanningDataset {
  places: Site[];
  people: Collaborator[];
  shifts: PlanningShift[];
}

export type AssignmentMap = Record<number, Assignment[]>;
export type CollaboratorMap = Record<number, Collaborator>;
export type PlaceMap = Record<number, Site>;

export function normalizePlanningShift(
  source: ShiftInstance & { assignments?: Assignment[]; conflicts?: ConflictEntry[] },
): PlanningShift {
  return {
    id: source.id,
    siteId: source.site_id,
    roleId: source.role_id,
    missionId: source.mission_id,
    startUtc: source.start_utc,
    endUtc: source.end_utc,
    status: source.status,
    source: source.source,
    capacity: source.capacity,
    assignments: source.assignments ?? [],
    conflicts: source.conflicts ?? [],
  };
}

export function normalizePlanningShiftFromApi(
  shift: ShiftInstance,
  assignments: Assignment[],
  conflicts: ConflictEntry[],
): PlanningShift {
  return {
    id: shift.id,
    siteId: shift.site_id,
    roleId: shift.role_id,
    missionId: shift.mission_id,
    startUtc: shift.start_utc,
    endUtc: shift.end_utc,
    status: shift.status,
    source: shift.source,
    capacity: shift.capacity,
    assignments,
    conflicts,
  };
}
