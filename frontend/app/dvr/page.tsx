"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { AlertTriangle, Package, FileWarning, CheckCircle2 } from "lucide-react";
import { cn } from "../../lib/utils";

const dvrs = [
  { id: "DVR-001", manifest: "F-99281-X", reason: "Product Shortage", severity: "Critical", status: "Pending Review", reporter: "Warehouse A" },
  { id: "DVR-002", manifest: "F-99282-Y", reason: "Physical Damage", severity: "Major", status: "Investigating", reporter: "Driver 104" },
  { id: "DVR-003", manifest: "F-99283-Z", reason: "Late Arrival Exception", severity: "Minor", status: "Resolved", reporter: "System" },
  { id: "DVR-004", manifest: "F-99285-B", reason: "Incorrect Documentation", severity: "Major", status: "Pending Review", reporter: "Admin Hub" },
];

export default function DVRPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Variance Control</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Tracking delivery discrepancies, shortages, and physical damage claims</p>
        </div>

        <section className="space-y-8">
          <LuxuryTable
            title="Active Discrepancy Ledger"
            data={dvrs}
            columns={[
              { 
                header: "Audit ID", 
                accessor: (item) => (
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20">
                      <FileWarning className="w-4 h-4 text-gold-500" />
                    </div>
                    <span className="font-mono text-white/40 text-[10px]">{item.id}</span>
                  </div>
                )
              },
              { header: "Manifest", accessor: "manifest", className: "font-mono font-bold text-gold-500" },
              { header: "Discrepancy Detail", accessor: "reason" },
              { 
                header: "Severity Index", 
                accessor: (item) => (
                  <span className={cn(
                    "text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded",
                    item.severity === 'Critical' ? "bg-destructive/10 text-destructive" :
                    item.severity === 'Major' ? "bg-amber-500/10 text-amber-500" :
                    "bg-white/5 text-white/40"
                  )}>
                    {item.severity}
                  </span>
                )
              },
              { 
                header: "Audit Status", 
                accessor: (item) => (
                  <div className="flex items-center gap-2">
                    {item.status === 'Resolved' ? <CheckCircle2 className="w-4 h-4 text-emerald-500" /> : <div className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />}
                    <span className="text-xs">{item.status}</span>
                  </div>
                )
              },
              { header: "Reported By", accessor: "reporter", className: "text-right text-xs text-white/30" },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}
