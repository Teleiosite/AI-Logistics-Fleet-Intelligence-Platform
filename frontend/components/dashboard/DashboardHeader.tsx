"use client";

import { Bell, Search, User, LogOut, Settings, HelpCircle } from "lucide-react";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from "../ui/dropdown-menu";
import { Avatar, AvatarFallback, AvatarImage } from "../ui/avatar";

export function DashboardHeader() {
  return (
    <header className="h-20 border-b border-white/5 bg-black/50 backdrop-blur-md px-8 flex items-center justify-between sticky top-0 z-30">
      <div className="flex-1 max-w-xl">
        <div className="relative group">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-muted-foreground group-focus-within:text-gold-400 transition-colors" />
          <input
            type="text"
            placeholder="Search shipments, vehicles, or drivers..."
            className="w-full bg-white/5 border border-white/10 rounded-xl py-2.5 pl-10 pr-4 text-sm text-white placeholder:text-white/20 focus:outline-none focus:ring-1 focus:ring-gold-500/30 focus:border-gold-500/30 transition-all focus:bg-white/[0.08]"
          />
        </div>
      </div>

      <div className="flex items-center gap-4">
        <button className="relative w-10 h-10 flex items-center justify-center rounded-xl bg-white/5 border border-white/10 hover:bg-white/10 transition-colors group">
          <Bell className="w-5 h-5 text-muted-foreground group-hover:text-gold-400 transition-colors" />
          <span className="absolute top-2.5 right-2.5 w-2 h-2 bg-gold-500 rounded-full border-2 border-black" />
        </button>

        <DropdownMenu>
          <DropdownMenuTrigger asChild>
            <button className="flex items-center gap-3 p-1.5 rounded-2xl hover:bg-white/5 transition-colors group">
              <Avatar className="h-9 w-9 border border-white/10 group-hover:border-gold-500/50 transition-colors">
                <AvatarImage src="" />
                <AvatarFallback className="bg-gradient-to-br from-gold-600 to-gold-900 text-white font-bold text-xs">JD</AvatarFallback>
              </Avatar>
              <div className="text-left hidden md:block">
                <p className="text-xs font-bold text-white group-hover:text-gold-400 transition-colors">John Doe</p>
                <p className="text-[10px] text-white/40 uppercase tracking-tighter font-medium">Logistics Director</p>
              </div>
            </button>
          </DropdownMenuTrigger>
          <DropdownMenuContent className="w-56 bg-card border-white/10" align="end">
            <DropdownMenuLabel className="text-xs font-bold uppercase tracking-widest text-gold-500">My Command</DropdownMenuLabel>
            <DropdownMenuSeparator className="bg-white/5" />
            <DropdownMenuItem className="text-sm cursor-pointer hover:bg-gold-500/10 focus:bg-gold-500/10 transition-colors">
              <User className="mr-2 h-4 w-4" />
              <span>Profile</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="text-sm cursor-pointer hover:bg-gold-500/10 focus:bg-gold-500/10 transition-colors">
              <Settings className="mr-2 h-4 w-4" />
              <span>Settings</span>
            </DropdownMenuItem>
            <DropdownMenuItem className="text-sm cursor-pointer hover:bg-gold-500/10 focus:bg-gold-500/10 transition-colors">
              <HelpCircle className="mr-2 h-4 w-4" />
              <span>Support</span>
            </DropdownMenuItem>
            <DropdownMenuSeparator className="bg-white/5" />
            <DropdownMenuItem className="text-sm text-destructive cursor-pointer hover:bg-destructive/10 focus:bg-destructive/10 transition-colors">
              <LogOut className="mr-2 h-4 w-4" />
              <span>Sign Out</span>
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>
    </header>
  );
}
