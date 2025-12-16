import { useMemo } from "react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

import { listCollaborators, listSites } from "../../api/entities";
import {
  createPlanningAssignment,
  fetchPlanningShiftInstances,
  PlanningShiftInstanceResponse,
  updatePlanningShiftInstance,
} from "../../api/planning";
import { AssignmentPayload, Collaborator, ShiftInstancePayload, Site } from "../../api/types";
import {
  DateRange,
  PlanningDataset,
  PlanningFilters,
  PlanningShift,
  normalizePlanningShiftFromApi,
} from "./types";

const backendUnavailable = typeof process !== "undefined" && process?.env?.BACKEND_UNAVAILABLE === "1";

const mockPlaces: Site[] = [
  { id: 1, organization_id: 1, name: "HQ", timezone: "UTC", address: "" },
  { id: 2, organization_id: 1, name: "Studio", timezone: "UTC", address: "" },
];

const mockPeople: Collaborator[] = [
  { id: 11, organization_id: 1, full_name: "Alex King", primary_role_id: 1, status: "active", email: "alex@example.com" },
  { id: 12, organization_id: 1, full_name: "Jamie Lee", primary_role_id: 1, status: "active", email: "jamie@example.com" },
  { id: 13, organization_id: 1, full_name: "Morgan Yu", primary_role_id: 2, status: "active", email: "morgan@example.com" },
];

const mockShifts: PlanningShift[] = [
  {
    id: 501,
    siteId: 1,
    roleId: 1,
    missionId: 1,
    startUtc: new Date().toISOString(),
    endUtc: new Date(Date.now() + 2 * 60 * 60 * 1000).toISOString(),
    status: "draft",
    source: "mock",
    capacity: 2,
    assignments: [
      { id: 1, shift_instance_id: 501, collaborator_id: 11, role_id: 1, status: "confirmed", source: "manual", note: null, is_locked: false, created_at: null, updated_at: null },
    ],
    conflicts: [],
  },
  {
    id: 502,
    siteId: 2,
    roleId: 2,
    missionId: 2,
    startUtc: new Date(Date.now() + 3 * 60 * 60 * 1000).toISOString(),
    endUtc: new Date(Date.now() + 5 * 60 * 60 * 1000).toISOString(),
    status: "published",
    source: "mock",
    capacity: 1,
    assignments: [
      { id: 2, shift_instance_id: 502, collaborator_id: 12, role_id: 2, status: "pending", source: "manual", note: null, is_locked: false, created_at: null, updated_at: null },
    ],
    conflicts: [],
  },
];

export const defaultFilters: PlanningFilters = {
  placeIds: [],
  personIds: [],
  status: [],
  search: "",
};

const normalizePayload = (payload: PlanningShiftInstanceResponse): PlanningShift =>
  normalizePlanningShiftFromApi(payload.shift, payload.assignments, payload.conflicts);

export function filterPlanningShifts(shifts: PlanningShift[], filters: PlanningFilters): PlanningShift[] {
  const search = filters.search.trim().toLowerCase();
  return shifts.filter((shift) => {
    if (filters.placeIds.length && !filters.placeIds.includes(shift.siteId)) return false;
    if (filters.personIds.length && !shift.assignments.some((assignment) => filters.personIds.includes(assignment.collaborator_id))) {
      return false;
    }
    if (filters.status.length && !filters.status.includes(shift.status)) return false;
    if (search) {
      const haystack = [`shift ${shift.id}`, shift.status, shift.source].join(" ").toLowerCase();
      if (!haystack.includes(search)) return false;
    }
    return true;
  });
}

export function usePlanningPlaces() {
  return useQuery({
    queryKey: ["planning", "places"],
    queryFn: async () => {
      if (backendUnavailable) return mockPlaces;
      const response = await listSites();
      return response.items ?? [];
    },
  });
}

export function usePlanningPeople() {
  return useQuery({
    queryKey: ["planning", "people"],
    queryFn: async () => {
      if (backendUnavailable) return mockPeople;
      const response = await listCollaborators();
      return response.items ?? [];
    },
  });
}

export function usePlanningShifts(range: DateRange, filters: PlanningFilters) {
  return useQuery({
    queryKey: [
      "planning",
      "shiftInstances",
      range.start.toISOString(),
      range.end.toISOString(),
      filters.placeIds.join(","),
      filters.personIds.join(","),
      filters.status.join(","),
      filters.search.trim(),
    ],
    queryFn: async () => {
      if (backendUnavailable) return filterPlanningShifts(mockShifts, filters);
      const response = await fetchPlanningShiftInstances({
        start: range.start.toISOString(),
        end: range.end.toISOString(),
        placeIds: filters.placeIds,
        personIds: filters.personIds,
        status: filters.status,
      });
      const normalized = response.map(normalizePayload);
      return filterPlanningShifts(normalized, filters);
    },
  });
}

export function usePlanningDataset(range: DateRange, filters: PlanningFilters) {
  const places = usePlanningPlaces();
  const people = usePlanningPeople();
  const shifts = usePlanningShifts(range, filters);

  const data: PlanningDataset | undefined = useMemo(() => {
    if (!places.data || !people.data || !shifts.data) return undefined;
    return {
      places: places.data,
      people: people.data,
      shifts: shifts.data,
    };
  }, [people.data, places.data, shifts.data]);

  return {
    data,
    isLoading: places.isLoading || people.isLoading || shifts.isLoading,
    error: places.error || people.error || shifts.error,
    refetch: () => {
      places.refetch();
      people.refetch();
      shifts.refetch();
    },
  };
}

export function useUpdateShift() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (input: { id: number; payload: Partial<ShiftInstancePayload> }) =>
      updatePlanningShiftInstance(input.id, input.payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["planning", "shiftInstances"] }),
  });
}

export function useCreateAssignment() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: (payload: AssignmentPayload) => createPlanningAssignment(payload),
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["planning", "shiftInstances"] }),
  });
}
