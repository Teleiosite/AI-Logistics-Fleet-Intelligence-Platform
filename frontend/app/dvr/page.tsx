"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { AlertTriangle, FileWarning, CheckCircle2, Plus, X } from "lucide-react";
import { cn } from "../../lib/utils";
import { fetchDVRs, createDVR, updateDVRStatus, DVR, DVRCreate } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const VARIANCE_TYPES = [
  { value: "short_delivery", label: "Short Delivery" },
  { value: "damage", label: "Physical Damage" },
  { value: "late_delivery", label: "Late Delivery" },
  { value: "wrong_items", label: "Wrong Items" },
  { value: "refused_delivery", label: "Refused Delivery" },
  { value: "route_deviation", label: "Route Deviation" },
  { value: "fuel_variance", label: "Fuel Variance" },
];

const SEVERITIES = ["minor", "moderate", "major", "critical"];

export default function DVRPage() {
  const [dvrs, setDvrs] = useState<DVR[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [form, setForm] = useState<Partial<DVRCreate>>({
    variance_type: "short_delivery",
    severity: "minor",
  });
  const [submitting, setSubmitting] = useState(false);
  const token = useRequireAuth();

  const load = () => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    fetchDVRs(token)
      .then(setDvrs)
      .catch(() => setError("Unable to load variance reports."))
      .finally(() => setIsLoading(false));
  };

  useEffect(load, [token]);

  const handleCreate = async () => {
    if (!token || !form.shipment_id || !form.variance_type || !form.description) return;
    setSubmitting(true);
    try {
      const dvr_number = `DVR-${Date.now()}`;
      await createDVR(token, { ...form, dvr_number } as DVRCreate);
      setShowCreate(false);
      setForm({ variance_type: "short_delivery", severity: "minor" });
      load();
    } catch {
      setError("Failed to create DVR.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleResolve = async (dvr: DVR) => {
    if (!token) return;
    await updateDVRStatus(token, dvr.id, dvr.status === "open" ? "resolved" : "open");
    load();
  };

  const severityColor = (s: string) =>
    s === "critical"
      ? "bg-destructive/10 text-destructive"
      : s === "major"
        ? "bg-amber-500/10 text-amber-500"
        : s === "moderate"
          ? "bg-yellow-500/10 text-yellow-500"
          : "bg-white/5 text-white/40";

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Variance Control</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">
              Tracking delivery discrepancies, shortages, and physical damage claims
            </p>
          </div>
          <button
            onClick={() => setShowCreate(true)}
            className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <Plus className="w-4 h-4" />
            New Report
          </button>
        </div>

        {/* Stats bar */}
        <div className="grid grid-cols-3 gap-4">
          {[
            { label: "Total Reports", value: dvrs.length, color: "text-white" },
            { label: "Open", value: dvrs.filter((d) => d.status === "open").length, color: "text-amber-400" },
            { label: "Resolved", value: dvrs.filter((d) => ["resolved", "closed"].includes(d.status)).length, color: "text-emerald-400" },
          ].map((s) => (
            <div key={s.label} className="glass-card p-5 rounded-2xl border border-white/5 text-center">
              <p className={cn("text-3xl font-bold tabular-nums", s.color)}>{s.value}</p>
              <p className="text-xs text-white/30 uppercase tracking-widest font-bold mt-1">{s.label}</p>
            </div>
          ))}
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading variance reports...</p>}
        {error && <p className="text-xs text-destructive">{error}</p>}

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
                    <span className="font-mono text-white/40 text-[10px]">{item.dvr_number}</span>
                  </div>
                ),
              },
              { header: "Shipment ID", accessor: "shipment_id", className: "font-mono font-bold text-gold-500 text-xs" },
              {
                header: "Discrepancy",
                accessor: (item) => (
                  <div>
                    <p className="text-xs font-bold">{item.variance_type.replace(/_/g, " ")}</p>
                    <p className="text-[10px] text-white/30 truncate max-w-[180px]">{item.description}</p>
                  </div>
                ),
              },
              {
                header: "Severity",
                accessor: (item) => (
                  <span className={cn("text-[10px] font-bold uppercase tracking-widest px-2 py-0.5 rounded", severityColor(item.severity))}>
                    {item.severity}
                  </span>
                ),
              },
              {
                header: "Status",
                accessor: (item) => (
                  <div className="flex items-center gap-2">
                    {item.status === "resolved" || item.status === "closed" ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-500" />
                    ) : (
                      <div className="w-1.5 h-1.5 rounded-full bg-gold-500 animate-pulse" />
                    )}
                    <span className="text-xs capitalize">{item.status}</span>
                  </div>
                ),
              },
              {
                header: "",
                accessor: (item) => (
                  <button
                    onClick={() => handleResolve(item)}
                    className="text-[10px] text-white/30 hover:text-gold-400 transition-colors uppercase tracking-widest font-bold"
                  >
                    {item.status === "open" ? "Resolve" : "Reopen"}
                  </button>
                ),
              },
            ]}
          />
        </section>

        {/* Create DVR modal */}
        {showCreate && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
            <div className="glass-card rounded-3xl border border-white/10 p-8 w-full max-w-lg space-y-6">
              <div className="flex justify-between items-center">
                <h2 className="text-xl font-bold text-white italic">New Variance Report</h2>
                <button onClick={() => setShowCreate(false)} className="text-white/40 hover:text-white">
                  <X className="w-5 h-5" />
                </button>
              </div>

              <div className="space-y-4">
                {[
                  { label: "Shipment ID *", key: "shipment_id", type: "text", placeholder: "Enter shipment ID" },
                  { label: "Description *", key: "description", type: "textarea", placeholder: "Describe the variance..." },
                  { label: "Financial Impact (optional)", key: "financial_impact", type: "number", placeholder: "0.00" },
                ].map(({ label, key, type, placeholder }) => (
                  <div key={key} className="space-y-1">
                    <label className="text-xs font-bold uppercase tracking-widest text-white/40">{label}</label>
                    {type === "textarea" ? (
                      <textarea
                        rows={3}
                        placeholder={placeholder}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30 resize-none"
                        onChange={(e) => setForm((f) => ({ ...f, [key]: e.target.value }))}
                      />
                    ) : (
                      <input
                        type={type}
                        placeholder={placeholder}
                        className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                        onChange={(e) =>
                          setForm((f) => ({ ...f, [key]: type === "number" ? parseFloat(e.target.value) || undefined : e.target.value }))
                        }
                      />
                    )}
                  </div>
                ))}

                <div className="grid grid-cols-2 gap-4">
                  <div className="space-y-1">
                    <label className="text-xs font-bold uppercase tracking-widest text-white/40">Variance Type</label>
                    <select
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                      value={form.variance_type}
                      onChange={(e) => setForm((f) => ({ ...f, variance_type: e.target.value }))}
                    >
                      {VARIANCE_TYPES.map((t) => (
                        <option key={t.value} value={t.value} className="bg-zinc-900">
                          {t.label}
                        </option>
                      ))}
                    </select>
                  </div>

                  <div className="space-y-1">
                    <label className="text-xs font-bold uppercase tracking-widest text-white/40">Severity</label>
                    <select
                      className="w-full bg-white/5 border border-white/10 rounded-xl px-4 py-2.5 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30"
                      value={form.severity}
                      onChange={(e) => setForm((f) => ({ ...f, severity: e.target.value }))}
                    >
                      {SEVERITIES.map((s) => (
                        <option key={s} value={s} className="bg-zinc-900 capitalize">
                          {s}
                        </option>
                      ))}
                    </select>
                  </div>
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => setShowCreate(false)}
                  className="flex-1 bg-white/5 text-white/60 py-3 rounded-xl text-sm font-bold hover:bg-white/10 transition-colors"
                >
                  Cancel
                </button>
                <button
                  onClick={handleCreate}
                  disabled={submitting || !form.shipment_id || !form.description}
                  className="flex-1 bg-gradient-to-r from-gold-500 to-gold-700 text-black py-3 rounded-xl text-sm font-bold disabled:opacity-40 transition-opacity"
                >
                  {submitting ? "Submitting..." : "Submit Report"}
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
