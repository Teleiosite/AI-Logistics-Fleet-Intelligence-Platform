"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { fetchLatestLocations, LocationPing } from "../../lib/api";
import { getToken } from "../../lib/auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

export default function MapPage() {
  const [locations, setLocations] = useState<LocationPing[]>([]);
  const [streamStatus, setStreamStatus] = useState("connecting");

  useEffect(() => {
    const token = getToken();
    if (!token) return;
    fetchLatestLocations(token).then(setLocations).catch(() => setStreamStatus("unavailable"));
    const controller = new AbortController();
    fetch(`${API_BASE_URL}/geofences/events/stream`, {
      headers: { Authorization: "Bearer " + token },
      signal: controller.signal,
    }).then(async (response) => {
      if (!response.ok || !response.body) throw new Error("stream unavailable");
      setStreamStatus("live");
      const reader = response.body.getReader();
      const decoder = new TextDecoder();
      while (!controller.signal.aborted) {
        const { done } = await reader.read();
        if (done) break;
        await fetchLatestLocations(token).then(setLocations);
        decoder.decode(); // Consume the SSE chunk and refresh the snapshot.
      }
    }).catch(() => {
      if (!controller.signal.aborted) setStreamStatus("reconnecting");
    });
    return () => controller.abort();
  }, []);

  return (
    <DashboardLayout>
      <div className="flex min-h-[calc(100vh-160px)] flex-col gap-6">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Live Geospatial Intelligence</h1>
          <p className="mt-1 text-sm text-muted-foreground">Latest tenant-scoped telemetry and geofence stream.</p>
        </div>
        <div className="grid flex-1 gap-4 rounded-3xl border border-white/5 bg-white/[0.02] p-6 md:grid-cols-2">
          {locations.length === 0 ? (
            <p className="text-sm text-white/50">No telemetry points available.</p>
          ) : locations.map((location) => (
            <article key={location.id} className="rounded-2xl border border-white/10 bg-black/20 p-4">
              <div className="flex justify-between">
                <strong className="text-white">{location.vehicle_id}</strong>
                <span className="text-xs text-emerald-400">{streamStatus}</span>
              </div>
              <p className="mt-3 font-mono text-sm text-white/70">
                {Number(location.latitude).toFixed(5)}, {Number(location.longitude).toFixed(5)}
              </p>
              <p className="mt-1 text-xs text-white/40">
                {location.speed_kph ?? 0} km/h · {new Date(location.recorded_at).toLocaleString()}
              </p>
            </article>
          ))}
        </div>
      </div>
    </DashboardLayout>
  );
}
