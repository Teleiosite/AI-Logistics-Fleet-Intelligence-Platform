"use client";

import { FormEvent, useState } from "react";
import { motion } from "framer-motion";
import { Truck, Mail, Lock, Eye, EyeOff, ArrowRight } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { login } from "../../lib/api";
import { setToken } from "../../lib/auth";

const REFRESH_KEY = "fleetiq_refresh_token";

export default function LoginPage() {
  const [showPassword, setShowPassword] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const router = useRouter();

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setError("");
    setIsLoading(true);
    try {
      const data = await login(email, password);
      setToken(data.access_token);
      if (data.refresh_token) {
        localStorage.setItem(REFRESH_KEY, data.refresh_token);
      }
      router.push("/");
    } catch {
      setError("Login failed. Check your credentials and backend availability.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center relative overflow-hidden bg-black">
      <div className="absolute top-[-10%] right-[-10%] w-[500px] h-[500px] bg-gold-600/10 rounded-full blur-[120px] animate-pulse-slow" />
      <div className="absolute bottom-[-10%] left-[-10%] w-[300px] h-[300px] bg-gold-900/20 rounded-full blur-[100px]" />

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
        className="w-full max-w-md p-8 relative z-10"
      >
        <div className="flex flex-col items-center mb-10">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="w-16 h-16 bg-gradient-to-br from-gold-400 to-gold-700 rounded-2xl flex items-center justify-center shadow-[0_0_30px_-5px_rgba(251,191,36,0.5)] mb-4"
          >
            <Truck className="w-10 h-10 text-black stroke-[2.5px]" />
          </motion.div>
          <h1 className="text-4xl font-bold tracking-tighter gold-text-gradient italic">FleetIQ</h1>
          <p className="text-gold-200/50 text-sm mt-2 font-medium tracking-widest uppercase">Intelligence Powered Logistics</p>
        </div>

        <div className="glass-card p-8 rounded-3xl space-y-6">
          <div className="space-y-1">
            <h2 className="text-2xl font-semibold text-white">Welcome Back</h2>
            <p className="text-muted-foreground text-sm">Access your command center</p>
          </div>

          <form className="space-y-4" onSubmit={handleSubmit}>
            <div className="space-y-2">
              <label className="text-xs font-semibold uppercase tracking-wider text-gold-400/80 ml-1">Corporate Email</label>
              <div className="relative group">
                <Mail className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground group-focus-within:text-gold-400 transition-colors" />
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="name@company.com"
                  className="w-full bg-black/50 border border-white/10 rounded-xl py-3 pl-10 pr-4 text-white placeholder:text-white/20 focus:outline-none focus:ring-1 focus:ring-gold-500/50 focus:border-gold-500/50 transition-all"
                />
              </div>
            </div>
            <div className="space-y-2">
              <div className="flex justify-between items-center ml-1">
                <label className="text-xs font-semibold uppercase tracking-wider text-gold-400/80">Security Token</label>
                <Link href="#" className="text-[10px] text-gold-600 hover:text-gold-400 transition-colors uppercase font-bold tracking-tighter">
                  Lost Access?
                </Link>
              </div>
              <div className="relative group">
                <Lock className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground group-focus-within:text-gold-400 transition-colors" />
                <input
                  type={showPassword ? "text" : "password"}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  required
                  placeholder="••••••••"
                  className="w-full bg-black/50 border border-white/10 rounded-xl py-3 pl-10 pr-12 text-white placeholder:text-white/20 focus:outline-none focus:ring-1 focus:ring-gold-500/50 focus:border-gold-500/50 transition-all"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  className="absolute right-3 top-1/2 -translate-y-1/2 text-white/40 hover:text-white transition-colors"
                >
                  {showPassword ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                </button>
              </div>
            </div>
            {error && <p className="text-xs text-destructive font-medium">{error}</p>}
            <button
              type="submit"
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-gold-500 to-gold-700 hover:from-gold-400 hover:to-gold-600 disabled:opacity-60 text-black font-bold py-4 rounded-xl shadow-lg shadow-gold-900/20 transform transition-all active:scale-[0.98] flex items-center justify-center gap-2 group"
            >
              {isLoading ? "Authorizing..." : "Authorize Access"}
              <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition-transform" />
            </button>
          </form>

          <div className="pt-4 text-center">
            <p className="text-xs text-white/30">
              Secured by Enterprise Shield |{" "}
              <span className="text-gold-600/80 font-medium">SSO Available</span>
            </p>
          </div>
        </div>

        <div className="mt-12 flex justify-center gap-6">
          <Link href="/" className="text-[10px] uppercase tracking-widest text-white/20 hover:text-gold-500 transition-colors">Platform Compliance</Link>
          <Link href="/" className="text-[10px] uppercase tracking-widest text-white/20 hover:text-gold-500 transition-colors">Privacy Policy</Link>
          <Link href="/" className="text-[10px] uppercase tracking-widest text-white/20 hover:text-gold-500 transition-colors">Operational Status</Link>
        </div>
      </motion.div>
    </div>
  );
}
