export interface Prediction {
  id: string;
  trendId: string;
  predictedGrowth: number;
  confidenceScore: number;
  timeframeHours: number;
  predictedPeakAt?: string;
  factors: PredictionFactor[];
  status: 'pending' | 'correct' | 'partially_correct' | 'incorrect' | 'expired';
  createdAt: string;
}

export interface PredictionFactor {
  id: string;
  factor: string;
  impact: 'positive' | 'negative' | 'neutral';
  weight: number;
  description: string;
  sourceType?: string;
}
