export type HealthResponse = {
  status: string;
  app_name: string;
  environment: string;
  checked_at: string;
};

export type HealthStatus = {
  status: "checking" | "ok" | "offline" | string;
};

