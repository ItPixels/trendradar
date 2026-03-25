const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  async get<T>(path: string, params?: Record<string, string>): Promise<T> {
    const url = new URL(`${this.baseUrl}/api${path}`);
    if (params) {
      Object.entries(params).forEach(([key, value]) => {
        if (value !== undefined && value !== null) {
          url.searchParams.set(key, value);
        }
      });
    }

    const res = await fetch(url.toString(), {
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }

    return res.json();
  }

  async post<T>(path: string, data?: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}/api${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }

    return res.json();
  }

  async put<T>(path: string, data?: unknown): Promise<T> {
    const res = await fetch(`${this.baseUrl}/api${path}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: data ? JSON.stringify(data) : undefined,
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }

    return res.json();
  }

  async delete<T>(path: string): Promise<T> {
    const res = await fetch(`${this.baseUrl}/api${path}`, {
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
    });

    if (!res.ok) {
      throw new Error(`API error: ${res.status} ${res.statusText}`);
    }

    return res.json();
  }
}

export const api = new ApiClient(API_URL);
