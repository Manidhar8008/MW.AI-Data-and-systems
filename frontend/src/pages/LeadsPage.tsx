import { Plus, Search } from "lucide-react";

export function LeadsPage(): JSX.Element {
  return (
    <div className="space-y-5">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-2xl font-semibold text-ink-900">Leads</h2>
        </div>
        <button className="inline-flex items-center justify-center gap-2 rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700">
          <Plus aria-hidden="true" className="h-4 w-4" />
          New lead
        </button>
      </div>

      <div className="rounded-lg border border-slate-200 bg-white shadow-panel">
        <div className="border-b border-slate-200 p-4">
          <label className="flex max-w-md items-center gap-2 rounded-md border border-slate-200 px-3 py-2">
            <Search aria-hidden="true" className="h-4 w-4 text-ink-500" />
            <input className="w-full outline-none" placeholder="Search leads" type="search" />
          </label>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full min-w-[720px] border-collapse text-left text-sm">
            <thead className="bg-slate-50 text-xs uppercase text-ink-500">
              <tr>
                <th className="px-4 py-3 font-medium">Name</th>
                <th className="px-4 py-3 font-medium">Phone</th>
                <th className="px-4 py-3 font-medium">Source</th>
                <th className="px-4 py-3 font-medium">Status</th>
                <th className="px-4 py-3 font-medium">Next follow-up</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td className="px-4 py-8 text-center text-ink-500" colSpan={5}>
                  No leads yet.
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
