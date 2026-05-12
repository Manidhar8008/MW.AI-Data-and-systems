import { CheckSquare, Plus } from "lucide-react";

export function TasksPage(): JSX.Element {
  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-ink-900">Tasks</h2>
        </div>
        <button className="inline-flex items-center justify-center gap-2 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">
          <Plus aria-hidden="true" className="h-4 w-4" />
          New task
        </button>
      </div>

      <div className="rounded-lg border border-slate-200 bg-white p-8 text-center shadow-panel">
        <CheckSquare aria-hidden="true" className="mx-auto h-10 w-10 text-brand-600" />
        <h3 className="mt-3 text-lg font-semibold text-ink-900">No tasks assigned</h3>
        <p className="mt-1 text-sm text-ink-500">No open tasks for this tenant.</p>
      </div>
    </div>
  );
}
