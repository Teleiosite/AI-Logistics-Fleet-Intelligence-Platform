"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { Truck, Users, BadgeCheck } from "lucide-react";

const vehicles = [
  { id: "VEH-001", reg: "LA-234-FG", model: "Mercedes Actros", type: "Heavy Duty", status: "Active", fuel: "82%" },
  { id: "VEH-002", reg: "LA-912-XY", model: "Volvo FH16", type: "Long Haul", status: "In Maintenance", fuel: "14%" },
  { id: "VEH-003", reg: "LA-455-AB", model: "Scania R500", type: "Heavy Duty", status: "Active", fuel: "65%" },
  { id: "VEH-004", reg: "LA-112-ZT", model: "MAN TGX", type: "Heavy Duty", status: "In Transit", fuel: "42%" },
  { id: "VEH-005", reg: "LA-778-MM", model: "Iveco S-Way", type: "Medium Duty", status: "Active", fuel: "91%" },
];

const drivers = [
  { id: "DRV-101", name: "Samuel Okon", license: "Class A-1", status: "On Mission", rating: 4.8, trips: 142 },
  { id: "DRV-102", name: "Ikechukwu Mensah", license: "Class A-1", status: "Resting", rating: 4.9, trips: 89 },
  { id: "DRV-103", name: "Ahmed Bello", license: "Class B", status: "On Mission", rating: 4.7, trips: 215 },
  { id: "DRV-104", name: "Tunde Olayinka", license: "Class A-1", status: "Unavailable", rating: 4.5, trips: 56 },
];

export default function FleetPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Fleet Repository</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Manage and monitor mobile assets across all corridors</p>
        </div>

        <section className="space-y-8">
          <LuxuryTable
            title="Strategic Vehicle Assets"
            data={vehicles.map(v => ({ ...v, id: v.id }))}
            columns={[
              { header: "Registry", accessor: "reg", className: "font-mono text-gold-500" },
              { header: "Model", accessor: "model" },
              { header: "Classification", accessor: "type" },
              { 
                header: "Operation Status", 
                accessor: (item) => (
                  <div className="flex items-center gap-2">
                    <div className={`w-1.5 h-1.5 rounded-full ${item.status === 'Active' ? 'bg-emerald-500' : item.status === 'In Transit' ? 'bg-sky-500' : 'bg-amber-500'}`} />
                    <span>{item.status}</span>
                  </div>
                )
              },
              { 
                header: "Fuel Reserve", 
                accessor: (item) => (
                  <div className="flex items-center gap-2 w-24">
                    <div className="flex-1 h-1 bg-white/5 rounded-full overflow-hidden">
                      <div className="h-full bg-gold-500" style={{ width: item.fuel }} />
                    </div>
                    <span className="text-[10px] tabular-nums">{item.fuel}</span>
                  </div>
                ) 
              },
            ]}
          />

          <LuxuryTable
            title="Certified Operators"
            data={drivers.map(d => ({ ...d, id: d.id }))}
            columns={[
              { 
                header: "Driver Interface", 
                accessor: (item) => (
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20">
                      <Users className="w-4 h-4 text-gold-500" />
                    </div>
                    <span className="font-bold">{item.name}</span>
                  </div>
                )
              },
              { header: "Registry ID", accessor: "id", className: "text-[10px] text-white/40 font-mono" },
              { header: "Credential", accessor: "license" },
              { 
                header: "Performance", 
                accessor: (item) => (
                  <div className="flex items-center gap-1">
                    <BadgeCheck className="w-3 h-3 text-gold-500" />
                    <span className="text-xs font-bold">{item.rating}</span>
                  </div>
                )
              },
              { 
                header: "Status", 
                accessor: (item) => (
                  <span className={`px-2 py-0.5 rounded text-[10px] font-bold uppercase tracking-widest ${item.status === 'On Mission' ? 'bg-sky-500/10 text-sky-500' : 'bg-white/5 text-white/40'}`}>
                    {item.status}
                  </span>
                )
              },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}
