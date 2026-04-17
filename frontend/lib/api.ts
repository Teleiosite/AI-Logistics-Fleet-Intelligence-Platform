export async function fetchShipmentMetrics(token: string) {
  const response = await fetch("http://localhost:8000/api/v1/analytics/shipments", {
    headers: { Authorization: `Bearer ${token}` },
    cache: "no-store"
  });
  if (!response.ok) throw new Error("Failed to fetch metrics");
  return response.json();
}
