"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../components/dashboard/DashboardLayout";
import { KpiCard } from "../components/dashboard/KpiCard";
import { Truck, Clock, PackageCheck, AlertTriangle, Activity, ArrowUpRight, TrendingUp } from "lucide-react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import {
  fetchShipmentMetrics,
  fetchShipmentTrend,
  fetchShipments,
  ShipmentMetrics,
  ShipmentTrendPoint,
  Shipment,
} from "../lib/api";
import { useRequireAuth } from "../lib/requireAuth";

const DEFAULT_METRICS: ShipmentMetrics = {
  total_shipments: 0,
  active_shipments: 0,
  delayed_shipments: 0,
  delivered_shipments: 0,
};

const CustomTooltip = ({ active, payload, label }: { active?: boolean; payload?: { value: number }[]; label?: string }) => {
  if (active && payload && payload.length) {
    return (
      <div className="bg-zinc-900 border border-white/10 rounded-xl px-4 py-2 text-xs text-white shadow-xl">
        <p className="font-bold text-gold-400">{label}</p>
        <p className="text-white/70">{payload[0].value} shipments</p>
      </div>
    );
  }
  return null;
};

const STATUS_BADGE: Record<string, string> = {
  draft: "bg-white/5 text-white/30",
  scheduled: "bg-blue-500/10 text-blue-400",
  assigned: "bg-indigo-500/10 text-indigo-400",
  dispatched: "bg-violet-500/10 text-violet-400",
  in_transit: "bg-amber-500/10 text-amber-400",
  delivered: "bg-emerald-500/10 text-emerald-400",
  delayed: "bg-destructive/10 text-destructive",
  exception: "bg-destructive/10 text-destructive",
};

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<ShipmentMetrics>(DEFAULT_METRICS);
  const [trend, setTrend] = useState<ShipmentTrendPoint[]>([]);
  const [recentShipments, setRecentShipments] = useState<Shipment[]>([]);
  const token = useRequireAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    Promise.allSettled([
      fetchShipmentMetrics(token).then(setMetrics),
      fetchShipmentTrend(token).then(setTrend),
      fetchShipments(token).then((s) => setRecentShipments(s.slice(-5).reverse())),
    ])
      .then((results) => {
        if (results.some((r) => r.status === "rejected")) setError("Some data could not be loaded.");
      })
      .finally(() => setIsLoading(false));
  }, [token]);

  const onTimeRate = metrics.total_shipments
    ? (((metrics.total_shipments - metrics.delayed_shipments) / metrics.total_shipments) * 100).toFixed(1)
    : "0.0";

  return (
    <DashboardLayout>
      <div className="space-y-8">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Operational Pulse</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium">Real-time intelligence from your global fleet network</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="bg-white/5 border border-white/10 px-4 py-2 rounded-xl flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-500" />
              <span className="text-xs font-bold text-white tracking-wider uppercase">Live Feed</span>
            </div>
            <button className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-4 py-2 rounded-xl text-xs font-bold shadow-lg hover:opacity-90 transition-opacity flex items-center gap-2 group">
              Export Analysis
              <ArrowUpRight className="w-3 h-3 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>
          </div>
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading live data...</p>}
        {error && <p className="text-xs text-amber-400">{error}</p>}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard title="Active Shipments" value={metrics.active_shipments} icon={Truck} description={`Total: ${metrics.total_shipments}`} />
          <KpiCard title="On-Time Rate" value={`${onTimeRate}%`} icon={Clock} description={`Delayed: ${metrics.delayed_shipments}`} />
          <KpiCard title="Delivered" value={metrics.delivered_shipments} icon={PackageCheck} description="Completed deliveries" />
          <KpiCard title="Open Exceptions" value={metrics.delayed_shipments} icon={AlertTriangle} className="border-destructive/20" description="Delayed / exception shipments" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Trend chart */}
          <div className="lg:col-span-2 glass-card rounded-3xl p-8 min-h-[340px] flex flex-col">
            <div className="flex items-center gap-2 mb-6">
              <TrendingUp className="w-4 h-4 text-gold-500" />
              <h3 className="text-sm font-bold text-white uppercase tracking-widest">7-Day Shipment Volume</h3>
            </div>
            {trend.length > 0 ? (
              <div className="flex-1">
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={trend} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                    <XAxis
                      dataKey="date"
                      tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 10 }}
                      tickFormatter={(v: string) => v.slice(5)}
                      axisLine={false}
                      tickLine={false}
                    />
                    <YAxis
                      tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 10 }}
                      axisLine={false}
                      tickLine={false}
                      allowDecimals={false}
                    />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="count" fill="#d4a017" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            ) : (
              <div className="flex-1 flex flex-col items-center justify-center text-center">
                <BarChart3Icon className="w-10 h-10 text-gold-500/20 mb-3" />
                <p className="text-xs text-white/20 uppercase tracking-widest">No shipment data yet</p>
                <p className="text-[10px] text-white/10 mt-1">Create shipments to see the trend</p>
              </div>
            )}
          </div>

          {/* Recent activity */}
          <div className="glass-card rounded-3xl p-6 flex flex-col">
            <h3 className="text-sm font-bold text-white uppercase tracking-widest mb-5">Recent Activity</h3>
            {recentShipments.length > 0 ? (
              <div className="space-y-3 flex-1">
                {recentShipments.map((s) => (
                  <div key={s.id} className="flex items-start gap-3 border-b border-white/5 pb-3 last:border-0">
                    <div className="w-7 h-7 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20 shrink-0 mt-0.5">
                      <Truck className="w-3 h-3 text-gold-500" />
                    </div>
                    <div className="min-w-0">
                      <p className="text-xs font-bold text-gold-400 font-mono">{s.shipment_number}</p>
                      <p className="text-[10px] text-white/30 truncate">{s.customer_name}</p>
                      <span
                        className={`text-[9px] font-bold uppercase tracking-widest px-1.5 py-0.5 rounded mt-0.5 inline-block ${STATUS_BADGE[s.status] ?? "bg-white/5 text-white/30"}`}
                      >
                        {s.status.replace(/_/g, " ")}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            ) : (
              <div className="flex-1 flex items-center justify-center">
                <p className="text-xs text-white/20 text-center">No recent shipments</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}

// Inline icon to avoid import conflict
function BarChart3Icon({ className }: { className?: string }) {
  return (
    <svg className={className} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth={1.5}>
      <path d="M3 3v18h18" strokeLinecap="round" strokeLinejoin="round" />
      <path d="M7 16V8" strokeLinecap="round" />
      <path d="M12 16V5" strokeLinecap="round" />
      <path d="M17 16v-4" strokeLinecap="round" />
    </svg>
  );
}
