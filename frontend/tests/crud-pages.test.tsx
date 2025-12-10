import { act, type ReactNode } from "react";
import { MemoryRouter, Route, Routes } from "react-router-dom";
import { render, screen, waitFor } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { beforeEach, describe, expect, it, vi } from "vitest";

import {
  CollaboratorsPage,
  CollaboratorCreatePage,
  CollaboratorEditPage,
} from "../src/pages/CollaboratorsPage";
import {
  OrganizationsPage,
  OrganizationCreatePage,
  OrganizationEditPage,
} from "../src/pages/OrganizationsPage";
import {
  createCollaborator,
  createOrganization,
  deleteCollaborator,
  deleteOrganization,
  getCollaborator,
  getOrganization,
  listCollaborators,
  listOrganizations,
  updateCollaborator,
  updateOrganization,
} from "../src/api/entities";

vi.mock("../src/api/entities");

const mockedApis = {
  listOrganizations: vi.mocked(listOrganizations),
  getOrganization: vi.mocked(getOrganization),
  createOrganization: vi.mocked(createOrganization),
  updateOrganization: vi.mocked(updateOrganization),
  deleteOrganization: vi.mocked(deleteOrganization),
  listCollaborators: vi.mocked(listCollaborators),
  getCollaborator: vi.mocked(getCollaborator),
  createCollaborator: vi.mocked(createCollaborator),
  updateCollaborator: vi.mocked(updateCollaborator),
  deleteCollaborator: vi.mocked(deleteCollaborator),
};

const baseOrg = {
  id: 1,
  name: "Acme",
  timezone: "UTC",
  currency: "EUR",
  contact_email: null,
};

const baseCollaborator = {
  id: 2,
  organization_id: 1,
  full_name: "Jane Doe",
  primary_role_id: null,
  status: "active",
  email: "jane@example.com",
};

const wrap = (element: ReactNode, initialEntries: string[]) => (
  <MemoryRouter initialEntries={initialEntries}>{element}</MemoryRouter>
);

describe("Organizations CRUD pages", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedApis.listOrganizations.mockResolvedValue({
      items: [baseOrg],
      total: 1,
      page: 1,
      page_size: 50,
    });
    mockedApis.getOrganization.mockResolvedValue(baseOrg);
    mockedApis.createOrganization.mockResolvedValue(baseOrg as never);
    mockedApis.updateOrganization.mockResolvedValue(baseOrg as never);
    mockedApis.deleteOrganization.mockResolvedValue();
  });

  it("renders loading then table for organizations", async () => {
    await act(async () => {
      render(wrap(<OrganizationsPage />, ["/organizations"]));
    });

    await waitFor(() => expect(mockedApis.listOrganizations).toHaveBeenCalled());
    expect(await screen.findByText("Acme")).toBeInTheDocument();
  });

  it("shows empty state when no organizations are returned", async () => {
    mockedApis.listOrganizations.mockResolvedValueOnce({
      items: [],
      total: 0,
      page: 1,
      page_size: 50,
    });

    await act(async () => {
      render(wrap(<OrganizationsPage />, ["/organizations"]));
    });

    await waitFor(() => expect(screen.getByText(/Aucune organisation disponible/i)).toBeInTheDocument());
  });

  it("handles deletion with confirmation", async () => {
    const confirmSpy = vi.spyOn(window, "confirm").mockReturnValue(true);

    await act(async () => {
      render(wrap(<OrganizationsPage />, ["/organizations"]));
    });

    await screen.findByText("Acme");
    await act(async () => {
      await userEvent.click(screen.getByText("Supprimer"));
    });

    expect(mockedApis.deleteOrganization).toHaveBeenCalledWith(1);
    confirmSpy.mockRestore();
  });

  it("loads an organization in edit form", async () => {
    await act(async () => {
      render(
        wrap(
          <Routes>
            <Route path="/organizations/:id/edit" element={<OrganizationEditPage />} />
          </Routes>,
          ["/organizations/1/edit"],
        ),
      );
    });

    await waitFor(() => expect(mockedApis.getOrganization).toHaveBeenCalledWith(1));
    expect(await screen.findByDisplayValue(/Acme/)).toBeInTheDocument();
  });
});

describe("Collaborators CRUD pages", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    mockedApis.listCollaborators.mockResolvedValue({
      items: [baseCollaborator],
      total: 1,
      page: 1,
      page_size: 50,
    });
    mockedApis.getCollaborator.mockResolvedValue(baseCollaborator);
    mockedApis.createCollaborator.mockResolvedValue(baseCollaborator as never);
    mockedApis.updateCollaborator.mockResolvedValue(baseCollaborator as never);
    mockedApis.deleteCollaborator.mockResolvedValue();
  });

  it("surfaces errors when collaborator listing fails", async () => {
    mockedApis.listCollaborators.mockRejectedValueOnce(new Error("API indisponible"));

    await act(async () => {
      render(wrap(<CollaboratorsPage />, ["/collaborators"]));
    });

    await waitFor(() => expect(screen.getByText(/API indisponible/i)).toBeInTheDocument());
  });

  it("shows empty state on collaborator page", async () => {
    mockedApis.listCollaborators.mockResolvedValueOnce({ items: [], total: 0, page: 1, page_size: 50 });

    await act(async () => {
      render(wrap(<CollaboratorsPage />, ["/collaborators"]));
    });

    await waitFor(() => expect(screen.getByText(/Aucun collaborateur/i)).toBeInTheDocument());
  });

  it("submits collaborator create form", async () => {
    await act(async () => {
      render(
        wrap(
          <Routes>
            <Route path="/collaborators/new" element={<CollaboratorCreatePage />} />
          </Routes>,
          ["/collaborators/new"],
        ),
      );
    });

    await act(async () => {
      await userEvent.type(screen.getByLabelText(/Organisation ID/i), "1");
      await userEvent.type(screen.getByLabelText(/Nom complet/i), "Jane Doe");
      await userEvent.type(screen.getByLabelText(/Email/i), "jane@example.com");
      await userEvent.click(screen.getByRole("button", { name: /Créer/i }));
    });

    await waitFor(() =>
      expect(mockedApis.createCollaborator).toHaveBeenCalledWith({
        organization_id: 1,
        full_name: "Jane Doe",
        primary_role_id: null,
        status: "active",
        email: "jane@example.com",
      }),
    );
  });

  it("prefills collaborator edit form", async () => {
    await act(async () => {
      render(
        wrap(
          <Routes>
            <Route path="/collaborators/:id/edit" element={<CollaboratorEditPage />} />
          </Routes>,
          ["/collaborators/2/edit"],
        ),
      );
    });

    await waitFor(() => expect(mockedApis.getCollaborator).toHaveBeenCalledWith(2));
    expect(await screen.findByDisplayValue(/Jane Doe/)).toBeInTheDocument();
  });
});
