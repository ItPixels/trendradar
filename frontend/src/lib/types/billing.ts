export type BillingInterval = 'monthly' | 'yearly';

export interface Subscription {
  id: string;
  userId: string;
  plan: string;
  status: 'active' | 'canceled' | 'past_due' | 'trialing' | 'incomplete';
  interval: BillingInterval;
  currentPeriodStart: string;
  currentPeriodEnd: string;
  cancelAtPeriodEnd: boolean;
  stripeSubscriptionId?: string;
  stripeCustomerId?: string;
  createdAt: string;
  updatedAt: string;
}

export interface Invoice {
  id: string;
  userId: string;
  amount: number;
  currency: string;
  status: 'draft' | 'open' | 'paid' | 'void' | 'uncollectible';
  invoiceUrl?: string;
  paidAt?: string;
  createdAt: string;
}
