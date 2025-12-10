import { act } from "react";

import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  createShift,
  deleteShift,
  listCollaborators,
  listMissions,
  listShifts,
  listSites,
  updateMission,
  updateShift,
} from "../src/api/entities";
import { PlanningPage } from "../src/pages/PlanningPage";

vi.mock("../src/api/entities");

const missionTime = () => {
  const start = new Date();
  const end = new Date(start.getTime() + 60 * 60 * 1000);
  return { start: start.toISOString(), end: end.toISOString() };
};

const flushPromises = () => new Promise((resolve) => setTimeout(resolve, 0));

const baseResponses = () => {
  const { start, end } = missionTime();
  return {
    missions: {
      items: [
        {
          id: 1,
          site_id: 1,
          role_id: 1,
          status: "draft",
          start_utc: start,
          end_utc: end,
          budget_target: null,
          note: null,
        },
      ],
      total: 1,
      page: 1,
      page_size: 50,
    },
    sites: {
      items: [{ id: 1, organization_id: 1, name: "HQ", timezone: "UTC", address: "" }],
      total: 1,
      page: 1,
      page_size: 50,
    },
    collaborators: {
      items: [
        {
          id: 1,
          organization_id: 1,
          full_name: "Jane Doe",
          primary_role_id: null,
          status: "active",
          email: "jane@example.com",
        },
      ],
      total: 1,
      page: 1,
      page_size: 50,
    },
    shifts: {
      items: [
        {
          id: 1,
          mission_id: 1,
          collaborator_id: 1,
          status: "draft",
          start_utc: start,
          end_utc: end,
          cancellation_reason: null,
        },
      ],
      total: 1,
      page: 1,
      page_size: 50,
    },
  };
};

const mockApis = () => ({
  missions: vi.mocked(listMissions),
  sites: vi.mocked(listSites),
  collaborators: vi.mocked(listCollaborators),
  shifts: vi.mocked(listShifts),
  saveMission: vi.mocked(updateMission),
  saveShift: vi.mocked(updateShift),
  createShift: vi.mocked(createShift),
  deleteShift: vi.mocked(deleteShift),
});

describe("PlanningPage", () => {
  const apis = mockApis();

  beforeEach(() => {
    vi.clearAllMocks();
    const fixtures = baseResponses();
    apis.missions.mockResolvedValue(fixtures.missions);
    apis.sites.mockResolvedValue(fixtures.sites);
    apis.collaborators.mockResolvedValue(fixtures.collaborators);
    apis.shifts.mockResolvedValue(fixtures.shifts);
    apis.saveMission.mockResolvedValue(fixtures.missions.items[0]);
    apis.saveShift.mockResolvedValue(fixtures.shifts.items[0]);
    apis.createShift.mockResolvedValue(fixtures.shifts.items[0]);
    apis.deleteShift.mockResolvedValue();
  });

  it("shows an empty state when no missions are available", async () => {
    apis.missions.mockResolvedValueOnce({
      items: [],
      total: 0,
      page: 1,
      page_size: 50,
    });

    await act(async () => {
      render(<PlanningPage />);
      await flushPromises();
    });

    await waitFor(() =>
      expect(
        screen.getByText(
          /Aucune mission à afficher pour l'instant. Créez des missions puis affectez-les à des collaborateurs./i,
        ),
      ).toBeInTheDocument(),
    );
  });

  it("displays an error message when the planning fetch fails", async () => {
    apis.missions.mockRejectedValueOnce(new Error("API indisponible"));

    await act(async () => {
      render(<PlanningPage />);
      await flushPromises();
    });

    await waitFor(() =>
      expect(screen.getByText(/API indisponible/i)).toBeInTheDocument(),
    );
  });

  it("opens the mission detail modal when clicking a mission", async () => {
    await act(async () => {
      render(<PlanningPage />);
      await flushPromises();
    });

    await waitFor(() => expect(screen.getByRole("heading", { name: /Planning visuel/i })).toBeInTheDocument());

    const missionButton = await screen.findByRole("button", { name: /Mission #1/i });
    await act(async () => {
      await userEvent.click(missionButton);
      await flushPromises();
    });

    expect(
      await screen.findByRole("heading", { name: /Détails et affectations/i }),
    ).toBeInTheDocument();
  });
});
