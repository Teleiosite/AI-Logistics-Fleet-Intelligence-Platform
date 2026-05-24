"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../components/dashboard/DashboardLayout";
import { KpiCard } from "../components/dashboard/KpiCard";
import { Truck, Clock, Fuel, AlertTriangle, BarChart3, Activity, ArrowUpRight } from "lucide-react";
import { fetchShipmentMetrics, ShipmentMetrics } from "../lib/api";
import { useRequireAuth } from "../lib/requireAuth";

const DEFAULT_METRICS: ShipmentMetrics = {
  total_shipments: 0,
  active_shipments: 0,
  delayed_shipments: 0,
  delivered_shipments: 0,
};

export default function DashboardPage() {
  const [metrics, setMetrics] = useState<ShipmentMetrics>(DEFAULT_METRICS);

  const token = useRequireAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    fetchShipmentMetrics(token).then(setMetrics).catch(() => setError("Unable to load live data.")).finally(() => setIsLoading(false))
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
            <button className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-4 py-2 rounded-xl text-xs font-bold shadow-lg shadow-gold-900/10 hover:shadow-gold-900/20 transition-all flex items-center gap-2 group">
              Export Analysis
              <ArrowUpRight className="w-3 h-3 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>
          </div>
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading live data...</p>}
        {error && <p className="text-xs text-destructive">{error}</p>}

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard title="Active Shipments" value={metrics.active_shipments} icon={Truck} description={`Total shipments: ${metrics.total_shipments}`} />
          <KpiCard title="On-Time Rate" value={`${onTimeRate}%`} icon={Clock} description={`Delayed shipments: ${metrics.delayed_shipments}`} />
          <KpiCard title="Delivered" value={metrics.delivered_shipments} icon={Fuel} description="Completed deliveries" />
          <KpiCard title="Open Exceptions" value={metrics.delayed_shipments} icon={AlertTriangle} className="border-destructive/20" description="Delayed / exception shipments" />
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 glass-card rounded-3xl p-8 min-h-[400px] flex flex-col items-center justify-center text-center space-y-4">
            <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-2">
              <BarChart3 className="w-8 h-8 text-gold-500/30" />
            </div>
            <h3 className="text-xl font-bold text-white/40">Shipment Volume Analysis</h3>
            <p className="text-xs text-white/20 max-w-xs uppercase tracking-widest font-bold">Integrating Intelligence Engine Data...</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
