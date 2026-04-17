"use client";

import { DashboardLayout } from "../components/dashboard/DashboardLayout";
import { KpiCard } from "../components/dashboard/KpiCard";
import { 
  Truck, 
  Clock, 
  Fuel, 
  AlertTriangle, 
  BarChart3, 
  Activity,
  ArrowUpRight
} from "lucide-react";

export default function DashboardPage() {
  return (
    <DashboardLayout>
      <div className="space-y-8">
        {/* Header Section */}
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Operational Pulse</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium">Real-time intelligence from your global fleet network</p>
          </div>
          <div className="flex items-center gap-2">
            <div className="bg-white/5 border border-white/10 px-4 py-2 rounded-xl flex items-center gap-2">
              <Activity className="w-4 h-4 text-emerald-500" />
              <span className="text-xs font-bold text-white tracking-wider uppercase">Live Feed</span>
            </div>
            <button className="bg-gradient-to-r from-gold-500 to-gold-700 text-black px-4 py-2 rounded-xl text-xs font-bold shadow-lg shadow-gold-900/10 hover:shadow-gold-900/20 transition-all flex items-center gap-2 group">
              Export Analysis
              <ArrowUpRight className="w-3 h-3 group-hover:translate-x-0.5 group-hover:-translate-y-0.5 transition-transform" />
            </button>
          </div>
        </div>

        {/* KPI Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          <KpiCard 
            title="Active Shipments" 
            value="142" 
            icon={Truck} 
            trend={{ value: 12, isUp: true }}
            description="32 scheduled for next hour"
          />
          <KpiCard 
            title="On-Time Rate" 
            value="94.2%" 
            icon={Clock} 
            trend={{ value: 1.4, isUp: true }}
            description="Industry avg: 88.5%"
          />
          <KpiCard 
            title="Fuel Efficiency" 
            value="2.8 km/L" 
            icon={Fuel} 
            trend={{ value: 4.2, isUp: false }}
            description="Variance detected on 2 routes"
          />
          <KpiCard 
            title="Open Exceptions" 
            value="3" 
            icon={AlertTriangle} 
            trend={{ value: 2, isUp: true }}
            className="border-destructive/20"
            description="1 critical priority"
          />
        </div>

        {/* Secondary Section - Placeholder for charts */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 glass-card rounded-3xl p-8 min-h-[400px] flex flex-col items-center justify-center text-center space-y-4">
            <div className="w-16 h-16 bg-white/5 rounded-full flex items-center justify-center mb-2">
              <BarChart3 className="w-8 h-8 text-gold-500/30" />
            </div>
            <h3 className="text-xl font-bold text-white/40">Shipment Volume Analysis</h3>
            <p className="text-xs text-white/20 max-w-xs uppercase tracking-widest font-bold">Integrating Intelligence Engine Data...</p>
          </div>
          
          <div className="glass-card rounded-3xl p-8 flex flex-col gap-6">
            <h3 className="text-lg font-bold text-white uppercase tracking-tighter">Fleet Activity</h3>
            <div className="space-y-4">
              {[1, 2, 3].map((i) => (
                <div key={i} className="flex items-center justify-between p-4 bg-white/5 rounded-2xl border border-white/5 hover:border-gold-500/20 transition-colors group cursor-pointer">
                  <div className="flex items-center gap-3">
                    <div className="w-10 h-10 rounded-xl bg-gold-500/10 flex items-center justify-center">
                      <Truck className="w-5 h-5 text-gold-500" />
                    </div>
                    <div>
                      <p className="text-xs font-bold text-white group-hover:text-gold-400 transition-colors">TRK-4920</p>
                      <p className="text-[10px] text-white/30">In Transit — Lagos City</p>
                    </div>
                  </div>
                  <div className="w-2 h-2 rounded-full bg-emerald-500 group-hover:shadow-[0_0_8px_rgba(16,185,129,0.5)] transition-all" />
                </div>
              ))}
            </div>
            <button className="text-xs font-bold text-gold-600 hover:text-gold-400 text-center py-2 transition-colors uppercase tracking-widest">View Fleet Monitor</button>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
