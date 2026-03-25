export interface SignalEvent {
  id: string;
  source: string;
  sourceId?: string;
  title: string;
  url?: string;
  content?: string;
  metrics: Record<string, number>;
  extractedTopics: string[];
  signalStrength: number;
  detectedAt: string;
}
