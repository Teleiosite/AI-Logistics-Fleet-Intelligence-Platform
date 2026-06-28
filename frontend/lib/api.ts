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

// ── Types ────────────────────────────────────────────────────────────────────

export type ShipmentMetrics = {
  total_shipments: number;
  active_shipments: number;
  delayed_shipments: number;
  delivered_shipments: number;
};

export type Shipment = {
  id: string;
  shipment_number: string;
  customer_name: string;
  pickup_address: string;
  delivery_address: string;
  status: string;
  priority?: string;
  cargo_description?: string | null;
  cargo_weight_kg?: number | null;
  reference_number?: string | null;
  scheduled_pickup_at?: string | null;
  scheduled_delivery_at?: string | null;
  created_at: string;
};

export type ShipmentCreate = {
  shipment_number: string;
  customer_name: string;
  pickup_address: string;
  delivery_address: string;
  priority?: string;
  cargo_description?: string;
  cargo_weight_kg?: number;
  reference_number?: string;
};

export type Vehicle = { id: string; vehicle_number: string; license_plate: string; vehicle_type: string; status: string };
export type Driver = { id: string; first_name: string; last_name: string; license_number: string; status: string };

export type FuelLog = {
  id: string;
  vehicle_id: string;
  quantity_liters: number;
  price_per_liter: number;
  total_cost: number;
  station_name?: string | null;
  fuel_efficiency_lkm?: number | null;
  is_anomaly: boolean;
  anomaly_reason: string | null;
  created_at: string;
};

export type FuelLogCreate = {
  vehicle_id: string;
  quantity_liters: number;
  price_per_liter: number;
  odometer_reading_km?: number;
  station_name?: string;
  shipment_id?: string;
};

export type FuelMetrics = {
  total_volume_liters: number;
  total_cost: number;
  anomaly_count: number;
  avg_efficiency_lkm: number | null;
};

export type FuelPriceEntry = {
  id: string;
  company_id: string;
  region: string;
  fuel_type: string;
  price_per_liter: number;
  recorded_at: string;
};

export type Invoice = {
  id: string;
  invoice_number: string;
  total_amount: number;
  status: string;
  discrepancy_count: number;
  created_at: string;
};

export type DVR = {
  id: string;
  shipment_id: string;
  dvr_number: string;
  variance_type: string;
  description: string;
  financial_impact: number | null;
  fault_assignment: string | null;
  severity: string;
  resolution_notes: string | null;
  status: string;
};

export type DVRCreate = {
  shipment_id: string;
  dvr_number: string;
  variance_type: string;
  description: string;
  financial_impact?: number;
  fault_assignment?: string;
  severity?: string;
};

export type FleetMetrics = {
  total_vehicles: number;
  active_vehicles: number;
  maintenance_vehicles: number;
  total_drivers: number;
  active_drivers: number;
};

export type DVRMetrics = {
  total: number;
  open: number;
  resolved: number;
  by_type: { type: string; count: number }[];
};

export type ShipmentTrendPoint = { date: string; count: number };

export type User = {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  is_active: boolean;
};

// ── Auth ─────────────────────────────────────────────────────────────────────

export async function login(
  email: string,
  password: string,
): Promise<{ access_token: string; refresh_token?: string }> {
  return apiFetch<{ access_token: string; refresh_token?: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
}

export async function refreshToken(
  refresh_token: string,
): Promise<{ access_token: string; refresh_token: string }> {
  return apiFetch<{ access_token: string; refresh_token: string }>("/auth/refresh", {
    method: "POST",
    body: JSON.stringify({ refresh_token }),
  });
}

// ── Analytics ────────────────────────────────────────────────────────────────

export async function fetchShipmentMetrics(token: string): Promise<ShipmentMetrics> {
  return apiFetch<ShipmentMetrics>("/analytics/shipments", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchShipmentTrend(token: string): Promise<ShipmentTrendPoint[]> {
  return apiFetch<ShipmentTrendPoint[]>("/analytics/shipments/trend", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchFuelMetrics(token: string): Promise<FuelMetrics> {
  return apiFetch<FuelMetrics>("/analytics/fuel", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchFleetMetrics(token: string): Promise<FleetMetrics> {
  return apiFetch<FleetMetrics>("/analytics/fleet", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchDVRMetrics(token: string): Promise<DVRMetrics> {
  return apiFetch<DVRMetrics>("/analytics/dvr", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

// ── Resources ─────────────────────────────────────────────────────────────────

export async function fetchShipments(token: string): Promise<Shipment[]> {
  return apiFetch<Shipment[]>("/shipments", { headers: { Authorization: `Bearer ${token}` } });
}

export async function createShipment(token: string, payload: ShipmentCreate): Promise<Shipment> {
  return apiFetch<Shipment>("/shipments", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
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

export async function createFuelLog(token: string, payload: FuelLogCreate): Promise<FuelLog> {
  return apiFetch<FuelLog>("/fuel", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function fetchFuelPrices(token: string): Promise<FuelPriceEntry[]> {
  return apiFetch<FuelPriceEntry[]>("/fuel/prices", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchInvoices(token: string): Promise<Invoice[]> {
  return apiFetch<Invoice[]>("/invoices", { headers: { Authorization: `Bearer ${token}` } });
}

export async function fetchDVRs(token: string): Promise<DVR[]> {
  return apiFetch<DVR[]>("/dvr", { headers: { Authorization: `Bearer ${token}` } });
}

export async function createDVR(token: string, payload: DVRCreate): Promise<DVR> {
  return apiFetch<DVR>("/dvr", {
    method: "POST",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(payload),
  });
}

export async function updateDVRStatus(
  token: string,
  dvrId: string,
  status: string,
  resolution_notes?: string,
  fault_assignment?: string,
): Promise<DVR> {
  return apiFetch<DVR>(`/dvr/${dvrId}/status`, {
    method: "PATCH",
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify({ status, resolution_notes, fault_assignment }),
  });
}

export async function fetchUsers(token: string): Promise<User[]> {
  return apiFetch<User[]>("/users", { headers: { Authorization: `Bearer ${token}` } });
}
