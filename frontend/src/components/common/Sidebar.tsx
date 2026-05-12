import { CheckSquare, LayoutDashboard, Users } from "lucide-react";
import { NavLink } from "react-router-dom";

const navItems = [
  { to: "/dashboard", label: "Dashboard", icon: LayoutDashboard },
  { to: "/leads", label: "Leads", icon: Users },
  { to: "/tasks", label: "Tasks", icon: CheckSquare },
];

export function Sidebar(): JSX.Element {
  return (
    <aside className="border-b border-slate-200 bg-white md:fixed md:inset-y-0 md:left-0 md:w-64 md:border-b-0 md:border-r">
      <div className="flex h-full flex-col">
        <div className="border-b border-slate-200 px-5 py-4">
          <p className="text-xs font-medium uppercase text-brand-700">MW.AI</p>
          <h2 className="text-lg font-semibold text-ink-900">Data and Systems</h2>
        </div>
        <nav className="flex gap-1 overflow-x-auto px-3 py-3 md:flex-col md:overflow-visible">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <NavLink
                key={item.to}
                to={item.to}
                className={({ isActive }) =>
                  [
                    "flex min-w-fit items-center gap-3 rounded-md px-3 py-2 text-sm font-medium transition",
                    isActive ? "bg-brand-50 text-brand-700" : "text-ink-700 hover:bg-slate-100",
                  ].join(" ")
                }
              >
                <Icon aria-hidden="true" className="h-4 w-4" />
                <span>{item.label}</span>
              </NavLink>
            );
          })}
        </nav>
      </div>
    </aside>
  );
}
