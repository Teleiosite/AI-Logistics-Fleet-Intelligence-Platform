"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { ClipboardList, Navigation2, Clock, Plus, X } from "lucide-react";
import { cn } from "../../lib/utils";
import { fetchShipments, createShipment, Shipment, ShipmentCreate } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const STATUS_COLOR: Record<string, string> = {
  draft: "text-white/40",
  scheduled: "text-blue-400",
  assigned: "text-indigo-400",
  dispatched: "text-violet-400",
  in_transit: "text-amber-400",
  delivered: "text-emerald-400",
  delayed: "text-destructive",
  exception: "text-destructive",
};

const PRIORITIES = ["standard", "urgent", "critical"];

const EMPTY_FORM: ShipmentCreate = {
  shipment_number: "",
  customer_name: "",
  pickup_address: "",
  delivery_address: "",
  priority: "standard",
  cargo_description: "",
  reference_number: "",
};

export default function ShipmentsPage() {
  const [shipments, setShipments] = useState<Shipment[]>([]);
  const token = useRequireAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState<ShipmentCreate>(EMPTY_FORM);
  const [submitting, setSubmitting] = useState(false);
  const [formError, setFormError] = useState("");

  const load = () => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    fetchShipments(token)
      .then(setShipments)
      .catch(() => setError("Unable to load live data."))
      .finally(() => setIsLoading(false));
  };

  useEffect(load, [token]);

  const handleCreate = async () => {
    if (!token) return;
    if (!form.shipment_number || !form.customer_name || !form.pickup_address || !form.delivery_address) {
      setFormError("Shipment number, customer, pickup and delivery address are required.");
      return;
    }
    setSubmitting(true);
    setFormError("");
    try {
      await createShipment(token, form);
      setShowCreate(false);
      setForm(EMPTY_FORM);
      load();
    } catch (e: unknown) {
      setFormError(e instanceof Error ? e.message : "Failed to create shipment.");
    } finally {
      setSubmitting(false);
    }
  };

  const field = (key: keyof ShipmentCreate, value: string | number | undefined) =>
    setForm((f) => ({ ...f, [key]: value }));

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Mission Control</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">
              Active logistics lifecycle monitoring and shipment routing
            </p>
          </div>
          <button
            onClick={() => setShowCreate(true)}
            className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" />
            New Shipment
          </button>
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading live data...</p>}
        {error && <p className="text-xs text-destructive">{error}</p>}

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
                    <div>
                      <span className="font-mono text-gold-400 font-bold block">{item.shipment_number}</span>
                      {item.reference_number && (
                        <span className="text-[9px] text-white/20 font-mono">REF: {item.reference_number}</span>
                      )}
                    </div>
                  </div>
                ),
              },
              { header: "Customer", accessor: "customer_name", className: "text-sm font-medium" },
              {
                header: "Route",
                accessor: (item) => (
                  <div className="flex items-center gap-2">
                    <div className="flex flex-col">
                      <span className="text-[10px] text-white/30 truncate max-w-[140px]">{item.pickup_address}</span>
                      <Navigation2 className="w-3 h-3 text-gold-600 rotate-90 my-0.5" />
                      <span className="text-xs font-bold text-white/80 truncate max-w-[140px]">{item.delivery_address}</span>
                    </div>
                  </div>
                ),
              },
              {
                header: "Priority",
                accessor: (item) => (
                  <span
                    className={cn(
                      "text-[9px] font-bold uppercase tracking-widest px-2 py-0.5 rounded",
                      item.priority === "critical"
                        ? "bg-destructive/10 text-destructive"
                        : item.priority === "urgent"
                          ? "bg-amber-500/10 text-amber-400"
                          : "bg-white/5 text-white/30",
                    )}
                  >
                    {item.priority ?? "standard"}
                  </span>
                ),
              },
              {
                header: "State",
                accessor: (item) => (
                  <div
                    className={cn(
                      "px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest inline-flex items-center gap-1.5 bg-white/5",
                      STATUS_COLOR[item.status] ?? "text-white/70",
                    )}
                  >
                    {item.status.replaceAll("_", " ")}
                  </div>
                ),
              },
              {
                header: "Created",
                accessor: (item) => (
                  <div className="flex items-center gap-2 text-gold-200/50">
                    <Clock className="w-3 h-3" />
                    <span className="text-xs tabular-nums">{new Date(item.created_at).toLocaleDateString()}</span>
                  </div>
                ),
              },
            ]}
          />
        </section>
      </div>

      {/* Create Shipment Modal */}
      {showCreate && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="glass-card rounded-3xl border border-white/10 p-8 w-full max-w-xl space-y-6 max-h-[90vh] overflow-y-auto">
            <div className="flex justify-between items-center">
              <h2 className="text-xl font-bold text-white italic">Create Shipment</h2>
              <button onClick={() => { setShowCreate(false); setFormError(""); }} className="text-white/40 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="grid grid-cols-2 gap-4">
              {[
                { label: "Shipment Number *", key: "shipment_number", placeholder: "SHP-2026-001", col: 1 },
                { label: "Reference Number", key: "reference_number", placeholder: "PO-12345", col: 1 },
                { label: "Customer Name *", key: "customer_name", placeholder: "Acme Corp", col: 2 },
              ].map(({ label, key, placeholder, col }) => (
                <div key={key} className={cn("space-y-1", col === 2 ? "col-span-2" : "")}>
                  <label className="text-xs font-bold uppercase tracking-widest text-white/40">{label}</label>
                  <input
                    type="text"
                    placeholder={placeholder}
                    value={(form[key as keyof ShipmentCreate] as string) ?? ""}
                    className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                    onChange={(e) => field(key as keyof ShipmentCreate, e.target.value)}
                  />
                </div>
              ))}

              <div className="col-span-2 space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Pickup Address *</label>
                <input
                  type="text"
                  placeholder="123 Warehouse Road, Lagos"
                  value={form.pickup_address}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => field("pickup_address", e.target.value)}
                />
              </div>

              <div className="col-span-2 space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Delivery Address *</label>
                <input
                  type="text"
                  placeholder="456 Customer Street, Abuja"
                  value={form.delivery_address}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => field("delivery_address", e.target.value)}
                />
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Priority</label>
                <select
                  value={form.priority ?? "standard"}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => field("priority", e.target.value)}
                >
                  {PRIORITIES.map((p) => (
                    <option key={p} value={p} className="bg-zinc-900 capitalize">{p}</option>
                  ))}
                </select>
              </div>

              <div className="space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Cargo Weight (kg)</label>
                <input
                  type="number"
                  placeholder="0.00"
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => field("cargo_weight_kg", parseFloat(e.target.value) || undefined)}
                />
              </div>

              <div className="col-span-2 space-y-1">
                <label className="text-xs font-bold uppercase tracking-widest text-white/40">Cargo Description</label>
                <input
                  type="text"
                  placeholder="FMCG goods — beverages, 200 cartons"
                  value={form.cargo_description ?? ""}
                  className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                  onChange={(e) => field("cargo_description", e.target.value)}
                />
              </div>
            </div>

            {formError && <p className="text-xs text-destructive">{formError}</p>}

            <div className="flex gap-3 pt-2">
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
                {submitting ? "Creating..." : "Create Shipment"}
              </button>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
