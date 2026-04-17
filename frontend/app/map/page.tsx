"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { Map as MapIcon, Navigation, Search } from "lucide-react";

export default function MapPage() {
  return (
    <DashboardLayout>
      <div className="h-[calc(100vh-160px)] flex flex-col gap-6">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Live Geospatial Intelligence</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Real-time asset positioning and route optimization overlay</p>
          </div>
          <div className="flex gap-4">
            <div className="relative group w-64">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-white/20 group-focus-within:text-gold-500 transition-colors" />
              <input
                type="text"
                placeholder="Search Asset ID..."
                className="w-full bg-white/5 border border-white/5 rounded-xl py-2.5 pl-9 pr-4 text-sm text-white focus:outline-none focus:ring-1 focus:ring-gold-500/30 transition-all"
              />
            </div>
            <button className="bg-gold-500 text-black px-6 py-2.5 rounded-xl text-xs font-bold hover:bg-gold-400 transition-all flex items-center gap-2">
              <Navigation className="w-4 h-4" />
              Optimize Routes
            </button>
          </div>
        </div>

        <div className="flex-1 glass-card rounded-3xl border border-white/5 relative overflow-hidden flex flex-col items-center justify-center text-center p-12">
          {/* Mock Map Background Grid */}
          <div className="absolute inset-0 opacity-10 pointer-events-none" 
               style={{ backgroundImage: 'radial-gradient(#fbbf24 1px, transparent 1px)', backgroundSize: '40px 40px' }} />
          
          <div className="relative">
            <div className="w-24 h-24 bg-gold-500/10 rounded-full flex items-center justify-center mb-6 animate-pulse border border-gold-500/20">
              <MapIcon className="w-12 h-12 text-gold-500/40" />
            </div>
          </div>
          
          <h3 className="text-2xl font-bold text-white mb-2 italic">Geospatial Engine Offline</h3>
          <p className="text-sm text-white/30 max-w-md mx-auto leading-relaxed">The Google Maps API integration is pending configuration. Once initialized, this view will provide real-time truck positioning, geofencing alerts, and predictive arrival heatmaps.</p>
          
          <div className="mt-12 grid grid-cols-2 md:grid-cols-4 gap-6 w-full max-w-4xl">
            {[1, 2, 3, 4].map(i => (
              <div key={i} className="bg-white/[0.02] border border-white/5 p-4 rounded-2xl flex flex-col items-center gap-2">
                <div className="w-2 h-2 rounded-full bg-emerald-500" />
                <span className="text-[10px] uppercase font-bold text-white/40 tracking-widest">Active Fleet {i}</span>
              </div>
            ))}
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
