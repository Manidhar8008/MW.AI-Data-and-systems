import { create } from "zustand";

type AuthState = {
  token: string | null;
  tenantId: string;
  setToken: (token: string | null) => void;
  setTenantId: (tenantId: string) => void;
};

const defaultTenantId = import.meta.env.VITE_DEFAULT_TENANT_ID ?? "local-demo-tenant";

export const useAuthStore = create<AuthState>((set) => ({
  token: null,
  tenantId: defaultTenantId,
  setToken: (token) => set({ token }),
  setTenantId: (tenantId) => set({ tenantId }),
}));

