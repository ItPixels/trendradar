export interface PredictionFactor {
  factor: string;
  impact: "positive" | "negative" | "neutral";
  weight: number;
  description: string;
  sourceType?: string;
}

export interface PredictionTrend {
  id: string;
  topic: string;
  topicSlug: string;
  trendScore: number;
  sourceCount: number;
  activeSources: string[];
  status: string;
  categoryId?: string;
}

export interface Prediction {
  id: string;
  trendId: string;
  predictedGrowth: number;
  confidenceScore: number;
  timeframeHours: number;
  predictedPeakAt?: string;
  modelVersion?: string;
  status: string;
  factors: PredictionFactor[];
  trend?: PredictionTrend;
  createdAt?: string;
}

export interface PredictionListResponse {
  items: Prediction[];
  total: number;
  limit: number;
  offset: number;
}
