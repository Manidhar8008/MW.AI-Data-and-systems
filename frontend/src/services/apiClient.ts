import axios from "axios";

import { useAuthStore } from "../store/authStore";

const baseURL = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL,
  timeout: 10000,
});

apiClient.interceptors.request.use((config) => {
  const { token, tenantId } = useAuthStore.getState();

  config.headers["X-Tenant-ID"] = tenantId;

  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

