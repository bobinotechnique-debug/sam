import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import {
  createOrganization,
  deleteOrganization,
  getOrganization,
  listOrganizations,
  updateOrganization,
} from "../api/entities";
import { Organization, OrganizationPayload, PaginatedResponse } from "../api/types";

interface FormState {
  name: string;
  timezone: string;
  currency: string;
  contact_email: string;
}

function OrganizationForm({ mode }: { mode: "create" | "edit" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<FormState>({
    name: "",
    timezone: "UTC",
    currency: "EUR",
    contact_email: "",
  });
  const [loading, setLoading] = useState(mode === "edit");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (mode === "edit" && id) {
      getOrganization(Number(id))
        .then((org) =>
          setForm({
            name: org.name,
            timezone: org.timezone,
            currency: org.currency,
            contact_email: org.contact_email ?? "",
          }),
        )
        .catch((err) => setError(err.message))
        .finally(() => setLoading(false));
    }
  }, [id, mode]);

  const onSubmit = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError(null);
    const payload: OrganizationPayload = {
      name: form.name,
      timezone: form.timezone,
      currency: form.currency,
      contact_email: form.contact_email || null,
    };

    try {
      if (mode === "create") {
        await createOrganization(payload);
      } else if (id) {
        await updateOrganization(Number(id), payload);
      }
      navigate("/organizations");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-sm text-slate-300">Chargement de l'organisation...</p>;
  }

  return (
    <form className="flex flex-col gap-4" onSubmit={onSubmit}>
      {error && <p className="rounded bg-red-900/40 px-3 py-2 text-red-200">{error}</p>}
      <div className="grid gap-4 md:grid-cols-2">
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Nom
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
          Devise (ISO)
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.currency}
            onChange={(e) => setForm({ ...form, currency: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Email de contact (optionnel)
          <input
            type="email"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.contact_email}
            onChange={(e) => setForm({ ...form, contact_email: e.target.value })}
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
          to="/organizations"
          className="rounded border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-slate-800"
        >
          Annuler
        </Link>
      </div>
    </form>
  );
}

export function OrganizationsPage() {
  const [data, setData] = useState<PaginatedResponse<Organization> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await listOrganizations();
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
    if (!confirm("Supprimer cette organisation ?")) return;
    try {
      await deleteOrganization(id);
      setMessage("Organisation supprimée");
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
          <h2 className="text-2xl font-semibold">Organisations</h2>
          <p className="text-sm text-slate-300">Lister, créer, éditer ou supprimer des organisations.</p>
        </div>
        <Link
          to="/organizations/new"
          className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          Nouvelle organisation
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
        <p className="text-sm text-slate-300">Aucune organisation disponible.</p>
      )}
      {!loading && !error && filtered && filtered.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-800 text-sm">
            <thead className="bg-slate-900/60">
              <tr>
                <th className="px-3 py-2 text-left font-semibold">Nom</th>
                <th className="px-3 py-2 text-left font-semibold">Fuseau</th>
                <th className="px-3 py-2 text-left font-semibold">Devise</th>
                <th className="px-3 py-2 text-left font-semibold">Email</th>
                <th className="px-3 py-2 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filtered.map((org) => (
                <tr key={org.id} className="hover:bg-slate-800/50">
                  <td className="px-3 py-2">{org.name}</td>
                  <td className="px-3 py-2">{org.timezone}</td>
                  <td className="px-3 py-2">{org.currency}</td>
                  <td className="px-3 py-2">{org.contact_email ?? "—"}</td>
                  <td className="px-3 py-2 text-right">
                    <Link
                      to={`/organizations/${org.id}/edit`}
                      className="mr-2 text-indigo-300 hover:text-indigo-100"
                    >
                      Éditer
                    </Link>
                    <button
                      className="text-red-300 hover:text-red-100"
                      onClick={() => onDelete(org.id)}
                    >
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

export function OrganizationCreatePage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Créer une organisation</h2>
      <OrganizationForm mode="create" />
    </div>
  );
}

export function OrganizationEditPage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Mettre à jour l'organisation</h2>
      <OrganizationForm mode="edit" />
    </div>
  );
}
