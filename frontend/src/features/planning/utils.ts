import { DateRange } from "./types";

export const DAY_START_HOUR = 6;
export const DAY_END_HOUR = 22;

export function startOfDay(value: Date): Date {
  return new Date(value.getFullYear(), value.getMonth(), value.getDate());
}

export function getWeekRange(anchor: Date): DateRange {
  const start = startOfDay(anchor);
  const day = start.getDay();
  const diff = day === 0 ? -6 : 1 - day;
  start.setDate(start.getDate() + diff);
  const end = new Date(start);
  end.setDate(start.getDate() + 6);
  return { start, end };
}

export function daysInRange(range: DateRange): Date[] {
  const days: Date[] = [];
  const cursor = startOfDay(range.start);
  while (cursor <= range.end) {
    days.push(new Date(cursor));
    cursor.setDate(cursor.getDate() + 1);
  }
  return days;
}

export function snapToInterval(date: Date, minutes: number): Date {
  const step = minutes * 60 * 1000;
  const snapped = Math.round(date.getTime() / step) * step;
  return new Date(snapped);
}

export function calculatePosition(
  startIso: string,
  endIso: string,
  dayStartHour = DAY_START_HOUR,
  dayEndHour = DAY_END_HOUR,
): { offsetPercent: number; widthPercent: number } {
  const start = new Date(startIso);
  const end = new Date(endIso);
  const windowStart = new Date(start);
  windowStart.setHours(dayStartHour, 0, 0, 0);
  const windowEnd = new Date(windowStart);
  windowEnd.setHours(dayEndHour, 0, 0, 0);

  const clampedStart = start < windowStart ? windowStart : start;
  const clampedEnd = end > windowEnd ? windowEnd : end;

  const totalMinutes = (windowEnd.getTime() - windowStart.getTime()) / 60000;
  const offsetMinutes = (clampedStart.getTime() - windowStart.getTime()) / 60000;
  const durationMinutes = Math.max(15, (clampedEnd.getTime() - clampedStart.getTime()) / 60000);

  return {
    offsetPercent: Math.max(0, Math.min(100, (offsetMinutes / totalMinutes) * 100)),
    widthPercent: Math.max(0, Math.min(100, (durationMinutes / totalMinutes) * 100)),
  };
}

export function isWithinRange(date: Date, range: DateRange): boolean {
  return date >= range.start && date <= range.end;
}

export function overlapsDay(startIso: string, endIso: string, day: Date): boolean {
  const dayStart = startOfDay(day);
  const dayEnd = new Date(dayStart);
  dayEnd.setDate(dayStart.getDate() + 1);
  const start = new Date(startIso);
  const end = new Date(endIso);
  return start < dayEnd && end > dayStart;
}
