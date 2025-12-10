import { request } from "./client";
import {
  Collaborator,
  CollaboratorPayload,
  ConflictEntry,
  PlanningProConfig,
  PlanningShift,
  Mission,
  MissionPayload,
  Organization,
  OrganizationPayload,
  PaginatedResponse,
  Role,
  RolePayload,
  Shift,
  ShiftPayload,
  ShiftInstancePayload,
  ShiftTemplate,
  ShiftTemplatePayload,
  Site,
  SitePayload,
  Assignment,
  AssignmentPayload,
  AssignmentWriteResponse,
  ShiftWriteResponse,
} from "./types";

const defaultPage = 1;
const defaultPageSize = 50;

const withPagination = (path: string, page = defaultPage, pageSize = defaultPageSize) =>
  `${path}?page=${page}&page_size=${pageSize}`;

export function listOrganizations(
  page?: number,
  pageSize?: number,
): Promise<PaginatedResponse<Organization>> {
  return request(withPagination("/api/v1/organizations", page, pageSize));
}

export function getOrganization(id: number): Promise<Organization> {
  return request(`/api/v1/organizations/${id}`);
}

export function createOrganization(payload: OrganizationPayload): Promise<Organization> {
  return request<Organization>("/api/v1/organizations", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateOrganization(id: number, payload: Partial<OrganizationPayload>): Promise<Organization> {
  return request<Organization>(`/api/v1/organizations/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteOrganization(id: number): Promise<void> {
  return request(`/api/v1/organizations/${id}`, { method: "DELETE" });
}

export function listCollaborators(
  page?: number,
  pageSize?: number,
): Promise<PaginatedResponse<Collaborator>> {
  return request(withPagination("/api/v1/collaborators", page, pageSize));
}

export function getCollaborator(id: number): Promise<Collaborator> {
  return request(`/api/v1/collaborators/${id}`);
}

export function createCollaborator(payload: CollaboratorPayload): Promise<Collaborator> {
  return request<Collaborator>("/api/v1/collaborators", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateCollaborator(
  id: number,
  payload: Partial<CollaboratorPayload>,
): Promise<Collaborator> {
  return request<Collaborator>(`/api/v1/collaborators/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteCollaborator(id: number): Promise<void> {
  return request(`/api/v1/collaborators/${id}`, { method: "DELETE" });
}

export function listSites(page?: number, pageSize?: number): Promise<PaginatedResponse<Site>> {
  return request(withPagination("/api/v1/sites", page, pageSize));
}

export function getSite(id: number): Promise<Site> {
  return request(`/api/v1/sites/${id}`);
}

export function createSite(payload: SitePayload): Promise<Site> {
  return request<Site>("/api/v1/sites", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateSite(id: number, payload: Partial<SitePayload>): Promise<Site> {
  return request<Site>(`/api/v1/sites/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteSite(id: number): Promise<void> {
  return request(`/api/v1/sites/${id}`, { method: "DELETE" });
}

export function listRoles(page?: number, pageSize?: number): Promise<PaginatedResponse<Role>> {
  return request(withPagination("/api/v1/roles", page, pageSize));
}

export function getRole(id: number): Promise<Role> {
  return request(`/api/v1/roles/${id}`);
}

export function createRole(payload: RolePayload): Promise<Role> {
  return request<Role>("/api/v1/roles", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateRole(id: number, payload: Partial<RolePayload>): Promise<Role> {
  return request<Role>(`/api/v1/roles/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteRole(id: number): Promise<void> {
  return request(`/api/v1/roles/${id}`, { method: "DELETE" });
}

export function listMissions(page?: number, pageSize?: number): Promise<PaginatedResponse<Mission>> {
  return request(withPagination("/api/v1/missions", page, pageSize));
}

export function getMission(id: number): Promise<Mission> {
  return request(`/api/v1/missions/${id}`);
}

export function createMission(payload: MissionPayload): Promise<Mission> {
  return request<Mission>("/api/v1/missions", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateMission(id: number, payload: Partial<MissionPayload>): Promise<Mission> {
  return request<Mission>(`/api/v1/missions/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteMission(id: number): Promise<void> {
  return request(`/api/v1/missions/${id}`, { method: "DELETE" });
}

export function listShifts(page?: number, pageSize?: number): Promise<PaginatedResponse<Shift>> {
  return request(withPagination("/api/v1/shifts", page, pageSize));
}

export function createShift(payload: ShiftPayload): Promise<Shift> {
  return request<Shift>("/api/v1/shifts", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateShift(id: number, payload: Partial<ShiftPayload>): Promise<Shift> {
  return request<Shift>(`/api/v1/shifts/${id}`, {
    method: "PATCH",
    body: JSON.stringify(payload),
  });
}

export function deleteShift(id: number): Promise<void> {
  return request(`/api/v1/shifts/${id}`, { method: "DELETE" });
}

export function getPlanningProConfig(): Promise<PlanningProConfig> {
  return request(`/api/v1/planning/rules`);
}

export function listShiftTemplates(): Promise<ShiftTemplate[]> {
  return request(`/api/v1/planning/shift-templates`);
}

export function createShiftTemplate(payload: ShiftTemplatePayload): Promise<ShiftTemplate> {
  return request<ShiftTemplate>(`/api/v1/planning/shift-templates`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function listShiftInstances(): Promise<PlanningShift[]> {
  return request(`/api/v1/planning/shifts`);
}

export function createShiftInstance(payload: ShiftInstancePayload): Promise<ShiftWriteResponse> {
  return request<ShiftWriteResponse>(`/api/v1/planning/shifts`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function listAssignments(): Promise<Assignment[]> {
  return request(`/api/v1/planning/assignments`);
}

export function createAssignment(payload: AssignmentPayload): Promise<AssignmentWriteResponse> {
  return request<AssignmentWriteResponse>(`/api/v1/planning/assignments`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function previewPlanningConflicts(payload: {
  shift?: ShiftInstancePayload;
  assignments?: AssignmentPayload[];
}): Promise<ConflictEntry[]> {
  return request<ConflictEntry[]>(`/api/v1/planning/conflicts/preview`, {
    method: "POST",
    body: JSON.stringify(payload),
  });
}
