"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { ClipboardList, Navigation2, Package, MapPin, Clock } from "lucide-react";
import { cn } from "../../lib/utils";

const shipments = [
  { id: "SH-1001", number: "F-99281-X", origin: "Apapa Port", destination: "Ikeja Distribution", status: "In Transit", weight: "24.5 Tons", eta: "1h 20m" },
  { id: "SH-1002", number: "F-99282-Y", origin: "Lekki Free Zone", destination: "Oshodi Hub", status: "Delayed", weight: "12.0 Tons", eta: "4h 45m" },
  { id: "SH-1003", number: "F-99283-Z", origin: "Abuja Depot", destination: "Kano Central", status: "En Route to Pickup", weight: "8.2 Tons", eta: "Tomorrow" },
  { id: "SH-1004", number: "F-99284-A", origin: "Port Harcourt", destination: "Onitsha Market", status: "Delivered", weight: "18.1 Tons", eta: "-" },
  { id: "SH-1005", number: "F-99285-B", origin: "Kaduna Terminal", destination: "Jos Plateau", status: "Scheduled", weight: "32.0 Tons", eta: "In 2 Days" },
];

export default function ShipmentsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Mission Control</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Active logistics lifecycle monitoring and shipment routing</p>
          </div>
          <button className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-6 py-2.5 rounded-xl text-xs font-bold shadow-lg shadow-gold-900/10 hover:shadow-gold-900/20 transition-all flex items-center gap-2 group">
            <Package className="w-4 h-4" />
            New Manifest
          </button>
        </div>

        <section className="space-y-8">
          <LuxuryTable
            title="Active Logistics Pipelines"
            data={shipments}
            columns={[
              { 
                header: "Manifest ID", 
                accessor: (item) => (
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20">
                      <ClipboardList className="w-4 h-4 text-gold-500" />
                    </div>
                    <span className="font-mono text-gold-400 font-bold">{item.number}</span>
                  </div>
                )
              },
              { 
                header: "Route Trajectory", 
                accessor: (item) => (
                  <div className="flex items-center gap-2">
                    <div className="flex flex-col">
                      <span className="text-[10px] text-white/30 truncate max-w-[100px]">{item.origin}</span>
                      <Navigation2 className="w-3 h-3 text-gold-600 rotate-90 my-0.5" />
                      <span className="text-xs font-bold text-white/80">{item.destination}</span>
                    </div>
                  </div>
                )
              },
              { header: "Cargo Weight", accessor: "weight", className: "tabular-nums" },
              { 
                header: "Operational State", 
                accessor: (item) => (
                  <div className={cn(
                    "px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest inline-flex items-center gap-1.5",
                    item.status === 'In Transit' ? "bg-sky-500/10 text-sky-500" : 
                    item.status === 'Delayed' ? "bg-destructive/10 text-destructive" :
                    item.status === 'Delivered' ? "bg-emerald-500/10 text-emerald-500" :
                    "bg-white/5 text-white/40"
                  )}>
                    <div className={cn(
                      "w-1.5 h-1.5 rounded-full animate-pulse",
                      item.status === 'In Transit' ? "bg-sky-500" : 
                      item.status === 'Delayed' ? "bg-destructive" :
                      item.status === 'Delivered' ? "bg-emerald-500" :
                      "bg-white/40"
                    )} />
                    {item.status}
                  </div>
                )
              },
              { 
                header: "Arrival Estimation", 
                accessor: (item) => (
                  <div className="flex items-center gap-2 text-gold-200/50">
                    <Clock className="w-3 h-3" />
                    <span className="text-xs tabular-nums">{item.eta}</span>
                  </div>
                ),
                className: "text-right font-medium"
              },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}

