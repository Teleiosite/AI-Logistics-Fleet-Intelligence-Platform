"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  LayoutDashboard, 
  Truck, 
  Map, 
  Fuel, 
  ClipboardList, 
  FileText, 
  Settings, 
  AlertCircle,
  BarChart3,
  Users
} from "lucide-react";
import { cn } from "../../lib/utils";
import { motion } from "framer-motion";

const navigation = [
  { name: "Dashboard", href: "/", icon: LayoutDashboard },
  { name: "Fleet", href: "/fleet", icon: Truck },
  { name: "Shipments", href: "/shipments", icon: ClipboardList },
  { name: "Live Map", href: "/map", icon: Map },
  { name: "Fuel Logs", href: "/fuel", icon: Fuel },
  { name: "DVR", href: "/dvr", icon: AlertCircle },
  { name: "Invoices", href: "/invoices", icon: FileText },
  { name: "Analytics", href: "/analytics", icon: BarChart3 },
  { name: "Team", href: "/team", icon: Users },
  { name: "Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <div className="flex h-full w-64 flex-col bg-black border-r border-white/5">
      <div className="flex h-20 items-center px-6">
        <Link href="/" className="flex items-center gap-2 group">
          <div className="w-8 h-8 bg-gradient-to-br from-gold-400 to-gold-700 rounded-lg flex items-center justify-center shadow-[0_0_15px_-3px_rgba(251,191,36,0.3)]">
            <Truck className="w-5 h-5 text-black" />
          </div>
          <span className="text-xl font-bold tracking-tighter gold-text-gradient italic group-hover:scale-105 transition-transform origin-left">FleetIQ</span>
        </Link>
      </div>
      
      <nav className="flex-1 space-y-1 px-4 py-4">
        {navigation.map((item) => {
          const isActive = pathname === item.href;
          return (
            <Link
              key={item.name}
              href={item.href}
              className={cn(
                "group flex items-center px-3 py-2.5 text-sm font-medium rounded-xl transition-all duration-300 relative",
                isActive 
                  ? "text-gold-400 bg-gold-400/5" 
                  : "text-muted-foreground hover:text-gold-200 hover:bg-white/5"
              )}
            >
              {isActive && (
                <motion.div 
                  layoutId="active-nav"
                  className="absolute left-0 w-1 h-6 bg-gold-500 rounded-r-full"
                  transition={{ type: "spring", stiffness: 300, damping: 30 }}
                />
              )}
              <item.icon className={cn(
                "mr-3 h-5 w-5 transition-colors",
                isActive ? "text-gold-500" : "group-hover:text-gold-400"
              )} />
              {item.name}
            </Link>
          );
        })}
      </nav>

      <div className="p-4 border-t border-white/5">
        <div className="bg-gold-500/5 rounded-2xl p-4 border border-gold-500/10">
          <p className="text-[10px] font-bold text-gold-500 uppercase tracking-widest mb-1">System status</p>
          <div className="flex items-center gap-2">
            <div className="w-1.5 h-1.5 rounded-full bg-emerald-500 animate-pulse" />
            <span className="text-xs text-white/50 font-medium">All systems operational</span>
          </div>
        </div>
      </div>
    </div>
  );
}
