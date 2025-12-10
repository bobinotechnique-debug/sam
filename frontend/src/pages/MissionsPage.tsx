import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";

import { createMission, deleteMission, getMission, listMissions, updateMission } from "../api/entities";
import { Mission, MissionPayload, PaginatedResponse } from "../api/types";
import { formatDateTime, toDateTimeLocalValue, toUtcISOString } from "../utils/datetime";

interface MissionFormState {
  site_id: number | "";
  role_id: number | "";
  status: string;
  start_local: string;
  end_local: string;
  budget_target: number | "";
  note: string;
}

function MissionForm({ mode }: { mode: "create" | "edit" }) {
  const { id } = useParams();
  const navigate = useNavigate();
  const now = new Date();
  const [form, setForm] = useState<MissionFormState>({
    site_id: "",
    role_id: "",
    status: "draft",
    start_local: toDateTimeLocalValue(now),
    end_local: toDateTimeLocalValue(new Date(now.getTime() + 60 * 60 * 1000)),
    budget_target: "",
    note: "",
  });
  const [loading, setLoading] = useState(mode === "edit");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (mode === "edit" && id) {
      getMission(Number(id))
        .then((mission) =>
          setForm({
            site_id: mission.site_id,
            role_id: mission.role_id,
            status: mission.status,
            start_local: toDateTimeLocalValue(mission.start_utc),
            end_local: toDateTimeLocalValue(mission.end_utc),
            budget_target: mission.budget_target ?? "",
            note: mission.note ?? "",
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

    const payload: MissionPayload = {
      site_id: Number(form.site_id),
      role_id: Number(form.role_id),
      status: form.status,
      start_utc: toUtcISOString(form.start_local),
      end_utc: toUtcISOString(form.end_local),
      budget_target: form.budget_target === "" ? null : Number(form.budget_target),
      note: form.note || null,
    };

    try {
      if (mode === "create") {
        await createMission(payload);
      } else if (id) {
        await updateMission(Number(id), payload);
      }
      navigate("/missions");
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  if (loading) {
    return <p className="text-sm text-slate-300">Chargement de la mission...</p>;
  }

  return (
    <form className="flex flex-col gap-4" onSubmit={handleSubmit}>
      {error && <p className="rounded bg-red-900/40 px-3 py-2 text-red-200">{error}</p>}
      <div className="grid gap-4 md:grid-cols-2">
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Site ID
          <input
            type="number"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.site_id}
            onChange={(e) => setForm({ ...form, site_id: e.target.value === "" ? "" : Number(e.target.value) })}
            required
            min={1}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Rôle ID
          <input
            type="number"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.role_id}
            onChange={(e) => setForm({ ...form, role_id: e.target.value === "" ? "" : Number(e.target.value) })}
            required
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
            <option value="draft">Brouillon</option>
            <option value="published">Publiée</option>
            <option value="cancelled">Annulée</option>
          </select>
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Budget cible (optionnel)
          <input
            type="number"
            min={0}
            step="0.01"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.budget_target}
            onChange={(e) => setForm({ ...form, budget_target: e.target.value === "" ? "" : Number(e.target.value) })}
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Début (UTC)
          <input
            type="datetime-local"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.start_local}
            onChange={(e) => setForm({ ...form, start_local: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200">
          Fin (UTC)
          <input
            type="datetime-local"
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.end_local}
            onChange={(e) => setForm({ ...form, end_local: e.target.value })}
            required
          />
        </label>
        <label className="flex flex-col gap-1 text-sm text-slate-200 md:col-span-2">
          Note (optionnel)
          <textarea
            className="rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white"
            value={form.note}
            onChange={(e) => setForm({ ...form, note: e.target.value })}
            rows={3}
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
          to="/missions"
          className="rounded border border-slate-700 px-4 py-2 text-sm font-semibold text-slate-200 hover:bg-slate-800"
        >
          Annuler
        </Link>
      </div>
    </form>
  );
}

export function MissionsPage() {
  const [data, setData] = useState<PaginatedResponse<Mission> | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [message, setMessage] = useState<string | null>(null);
  const [filter, setFilter] = useState("");

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await listMissions();
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
    if (!confirm("Supprimer cette mission ?")) return;
    try {
      await deleteMission(id);
      setMessage("Mission supprimée");
      await load();
    } catch (err) {
      setError((err as Error).message);
    }
  };

  const filtered = data?.items.filter((item) =>
    item.status.toLowerCase().includes(filter.trim().toLowerCase()) ||
    item.note?.toLowerCase().includes(filter.trim().toLowerCase()) ||
    item.id.toString() === filter.trim(),
  );

  return (
    <div className="flex flex-col gap-4">
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <div>
          <h2 className="text-2xl font-semibold">Missions</h2>
          <p className="text-sm text-slate-300">Création et suivi des missions (pas encore de planning visuel).</p>
        </div>
        <Link
          to="/missions/new"
          className="rounded bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-500"
        >
          Nouvelle mission
        </Link>
      </div>
      <div className="flex flex-col gap-2 md:flex-row md:items-center md:justify-between">
        <input
          placeholder="Filtrer par statut, note ou ID exact"
          className="w-full rounded border border-slate-700 bg-slate-900 px-3 py-2 text-white md:w-80"
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
        />
        {message && <p className="text-sm text-green-300">{message}</p>}
      </div>
      {loading && <p className="text-sm text-slate-300">Chargement...</p>}
      {error && <p className="rounded bg-red-900/30 px-3 py-2 text-red-200">{error}</p>}
      {!loading && !error && filtered && filtered.length === 0 && (
        <p className="text-sm text-slate-300">Aucune mission disponible.</p>
      )}
      {!loading && !error && filtered && filtered.length > 0 && (
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-slate-800 text-sm">
            <thead className="bg-slate-900/60">
              <tr>
                <th className="px-3 py-2 text-left font-semibold">ID</th>
                <th className="px-3 py-2 text-left font-semibold">Site</th>
                <th className="px-3 py-2 text-left font-semibold">Rôle</th>
                <th className="px-3 py-2 text-left font-semibold">Statut</th>
                <th className="px-3 py-2 text-left font-semibold">Début</th>
                <th className="px-3 py-2 text-left font-semibold">Fin</th>
                <th className="px-3 py-2 text-left font-semibold">Budget</th>
                <th className="px-3 py-2 text-left font-semibold">Note</th>
                <th className="px-3 py-2 text-right font-semibold">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {filtered.map((mission) => (
                <tr key={mission.id} className="hover:bg-slate-800/50">
                  <td className="px-3 py-2">{mission.id}</td>
                  <td className="px-3 py-2">{mission.site_id}</td>
                  <td className="px-3 py-2">{mission.role_id}</td>
                  <td className="px-3 py-2 capitalize">{mission.status}</td>
                  <td className="px-3 py-2">{formatDateTime(mission.start_utc)}</td>
                  <td className="px-3 py-2">{formatDateTime(mission.end_utc)}</td>
                  <td className="px-3 py-2">{mission.budget_target ?? "—"}</td>
                  <td className="px-3 py-2">{mission.note ?? "—"}</td>
                  <td className="px-3 py-2 text-right">
                    <Link to={`/missions/${mission.id}/edit`} className="mr-2 text-indigo-300 hover:text-indigo-100">
                      Éditer
                    </Link>
                    <button className="text-red-300 hover:text-red-100" onClick={() => onDelete(mission.id)}>
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

export function MissionCreatePage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Créer une mission</h2>
      <MissionForm mode="create" />
    </div>
  );
}

export function MissionEditPage() {
  return (
    <div className="flex flex-col gap-4">
      <h2 className="text-2xl font-semibold">Mettre à jour la mission</h2>
      <MissionForm mode="edit" />
    </div>
  );
}
