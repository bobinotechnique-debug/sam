import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { createSite, deleteSite, getSite, listSites, updateSite } from "../api/entities";
import { PaginatedResponse, Site, SitePayload } from "../api/types";

interface SiteFormState {
  organization_id: number | "";
  name: string;
  timezone: string;
  address: string;
}

function SiteForm({ mode }: { mode: "create" | "edit" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<SiteFormState>({
    organization_id: "",
    name: "",
    timezone: "UTC",
    address: "",
  });
  const [loading, setLoading] = useState(mode === "edit");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (mode === "edit" && id) {
      getSite(Number(id))
        .then((site) =>
          setForm({
            organization_id: site.organization_id,
            name: site.name,
            timezone: site.timezone,
            address: site.address ?? "",
          }),
        )
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id, mode]);

  const handleSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError(null);

    const payload: SitePayload = {
      organization_id: Number(form.organization_id),
      name: form.name,
      timezone: form.timezone,
      address: form.address || null,
    };

    try {
      if (mode === "create") {
        await createSite(payload);
      } else if (id) {
        await updateSite(Number(id), payload);
      }
      navigate("/sites");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-sm text-slate-300">Chargement du lieu...</p>;
  }

  return (
    <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
      {error && <p className="rounded bg-red-900/40 px-3 py-2 text-red-200">{error}</p>}
      <div className="grid gap-4 md:grid-cols-2">
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Organisation ID
          <input
            type="number"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.organization_id}
            onChange={(e) => setForm({ ...form, organization_id: e.target.value === "" ? "" : Number(e.target.value) })}
            required
            min={1}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Nom du site
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Fuseau horaire
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.timezone}
            onChange={(e) => setForm({ ...form, timezone: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Adresse (optionnel)
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.address}
            onChange={(e) => setForm({ ...form, address: e.target.value })}
          />
        </label>
      </div>
      <div className="flex gap-2">
        <button
          type="submit"
          className="rounded bg-indigo-600 px-4 py-2 font-semibold text-white hover:bg-indigo-500 disabled:opacity-60"
          disabled={saving}
        >
          {saving ? "Enregistrement..." : mode === "create" ? "Créer" : "Mettre à jour"}
        </button>
        <Link
          to="/sites"
          className="rounded border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-slate-800"
        >
          Annuler
        </Link>
      </div>
    </form>
  );
}

export function SitesPage() {
  const [data, setData] = useState<PaginatedResponse<Site> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await listSites();
      setData(response);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const onDelete = async (id: number) => {
    if (!confirm("Supprimer ce lieu ?")) return;
    try {
      await deleteSite(id);
      setMessage("Lieu supprimé");
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const filtered = data?.items.filter((item) =>
    item.name.toLowerCase().includes(filter.trim().toLowerCase()),
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Sites / Lieux</h2>
          <p className="text-sm text-slate-300">Référentiel des sites avec fuseau et adresse.</p>
        </div>
        <Link
          to="/sites/new"
          className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          Nouveau lieu
        </Link>
      </div>
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <input
          placeholder="Filtrer par nom"
          className="w-full rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white md:w-64"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        {message && <p className="text-sm text-green-300">{message}</p>}
      </div>
      {loading && <p className="text-sm text-slate-300">Chargement...</p>}
      {error && <p className="rounded bg-red-900/30 px-3 py-2 text-red-200">{error}</p>}
      {!loading && !error && filtered && filtered.length === 0 && (
        <p className="text-sm text-slate-300">Aucun lieu disponible.</p>
      )}
      {!loading && !error && filtered && filtered.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-800 text-sm">
            <thead className="bg-slate-900/60">
              <tr>
                <th className="px-3 py-2 text-left font-semibold">Nom</th>
                <th className="px-3 py-2 text-left font-semibold">Organisation</th>
                <th className="px-3 py-2 text-left font-semibold">Fuseau</th>
                <th className="px-3 py-2 text-left font-semibold">Adresse</th>
                <th className="px-3 py-2 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filtered.map((site) => (
                <tr key={site.id} className="hover:bg-slate-800/50">
                  <td className="px-3 py-2">{site.name}</td>
                  <td className="px-3 py-2">{site.organization_id}</td>
                  <td className="px-3 py-2">{site.timezone}</td>
                  <td className="px-3 py-2">{site.address ?? "—"}</td>
                  <td className="px-3 py-2 text-right">
                    <Link to={`/sites/${site.id}/edit`} className="mr-2 text-indigo-300 hover:text-indigo-100">
                      Éditer
                    </Link>
                    <button className="text-red-300 hover:text-red-100" onClick={() => onDelete(site.id)}>
                      Supprimer
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

export function SiteCreatePage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Créer un lieu</h2>
      <SiteForm mode="create" />
    </div>
  );
}

export function SiteEditPage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Mettre à jour le lieu</h2>
      <SiteForm mode="edit" />
    </div>
  );
}
