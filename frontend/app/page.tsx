import { KpiCard } from "../components/kpi-card";

export default async function DashboardPage() {
  return (
    <main style={{ padding: 24 }}>
      <h1>FleetIQ Operations Dashboard</h1>
      <p>Starter dashboard skeleton for shipment, fleet, fuel, and finance KPIs.</p>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 12 }}>
        <KpiCard title="Active Shipments" value="--" />
        <KpiCard title="On-Time Rate" value="--" />
        <KpiCard title="Fuel Cost / KM" value="--" />
        <KpiCard title="Open Exceptions" value="--" />
      </div>
    </main>
  );
}
