import { render, screen, waitFor, within } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { listCollaborators, listSites } from "../src/api/entities";
import {
  createPlanningAssignment,
  fetchPlanningShiftInstances,
  updatePlanningShiftInstance,
} from "../src/api/planning";
import { PlanningPage } from "../src/pages/PlanningPage";

vi.mock("../src/api/entities");
vi.mock("../src/api/planning");

const renderWithProviders = () => {
  const client = new QueryClient();
  return render(
    <QueryClientProvider client={client}>
      <PlanningPage />
    </QueryClientProvider>,
  );
};

describe("PlanningPage", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    vi.mocked(listSites).mockResolvedValue({
      items: [{ id: 1, organization_id: 1, name: "HQ", timezone: "UTC", address: "" }],
      total: 1,
      page: 1,
      page_size: 50,
    });
    vi.mocked(listCollaborators).mockResolvedValue({
      items: [
        { id: 11, organization_id: 1, full_name: "Alex King", primary_role_id: 1, status: "active", email: "alex@example.com" },
        { id: 12, organization_id: 1, full_name: "Jamie Lee", primary_role_id: 1, status: "active", email: "jamie@example.com" },
      ],
      total: 2,
      page: 1,
      page_size: 50,
    });
    vi.mocked(fetchPlanningShiftInstances).mockResolvedValue([
      {
        shift: {
          id: 10,
          mission_id: 1,
          template_id: null,
          site_id: 1,
          role_id: 1,
          team_id: null,
          status: "draft",
          source: "manual",
          capacity: 2,
          start_utc: new Date().toISOString(),
          end_utc: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
        },
        assignments: [
          {
            id: 1,
            shift_instance_id: 10,
            collaborator_id: 11,
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
    ]);
    vi.mocked(updatePlanningShiftInstance).mockResolvedValue({
      shift: {
        id: 10,
        mission_id: 1,
        template_id: null,
        site_id: 1,
        role_id: 1,
        team_id: null,
        status: "draft",
        source: "manual",
        capacity: 2,
        start_utc: new Date().toISOString(),
        end_utc: new Date(Date.now() + 60 * 60 * 1000).toISOString(),
      },
      assignments: [],
      conflicts: [],
    });
    vi.mocked(createPlanningAssignment).mockResolvedValue({
      assignment: {
        id: 2,
        shift_instance_id: 10,
        collaborator_id: 12,
        role_id: 1,
        status: "pending",
        source: "manual",
        note: null,
        is_locked: false,
        created_at: null,
        updated_at: null,
      },
      conflicts: [],
    });
  });

  it("renders shifts from the planning API", async () => {
    renderWithProviders();

    await waitFor(() => expect(screen.getByText(/Shift #10/i)).toBeInTheDocument());
    expect(screen.getAllByText(/HQ/).length).toBeGreaterThan(0);
  });

  it("opens the editor when a shift is selected", async () => {
    renderWithProviders();

    const button = await screen.findByRole("button", { name: /Shift #10/i });
    await userEvent.click(button);

    await waitFor(() => expect(screen.getByText(/Edit shift #10/i)).toBeInTheDocument());
  });

  it("sends an assignment when the user selects a collaborator", async () => {
    renderWithProviders();
    const button = await screen.findByRole("button", { name: /Shift #10/i });
    await userEvent.click(button);

    const editor = await screen.findByText(/Assign collaborator/i);
    const modal = editor.closest("div");
    if (!modal) throw new Error("editor modal missing");

    const selects = within(modal).getAllByRole("combobox");
    await userEvent.selectOptions(selects[selects.length - 1], "12");
    await userEvent.click(screen.getByRole("button", { name: /Assign/i }));

    await waitFor(() => expect(createPlanningAssignment).toHaveBeenCalled());
  });
});

