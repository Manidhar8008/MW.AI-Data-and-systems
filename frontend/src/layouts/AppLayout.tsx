import { Outlet } from "react-router-dom";

import { Sidebar } from "../components/common/Sidebar";
import { useHealthCheck } from "../hooks/useHealthCheck";
import { useAuthStore } from "../store/authStore";

export function AppLayout(): JSX.Element {
  const tenantId = useAuthStore((state) => state.tenantId);
  const health = useHealthCheck();

  return (
    <div className="min-h-screen bg-[#f6f8f7] text-ink-900">
      <Sidebar />
      <main className="min-h-screen pl-0 md:pl-64">
        <header className="border-b border-slate-200 bg-white px-5 py-4">
          <div className="flex flex-col gap-2 sm:flex-row sm:items-center sm:justify-between">
            <div>
              <p className="text-xs font-medium uppercase text-ink-500">Tenant</p>
              <h1 className="text-xl font-semibold">{tenantId}</h1>
            </div>
            <div className="text-sm text-ink-500">
              API status:{" "}
              <span className={health.status === "ok" ? "font-medium text-brand-700" : "font-medium text-red-600"}>
                {health.status}
              </span>
            </div>
          </div>
        </header>
        <section className="px-5 py-6">
          <Outlet />
        </section>
      </main>
    </div>
  );
}
