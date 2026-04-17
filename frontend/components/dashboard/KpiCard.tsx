"use client";

import { motion } from "framer-motion";
import { LucideIcon, TrendingUp, TrendingDown } from "lucide-react";
import { cn } from "../../lib/utils";

interface KpiCardProps {
  title: string;
  value: string | number;
  icon: LucideIcon;
  trend?: {
    value: number;
    isUp: boolean;
  };
  description?: string;
  className?: string;
}

export function KpiCard({ title, value, icon: Icon, trend, description, className }: KpiCardProps) {
  return (
    <motion.div
      whileHover={{ y: -5, scale: 1.02 }}
      className={cn(
        "glass-card p-6 rounded-3xl relative overflow-hidden group transition-all duration-300",
        className
      )}
    >
      {/* Background Glow */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-gold-500/5 rounded-full blur-3xl -mr-16 -mt-16 group-hover:bg-gold-500/10 transition-colors" />
      
      <div className="flex justify-between items-start mb-4">
        <div className="p-3 bg-white/5 border border-white/5 rounded-2xl group-hover:border-gold-500/30 transition-colors">
          <Icon className="w-5 h-5 text-gold-500" />
        </div>
        {trend && (
          <div className={cn(
            "flex items-center gap-1 text-[10px] font-bold px-2 py-1 rounded-full",
            trend.isUp ? "bg-emerald-500/10 text-emerald-500" : "bg-destructive/10 text-destructive"
          )}>
            {trend.isUp ? <TrendingUp className="w-3 h-3" /> : <TrendingDown className="w-3 h-3" />}
            {trend.value}%
          </div>
        )}
      </div>

      <div className="space-y-1">
        <p className="text-xs font-medium text-white/40 uppercase tracking-widest">{title}</p>
        <h3 className="text-3xl font-bold tracking-tight text-white group-hover:gold-text-gradient transition-all">{value}</h3>
        {description && <p className="text-[10px] text-white/20 font-medium">{description}</p>}
      </div>

      {/* Progress Line Decor */}
      <div className="mt-4 h-1 w-full bg-white/5 rounded-full overflow-hidden">
        <motion.div 
          initial={{ width: 0 }}
          animate={{ width: "65%" }}
          transition={{ duration: 1, delay: 0.5 }}
          className="h-full bg-gradient-to-r from-gold-600 to-gold-400 group-hover:from-gold-500 group-hover:to-gold-300 transition-all" 
        />
      </div>
    </motion.div>
  );
}
