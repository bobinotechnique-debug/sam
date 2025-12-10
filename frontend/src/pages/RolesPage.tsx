import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { createRole, deleteRole, getRole, listRoles, updateRole } from "../api/entities";
import { PaginatedResponse, Role, RolePayload } from "../api/types";

interface RoleFormState {
  organization_id: number | "";
  name: string;
  description: string;
  tags: string;
}

function RoleForm({ mode }: { mode: "create" | "edit" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const [form, setForm] = useState<RoleFormState>({
    organization_id: "",
    name: "",
    description: "",
    tags: "",
  });
  const [loading, setLoading] = useState(mode === "edit");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (mode === "edit" && id) {
      getRole(Number(id))
        .then((role) =>
          setForm({
            organization_id: role.organization_id,
            name: role.name,
            description: role.description ?? "",
            tags: role.tags.join(", "),
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

    const payload: RolePayload = {
      organization_id: Number(form.organization_id),
      name: form.name,
      description: form.description || null,
      tags:
        form.tags
          .split(",")
          .map((tag) => tag.trim())
          .filter((tag) => tag.length > 0) || [],
    };

    try {
      if (mode === "create") {
        await createRole(payload);
      } else if (id) {
        await updateRole(Number(id), payload);
      }
      navigate("/roles");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-sm text-slate-300">Chargement du rôle...</p>;
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
            onChange={(e) =>
              setForm({ ...form, organization_id: e.target.value === "" ? "" : Number(e.target.value) })
            }
            required
            min={1}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Nom du rôle
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.name}
            onChange={(e) => setForm({ ...form, name: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200 md:col-span-2">
          Description (optionnel)
          <textarea
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.description}
            onChange={(e) => setForm({ ...form, description: e.target.value })}
            rows={3}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200 md:col-span-2">
          Tags (séparés par des virgules)
          <input
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.tags}
            onChange={(e) => setForm({ ...form, tags: e.target.value })}
            placeholder="ex: caisse, barista, sécurité"
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
          to="/roles"
          className="rounded border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-slate-800"
        >
          Annuler
        </Link>
      </div>
    </form>
  );
}

export function RolesPage() {
  const [data, setData] = useState<PaginatedResponse<Role> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await listRoles();
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
    if (!confirm("Supprimer ce rôle ?")) return;
    try {
      await deleteRole(id);
      setMessage("Rôle supprimé");
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const filtered = data?.items.filter((item) => {
    const search = filter.trim().toLowerCase();
    return (
      item.name.toLowerCase().includes(search) ||
      item.tags.some((tag) => tag.toLowerCase().includes(search)) ||
      item.id.toString() === search
    );
  });

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Rôles / Compétences</h2>
          <p className="text-sm text-slate-300">Référentiel des rôles requis par les missions et les collaborateurs.</p>
        </div>
        <Link
          to="/roles/new"
          className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          Nouveau rôle
        </Link>
      </div>
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <input
          placeholder="Filtrer par nom, tag ou ID exact"
          className="w-full rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white md:w-80"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        {message && <p className="text-sm text-green-300">{message}</p>}
      </div>
      {loading && <p className="text-sm text-slate-300">Chargement...</p>}
      {error && <p className="rounded bg-red-900/30 px-3 py-2 text-red-200">{error}</p>}
      {!loading && !error && filtered && filtered.length === 0 && (
        <p className="text-sm text-slate-300">Aucun rôle disponible.</p>
      )}
      {!loading && !error && filtered && filtered.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-800 text-sm">
            <thead className="bg-slate-900/60">
              <tr>
                <th className="px-3 py-2 text-left font-semibold">ID</th>
                <th className="px-3 py-2 text-left font-semibold">Organisation</th>
                <th className="px-3 py-2 text-left font-semibold">Nom</th>
                <th className="px-3 py-2 text-left font-semibold">Tags</th>
                <th className="px-3 py-2 text-left font-semibold">Description</th>
                <th className="px-3 py-2 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filtered.map((role) => (
                <tr key={role.id} className="hover:bg-slate-800/50">
                  <td className="px-3 py-2">{role.id}</td>
                  <td className="px-3 py-2">{role.organization_id}</td>
                  <td className="px-3 py-2">{role.name}</td>
                  <td className="px-3 py-2">{role.tags.length ? role.tags.join(", ") : "—"}</td>
                  <td className="px-3 py-2">{role.description ?? "—"}</td>
                  <td className="px-3 py-2 text-right">
                    <Link to={`/roles/${role.id}/edit`} className="mr-2 text-indigo-300 hover:text-indigo-100">
                      Éditer
                    </Link>
                    <button className="text-red-300 hover:text-red-100" onClick={() => onDelete(role.id)}>
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

export function RoleCreatePage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Créer un rôle</h2>
      <RoleForm mode="create" />
    </div>
  );
}

export function RoleEditPage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Mettre à jour le rôle</h2>
      <RoleForm mode="edit" />
    </div>
  );
}
