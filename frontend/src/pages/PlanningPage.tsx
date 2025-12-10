import { useEffect, useMemo, useState } from "react";

import { listCollaborators, listMissions, listShifts, listSites } from "../api/entities";
import { Collaborator, Mission, Shift, Site } from "../api/types";
import { MissionDetailModal } from "../components/planning/MissionDetailModal";
import { PlanningLane } from "../components/planning/PlanningLane";
import { PlanningToolbar } from "../components/planning/PlanningToolbar";
import {
  PLANNING_END_HOUR,
  PLANNING_START_HOUR,
  getDayRange,
  getWeekDays,
  missionOverlapsRange,
  startOfDay,
  TimeRange,
} from "../utils/planning";

export function PlanningPage() {
  const [mode, setMode] = useState<"day" | "week">("day");
  const [date, setDate] = useState<Date>(startOfDay(new Date()));
  const [missions, setMissions] = useState<Mission[]>([]);
  const [sites, setSites] = useState<Site[]>([]);
  const [collaborators, setCollaborators] = useState<Collaborator[]>([]);
  const [shifts, setShifts] = useState<Shift[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedMission, setSelectedMission] = useState<Mission | null>(null);

  const loadData = async () => {
    setLoading(true);
    setError(null);
    try {
      const [missionsResponse, sitesResponse, collaboratorsResponse, shiftsResponse] = await Promise.all([
        listMissions(),
        listSites(),
        listCollaborators(),
        listShifts(),
      ]);
      setMissions(missionsResponse.items ?? []);
      setSites(sitesResponse.items ?? []);
      setCollaborators(collaboratorsResponse.items ?? []);
      setShifts(shiftsResponse.items ?? []);
    } catch (err) {
      setError((err as Error).message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const assignmentsByMission = useMemo(() => {
    const map: Record<number, string[]> = {};
    const collabMap = Object.fromEntries(collaborators.map((collab) => [collab.id, collab.full_name]));
    shifts.forEach((shift) => {
      const name = collabMap[shift.collaborator_id];
      if (!name) return;
      if (!map[shift.mission_id]) {
        map[shift.mission_id] = [];
      }
      map[shift.mission_id].push(name);
    });
    return map;
  }, [collaborators, shifts]);

  const range: TimeRange = useMemo(() => getDayRange(date), [date]);
  const weekDays = useMemo(() => getWeekDays(date), [date]);

  const filteredMissions = missions.filter((mission) => missionOverlapsRange(mission, range));

  const missionsBySite = useMemo(() => {
    const map: Record<number, Mission[]> = {};
    filteredMissions.forEach((mission) => {
      if (!map[mission.site_id]) {
        map[mission.site_id] = [];
      }
      map[mission.site_id].push(mission);
    });
    return map;
  }, [filteredMissions]);

  const missionsBySiteAndDay = useMemo(() => {
    const map: Record<number, Record<string, Mission[]>> = {};
    weekDays.forEach((day) => {
      const dayRange = getDayRange(day);
      missions.forEach((mission) => {
        if (!missionOverlapsRange(mission, dayRange)) return;
        if (!map[mission.site_id]) map[mission.site_id] = {};
        const key = dayRange.start.toISOString();
        if (!map[mission.site_id][key]) map[mission.site_id][key] = [];
        map[mission.site_id][key].push(mission);
      });
    });
    return map;
  }, [missions, weekDays]);

  const selectedMissionShifts = selectedMission
    ? shifts.filter((shift) => shift.mission_id === selectedMission.id)
    : [];

  return (
    <div className="flex flex-col gap-6">
      <div className="flex flex-col gap-2">
        <p className="text-xs uppercase tracking-[0.3em] text-indigo-400">Phase 4.3</p>
        <h2 className="text-3xl font-semibold text-white">Planning visuel</h2>
        <p className="text-sm text-slate-300">
          Vue jour/semaine, groupée par lieu, avec affectations visibles. Fenêtre horaire configurable {PLANNING_START_HOUR}:00 → {PLANNING_END_HOUR % 24}:00.
        </p>
      </div>

      <PlanningToolbar mode={mode} date={date} onModeChange={setMode} onDateChange={setDate} onRefresh={loadData} />

      {loading && <p className="text-sm text-slate-300">Chargement du planning...</p>}
      {error && <p className="rounded bg-red-900/30 px-3 py-2 text-red-200">{error}</p>}
      {!loading && !error && missions.length === 0 && (
        <p className="rounded border border-slate-800 bg-slate-950/60 px-3 py-2 text-sm text-slate-300">
          Aucune mission à afficher pour l'instant. Créez des missions puis affectez-les à des collaborateurs.
        </p>
      )}

      {!loading && !error && missions.length > 0 && (
        <div className="space-y-8">
          {mode === "day" && (
            <div className="space-y-6">
              {sites.map((site) => (
                <PlanningLane
                  key={site.id}
                  label={site.name}
                  missions={missionsBySite[site.id] || []}
                  assignmentsByMission={assignmentsByMission}
                  range={range}
                  onSelect={setSelectedMission}
                />
              ))}
            </div>
          )}

          {mode === "week" && (
            <div className="space-y-6">
              {sites.map((site) => (
                <div key={site.id} className="rounded-xl border border-slate-800 bg-slate-900/40 p-4">
                  <div className="mb-3 flex items-center justify-between">
                    <div>
                      <p className="text-xs uppercase tracking-[0.25em] text-indigo-300">Lieu</p>
                      <h3 className="text-lg font-semibold text-white">{site.name}</h3>
                    </div>
                    <span className="text-xs text-slate-400">Fenêtre horaire {PLANNING_START_HOUR}:00 → {PLANNING_END_HOUR % 24}:00</span>
                  </div>
                  <div className="space-y-4">
                    {weekDays.map((day) => {
                      const dayRange = getDayRange(day);
                      const key = dayRange.start.toISOString();
                      const list = missionsBySiteAndDay[site.id]?.[key] || [];
                      return (
                        <div key={key} className="rounded-lg border border-slate-800 bg-slate-950/40 p-3">
                          <div className="mb-2 flex items-center justify-between">
                            <p className="text-sm font-semibold text-slate-100">
                              {day.toLocaleDateString(undefined, { weekday: "short", day: "2-digit", month: "short" })}
                            </p>
                            <span className="text-xs text-slate-400">{list.length} mission(s)</span>
                          </div>
                          <PlanningLane
                            label="Heures"
                            missions={list}
                            assignmentsByMission={assignmentsByMission}
                            range={dayRange}
                            onSelect={setSelectedMission}
                          />
                        </div>
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      )}

      {selectedMission && (
        <MissionDetailModal
          mission={selectedMission}
          sites={sites}
          collaborators={collaborators}
          shifts={selectedMissionShifts}
          onClose={() => setSelectedMission(null)}
          onSaved={() => {
            setSelectedMission(null);
            loadData();
          }}
        />
      )}
    </div>
  );
}
