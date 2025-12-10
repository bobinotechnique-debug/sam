import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import {
  createCollaborator,
  deleteCollaborator,
  getCollaborator,
  listCollaborators,
  updateCollaborator,
} from "../api/entities";
import { Collaborator, CollaboratorPayload, PaginatedResponse } from "../api/types";

interface CollaboratorFormState {
  organization_id: number | "";
  full_name: string;
  primary_role_id: number | "";
  status: string;
  email: string;
}

function CollaboratorForm({ mode }: { mode: "create" | "edit" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<CollaboratorFormState>({
    organization_id: "",
    full_name: "",
    primary_role_id: "",
    status: "active",
    email: "",
  });
  const [loading, setLoading] = useState(mode === "edit");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (mode === "edit" && id) {
      getCollaborator(Number(id))
        .then((collaborator) =>
          setForm({
            organization_id: collaborator.organization_id,
            full_name: collaborator.full_name,
            primary_role_id: collaborator.primary_role_id ?? "",
            status: collaborator.status,
            email: collaborator.email ?? "",
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

    const payload: CollaboratorPayload = {
      organization_id: Number(form.organization_id),
      full_name: form.full_name,
      primary_role_id: form.primary_role_id === "" ? null : Number(form.primary_role_id),
      status: form.status,
      email: form.email || null,
    };

    try {
      if (mode === "create") {
        await createCollaborator(payload);
      } else if (id) {
        await updateCollaborator(Number(id), payload);
      }
      navigate("/collaborators");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-sm text-slate-300">Chargement du collaborateur...</p>;
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
          Nom complet
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.full_name}
            onChange={(e) => setForm({ ...form, full_name: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Rôle principal (ID optionnel)
          <input
            type="number"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.primary_role_id}
            onChange={(e) =>
              setForm({
                ...form,
                primary_role_id: e.target.value === "" ? "" : Number(e.target.value),
              })
            }
            min={1}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Statut
          <select
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.status}
            onChange={(e) => setForm({ ...form, status: e.target.value })}
          >
            <option value="active">Actif</option>
            <option value="inactive">Inactif</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Email (optionnel)
          <input
            type="email"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.email}
            onChange={(e) => setForm({ ...form, email: e.target.value })}
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
          to="/collaborators"
          className="rounded border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-slate-800"
        >
          Annuler
        </Link>
      </div>
    </form>
  );
}

export function CollaboratorsPage() {
  const [data, setData] = useState<PaginatedResponse<Collaborator> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await listCollaborators();
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
    if (!confirm("Supprimer ce collaborateur ?")) return;
    try {
      await deleteCollaborator(id);
      setMessage("Collaborateur supprimé");
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const filtered = data?.items.filter((item) =>
    item.full_name.toLowerCase().includes(filter.trim().toLowerCase()) ||
    (item.email ?? "").toLowerCase().includes(filter.trim().toLowerCase()),
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Collaborateurs</h2>
          <p className="text-sm text-slate-300">Gestion des collaborateurs et de leurs statuts.</p>
        </div>
        <Link
          to="/collaborators/new"
          className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          Nouveau collaborateur
        </Link>
      </div>
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <input
          placeholder="Filtrer par nom ou email"
          className="w-full rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white md:w-72"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        {message && <p className="text-sm text-green-300">{message}</p>}
      </div>
      {loading && <p className="text-sm text-slate-300">Chargement...</p>}
      {error && <p className="rounded bg-red-900/30 px-3 py-2 text-red-200">{error}</p>}
      {!loading && !error && filtered && filtered.length === 0 && (
        <p className="text-sm text-slate-300">Aucun collaborateur trouvé.</p>
      )}
      {!loading && !error && filtered && filtered.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-800 text-sm">
            <thead className="bg-slate-900/60">
              <tr>
                <th className="px-3 py-2 text-left font-semibold">Nom</th>
                <th className="px-3 py-2 text-left font-semibold">Organisation</th>
                <th className="px-3 py-2 text-left font-semibold">Email</th>
                <th className="px-3 py-2 text-left font-semibold">Statut</th>
                <th className="px-3 py-2 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filtered.map((collaborator) => (
                <tr key={collaborator.id} className="hover:bg-slate-800/50">
                  <td className="px-3 py-2">{collaborator.full_name}</td>
                  <td className="px-3 py-2">{collaborator.organization_id}</td>
                  <td className="px-3 py-2">{collaborator.email ?? "—"}</td>
                  <td className="px-3 py-2 capitalize">{collaborator.status}</td>
                  <td className="px-3 py-2 text-right">
                    <Link
                      to={`/collaborators/${collaborator.id}/edit`}
                      className="mr-2 text-indigo-300 hover:text-indigo-100"
                    >
                      Éditer
                    </Link>
                    <button
                      className="text-red-300 hover:text-red-100"
                      onClick={() => onDelete(collaborator.id)}
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

export function CollaboratorCreatePage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Créer un collaborateur</h2>
      <CollaboratorForm mode="create" />
    </div>
  );
}

export function CollaboratorEditPage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Mettre à jour le collaborateur</h2>
      <CollaboratorForm mode="edit" />
    </div>
  );
}
