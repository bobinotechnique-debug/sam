export function toDateTimeLocalValue(value: string | Date): string {
  const date = typeof value === "string" ? new Date(value) : value;
  return new Date(date.getTime() - date.getTimezoneOffset() * 60000)
    .toISOString()
    .slice(0, 16);
}

export function toUtcISOString(localValue: string): string {
  // datetime-local is interpreted in local timezone, convert to UTC ISO string
  const date = new Date(localValue);
  return date.toISOString();
}

export function formatDateTime(value: string): string {
  const date = new Date(value);
  return `${date.toLocaleDateString()} ${date.toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" })}`;
}
