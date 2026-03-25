import { api } from "./client";
import type { Trend, TrendFilters } from "@/lib/types/trend";

interface TrendListResponse {
  items: Trend[];
  total: number;
  limit: number;
  offset: number;
}

export async function getTrends(filters?: TrendFilters): Promise<TrendListResponse> {
  const params: Record<string, string> = {};
  if (filters?.category) params.category = filters.category;
  if (filters?.status) params.status = filters.status;
  if (filters?.minScore) params.min_score = String(filters.minScore);
  if (filters?.sortBy) params.sort_by = filters.sortBy;
  if (filters?.timeRange) params.time_range = filters.timeRange;

  return api.get<TrendListResponse>("/v1/trends", params);
}

export async function getTrend(id: string): Promise<Trend> {
  return api.get<Trend>(`/v1/trends/${id}`);
}

export async function getTrendBySlug(slug: string): Promise<Trend> {
  return api.get<Trend>(`/v1/trends/slug/${slug}`);
}

export async function searchTrends(query: string): Promise<{ items: Trend[] }> {
  return api.get<{ items: Trend[] }>("/v1/search", { q: query });
}
