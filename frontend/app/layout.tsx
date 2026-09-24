import type { Metadata } from "next";
import "./globals.css";
import { cn } from "../lib/utils";

export const metadata: Metadata = {
  title: "FleetIQ — AI Logistics & Fleet Intelligence",
  description: "Enterprise Logistics and Fleet Management Platform",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="dark">
      <body
        className={cn(
          "min-h-screen bg-background font-sans antialiased text-foreground",
        )}
      >
        {children}
      </body>
    </html>
  );
}
