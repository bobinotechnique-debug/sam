export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface Organization {
  id: number;
  name: string;
  timezone: string;
  currency: string;
  contact_email: string | null;
}

export interface OrganizationPayload {
  name: string;
  timezone?: string;
  currency?: string;
  contact_email?: string | null;
}

export interface Collaborator {
  id: number;
  organization_id: number;
  full_name: string;
  primary_role_id: number | null;
  status: string;
  email: string | null;
}

export interface CollaboratorPayload {
  organization_id: number;
  full_name: string;
  primary_role_id?: number | null;
  status?: string;
  email?: string | null;
}

export interface Site {
  id: number;
  organization_id: number;
  name: string;
  timezone: string;
  address: string | null;
}

export interface SitePayload {
  organization_id: number;
  name: string;
  timezone?: string | null;
  address?: string | null;
}

export interface Mission {
  id: number;
  site_id: number;
  role_id: number;
  status: string;
  start_utc: string;
  end_utc: string;
  budget_target: number | null;
  note: string | null;
}

export interface MissionPayload {
  site_id: number;
  role_id: number;
  status?: string;
  start_utc: string;
  end_utc: string;
  budget_target?: number | null;
  note?: string | null;
}

export interface Shift {
  id: number;
  mission_id: number;
  collaborator_id: number;
  status: string;
  start_utc: string;
  end_utc: string;
  cancellation_reason: string | null;
}

export interface ShiftPayload {
  mission_id: number;
  collaborator_id: number;
  status?: string;
  start_utc: string;
  end_utc: string;
  cancellation_reason?: string | null;
}
