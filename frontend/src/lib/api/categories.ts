import { api } from "./client";

export interface Category {
  id: string;
  name: string;
  slug: string;
  description?: string;
  icon?: string;
  color: string;
  sortOrder: number;
  trendCount: number;
}

export async function getCategories(): Promise<{ items: Category[] }> {
  return api.get<{ items: Category[] }>("/v1/categories");
}

export async function getCategory(slug: string): Promise<Category> {
  return api.get<Category>(`/v1/categories/${slug}`);
}
