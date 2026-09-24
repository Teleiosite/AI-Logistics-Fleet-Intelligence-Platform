"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
  Legend,
} from "recharts";
import { BarChart3, Fuel, Truck, AlertTriangle, Clock, TrendingUp } from "lucide-react";
import {
  fetchShipmentMetrics,
  fetchShipmentTrend,
  fetchFuelMetrics,
  fetchFleetMetrics,
  fetchDVRMetrics,
  ShipmentMetrics,
  ShipmentTrendPoint,
  FuelMetrics,
  FleetMetrics,
  DVRMetrics,
} from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const CHART_COLORS = ["#d4a017", "#f59e0b", "#ef4444", "#10b981"];

const DEFAULT_SHIPMENT_METRICS: ShipmentMetrics = {
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

export default function AnalyticsPage() {
  const [metrics, setMetrics] = useState<ShipmentMetrics>(DEFAULT_SHIPMENT_METRICS);
  const [trend, setTrend] = useState<ShipmentTrendPoint[]>([]);
  const [fuelMetrics, setFuelMetrics] = useState<FuelMetrics | null>(null);
  const [fleetMetrics, setFleetMetrics] = useState<FleetMetrics | null>(null);
  const [dvrMetrics, setDvrMetrics] = useState<DVRMetrics | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const token = useRequireAuth();

  useEffect(() => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    Promise.allSettled([
      fetchShipmentMetrics(token).then(setMetrics),
      fetchShipmentTrend(token).then(setTrend),
      fetchFuelMetrics(token).then(setFuelMetrics),
      fetchFleetMetrics(token).then(setFleetMetrics),
      fetchDVRMetrics(token).then(setDvrMetrics),
    ])
      .then((results) => {
        const failed = results.some((r) => r.status === "rejected");
        if (failed) setError("Some data could not be loaded.");
      })
      .finally(() => setIsLoading(false));
  }, [token]);

  const onTimeRate = metrics.total_shipments
    ? (((metrics.total_shipments - metrics.delayed_shipments) / metrics.total_shipments) * 100).toFixed(1)
    : "0.0";

  const statusPieData = [
    { name: "Delivered", value: metrics.delivered_shipments },
    { name: "Active", value: metrics.active_shipments },
    { name: "Delayed", value: metrics.delayed_shipments },
    { name: "Other", value: Math.max(0, metrics.total_shipments - metrics.delivered_shipments - metrics.active_shipments - metrics.delayed_shipments) },
  ].filter((d) => d.value > 0);

  return (
    <DashboardLayout>
      <div className="space-y-10">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Business Intelligence</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">
            Advanced analytics, forecasting, and operational KPIs
          </p>
        </div>

        {isLoading && <p className="text-xs text-white/40">Refreshing intelligence data...</p>}
        {error && <p className="text-xs text-amber-400">{error}</p>}

        {/* Top KPI row */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { label: "Total Shipments", value: metrics.total_shipments, icon: Truck, color: "text-gold-400" },
            { label: "On-Time Rate", value: `${onTimeRate}%`, icon: Clock, color: "text-emerald-400" },
            { label: "Active Fleet", value: fleetMetrics?.active_vehicles ?? "—", icon: Truck, color: "text-blue-400" },
            { label: "DVR Open", value: dvrMetrics?.open ?? "—", icon: AlertTriangle, color: "text-destructive" },
          ].map((kpi) => (
            <div key={kpi.label} className="glass-card p-5 rounded-2xl border border-white/5">
              <div className="flex items-center gap-2 mb-2">
                <kpi.icon className={`w-4 h-4 ${kpi.color}`} />
                <span className="text-[10px] uppercase font-bold tracking-widest text-white/30">{kpi.label}</span>
              </div>
              <p className={`text-3xl font-bold tabular-nums ${kpi.color}`}>{kpi.value}</p>
            </div>
          ))}
        </div>

        {/* Charts row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* 7-day trend */}
          <div className="lg:col-span-2 glass-card rounded-3xl p-6 border border-white/5">
            <div className="flex items-center gap-2 mb-6">
              <TrendingUp className="w-4 h-4 text-gold-500" />
              <h3 className="text-sm font-bold text-white uppercase tracking-widest">7-Day Shipment Volume</h3>
            </div>
            {trend.length > 0 ? (
              <ResponsiveContainer width="100%" height={220}>
                <BarChart data={trend} margin={{ top: 0, right: 0, left: -20, bottom: 0 }}>
                  <XAxis
                    dataKey="date"
                    tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 10 }}
                    tickFormatter={(v) => v.slice(5)}
                    axisLine={false}
                    tickLine={false}
                  />
                  <YAxis tick={{ fill: "rgba(255,255,255,0.3)", fontSize: 10 }} axisLine={false} tickLine={false} allowDecimals={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Bar dataKey="count" fill="#d4a017" radius={[4, 4, 0, 0]} />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[220px] flex items-center justify-center">
                <div className="text-center">
                  <BarChart3 className="w-10 h-10 text-gold-500/20 mx-auto mb-2" />
                  <p className="text-xs text-white/20 uppercase tracking-widest">No trend data yet</p>
                </div>
              </div>
            )}
          </div>

          {/* Status distribution pie */}
          <div className="glass-card rounded-3xl p-6 border border-white/5">
            <div className="flex items-center gap-2 mb-6">
              <BarChart3 className="w-4 h-4 text-gold-500" />
              <h3 className="text-sm font-bold text-white uppercase tracking-widest">Status Mix</h3>
            </div>
            {statusPieData.length > 0 ? (
              <ResponsiveContainer width="100%" height={220}>
                <PieChart>
                  <Pie data={statusPieData} cx="50%" cy="45%" outerRadius={75} dataKey="value" labelLine={false}>
                    {statusPieData.map((_, index) => (
                      <Cell key={index} fill={CHART_COLORS[index % CHART_COLORS.length]} />
                    ))}
                  </Pie>
                  <Legend wrapperStyle={{ fontSize: 10, color: "rgba(255,255,255,0.4)" }} />
                  <Tooltip
                    contentStyle={{ background: "#18181b", border: "1px solid rgba(255,255,255,0.1)", borderRadius: 12, fontSize: 12 }}
                    itemStyle={{ color: "#fff" }}
                  />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-[220px] flex items-center justify-center">
                <p className="text-xs text-white/20 uppercase tracking-widest">No shipment data</p>
              </div>
            )}
          </div>
        </div>

        {/* Fuel + Fleet + DVR metrics row */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Fuel metrics */}
          <div className="glass-card rounded-3xl p-6 border border-white/5 space-y-4">
            <div className="flex items-center gap-2">
              <Fuel className="w-4 h-4 text-gold-500" />
              <h3 className="text-sm font-bold text-white uppercase tracking-widest">Fuel Intelligence</h3>
            </div>
            {fuelMetrics ? (
              <div className="space-y-3">
                {[
                  { label: "Total Volume", value: `${fuelMetrics.total_volume_liters.toLocaleString()} L` },
                  { label: "Total Cost", value: `₦${fuelMetrics.total_cost.toLocaleString()}` },
                  { label: "Anomalies", value: fuelMetrics.anomaly_count, highlight: fuelMetrics.anomaly_count > 0 },
                  { label: "Avg Efficiency", value: fuelMetrics.avg_efficiency_lkm ? `${fuelMetrics.avg_efficiency_lkm} L/100km` : "N/A" },
                ].map((row) => (
                  <div key={row.label} className="flex justify-between items-center border-b border-white/5 pb-2">
                    <span className="text-xs text-white/30 uppercase tracking-widest">{row.label}</span>
                    <span className={`text-sm font-bold tabular-nums ${row.highlight ? "text-destructive" : "text-white"}`}>{row.value}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-white/20">Loading fuel data...</p>
            )}
          </div>

          {/* Fleet metrics */}
          <div className="glass-card rounded-3xl p-6 border border-white/5 space-y-4">
            <div className="flex items-center gap-2">
              <Truck className="w-4 h-4 text-gold-500" />
              <h3 className="text-sm font-bold text-white uppercase tracking-widest">Fleet Status</h3>
            </div>
            {fleetMetrics ? (
              <div className="space-y-3">
                {[
                  { label: "Total Vehicles", value: fleetMetrics.total_vehicles },
                  { label: "Active", value: fleetMetrics.active_vehicles, color: "text-emerald-400" },
                  { label: "In Maintenance", value: fleetMetrics.maintenance_vehicles, color: fleetMetrics.maintenance_vehicles > 0 ? "text-amber-400" : "text-white" },
                  { label: "Total Drivers", value: fleetMetrics.total_drivers },
                  { label: "Active Drivers", value: fleetMetrics.active_drivers, color: "text-emerald-400" },
                ].map((row) => (
                  <div key={row.label} className="flex justify-between items-center border-b border-white/5 pb-2">
                    <span className="text-xs text-white/30 uppercase tracking-widest">{row.label}</span>
                    <span className={`text-sm font-bold tabular-nums ${row.color ?? "text-white"}`}>{row.value}</span>
                  </div>
                ))}
              </div>
            ) : (
              <p className="text-xs text-white/20">Loading fleet data...</p>
            )}
          </div>

          {/* DVR metrics */}
          <div className="glass-card rounded-3xl p-6 border border-white/5 space-y-4">
            <div className="flex items-center gap-2">
              <AlertTriangle className="w-4 h-4 text-gold-500" />
              <h3 className="text-sm font-bold text-white uppercase tracking-widest">Variance Summary</h3>
            </div>
            {dvrMetrics ? (
              <div className="space-y-3">
                {[
                  { label: "Total DVRs", value: dvrMetrics.total },
                  { label: "Open", value: dvrMetrics.open, color: dvrMetrics.open > 0 ? "text-amber-400" : "text-white" },
                  { label: "Resolved", value: dvrMetrics.resolved, color: "text-emerald-400" },
                ].map((row) => (
                  <div key={row.label} className="flex justify-between items-center border-b border-white/5 pb-2">
                    <span className="text-xs text-white/30 uppercase tracking-widest">{row.label}</span>
                    <span className={`text-sm font-bold tabular-nums ${row.color ?? "text-white"}`}>{row.value}</span>
                  </div>
                ))}
                {dvrMetrics.by_type.length > 0 && (
                  <div className="pt-1">
                    <p className="text-[10px] text-white/20 uppercase tracking-widest mb-2">By Type</p>
                    {dvrMetrics.by_type.map((t) => (
                      <div key={t.type} className="flex justify-between text-[10px] text-white/40 py-0.5">
                        <span>{t.type.replace(/_/g, " ")}</span>
                        <span className="font-bold">{t.count}</span>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            ) : (
              <p className="text-xs text-white/20">Loading DVR data...</p>
            )}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
