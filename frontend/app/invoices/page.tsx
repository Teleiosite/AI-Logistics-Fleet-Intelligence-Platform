"use client";

import { useEffect, useMemo, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { FileText, CheckCircle2, AlertCircle, ScanText, WandSparkles, ScrollText, X } from "lucide-react";
import { cn } from "../../lib/utils";
import {
  autoMatchInvoice,
  createInvoiceFromText,
  fetchDisputeMemo,
  fetchInvoices,
  Invoice,
  InvoiceUploadText,
} from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const EMPTY_UPLOAD: InvoiceUploadText = {
  raw_text: "",
};

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const token = useRequireAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const [showUpload, setShowUpload] = useState(false);
  const [uploadForm, setUploadForm] = useState<InvoiceUploadText>(EMPTY_UPLOAD);
  const [uploading, setUploading] = useState(false);
  const [memoInvoice, setMemoInvoice] = useState<Invoice | null>(null);
  const [memo, setMemo] = useState("");
  const [memoLoading, setMemoLoading] = useState(false);
  const [activeInvoiceId, setActiveInvoiceId] = useState<string | null>(null);

  const load = () => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    fetchInvoices(token)
      .then(setInvoices)
      .catch(() => setError("Unable to load live data."))
      .finally(() => setIsLoading(false));
  };

  useEffect(load, [token]);

  const summary = useMemo(
    () => ({
      total: invoices.length,
      matched: invoices.filter((invoice) => invoice.status === "matched").length,
      pendingReview: invoices.filter((invoice) => invoice.status !== "matched").length,
      discrepancies: invoices.reduce((total, invoice) => total + invoice.discrepancy_count, 0),
    }),
    [invoices],
  );

  const handleUpload = async () => {
    if (!token || !uploadForm.raw_text.trim()) {
      setError("Invoice OCR text is required.");
      return;
    }
    setUploading(true);
    setError("");
    try {
      await createInvoiceFromText(token, uploadForm);
      setShowUpload(false);
      setUploadForm(EMPTY_UPLOAD);
      load();
    } catch (uploadError: unknown) {
      setError(uploadError instanceof Error ? uploadError.message : "Failed to process invoice text.");
    } finally {
      setUploading(false);
    }
  };

  const handleAutoMatch = async (invoiceId: string) => {
    if (!token) return;
    setActiveInvoiceId(invoiceId);
    setError("");
    try {
      const result = await autoMatchInvoice(token, invoiceId);
      load();
      setError(`Auto-match complete: ${result.matched} matched, ${result.discrepancies} discrepancies.`);
    } catch (matchError: unknown) {
      setError(matchError instanceof Error ? matchError.message : "Failed to auto-match invoice.");
    } finally {
      setActiveInvoiceId(null);
    }
  };

  const handleViewMemo = async (invoice: Invoice) => {
    if (!token) return;
    setMemoInvoice(invoice);
    setMemo("");
    setMemoLoading(true);
    try {
      setMemo(await fetchDisputeMemo(token, invoice.id));
    } catch (memoError: unknown) {
      setMemo(memoError instanceof Error ? memoError.message : "Unable to load memo.");
    } finally {
      setMemoLoading(false);
    }
  };

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Financial Reconciliation</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">
              AI-driven invoice matching and transporter payout settlement
            </p>
          </div>
          <button
            onClick={() => setShowUpload(true)}
            className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-5 py-2.5 rounded-xl text-xs font-bold flex items-center gap-2 hover:opacity-90 transition-opacity"
          >
            <ScanText className="w-4 h-4" />
            Upload OCR Text
          </button>
        </div>

        <div className="grid grid-cols-1 gap-4 md:grid-cols-4">
          {[
            { label: "Invoices", value: summary.total, color: "text-white" },
            { label: "Matched", value: summary.matched, color: "text-emerald-400" },
            { label: "Pending Review", value: summary.pendingReview, color: "text-amber-400" },
            { label: "Discrepancies", value: summary.discrepancies, color: "text-destructive" },
          ].map((card) => (
            <div key={card.label} className="glass-card rounded-2xl border border-white/5 p-5">
              <p className="text-[10px] uppercase tracking-widest text-white/30 font-bold">{card.label}</p>
              <p className={cn("mt-2 text-3xl font-bold tabular-nums", card.color)}>{card.value}</p>
            </div>
          ))}
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading live data...</p>}
        {error && <p className="text-xs text-destructive">{error}</p>}

        <section className="space-y-8">
          <LuxuryTable
            title="Inbound Transporter Invoices"
            data={invoices}
            columns={[
              {
                header: "Invoice Reference",
                accessor: (item) => (
                  <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20">
                      <FileText className="w-4 h-4 text-gold-500" />
                    </div>
                    <span className="font-mono font-bold text-sm">{item.invoice_number}</span>
                  </div>
                ),
              },
              { header: "Invoice Value", accessor: (item) => <span className="tabular-nums font-bold">₦{Number(item.total_amount).toLocaleString()}</span> },
              {
                header: "Audit Result",
                accessor: (item) => (
                  <div
                    className={cn(
                      "px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest inline-flex items-center gap-1.5",
                      item.status === "matched"
                        ? "bg-emerald-500/10 text-emerald-500"
                        : item.discrepancy_count > 0
                          ? "bg-destructive/10 text-destructive"
                          : "bg-white/5 text-white/40",
                    )}
                  >
                    {item.status === "matched" ? <CheckCircle2 className="w-3 h-3" /> : item.discrepancy_count > 0 ? <AlertCircle className="w-3 h-3" /> : null}
                    {item.status}
                    {item.discrepancy_count > 0 && <span className="ml-1 opacity-50">({item.discrepancy_count})</span>}
                  </div>
                ),
              },
              { header: "Created", accessor: (item) => new Date(item.created_at).toLocaleString(), className: "text-center tabular-nums text-white/40" },
              {
                header: "Workflow",
                accessor: (item) => (
                  <div className="flex justify-end gap-2">
                    <button
                      onClick={() => handleAutoMatch(item.id)}
                      disabled={activeInvoiceId === item.id}
                      className="inline-flex items-center gap-1 rounded-lg border border-gold-500/20 px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-gold-400 transition-colors hover:bg-gold-500/10 disabled:opacity-40"
                    >
                      <WandSparkles className="w-3 h-3" />
                      {activeInvoiceId === item.id ? "Matching" : "Auto-match"}
                    </button>
                    <button
                      onClick={() => handleViewMemo(item)}
                      className="inline-flex items-center gap-1 rounded-lg border border-white/10 px-2.5 py-1 text-[10px] font-bold uppercase tracking-widest text-white/60 transition-colors hover:bg-white/5"
                    >
                      <ScrollText className="w-3 h-3" />
                      Memo
                    </button>
                  </div>
                ),
              },
            ]}
          />
        </section>
      </div>

      {showUpload && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="glass-card rounded-3xl border border-white/10 p-8 w-full max-w-2xl space-y-6">
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-bold text-white italic">Upload Invoice OCR Text</h2>
              <button
                onClick={() => {
                  setShowUpload(false);
                  setUploadForm(EMPTY_UPLOAD);
                }}
                className="text-white/40 hover:text-white"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="space-y-2">
              <label className="text-xs font-bold uppercase tracking-widest text-white/40">Invoice OCR Text *</label>
              <textarea
                rows={10}
                value={uploadForm.raw_text}
                onChange={(event) => setUploadForm({ raw_text: event.target.value })}
                placeholder={"Invoice INV-2026-001\nTransport charge - SHP-1001 - 450000\nFuel surcharge - 35000\nTotal: 485000"}
                className="w-full rounded-2xl border border-white/10 bg-white/5 px-4 py-3 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30 resize-none"
              />
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => {
                  setShowUpload(false);
                  setUploadForm(EMPTY_UPLOAD);
                }}
                className="flex-1 bg-white/5 text-white/60 py-3 rounded-xl text-sm font-bold hover:bg-white/10 transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleUpload}
                disabled={uploading}
                className="flex-1 bg-gradient-to-r from-gold-500 to-gold-700 text-black py-3 rounded-xl text-sm font-bold disabled:opacity-40 hover:opacity-90 transition-opacity"
              >
                {uploading ? "Processing..." : "Create Invoice"}
              </button>
            </div>
          </div>
        </div>
      )}

      {memoInvoice && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/70 backdrop-blur-sm p-4">
          <div className="glass-card rounded-3xl border border-white/10 p-8 w-full max-w-3xl space-y-6">
            <div className="flex items-center justify-between">
              <div>
                <h2 className="text-xl font-bold text-white italic">Dispute Memo</h2>
                <p className="text-xs text-white/40 mt-1">{memoInvoice.invoice_number}</p>
              </div>
              <button onClick={() => setMemoInvoice(null)} className="text-white/40 hover:text-white">
                <X className="w-5 h-5" />
              </button>
            </div>

            <div className="rounded-2xl border border-white/10 bg-black/40 p-4">
              <pre className="whitespace-pre-wrap text-xs leading-6 text-white/80 font-mono">
                {memoLoading ? "Generating dispute memo..." : memo}
              </pre>
            </div>
          </div>
        </div>
      )}
    </DashboardLayout>
  );
}
