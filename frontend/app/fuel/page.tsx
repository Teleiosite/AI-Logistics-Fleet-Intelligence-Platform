"use client";

import { useEffect, useMemo, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { Fuel, AlertTriangle, Droplets, CreditCard, Plus, X, Gauge } from "lucide-react";
import { createFuelLog, fetchFuelLogs, fetchShipments, fetchVehicles, FuelLog, FuelLogCreate, Shipment, Vehicle } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const EMPTY_FORM: FuelLogCreate = {
  vehicle_id: "",
  quantity_liters: 0,
  price_per_liter: 0,
};

export default function FuelPage() {
  const [fuelLogs, setFuelLogs] = useState<FuelLog[]>([]);
  const [vehicles, setVehicles] = useState<Vehicle[]>([]);
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const token = useRequireAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState<FuelLogCreate>(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");

  const load = () => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    Promise.all([fetchFuelLogs(token), fetchVehicles(token), fetchShipments(token)])
      .then(([fuelLogData, vehicleData, shipmentData]) => {
        setFuelLogs(fuelLogData);
        setVehicles(vehicleData);
        setShipments(shipmentData);
      })
      .catch(() => setError("Unable to load live data."))
      .finally(() => setIsLoading(false));
  };

  useEffect(load, [token]);

  const stats = useMemo(() => {
    const totalVolume = fuelLogs.reduce((acc, item) => acc + Number(item.quantity_liters || 0), 0);
    const aggregateCost = fuelLogs.reduce((acc, item) => acc + Number(item.total_cost || 0), 0);
    const anomalies = fuelLogs.filter((item) => item.is_anomaly).length;
    const efficiencies = fuelLogs.filter((l) => l.fuel_efficiency_lkm).map((l) => Number(l.fuel_efficiency_lkm));
    const avgEff = efficiencies.length ? (efficiencies.reduce((a, b) => a + b, 0) / efficiencies.length).toFixed(2) : null;
    return { totalVolume, aggregateCost, anomalies, avgEff };
  }, [fuelLogs]);

  const handleCreate = async () => {
    if (!token || !form.vehicle_id || !form.quantity_liters || !form.price_per_liter) {
      setFormError("Vehicle ID, quantity, and price are required.");
      return;
    }
    setSubmitting(true);
    setFormError("");
    try {
      await createFuelLog(token, form);
      setShowCreate(false);
      setForm(EMPTY_FORM);
      load();
    } catch (e: unknown) {
      setFormError(e instanceof Error ? e.message : "Failed to log fuel.");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Consumption Intelligence</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">
              Advanced monitoring of fuel issuance and anomaly detection
            </p>
          </div>
          <button
            onClick={() => setShowCreate(true)}
            className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" />
            Log Fuel
          </button>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900">
            <div className="flex items-center gap-3 mb-2 text-gold-500"><Droplets className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Total Volume</span></div>
            <p className="text-3xl font-bold text-white tabular-nums">{stats.totalVolume.toFixed(2)} <span className="text-xs text-white/30 tracking-tight">Liters</span></p>
          </div>
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900">
            <div className="flex items-center gap-3 mb-2 text-gold-500"><CreditCard className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Aggregate Cost</span></div>
            <p className="text-3xl font-bold text-white tabular-nums">₦{stats.aggregateCost.toLocaleString()} <span className="text-xs text-white/30 tracking-tight">NGN</span></p>
          </div>
          <div className="glass-card p-6 rounded-3xl border border-white/5 bg-gradient-to-br from-black to-grey-900">
            <div className="flex items-center gap-3 mb-2 text-gold-500"><Gauge className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Avg Efficiency</span></div>
            <p className="text-3xl font-bold text-white tabular-nums">
              {stats.avgEff ? `${stats.avgEff}` : "—"} <span className="text-xs text-white/30 tracking-tight">L/100km</span>
            </p>
          </div>
          <div className={`glass-card p-6 rounded-3xl border ${stats.anomalies > 0 ? "border-destructive/20 bg-destructive/10 animate-pulse" : "border-white/5"}`}>
            <div className={`flex items-center gap-3 mb-2 ${stats.anomalies > 0 ? "text-destructive" : "text-white/40"}`}>
              <AlertTriangle className="w-5 h-5" /><span className="text-xs font-bold uppercase tracking-widest">Critical Anomalies</span>
            </div>
            <p className="text-3xl font-bold text-white tabular-nums">{stats.anomalies} <span className="text-xs text-white/30 tracking-tight">Detected</span></p>
          </div>
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading live data...</p>}
        {error && <p className="text-xs text-destructive">{error}</p>}

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
                    <span className="font-mono text-white/40 text-[10px]">{item.id.slice(0, 8)}…</span>
                  </div>
                ),
              },
              { header: "Vehicle ID", accessor: "vehicle_id", className: "font-mono font-bold text-gold-500 text-xs" },
              {
                header: "Volume / Cost",
                accessor: (item) => (
                  <div className="flex flex-col">
                    <span className="text-white font-bold">{item.quantity_liters} L</span>
                    <span className="text-[10px] text-white/30 font-mono tracking-tighter">₦{Number(item.total_cost).toLocaleString()}</span>
                  </div>
                ),
              },
              {
                header: "Efficiency",
                accessor: (item) => (
                  <span className="text-xs tabular-nums text-white/60">
                    {item.fuel_efficiency_lkm ? `${item.fuel_efficiency_lkm} L/100km` : "—"}
                  </span>
                ),
              },
              { header: "Station", accessor: (item) => <span className="text-xs text-white/40">{item.station_name ?? "—"}</span> },
              {
                header: "Anomaly Guard",
                accessor: (item) =>
                  item.is_anomaly ? (
                    <span className="text-[10px] font-bold text-destructive uppercase tracking-tighter max-w-[150px] truncate">{item.anomaly_reason || "Anomaly"}</span>
                  ) : (
                    <span className="text-[10px] uppercase font-bold tracking-widest text-emerald-500/60">Validated</span>
                  ),
              },
              {
                header: "Timestamp",
                accessor: (item) => new Date(item.created_at).toLocaleString(),
                className: "text-right tabular-nums text-white/50 text-xs",
              },
            ]}
          />
        </section>
      </div>

      {/* Log Fuel Modal */}
      {showCreate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="glass-card rounded-3xl border border-white/10 p-8 w-full max-w-md space-y-6">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-white italic">Log Fuel Issuance</h2>
              <button onClick={() => { setShowCreate(false); setFormError(""); }} className="text-white/40 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-4">
              {[
                { label: "Quantity (Liters) *", key: "quantity_liters", type: "number", placeholder: "50.00" },
                { label: "Price per Liter *", key: "price_per_liter", type: "number", placeholder: "650.00" },
                { label: "Odometer Reading (km)", key: "odometer_reading_km", type: "number", placeholder: "12500" },
                { label: "Station Name", key: "station_name", type: "text", placeholder: "NNPC Filling Station" },
              ].map(({ label, key, type, placeholder }) => (
                <div key={key} className="space-y-1">
                  <label className="text-xs font-bold uppercase tracking-widest text-white/40">{label}</label>
                  <input
                    type={type}
                    placeholder={placeholder}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                    onChange={(e) =>
                      setForm((f) => ({
                        ...f,
                        [key]: type === "number" && e.target.value ? parseFloat(e.target.value) : (e.target.value || undefined),
                      }))
                    }
                  />
                </div>
              ))}

              <div className="space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Vehicle *</label>
                <select
                  value={form.vehicle_id}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => setForm((current) => ({ ...current, vehicle_id: e.target.value }))}
                >
                  <option value="" className="bg-zinc-900">Select a vehicle</option>
                  {vehicles.map((vehicle) => (
                    <option key={vehicle.id} value={vehicle.id} className="bg-zinc-900">
                      {vehicle.license_plate} · {vehicle.vehicle_number}
                    </option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Shipment (optional)</label>
                <select
                  value={form.shipment_id ?? ""}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => setForm((current) => ({ ...current, shipment_id: e.target.value || undefined }))}
                >
                  <option value="" className="bg-zinc-900">Unlinked fuel issuance</option>
                  {shipments.map((shipment) => (
                    <option key={shipment.id} value={shipment.id} className="bg-zinc-900">
                      {shipment.shipment_number} · {shipment.customer_name}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            {formError && <p className="text-xs text-destructive">{formError}</p>}

            <div className="flex gap-3">
              <button
                onClick={() => { setShowCreate(false); setFormError(""); }}
                className="flex-1 bg-white/5 text-white/60 py-3 rounded-xl text-sm font-bold hover:bg-white/10 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleCreate}
                disabled={submitting}
                className="flex-1 bg-gradient-to-r from-gold-500 to-gold-700 text-black py-3 rounded-xl text-sm font-bold disabled:opacity-40 hover:opacity-90 transition-opacity"
              >
                {submitting ? "Logging..." : "Log Fuel"}
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
