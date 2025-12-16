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

export interface Role {
  id: number;
  organization_id: number;
  name: string;
  description: string | null;
  tags: string[];
}

export interface RolePayload {
  organization_id: number;
  name: string;
  description?: string | null;
  tags?: string[];
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

export interface Team {
  id: number;
  organization_id: number;
  site_id: number | null;
  name: string;
  color_hex: string | null;
}

export interface Skill {
  id: number;
  organization_id: number;
  name: string;
}

export interface ShiftTemplate {
  id: number;
  mission_id: number;
  site_id: number;
  role_id: number;
  team_id: number | null;
  recurrence_rule: string | null;
  start_time_utc: string;
  end_time_utc: string;
  expected_headcount: number;
  is_active: boolean;
}

export interface ShiftTemplatePayload {
  mission_id: number;
  site_id: number;
  role_id: number;
  team_id?: number | null;
  recurrence_rule?: string | null;
  start_time_utc: string;
  end_time_utc: string;
  expected_headcount?: number;
  is_active?: boolean;
}

export interface ShiftInstance {
  id: number;
  mission_id: number;
  template_id: number | null;
  site_id: number;
  role_id: number;
  team_id: number | null;
  status: string;
  source: string;
  capacity: number;
  start_utc: string;
  end_utc: string;
}

export interface ShiftInstancePayload {
  mission_id: number;
  template_id?: number | null;
  site_id: number;
  role_id: number;
  team_id?: number | null;
  status?: string;
  source?: string;
  capacity?: number;
  start_utc: string;
  end_utc: string;
}

export interface Assignment {
  id: number;
  shift_instance_id: number;
  collaborator_id: number;
  role_id: number;
  status: string;
  source: string;
  note: string | null;
  is_locked: boolean;
  created_at: string | null;
  updated_at: string | null;
}

export interface AssignmentPayload {
  shift_instance_id: number;
  collaborator_id: number;
  role_id: number;
  status?: string;
  source?: string;
  note?: string | null;
  is_locked?: boolean;
}

export interface UserAvailability {
  id: number;
  collaborator_id: number;
  start_utc: string;
  end_utc: string;
  is_available: boolean;
  reason: string | null;
}

export interface UserAvailabilityPayload {
  collaborator_id: number;
  start_utc: string;
  end_utc: string;
  is_available?: boolean;
  reason?: string | null;
}

export interface HrRule {
  id: number;
  organization_id: number;
  code: string;
  severity: string;
  description: string | null;
  config: Record<string, unknown>;
}

export interface ConflictRule {
  id: number;
  organization_id: number;
  code: string;
  severity: string;
  description: string | null;
  config: Record<string, unknown>;
}

export interface Publication {
  id: number;
  organization_id: number;
  author_user_id: number | null;
  status: string;
  version: number;
  message: string | null;
  published_at: string | null;
}

export interface NotificationEvent {
  id: number;
  organization_id: number;
  recipient_user_id: number | null;
  event_type: string;
  payload: Record<string, unknown>;
  related_shift_instance_id: number | null;
  created_at: string | null;
  read_at: string | null;
}

export interface PlanningProConfig {
  hr_rules: HrRule[];
  conflict_rules: ConflictRule[];
}

export interface ConflictEntry {
  type: "hard" | "soft";
  rule: string;
  details: Record<string, unknown>;
}

export interface ConflictPreviewResult {
  shift?: ShiftInstancePayload | ShiftInstance;
  assignment?: AssignmentPayload | Assignment;
  conflicts: ConflictEntry[];
}

export interface ShiftWriteResponse {
  shift: ShiftInstance;
  conflicts: ConflictEntry[];
}

export interface AssignmentWriteResponse {
  assignment: Assignment;
  conflicts: ConflictEntry[];
}

export interface PlanningShift {
  shift: ShiftInstance;
  assignments: Assignment[];
  conflicts: ConflictEntry[];
}

export interface AutoAssignJobStatus {
  job_id: string;
  status: string;
  started_at?: string;
  completed_at?: string;
  assignments_created: number;
  conflicts: ConflictEntry[];
}
