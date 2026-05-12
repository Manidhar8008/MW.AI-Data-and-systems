import { CalendarClock, PhoneCall, Users } from "lucide-react";

const metrics = [
  { label: "Open leads", value: "0", icon: Users },
  { label: "Today follow-ups", value: "0", icon: PhoneCall },
  { label: "Pending tasks", value: "0", icon: CalendarClock },
];

export function DashboardPage(): JSX.Element {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-2xl font-semibold text-ink-900">Operations dashboard</h2>
      </div>

      <div className="grid gap-4 md:grid-cols-3">
        {metrics.map((metric) => {
          const Icon = metric.icon;
          return (
            <div key={metric.label} className="rounded-lg border border-slate-200 bg-white p-5 shadow-panel">
              <div className="flex items-center justify-between">
                <p className="text-sm font-medium text-ink-500">{metric.label}</p>
                <Icon aria-hidden="true" className="h-5 w-5 text-brand-600" />
              </div>
              <p className="mt-4 text-3xl font-semibold text-ink-900">{metric.value}</p>
            </div>
          );
        })}
      </div>
    </div>
  );
}
