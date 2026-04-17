"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { FileText, Cpu, CheckCircle2, AlertCircle, FileUp, Sparkles } from "lucide-react";
import { cn } from "../../lib/utils";

const invoices = [
  { id: "INV-2001", number: "FTQ/2026/012", transporter: "Speedy Haulage Ltd", amount: 1250000, status: "Pending Match", items: 12, discrepancies: 0 },
  { id: "INV-2002", number: "FTQ/2026/013", transporter: "Global Freight Corp", amount: 840000, status: "Dispute", items: 8, discrepancies: 2 },
  { id: "INV-2003", number: "FTQ/2026/014", transporter: "Interstate Transit", amount: 560000, status: "Matched", items: 15, discrepancies: 0 },
  { id: "INV-2004", number: "FTQ/2026/015", transporter: "NorthStar Logistics", amount: 920000, status: "Pending Match", items: 10, discrepancies: 0 },
  { id: "INV-2005", number: "FTQ/2026/016", transporter: "OceanView Shipping", amount: 2100000, status: "Matched", items: 3, discrepancies: 0 },
];

export default function InvoicesPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Financial Reconciliation</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">AI-driven invoice matching and transporter payout settlement</p>
          </div>
          <div className="flex gap-3">
            <button className="bg-white/5 border border-white/10 text-white px-6 py-2.5 rounded-xl text-xs font-bold hover:bg-white/10 transition-all flex items-center gap-2 group">
              <FileUp className="w-4 h-4 text-gold-500" />
              Upload OCR
            </button>
            <button className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-6 py-2.5 rounded-xl text-xs font-bold shadow-lg shadow-gold-900/10 hover:shadow-gold-900/20 transition-all flex items-center gap-2 group">
              <Sparkles className="w-4 h-4" />
              Run Intelligent Batch
            </button>
          </div>
        </div>

        {/* Intelligence Alert */}
        <div className="bg-gold-500/5 border border-gold-500/20 rounded-3xl p-6 flex items-center gap-6">
          <div className="w-12 h-12 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20">
            <Cpu className="w-6 h-6 text-gold-500" />
          </div>
          <div className="flex-1">
            <h4 className="text-gold-400 font-bold text-sm tracking-tight capitalize">Intelligent auditor active</h4>
            <p className="text-xs text-white/50 max-w-2xl leading-relaxed">FleetIQ has identified 2 discrepancies in recent submissions. Most discrepancies are related to "Detention Fees" not being pre-authorized. Automated dispute memos have been drafted.</p>
          </div>
          <button className="text-xs font-bold text-gold-500 px-4 py-2 hover:bg-gold-500/10 rounded-xl transition-all">Review Memos</button>
        </div>

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
                    <span className="font-mono font-bold text-sm">{item.number}</span>
                  </div>
                )
              },
              { header: "Entity", accessor: "transporter" },
              { 
                header: "Invoice Value", 
                accessor: (item) => (
                  <span className="tabular-nums font-bold">₦{item.amount.toLocaleString()}</span>
                )
              },
              { 
                header: "Audit Result", 
                accessor: (item) => (
                  <div className={cn(
                    "px-2 py-0.5 rounded-md text-[10px] font-bold uppercase tracking-widest inline-flex items-center gap-1.5",
                    item.status === 'Matched' ? "bg-emerald-500/10 text-emerald-500" : 
                    item.status === 'Dispute' ? "bg-destructive/10 text-destructive" :
                    "bg-white/5 text-white/40"
                  )}>
                    {item.status === 'Matched' ? <CheckCircle2 className="w-3 h-3" /> : 
                     item.status === 'Dispute' ? <AlertCircle className="w-3 h-3" /> : null}
                    {item.status}
                    {item.discrepancies > 0 && <span className="ml-1 opacity-50">({item.discrepancies} items)</span>}
                  </div>
                )
              },
              { header: "Line Items", accessor: "items", className: "text-center tabular-nums text-white/40" },
              { 
                header: "Actions", 
                accessor: () => (
                  <button className="text-[10px] font-bold text-gold-600 hover:text-gold-400 uppercase tracking-widest px-3 py-1 bg-gold-500/[0.03] border border-gold-500/10 rounded-full transition-all">Approve Setltement</button>
                ),
                className: "text-right"
              },
            ]}
          />
        </section>
      </div>
    </DashboardLayout>
  );
}
