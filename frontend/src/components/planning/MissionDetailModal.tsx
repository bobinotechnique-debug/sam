import { useEffect, useState } from "react";

import {
  Collaborator,
  Mission,
  MissionPayload,
  Shift,
  Site,
} from "../../api/types";
import { createShift, deleteShift, updateMission, updateShift } from "../../api/entities";
import { toDateTimeLocalValue, toUtcISOString } from "../../utils/datetime";

interface MissionDetailModalProps {
  mission: Mission;
  sites: Site[];
  collaborators: Collaborator[];
  shifts: Shift[];
  onClose: () => void;
  onSaved: () => void;
}

export function MissionDetailModal({ mission, sites, collaborators, shifts, onClose, onSaved }: MissionDetailModalProps) {
  const [siteId, setSiteId] = useState<number>(mission.site_id);
  const [startLocal, setStartLocal] = useState<string>(toDateTimeLocalValue(mission.start_utc));
  const [endLocal, setEndLocal] = useState<string>(toDateTimeLocalValue(mission.end_utc));
  const [selectedCollaborators, setSelectedCollaborators] = useState<Set<number>>(new Set(shifts.map((shift) => shift.collaborator_id)));
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setSiteId(mission.site_id);
    setStartLocal(toDateTimeLocalValue(mission.start_utc));
    setEndLocal(toDateTimeLocalValue(mission.end_utc));
    setSelectedCollaborators(new Set(shifts.map((shift) => shift.collaborator_id)));
  }, [mission, shifts]);

  const toggleCollaborator = (id: number) => {
    setSelectedCollaborators((prev) => {
      const next = new Set(prev);
      if (next.has(id)) {
        next.delete(id);
      } else {
        next.add(id);
      }
      return next;
    });
  };

  const handleSave = async (event: React.FormEvent) => {
    event.preventDefault();
    setSaving(true);
    setError(null);

    const payload: Partial<MissionPayload> = {
      site_id: siteId,
      start_utc: toUtcISOString(startLocal),
      end_utc: toUtcISOString(endLocal),
    };

    try {
      await updateMission(mission.id, payload);
      const currentIds = Array.from(selectedCollaborators);
      const existingIds = shifts.map((shift) => shift.collaborator_id);
      const toCreate = currentIds.filter((id) => !existingIds.includes(id));
      const toDelete = shifts.filter((shift) => !selectedCollaborators.has(shift.collaborator_id));
      const toUpdate = shifts.filter(
        (shift) =>
          selectedCollaborators.has(shift.collaborator_id) &&
          (shift.start_utc !== payload.start_utc || shift.end_utc !== payload.end_utc),
      );

      const missionStart = payload.start_utc as string;
      const missionEnd = payload.end_utc as string;

      await Promise.all([
        ...toCreate.map((collaboratorId) =>
          createShift({
            mission_id: mission.id,
            collaborator_id: collaboratorId,
            start_utc: missionStart,
            end_utc: missionEnd,
            status: "draft",
          }),
        ),
        ...toUpdate.map((shift) => updateShift(shift.id, { start_utc: missionStart, end_utc: missionEnd })),
        ...toDelete.map((shift) => deleteShift(shift.id)),
      ]);

      onSaved();
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/80 p-4">
      <div className="w-full max-w-2xl rounded-xl border border-slate-800 bg-slate-900 p-6 shadow-2xl">
        <div className="flex items-start justify-between">
          <div>
            <p className="text-xs uppercase tracking-[0.2em] text-indigo-300">Mission #{mission.id}</p>
            <h3 className="text-2xl font-semibold text-white">Détails et affectations</h3>
            <p className="text-sm text-slate-300">Mettre à jour l'horaire, le lieu et les collaborateurs assignés.</p>
          </div>
          <button
            className="rounded bg-slate-800 px-3 py-1 text-sm font-semibold text-slate-100 hover:bg-slate-700"
            onClick={onClose}
          >
            Fermer
          </button>
        </div>
        <form className="mt-4 space-y-4" onSubmit={handleSave}>
          {error && <p className="rounded bg-red-900/40 px-3 py-2 text-sm text-red-100">{error}</p>}
          <div className="grid gap-4 md:grid-cols-2">
            <label className="flex flex-col gap-2 text-sm text-slate-200">
              Lieu
              <select
                className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                value={siteId}
                onChange={(e) => setSiteId(Number(e.target.value))}
              >
                {sites.map((site) => (
                  <option key={site.id} value={site.id}>
                    {site.name} (#{site.id})
                  </option>
                ))}
              </select>
            </label>
            <div className="flex flex-col gap-2 text-sm text-slate-200">
              Statut
              <span className="rounded border border-slate-700 bg-slate-950 px-3 py-2 capitalize text-slate-100">{mission.status}</span>
            </div>
            <label className="flex flex-col gap-2 text-sm text-slate-200">
              Début (UTC)
              <input
                type="datetime-local"
                className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                value={startLocal}
                onChange={(e) => setStartLocal(e.target.value)}
                required
              />
            </label>
            <label className="flex flex-col gap-2 text-sm text-slate-200">
              Fin (UTC)
              <input
                type="datetime-local"
                className="rounded border border-slate-700 bg-slate-950 px-3 py-2 text-white"
                value={endLocal}
                onChange={(e) => setEndLocal(e.target.value)}
                required
              />
            </label>
          </div>
          <div className="rounded-lg border border-slate-800 bg-slate-950/60 p-4">
            <div className="mb-2 flex items-center justify-between">
              <p className="text-sm font-semibold text-slate-100">Collaborateurs affectés</p>
              <span className="text-xs text-slate-400">{selectedCollaborators.size} sélectionné(s)</span>
            </div>
            <div className="grid gap-2 md:grid-cols-2">
              {collaborators.map((collaborator) => (
                <label key={collaborator.id} className="flex items-center gap-2 text-sm text-slate-100">
                  <input
                    type="checkbox"
                    className="h-4 w-4 rounded border-slate-700 bg-slate-900"
                    checked={selectedCollaborators.has(collaborator.id)}
                    onChange={() => toggleCollaborator(collaborator.id)}
                  />
                  <span>{collaborator.full_name}</span>
                </label>
              ))}
            </div>
          </div>
          <div className="flex items-center justify-between border-t border-slate-800 pt-4 text-xs text-slate-400">
            <p>Les heures sont stockées en UTC. Les affectations sont alignées sur la mission.</p>
            <div className="flex gap-2">
              <button
                type="button"
                className="rounded border border-slate-700 px-4 py-2 font-semibold text-slate-100 hover:bg-slate-800"
                onClick={onClose}
              >
                Annuler
              </button>
              <button
                type="submit"
                className="rounded bg-indigo-600 px-4 py-2 font-semibold text-white hover:bg-indigo-500 disabled:opacity-60"
                disabled={saving}
              >
                {saving ? "Enregistrement..." : "Enregistrer"}
              </button>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
