"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { Settings, Sliders, Bell, Globe, Lock } from "lucide-react";

export default function SettingsPage() {
  const sections = [
    { title: "Fleet Parameters", icon: Sliders, desc: "Operational thresholds and geofencing defaults" },
    { title: "Notification Logic", icon: Bell, desc: "Webhook registrations and alert priorities" },
    { title: "Localization", icon: Globe, desc: "Timezone, currency, and unit system configurations" },
    { title: "Security Matrix", icon: Lock, desc: "API key rotation and authentication policies" },
  ];

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-white italic">Platform Configuration</h1>
          <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Low-level system adjustments and environment variables</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          {sections.map(section => (
            <div key={section.title} className="glass-card p-8 rounded-3xl border border-white/5 hover:border-gold-500/20 group cursor-pointer transition-all">
              <div className="flex items-center gap-4 mb-4">
                <div className="w-12 h-12 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20 group-hover:bg-gold-600/20 transition-colors">
                  <section.icon className="w-6 h-6 text-gold-500" />
                </div>
                <h3 className="text-lg font-bold text-white group-hover:text-gold-400 transition-colors">{section.title}</h3>
              </div>
              <p className="text-xs text-white/30 leading-relaxed font-medium">{section.desc}</p>
            </div>
          ))}
        </div>

        <div className="glass-card rounded-3xl p-12 flex flex-col items-center justify-center text-center space-y-6">
          <div className="w-20 h-20 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20">
            <Settings className="w-10 h-10 text-gold-500" />
          </div>
          <h3 className="text-2xl font-bold text-white italic">Configuration Engine Standardizing</h3>
          <p className="text-sm text-white/30 max-w-sm mx-auto leading-relaxed">System-wide settings are being unified. Production environment variables are currently locked by the deployment engine.</p>
        </div>
      </div>
    </DashboardLayout>
  );
}
