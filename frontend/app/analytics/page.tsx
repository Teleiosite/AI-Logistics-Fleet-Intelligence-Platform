"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { BarChart3, Binary, Clock, Truck } from "lucide-react";
import { fetchShipmentMetrics, ShipmentMetrics } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const DEFAULT_METRICS: ShipmentMetrics = {
  total_shipments: 0,
  active_shipments: 0,
  delayed_shipments: 0,
  delivered_shipments: 0,
};

export default function AnalyticsPage() {
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
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Business Intelligence</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Advanced analytics, forecasting, and operational KPIs</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-card rounded-3xl p-12 flex flex-col items-center justify-center text-center space-y-6 min-h-[400px]">
            <div className="w-20 h-20 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20 animate-pulse">
              <BarChart3 className="w-10 h-10 text-gold-500" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-white mb-2 italic text-gold-500">Live Operations Snapshot</h3>
              <p className="text-sm text-white/30 max-w-sm mx-auto">Total: {metrics.total_shipments} · Delivered: {metrics.delivered_shipments} · Active: {metrics.active_shipments}</p>
            </div>
          </div>

          <div className="glass-card rounded-3xl p-12 flex flex-col items-center justify-center text-center space-y-6 min-h-[400px]">
            <div className="w-20 h-20 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20">
              <Binary className="w-10 h-10 text-gold-500/50" />
            </div>
            <div className="space-y-2">
              <h3 className="text-2xl font-bold text-white mb-2 italic">On-Time Performance</h3>
              <p className="text-sm text-white/30 max-w-sm mx-auto">On-time rate: {onTimeRate}% · Delayed shipments: {metrics.delayed_shipments}</p>
              <div className="flex items-center justify-center gap-4 text-xs text-white/40 uppercase tracking-widest">
                <span className="inline-flex items-center gap-1"><Truck className="w-3 h-3" /> Fleet</span>
                <span className="inline-flex items-center gap-1"><Clock className="w-3 h-3" /> Real-time</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
