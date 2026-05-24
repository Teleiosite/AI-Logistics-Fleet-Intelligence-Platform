"use client";

import { useEffect, useMemo, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { Fuel, AlertTriangle, Droplets, CreditCard } from "lucide-react";
import { fetchFuelLogs, FuelLog } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

export default function FuelPage() {
  const [fuelLogs, setFuelLogs] = useState<FuelLog[]>([]);
  const token = useRequireAuth();

  useEffect(() => {
    if (!token) return;
    fetchFuelLogs(token).then(setFuelLogs).catch(() => undefined);
  }, [token]);

  const stats = useMemo(() => {
    const totalVolume = fuelLogs.reduce((acc, item) => acc + Number(item.quantity_liters || 0), 0);
    const aggregateCost = fuelLogs.reduce((acc, item) => acc + Number(item.total_cost || 0), 0);
    const anomalies = fuelLogs.filter((item) => item.is_anomaly).length;
    return { totalVolume, aggregateCost, anomalies };
  }, [fuelLogs]);

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Consumption Intelligence</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Advanced monitoring of fuel issuance and anomaly detection</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900"><div className="flex items-center gap-3 mb-2 text-gold-500"><Droplets className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Total Volume</span></div><p className="text-3xl font-bold text-white tabular-nums">{stats.totalVolume.toFixed(2)} <span className="text-xs text-white/30 tracking-tight">Liters</span></p></div>
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900"><div className="flex items-center gap-3 mb-2 text-gold-500"><CreditCard className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Aggregate Cost</span></div><p className="text-3xl font-bold text-white tabular-nums">₦{stats.aggregateCost.toLocaleString()} <span className="text-xs text-white/30 tracking-tight">NGN</span></p></div>
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-destructive/10 border-destructive/20 animate-pulse"><div className="flex items-center gap-3 mb-2 text-destructive"><AlertTriangle className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Critical Anomalies</span></div><p className="text-3xl font-bold text-white tabular-nums">{stats.anomalies} <span className="text-xs text-white/30 tracking-tight">Detected</span></p></div>
        </div>

        <section className="space-y-8">
          <LuxuryTable title="Fuel Issuance Ledger" data={fuelLogs} columns={[
            { header: "Audit ID", accessor: (item) => <div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20"><Fuel className="w-4 h-4 text-gold-500" /></div><span className="font-mono text-white/40 text-[10px]">{item.id}</span></div> },
            { header: "Vehicle ID", accessor: "vehicle_id", className: "font-mono font-bold text-gold-500" },
            { header: "Volume / Amount", accessor: (item) => <div className="flex flex-col"><span className="text-white font-bold">{item.quantity_liters} L</span><span className="text-[10px] text-white/30 font-mono tracking-tighter">₦{Number(item.total_cost).toLocaleString()}</span></div> },
            { header: "Anomaly Guard", accessor: (item) => item.is_anomaly ? <span className="text-[10px] font-bold text-destructive uppercase tracking-tighter max-w-[150px] truncate">{item.anomaly_reason || "Anomaly"}</span> : <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-500/60">Validated</span> },
            { header: "Timestamp", accessor: (item) => new Date(item.created_at).toLocaleString(), className: "text-right tabular-nums text-white/50 text-xs" },
          ]} />
        </section>
      </div>
    </DashboardLayout>
  );
}
