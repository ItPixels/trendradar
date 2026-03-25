import { api } from "./client";
import type { Prediction, PredictionListResponse } from "@/lib/types/prediction";

export async function getPredictions(params?: {
  status?: string;
  minConfidence?: number;
  limit?: number;
  offset?: number;
}): Promise<PredictionListResponse> {
  const query: Record<string, string> = {};
  if (params?.status) query.status = params.status;
  if (params?.minConfidence) query.min_confidence = String(params.minConfidence);
  if (params?.limit) query.limit = String(params.limit);
  if (params?.offset) query.offset = String(params.offset);

  return api.get<PredictionListResponse>("/v1/predictions", query);
}

export async function getTrendPredictions(trendId: string): Promise<{ items: Prediction[] }> {
  return api.get<{ items: Prediction[] }>(`/v1/predictions/trend/${trendId}`);
}

export async function getLatestPrediction(trendId: string): Promise<Prediction> {
  return api.get<Prediction>(`/v1/predictions/trend/${trendId}/latest`);
}
