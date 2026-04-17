export function KpiCard({ title, value }: { title: string; value: string }) {
  return (
    <div style={{ background: "white", borderRadius: 12, padding: 16, boxShadow: "0 1px 4px rgba(0,0,0,0.08)" }}>
      <p style={{ margin: 0, color: "#6b7280", fontSize: 13 }}>{title}</p>
      <h3 style={{ margin: "8px 0 0", fontSize: 24 }}>{value}</h3>
    </div>
  );
}
