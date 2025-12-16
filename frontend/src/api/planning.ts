import { request } from "./http";
import {
  Assignment,
  AssignmentPayload,
  AssignmentWriteResponse,
  ConflictEntry,
  ShiftInstance,
  ShiftInstancePayload,
} from "./types";

export interface PlanningShiftInstanceResponse {
  shift: ShiftInstance;
  assignments: Assignment[];
  conflicts: ConflictEntry[];
}

export interface ShiftInstanceQuery {
  start?: string;
  end?: string;
  placeIds?: number[];
  personIds?: number[];
  status?: string[];
}

const buildQueryString = (query: ShiftInstanceQuery): string => {
  const params = new URLSearchParams();
  if (query.start) params.set("start", query.start);
  if (query.end) params.set("end", query.end);
  if (query.placeIds?.length) params.set("place_ids", query.placeIds.join(","));
  if (query.personIds?.length) params.set("person_ids", query.personIds.join(","));
  if (query.status?.length) params.set("status", query.status.join(","));
  const search = params.toString();
  return search ? `?${search}` : "";
};

function unwrapShiftInstances(
  response: PlanningShiftInstanceResponse[] | { items: PlanningShiftInstanceResponse[] },
): PlanningShiftInstanceResponse[] {
  if (Array.isArray(response)) return response;
  if (Array.isArray((response as { items: PlanningShiftInstanceResponse[] }).items)) {
    return (response as { items: PlanningShiftInstanceResponse[] }).items;
  }
  return [];
}

export async function fetchPlanningShiftInstances(
  query: ShiftInstanceQuery = {},
): Promise<PlanningShiftInstanceResponse[]> {
  const search = buildQueryString(query);
  const response = await request<PlanningShiftInstanceResponse[] | { items: PlanningShiftInstanceResponse[] }>(
    `/api/v1/planning/shift-instances${search}`,
  );
  return unwrapShiftInstances(response);
}

export function updatePlanningShiftInstance(
  id: number,
  payload: Partial<ShiftInstancePayload>,
): Promise<PlanningShiftInstanceResponse> {
  return request<PlanningShiftInstanceResponse>(`/api/v1/planning/shift-instances/${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function createPlanningAssignment(payload: AssignmentPayload): Promise<AssignmentWriteResponse> {
  return request<AssignmentWriteResponse>(`/api/v1/planning/assignments`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updatePlanningAssignment(
  id: number,
  payload: Partial<AssignmentPayload>,
): Promise<AssignmentWriteResponse> {
  return request<AssignmentWriteResponse>(`/api/v1/planning/assignments/${id}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

