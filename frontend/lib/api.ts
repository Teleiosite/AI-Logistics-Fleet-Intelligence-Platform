const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://localhost:8000/api/v1";

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(options.headers ?? {}),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const message = await response.text();
    throw new Error(message || `Request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

export type ShipmentMetrics = { total_shipments: number; active_shipments: number; delayed_shipments: number; delivered_shipments: number };
export type Shipment = { id: string; shipment_number: string; pickup_address: string; delivery_address: string; status: string; created_at: string };
export type Vehicle = { id: string; vehicle_number: string; license_plate: string; vehicle_type: string; status: string };
export type Driver = { id: string; first_name: string; last_name: string; license_number: string; status: string };
export type FuelLog = { id: string; vehicle_id: string; quantity_liters: number; total_cost: number; is_anomaly: boolean; anomaly_reason: string | null; created_at: string };
export type Invoice = { id: string; invoice_number: string; total_amount: number; status: string; discrepancy_count: number; created_at: string };

export async function login(email: string, password: string): Promise<string> {
  const data = await apiFetch<{ access_token: string }>("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) });
  return data.access_token;
}

export async function fetchShipmentMetrics(token: string): Promise<ShipmentMetrics> {
  return apiFetch<ShipmentMetrics>("/analytics/shipments", { headers: { Authorization: `Bearer ${token}` } });
}
export async function fetchShipments(token: string): Promise<Shipment[]> {
  return apiFetch<Shipment[]>("/shipments", { headers: { Authorization: `Bearer ${token}` } });
}
export async function fetchVehicles(token: string): Promise<Vehicle[]> {
  return apiFetch<Vehicle[]>("/vehicles", { headers: { Authorization: `Bearer ${token}` } });
}
export async function fetchDrivers(token: string): Promise<Driver[]> {
  return apiFetch<Driver[]>("/drivers", { headers: { Authorization: `Bearer ${token}` } });
}
export async function fetchFuelLogs(token: string): Promise<FuelLog[]> {
  return apiFetch<FuelLog[]>("/fuel", { headers: { Authorization: `Bearer ${token}` } });
}
export async function fetchInvoices(token: string): Promise<Invoice[]> {
  return apiFetch<Invoice[]>("/invoices", { headers: { Authorization: `Bearer ${token}` } });
}
