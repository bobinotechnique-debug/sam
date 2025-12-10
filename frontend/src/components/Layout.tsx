import { NavLink, Outlet } from "react-router-dom";

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `rounded-md px-3 py-2 text-sm font-medium ${
    isActive
      ? "bg-indigo-600 text-white"
      : "text-slate-200 hover:bg-indigo-500/20 hover:text-white"
  }`;

export function Layout() {
  return (
    <div className="min-h-screen bg-slate-950 text-slate-50">
      <div className="mx-auto flex max-w-6xl flex-col gap-6 px-6 py-8">
        <header className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between">
          <div>
            <p className="text-xs uppercase tracking-widest text-indigo-300">Phase 4.3</p>
            <h1 className="text-3xl font-semibold">Planning – vue visuelle</h1>
            <p className="text-sm text-slate-300">Gérer les référentiels et le planning jour/semaine par lieu avec affectations.</p>
          </div>
          <nav className="flex flex-wrap gap-2">
            <NavLink to="/planning" className={navLinkClass}>
              Planning
            </NavLink>
            <NavLink to="/organizations" className={navLinkClass}>
              Organisations
            </NavLink>
            <NavLink to="/collaborators" className={navLinkClass}>
              Collaborateurs
            </NavLink>
            <NavLink to="/sites" className={navLinkClass}>
              Lieux
            </NavLink>
            <NavLink to="/missions" className={navLinkClass}>
              Missions
            </NavLink>
          </nav>
        </header>
        <main className="rounded-xl border border-slate-800 bg-slate-900/60 p-6 shadow-xl">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

export default Layout;
