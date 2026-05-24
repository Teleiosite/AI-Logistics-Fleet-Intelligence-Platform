"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { FileText, CheckCircle2, AlertCircle } from "lucide-react";
import { cn } from "../../lib/utils";
import { fetchInvoices, Invoice } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

export default function InvoicesPage() {
  const [invoices, setInvoices] = useState<Invoice[]>([]);
  const token = useRequireAuth();

  useEffect(() => {
    if (!token) return;
    fetchInvoices(token).then(setInvoices).catch(() => undefined);
  }, [token]);

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Financial Reconciliation</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">AI-driven invoice matching and transporter payout settlement</p>
          </div>
        </div>

        <section className="space-y-8">
          <LuxuryTable
            title="Inbound Transporter Invoices"
            data={invoices}
            columns={[
              { header: "Invoice Reference", accessor: (item) => <div className="flex items-center gap-3"><div className="w-8 h-8 rounded-lg bg-gold-600/10 flex items-center justify-center border border-gold-600/20"><FileText className="w-4 h-4 text-gold-500" /></div><span className="font-mono font-bold text-sm">{item.invoice_number}</span></div> },
              { header: "Invoice Value", accessor: (item) => <span className="tabular-nums font-bold">₦{Number(item.total_amount).toLocaleString()}</span> },
              { header: "Audit Result", accessor: (item) => <div className={cn("px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest inline-flex items-center gap-1.5", item.status === 'matched' ? "bg-emerald-500/10 text-emerald-500" : item.discrepancy_count > 0 ? "bg-destructive/10 text-destructive" : "bg-white/5 text-white/40")}>{item.status === 'matched' ? <CheckCircle2 className="w-3 h-3" /> : item.discrepancy_count > 0 ? <AlertCircle className="w-3 h-3" /> : null}{item.status}{item.discrepancy_count > 0 && <span className="ml-1 opacity-50">({item.discrepancy_count})</span>}</div> },
              { header: "Created", accessor: (item) => new Date(item.created_at).toLocaleString(), className: "text-center tabular-nums text-white/40" },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}
