import { api } from "./client";
import type { Alert } from "@/lib/types/alert";

export async function getAlerts(): Promise<{ items: Alert[] }> {
  return api.get<{ items: Alert[] }>("/v1/alerts");
}

export async function createAlert(data: {
  name: string;
  categories?: string[];
  keywords?: string[];
  minScore?: number;
  minSources?: number;
  channels?: string[];
}): Promise<Alert> {
  return api.post<Alert>("/v1/alerts", data);
}

export async function deleteAlert(id: string): Promise<void> {
  return api.delete<void>(`/v1/alerts/${id}`);
}

export async function toggleAlert(id: string): Promise<Alert> {
  return api.post<Alert>(`/v1/alerts/${id}/toggle`);
}
