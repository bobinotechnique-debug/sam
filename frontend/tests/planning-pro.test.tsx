import React from "react";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { PlanningProPage } from "../src/pages/PlanningProPage";

function createWrapper(ui: React.ReactElement) {
  const queryClient = new QueryClient({
    defaultOptions: {
      queries: { retry: false },
    },
  });
  return render(<QueryClientProvider client={queryClient}>{ui}</QueryClientProvider>);
}

const shiftsResponse = [
  {
    shift: {
      id: 1,
      mission_id: 1,
      template_id: null,
      site_id: 2,
      role_id: 3,
      team_id: null,
      start_utc: "2025-01-01T08:00:00Z",
      end_utc: "2025-01-01T12:00:00Z",
      status: "draft",
      source: "manual",
      capacity: 1,
    },
    assignments: [
      {
        id: 10,
        shift_instance_id: 1,
        collaborator_id: 5,
        role_id: 3,
        status: "proposed",
        source: "auto-assign-v1",
        note: null,
        is_locked: false,
        created_at: null,
        updated_at: null,
      },
    ],
    conflicts: [
      {
        rule: "availability_partial",
        type: "soft",
        details: {},
      },
    ],
  },
];

beforeEach(() => {
  vi.restoreAllMocks();
  vi.spyOn(global, "fetch").mockImplementation((input) => {
    const url = typeof input === "string" ? input : input.url;
    if (url.endsWith("/api/v1/planning/shifts")) {
      return Promise.resolve(
        new Response(JSON.stringify(shiftsResponse), {
          status: 200,
          headers: { "Content-Type": "application/json" },
        }),
      );
    }
    if (url.endsWith("/api/v1/planning/rules")) {
      return Promise.resolve(
        new Response(
          JSON.stringify({ hr_rules: [], conflict_rules: [{ id: 1, organization_id: 1, code: "double_booking", severity: "error", description: null, config: {} }] }),
          { status: 200, headers: { "Content-Type": "application/json" } },
        ),
      );
    }
    return Promise.resolve(new Response("", { status: 404 }));
  });
});

describe("PlanningProPage", () => {
  it("renders real shifts and conflicts from the API", async () => {
    createWrapper(<PlanningProPage />);

    expect(await screen.findByText(/Connected timeline/)).toBeInTheDocument();
    await waitFor(() => expect(screen.getByText(/Site 2/)).toBeInTheDocument());
    expect(screen.getByText(/Collab 5 - proposed/)).toBeInTheDocument();
    expect(screen.getByText(/availability_partial/)).toBeInTheDocument();
  });
});
