import { Mission } from "../api/types";

export const PLANNING_START_HOUR = 6;
export const PLANNING_END_HOUR = 26; // 2AM next day

export interface TimeRange {
  start: Date;
  end: Date;
}

export function startOfDay(date: Date): Date {
  return new Date(date.getFullYear(), date.getMonth(), date.getDate());
}

export function startOfWeek(date: Date): Date {
  const start = startOfDay(date);
  const day = start.getDay();
  const diff = (day === 0 ? -6 : 1 - day); // Monday as first day
  start.setDate(start.getDate() + diff);
  return start;
}

export function getDayRange(date: Date): TimeRange {
  const start = startOfDay(date);
  const end = new Date(start);
  end.setDate(end.getDate() + 1);
  return { start, end };
}

export function getWeekDays(date: Date): Date[] {
  const start = startOfWeek(date);
  return Array.from({ length: 7 }, (_, index) => {
    const day = new Date(start);
    day.setDate(start.getDate() + index);
    return day;
  });
}

export function missionOverlapsRange(mission: Mission, range: TimeRange): boolean {
  const start = new Date(mission.start_utc);
  const end = new Date(mission.end_utc);
  return start < range.end && end > range.start;
}

export function minutesFromPlanningStart(date: Date): number {
  return (date.getHours() - PLANNING_START_HOUR) * 60 + date.getMinutes();
}

export function clampToRange(date: Date, range: TimeRange): Date {
  if (date < range.start) return range.start;
  if (date > range.end) return range.end;
  return date;
}

export function computeBlockPosition(mission: Mission, range: TimeRange): {
  offsetPercent: number;
  widthPercent: number;
} {
  const start = clampToRange(new Date(mission.start_utc), range);
  const end = clampToRange(new Date(mission.end_utc), range);
  const totalMinutes = (PLANNING_END_HOUR - PLANNING_START_HOUR) * 60;
  const rangeStart = new Date(range.start);
  rangeStart.setHours(PLANNING_START_HOUR, 0, 0, 0);
  const rangeEnd = new Date(range.start);
  rangeEnd.setHours(PLANNING_END_HOUR, 0, 0, 0);
  const clampedStart = clampToRange(start, { start: rangeStart, end: rangeEnd });
  const clampedEnd = clampToRange(end, { start: rangeStart, end: rangeEnd });
  const offsetMinutes = minutesFromPlanningStart(clampedStart);
  const durationMinutes = Math.max(15, (clampedEnd.getTime() - clampedStart.getTime()) / 60000);
  return {
    offsetPercent: Math.max(0, (offsetMinutes / totalMinutes) * 100),
    widthPercent: Math.min(100, (durationMinutes / totalMinutes) * 100),
  };
}

export function formatHourLabel(hour: number): string {
  const normalized = hour >= 24 ? hour - 24 : hour;
  return `${normalized.toString().padStart(2, "0")}:00`;
}
