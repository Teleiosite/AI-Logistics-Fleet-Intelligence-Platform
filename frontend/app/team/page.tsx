"use client";

import { useEffect, useState } from "react";
import { DashboardLayout } from "../../components/dashboard/DashboardLayout";
import { LuxuryTable } from "../../components/ui/luxury-table";
import { Users, ShieldCheck, UserPlus } from "lucide-react";
import { cn } from "../../lib/utils";
import { fetchUsers, User } from "../../lib/api";
import { useRequireAuth } from "../../lib/requireAuth";

const ROLE_COLORS: Record<string, string> = {
  super_admin: "bg-gold-500/20 text-gold-400",
  company_admin: "bg-violet-500/10 text-violet-400",
  transport_admin: "bg-blue-500/10 text-blue-400",
  logistics_manager: "bg-indigo-500/10 text-indigo-400",
  finance_officer: "bg-emerald-500/10 text-emerald-400",
  driver: "bg-amber-500/10 text-amber-400",
  auditor: "bg-white/5 text-white/40",
};

export default function TeamPage() {
  const [users, setUsers] = useState<User[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState("");
  const token = useRequireAuth();

  useEffect(() => {
    if (!token) return;
    setIsLoading(true);
    setError("");
    fetchUsers(token)
      .then(setUsers)
      .catch(() => setError("Unable to load team members. Admin access required."))
      .finally(() => setIsLoading(false));
  }, [token]);

  return (
    <DashboardLayout>
      <div className="space-y-12">
        <div className="flex justify-between items-end">
          <div>
            <h1 className="text-3xl font-bold tracking-tight text-white italic">Administration Hub</h1>
            <p className="text-muted-foreground text-sm mt-1 font-medium underline decoration-gold-600/30 underline-offset-4">
              Manage organizational roles, permissions, and security policies
            </p>
          </div>
          <button className="bg-white/5 border border-white/10 text-white px-6 py-2.5 rounded-xl text-xs font-bold hover:bg-white/10 transition-all flex items-center gap-2">
            <UserPlus className="w-4 h-4 text-gold-500" />
            Provision New User
          </button>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {[
            { label: "Total Users", value: users.length },
            { label: "Active", value: users.filter((u) => u.is_active).length },
            { label: "Admins", value: users.filter((u) => u.role.includes("admin")).length },
            { label: "Drivers", value: users.filter((u) => u.role === "driver").length },
          ].map((s) => (
            <div key={s.label} className="glass-card p-5 rounded-2xl border border-white/5 text-center">
              <p className="text-3xl font-bold text-white tabular-nums">{s.value}</p>
              <p className="text-xs text-white/30 uppercase tracking-widest font-bold mt-1">{s.label}</p>
            </div>
          ))}
        </div>

        {isLoading && <p className="text-xs text-white/40">Loading team data...</p>}
        {error && (
          <div className="glass-card rounded-3xl p-8 flex flex-col items-center justify-center text-center space-y-4">
            <div className="w-14 h-14 bg-gold-600/10 rounded-2xl flex items-center justify-center border border-gold-600/20">
              <ShieldCheck className="w-7 h-7 text-gold-500" />
            </div>
            <p className="text-sm text-white/50 max-w-sm">{error}</p>
          </div>
        )}

        {!isLoading && !error && (
          <section>
            <LuxuryTable
              title="Personnel Directory"
              data={users}
              columns={[
                {
                  header: "Member",
                  accessor: (item) => (
                    <div className="flex items-center gap-3">
                      <div className="w-9 h-9 rounded-xl bg-gold-600/10 border border-gold-600/20 flex items-center justify-center text-sm font-bold text-gold-400">
                        {item.first_name[0]}{item.last_name[0]}
                      </div>
                      <div>
                        <p className="text-sm font-bold text-white">{item.first_name} {item.last_name}</p>
                        <p className="text-[10px] text-white/30">{item.email}</p>
                      </div>
                    </div>
                  ),
                },
                {
                  header: "Role",
                  accessor: (item) => (
                    <span className={cn("text-[10px] font-bold uppercase tracking-widest px-2.5 py-1 rounded-lg", ROLE_COLORS[item.role] ?? "bg-white/5 text-white/40")}>
                      {item.role.replace(/_/g, " ")}
                    </span>
                  ),
                },
                {
                  header: "Status",
                  accessor: (item) => (
                    <div className="flex items-center gap-2">
                      <div className={cn("w-1.5 h-1.5 rounded-full", item.is_active ? "bg-emerald-500" : "bg-white/20")} />
                      <span className={cn("text-xs font-bold", item.is_active ? "text-emerald-400" : "text-white/30")}>
                        {item.is_active ? "Active" : "Inactive"}
                      </span>
                    </div>
                  ),
                },
              ]}
            />
          </section>
        )}

        <div className="glass-card rounded-2xl p-5 flex items-center gap-4 border border-white/5">
          <div className="w-10 h-10 bg-gold-600/10 rounded-xl flex items-center justify-center border border-gold-600/20 shrink-0">
            <Users className="w-5 h-5 text-gold-500" />
          </div>
          <div>
            <p className="text-xs font-bold text-white">Role-Based Access Control is active</p>
            <p className="text-[10px] text-white/30 mt-0.5">8 predefined roles with granular resource-action permissions are enforced on every API request.</p>
          </div>
        </div>
      </div>
    </DashboardLayout>
  );
}
