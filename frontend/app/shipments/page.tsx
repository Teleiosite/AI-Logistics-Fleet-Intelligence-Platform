"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { ClipboardList, Navigation2, Clock } from "lucide-react";
import { cn } from "../../lib/utils";
import { fetchShipments, Shipment } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState<Shipment[]>([]);

  const token = useRequireAuth();

  useEffect(() => {
    if (!token) return;
    fetchShipments(token).then(setShipments).catch(() => undefined);
  }, [token]);

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Mission Control</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Active logistics lifecycle monitoring and shipment routing</p>
          </div>
        </div>

        <section className="space-y-8">
          <LuxuryTable
            title="Active Logistics Pipelines"
            data={shipments.map((s) => ({ ...s, id: s.id }))}
            columns={[
              {
                header: "Manifest ID",
                accessor: (item) => (
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20">
                      <ClipboardList className="w-4 h-4 text-gold-500" />
                    </div>
                    <span className="font-mono text-gold-400 font-bold">{item.shipment_number}</span>
                  </div>
                ),
              },
              {
                header: "Route Trajectory",
                accessor: (item) => (
                  <div className="flex items-center gap-2">
                    <div className="flex flex-col">
                      <span className="text-[10px] text-white/30 truncate max-w-[150px]">{item.pickup_address}</span>
                      <Navigation2 className="w-3 h-3 text-gold-600 rotate-90 my-0.5" />
                      <span className="text-xs font-bold text-white/80 truncate max-w-[150px]">{item.delivery_address}</span>
                    </div>
                  </div>
                ),
              },
              {
                header: "Operational State",
                accessor: (item) => (
                  <div className={cn("px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest inline-flex items-center gap-1.5 bg-white/5 text-white/70")}>{item.status.replaceAll("_", " ")}</div>
                ),
              },
              {
                header: "Created",
                accessor: (item) => (
                  <div className="flex items-center gap-2 text-gold-200/50">
                    <Clock className="w-3 h-3" />
                    <span className="text-xs tabular-nums">{new Date(item.created_at).toLocaleString()}</span>
                  </div>
                ),
              },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}
