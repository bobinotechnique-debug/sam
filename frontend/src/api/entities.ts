import { request } from "./client";
import {
  Collaborator,
  CollaboratorPayload,
  Mission,
  MissionPayload,
  Organization,
  OrganizationPayload,
  PaginatedResponse,
  Shift,
  ShiftPayload,
  Site,
  SitePayload,
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
