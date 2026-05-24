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

export type ShipmentMetrics = {
  total_shipments: number;
  active_shipments: number;
  delayed_shipments: number;
  delivered_shipments: number;
};

export type Shipment = {
  id: string;
  shipment_number: string;
  pickup_address: string;
  delivery_address: string;
  status: string;
  created_at: string;
};

export async function login(email: string, password: string): Promise<string> {
  const data = await apiFetch<{ access_token: string }>("/auth/login", {
    method: "POST",
    body: JSON.stringify({ email, password }),
  });
  return data.access_token;
}

export async function fetchShipmentMetrics(token: string): Promise<ShipmentMetrics> {
  return apiFetch<ShipmentMetrics>("/analytics/shipments", {
    headers: { Authorization: `Bearer ${token}` },
  });
}

export async function fetchShipments(token: string): Promise<Shipment[]> {
  return apiFetch<Shipment[]>("/shipments", {
    headers: { Authorization: `Bearer ${token}` },
  });
}
