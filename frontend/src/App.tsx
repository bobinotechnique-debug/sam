import { BrowserRouter, Navigate, Route, Routes } from "react-router-dom";

import Layout from "./components/Layout";
import { CollaboratorCreatePage, CollaboratorEditPage, CollaboratorsPage } from "./pages/CollaboratorsPage";
import { MissionCreatePage, MissionEditPage, MissionsPage } from "./pages/MissionsPage";
import { PlanningPage } from "./pages/PlanningPage";
import { PlanningProPage } from "./pages/PlanningProPage";
import { OrganizationCreatePage, OrganizationEditPage, OrganizationsPage } from "./pages/OrganizationsPage";
import { RoleCreatePage, RoleEditPage, RolesPage } from "./pages/RolesPage";
import { SiteCreatePage, SiteEditPage, SitesPage } from "./pages/SitesPage";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/planning" replace />} />
          <Route path="organizations" element={<OrganizationsPage />} />
          <Route path="organizations/new" element={<OrganizationCreatePage />} />
          <Route path="organizations/:id/edit" element={<OrganizationEditPage />} />

          <Route path="collaborators" element={<CollaboratorsPage />} />
          <Route path="collaborators/new" element={<CollaboratorCreatePage />} />
          <Route path="collaborators/:id/edit" element={<CollaboratorEditPage />} />

          <Route path="sites" element={<SitesPage />} />
          <Route path="sites/new" element={<SiteCreatePage />} />
          <Route path="sites/:id/edit" element={<SiteEditPage />} />

          <Route path="roles" element={<RolesPage />} />
          <Route path="roles/new" element={<RoleCreatePage />} />
          <Route path="roles/:id/edit" element={<RoleEditPage />} />

          <Route path="missions" element={<MissionsPage />} />
          <Route path="missions/new" element={<MissionCreatePage />} />
          <Route path="missions/:id/edit" element={<MissionEditPage />} />

          <Route path="planning" element={<PlanningPage />} />
          <Route path="planning/pro" element={<PlanningProPage />} />
        </Route>
      </Routes>
    </BrowserRouter>
  );
}

export default App;
