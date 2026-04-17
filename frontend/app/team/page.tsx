"use client";

import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { Users, UserPlus, ShieldAlert } from "lucide-react";

export default function TeamPage() {
  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Administration Hub</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">Manage organizational roles, permissions, and security policies</p>
          </div>
          <button className="bg-white/5 border border-white/10 text-white px-6 py-2.5 rounded-xl text-xs font-bold hover:bg-white/10 transition-all flex items-center gap-2">
            <UserPlus className="w-4 h-4 text-gold-500" />
            Provision New User
          </button>
        </div>

        <div className="glass-card rounded-3xl p-12 flex flex-col items-center justify-center text-center space-y-6">
          <div className="w-20 h-20 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20">
            <Users className="w-10 h-10 text-gold-500" />
          </div>
          <h3 className="text-2xl font-bold text-white italic">Personnel Directory Syncing</h3>
          <p className="text-sm text-white/30 max-w-sm mx-auto leading-relaxed">Access control management and team identity synchronization is currently being established. Role-Based Access Control (RBAC) definitions are active in the backend.</p>
          
          <div className="bg-destructive/5 border border-destructive/20 rounded-2xl p-4 flex items-center gap-3">
            <ShieldAlert className="w-4 h-4 text-destructive" />
            <span className="text-xs font-bold text-destructive uppercase tracking-widest">Administrator Override Required</span>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
