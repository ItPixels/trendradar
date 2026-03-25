export interface Alert {
  id: string;
  name: string;
  categories: string[];
  keywords: string[];
  minScore: number;
  minVelocity: number;
  minSources: number;
  channels: AlertChannel[];
  isActive: boolean;
  triggerCount: number;
  lastTriggeredAt?: string;
  createdAt: string;
}

export type AlertChannel = 'email' | 'push' | 'telegram' | 'webhook';
