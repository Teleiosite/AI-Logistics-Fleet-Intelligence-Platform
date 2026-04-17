"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { Fuel, AlertTriangle, Droplets, CreditCard } from "lucide-react";
import { cn } from "../../lib/utils";

const fuelLogs = [
  { id: "FL-9001", date: "2026-04-17 08:32", vehicle: "LA-234-FG", driver: "Samuel Okon", quantity: 450, cost: 225000, isAnomaly: true, reason: "Excessive fill: exceeds 110% of tank capacity" },
  { id: "FL-9002", date: "2026-04-17 10:15", vehicle: "LA-912-XY", driver: "Ahmed Bello", quantity: 180, cost: 90000, isAnomaly: false, reason: "" },
  { id: "FL-9003", date: "2026-04-16 14:22", vehicle: "LA-455-AB", driver: "Ikechukwu Mensah", quantity: 510, cost: 255000, isAnomaly: true, reason: "Frequency anomaly: more than 2 fills in 24 hours" },
  { id: "FL-9004", date: "2026-04-16 16:45", vehicle: "LA-112-ZT", driver: "Tunde Olayinka", quantity: 220, cost: 110000, isAnomaly: false, reason: "" },
  { id: "FL-9005", date: "2026-04-15 09:10", vehicle: "LA-778-MM", driver: "Samuel Okon", quantity: 95, cost: 47500, isAnomaly: false, reason: "" },
];

export default function FuelPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Consumption Intelligence</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Advanced monitoring of fuel issuance and anomaly detection</p>
        </div>

        {/* Analytics Summary */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900">
            <div className="flex items-center gap-3 mb-2 text-gold-500">
              <Droplets className="w-5 h-5" />
              <span className="text-xs font-bold uppercase tracking-widest">Total Volume</span>
            </div>
            <p className="text-3xl font-bold text-white tabular-nums">1,455 <span className="text-xs text-white/30 tracking-tight">Liters</span></p>
          </div>
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900">
            <div className="flex items-center gap-3 mb-2 text-gold-500">
              <CreditCard className="w-5 h-5" />
              <span className="text-xs font-bold uppercase tracking-widest">Aggregate Cost</span>
            </div>
            <p className="text-3xl font-bold text-white tabular-nums">₦727,500 <span className="text-xs text-white/30 tracking-tight">NGN</span></p>
          </div>
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-destructive/10 border-destructive/20 animate-pulse">
            <div className="flex items-center gap-3 mb-2 text-destructive">
              <AlertTriangle className="w-5 h-5" />
              <span className="text-xs font-bold uppercase tracking-widest">Critical Anomalies</span>
            </div>
            <p className="text-3xl font-bold text-white tabular-nums">2 <span className="text-xs text-white/30 tracking-tight">Detected</span></p>
          </div>
        </div>

        <section className="space-y-8">
          <LuxuryTable
            title="Fuel Issuance Ledger"
            data={fuelLogs}
            columns={[
              { 
                header: "Audit ID", 
                accessor: (item) => (
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20">
                      <Fuel className="w-4 h-4 text-gold-500" />
                    </div>
                    <span className="font-mono text-white/40 text-[10px]">{item.id}</span>
                  </div>
                )
              },
              { header: "Registry", accessor: "vehicle", className: "font-mono font-bold text-gold-500" },
              { header: "Operator", accessor: "driver" },
              { 
                header: "Volume / Amount", 
                accessor: (item) => (
                  <div className="flex flex-col">
                    <span className="text-white font-bold">{item.quantity} L</span>
                    <span className="text-[10px] text-white/30 font-mono tracking-tighter">₦{item.cost.toLocaleString()}</span>
                  </div>
                )
              },
              { 
                header: "Anomaly Guard", 
                accessor: (item) => (
                  item.isAnomaly ? (
                    <div className="flex items-center gap-2 group relative cursor-help">
                      <AlertTriangle className="w-4 h-4 text-destructive animate-pulse" />
                      <span className="text-[10px] font-bold text-destructive uppercase tracking-tighter max-w-[150px] truncate">{item.reason}</span>
                    </div>
                  ) : (
                    <div className="flex items-center gap-2 text-emerald-500/40">
                      <div className="w-1.5 h-1.5 rounded-full bg-emerald-500/50" />
                      <span className="text-[10px] uppercase font-bold tracking-widest">Validated</span>
                    </div>
                  )
                )
              },
              { header: "Timestamp", accessor: "date", className: "text-right tabular-nums text-white/50 text-xs" },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}
