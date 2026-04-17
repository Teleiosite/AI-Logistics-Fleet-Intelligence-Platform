"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { BarChart3, Binary, Search } from "lucide-react";

export default function AnalyticsPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Business Intelligence</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Advanced analytics, forecasting, and operational KPIs</p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="glass-card rounded-3xl p-12 flex flex-col items-center justify-center text-center space-y-6 min-h-[400px]">
            <div className="w-20 h-20 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20 animate-pulse">
              <BarChart3 className="w-10 h-10 text-gold-500" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-white mb-2 italic text-gold-500">Intelligence Engine Initializing</h3>
              <p className="text-sm text-white/30 max-w-sm mx-auto">This module is being connected to the historical shipment dataset. Advanced clustering and delay prediction features will appear here shortly.</p>
            </div>
          </div>

          <div className="glass-card rounded-3xl p-12 flex flex-col items-center justify-center text-center space-y-6 min-h-[400px]">
            <div className="w-20 h-20 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20">
              <Binary className="w-10 h-10 text-gold-500/50" />
            </div>
            <div>
              <h3 className="text-2xl font-bold text-white mb-2 italic">Data Stream Offline</h3>
              <p className="text-sm text-white/30 max-w-sm mx-auto">Waiting for real-time corridor data integration. Predictitive route heatmaps and fuel optimization models pending.</p>
            </div>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
