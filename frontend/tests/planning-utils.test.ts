import { describe, expect, it } from "vitest";

import { filterPlanningShifts } from "../src/features/planning/hooks";
import { PlanningShift } from "../src/features/planning/types";
import { calculatePosition, snapToInterval } from "../src/features/planning/utils";

describe("planning utils", () => {
  it("snaps dates to the given interval", () => {
    const date = new Date("2024-01-01T10:07:00Z");
    const snapped = snapToInterval(date, 15);
    expect(snapped.getUTCMinutes() % 15).toBe(0);
  });

  it("computes relative positions inside the day window", () => {
    const { offsetPercent, widthPercent } = calculatePosition(
      "2024-01-01T08:00:00Z",
      "2024-01-01T10:00:00Z",
      6,
      22,
    );
    expect(offsetPercent).toBeGreaterThan(0);
    expect(widthPercent).toBeGreaterThan(0);
  });

  it("filters planning shifts by place, person, and status", () => {
    const shifts: PlanningShift[] = [
      {
        id: 1,
        siteId: 1,
        roleId: 1,
        missionId: 1,
        startUtc: "2024-01-01T08:00:00Z",
        endUtc: "2024-01-01T09:00:00Z",
        status: "draft",
        source: "manual",
        capacity: 1,
        assignments: [
          {
            id: 1,
            shift_instance_id: 1,
            collaborator_id: 50,
            role_id: 1,
            status: "confirmed",
            source: "manual",
            note: null,
            is_locked: false,
            created_at: null,
            updated_at: null,
          },
        ],
        conflicts: [],
      },
    ];

    const filtered = filterPlanningShifts(shifts, {
      placeIds: [1],
      personIds: [50],
      status: ["draft"],
      search: "shift 1",
    });

    expect(filtered).toHaveLength(1);
  });
});

