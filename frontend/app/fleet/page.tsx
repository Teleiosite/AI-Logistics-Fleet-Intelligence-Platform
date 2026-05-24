"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { Users } from "lucide-react";
import { fetchDrivers, fetchVehicles, Driver, Vehicle } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

export default function FleetPage() {
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [drivers, setDrivers] = useState<Driver[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const token = useRequireAuth();

  useEffect(() => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    Promise.all([fetchVehicles(token), fetchDrivers(token)])
      .then(([vehiclesData, driversData]) => {
        setVehicles(vehiclesData);
        setDrivers(driversData);
      })
      .catch(() => setError("Unable to load live data."))
      .finally(() => setIsLoading(false));
  }, [token]);

  return (<DashboardLayout><div className="space-y-12"><div><h1 className="text-3xl font-bold tracking-tight text-white italic">Fleet Repository</h1><p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Manage and monitor mobile assets across all corridors</p></div>{isLoading && <p className="text-xs text-white/40">Loading live data...</p>}{error && <p className="text-xs text-destructive">{error}</p>}<section className="space-y-8"><LuxuryTable title="Strategic Vehicle Assets" data={vehicles.map((v) => ({ ...v, id: v.id }))} columns={[{ header: "Registry", accessor: "license_plate", className: "font-mono text-gold-500" }, { header: "Vehicle No", accessor: "vehicle_number" }, { header: "Classification", accessor: "vehicle_type" }, { header: "Operation Status", accessor: "status" }]} /><LuxuryTable title="Certified Operators" data={drivers.map((d) => ({ ...d, id: d.id, name: `${d.first_name} ${d.last_name}` }))} columns={[{ header: "Driver Interface", accessor: (item) => (<div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20"><Users className="w-4 h-4 text-gold-500" /></div><span className="font-bold">{item.name}</span></div>) }, { header: "License", accessor: "license_number", className: "text-[10px] text-white/40 font-mono" }, { header: "Status", accessor: "status" }]} /></section></div></DashboardLayout>);
}
