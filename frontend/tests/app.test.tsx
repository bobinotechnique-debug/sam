import { act } from "react";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import App from "../src/App";

const mockResponse = (data: unknown) =>
  Promise.resolve({
    ok: true,
    status: 200,
    json: async () => data,
  }) as Promise<Response>;

describe("App", () => {
  beforeEach(() => {
    const organizations = { items: [{ id: 1, name: "Acme", timezone: "UTC", currency: "EUR", contact_email: null }], total: 1, page: 1, page_size: 50 };
    const collaborators = {
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
    };
    const sites = {
      items: [{ id: 1, organization_id: 1, name: "HQ", timezone: "UTC", address: "" }],
      total: 1,
      page: 1,
      page_size: 50,
    };
    const missions = {
      items: [
        {
          id: 1,
          site_id: 1,
          role_id: 2,
          status: "draft",
          start_utc: new Date().toISOString(),
          end_utc: new Date(Date.now() + 3600000).toISOString(),
          budget_target: null,
          note: null,
        },
      ],
      total: 1,
      page: 1,
      page_size: 50,
    };
    const shifts = {
      items: [
        {
          id: 1,
          mission_id: 1,
          collaborator_id: 1,
          status: "draft",
          start_utc: new Date().toISOString(),
          end_utc: new Date(Date.now() + 3600000).toISOString(),
          cancellation_reason: null,
        },
      ],
      total: 1,
      page: 1,
      page_size: 50,
    };

    global.fetch = vi.fn((url: RequestInfo | URL) => {
      const href = url.toString();
      if (href.includes("/organizations")) return mockResponse(organizations);
      if (href.includes("/collaborators")) return mockResponse(collaborators);
      if (href.includes("/sites")) return mockResponse(sites);
      if (href.includes("/missions")) return mockResponse(missions);
      if (href.includes("/shifts")) return mockResponse(shifts);
      return mockResponse({});
    }) as unknown as typeof fetch;
  });

  it("renders planning view by default", async () => {
    await act(async () => {
      render(<App />);
    });

    expect(await screen.findByRole("heading", { name: /Planning visuel/i })).toBeInTheDocument();
    await screen.findByText(/HQ/);
    expect(screen.getByText(/Vue jour\/semaine/i)).toBeInTheDocument();
  });

  it("navigates to collaborators and missions", async () => {
    await act(async () => {
      render(<App />);
    });

    await act(async () => {
      await userEvent.click(screen.getByRole("link", { name: "Collaborateurs" }));
    });
    await screen.findByText("Jane Doe");

    await act(async () => {
      await userEvent.click(screen.getByRole("link", { name: "Missions" }));
    });
    await screen.findByRole("heading", { name: /Missions/i });
    expect(screen.queryByText(/Aucune mission/)).not.toBeInTheDocument();
  });
});
