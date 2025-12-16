import { Collaborator } from "../../../api/types";

const badgePalette = [
  "bg-indigo-600",
  "bg-sky-500",
  "bg-emerald-500",
  "bg-amber-500",
  "bg-rose-500",
];

const textPalette = [
  "text-indigo-50",
  "text-sky-50",
  "text-emerald-50",
  "text-amber-50",
  "text-rose-50",
];

function initials(name: string): string {
  const parts = name.trim().split(" ").filter(Boolean);
  if (parts.length === 0) return "?";
  if (parts.length === 1) return parts[0].slice(0, 2).toUpperCase();
  return `${parts[0][0]}${parts[parts.length - 1][0]}`.toUpperCase();
}

export function AvatarStack({ people, limit = 3 }: { people: Collaborator[]; limit?: number }) {
  const visible = people.slice(0, limit);
  const remaining = people.length - visible.length;

  return (
    <div className="flex items-center gap-1">
      <div className="flex -space-x-2">
        {visible.map((person) => {
          const colorIndex = person.id % badgePalette.length;
          return (
            <span
              key={person.id}
              className={`inline-flex h-8 w-8 items-center justify-center rounded-full border border-slate-900 text-xs font-semibold ${badgePalette[colorIndex]} ${textPalette[colorIndex]}`}
              title={person.full_name}
              aria-label={person.full_name}
            >
              {initials(person.full_name)}
            </span>
          );
        })}
        {remaining > 0 && (
          <span className="inline-flex h-8 w-8 items-center justify-center rounded-full border border-slate-800 bg-slate-800 text-xs font-semibold text-slate-200">
            +{remaining}
          </span>
        )}
      </div>
    </div>
  );
}

