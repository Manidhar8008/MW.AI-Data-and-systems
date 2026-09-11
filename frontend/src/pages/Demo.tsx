import { useMemo, useState } from "react";
import { CheckCircle2, ChevronRight, CircleAlert, Factory, FileText, LayoutDashboard, MessageSquare, PackageCheck, Settings2, Truck, Wrench } from "lucide-react";

const stages = ["Enquiry", "Engineering", "Quote", "Production", "QC", "Installation"];

const order = {
  id: "MW-ORD-0001",
  customer: "Demo Customer",
  site: "Warangal",
  product: "UPVC Sliding Window",
  profile: "Matrix",
  glass: "Double",
  area: "42.6 SFT",
};

export default function Demo() {
  const [activeStage, setActiveStage] = useState("Production");
  const [approved, setApproved] = useState(false);
  const [observed, setObserved] = useState(18);

  const unobserved = 24 - observed;
  const wasteMeters = Math.max(0, Number(((24 - observed) * 0.4).toFixed(1)));
  const wasteValue = wasteMeters * 240;

  const activity = useMemo(
    () => [
      "Customer enquiry captured",
      "Reference photo attached",
      "Measurements validated",
      approved ? "Customer approval recorded" : "Quote awaiting approval",
      `Workshop observation: ${observed}/24 pieces recorded`,
    ],
    [approved, observed],
  );

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <header className="border-b border-white/10 bg-slate-950/95 px-6 py-4 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="rounded-xl bg-white/10 p-2"><Factory className="h-5 w-5" /></div>
            <div>
              <div className="text-sm font-semibold tracking-wide">MW.AI</div>
              <div className="text-xs text-slate-400">uPVC Fabrication OS</div>
            </div>
          </div>
          <div className="rounded-full border border-emerald-400/20 bg-emerald-400/10 px-3 py-1 text-xs text-emerald-300">Demo Tenant · Live</div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl space-y-6 px-6 py-6">
        <section className="grid gap-4 lg:grid-cols-[1.5fr_1fr]">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
            <div className="flex items-start justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.2em] text-slate-500">Active project</p>
                <h1 className="mt-2 text-3xl font-semibold">{order.id}</h1>
                <p className="mt-2 text-slate-400">{order.customer} · {order.site} · {order.product}</p>
              </div>
              <div className="rounded-xl bg-white/5 px-3 py-2 text-right">
                <div className="text-xs text-slate-500">Stage</div>
                <div className="mt-1 font-medium">{activeStage}</div>
              </div>
            </div>

            <div className="mt-8 grid grid-cols-2 gap-3 md:grid-cols-4">
              {[
                ["Area", order.area],
                ["Profile", order.profile],
                ["Glass", order.glass],
                ["Quote", approved ? "Approved" : "Pending"],
              ].map(([label, value]) => (
                <div key={label} className="rounded-xl border border-white/10 bg-slate-900/70 p-4">
                  <div className="text-xs text-slate-500">{label}</div>
                  <div className="mt-2 font-medium">{value}</div>
                </div>
              ))}
            </div>

            <div className="mt-8 flex flex-wrap gap-2">
              {stages.map((stage, index) => {
                const active = stage === activeStage;
                return (
                  <button key={stage} onClick={() => setActiveStage(stage)} className={`flex items-center gap-2 rounded-full border px-3 py-2 text-xs transition ${active ? "border-white bg-white text-slate-950" : "border-white/10 bg-white/[0.03] text-slate-400 hover:text-white"}`}>
                    {index < stages.indexOf(activeStage) ? <CheckCircle2 className="h-3.5 w-3.5" /> : <span className="h-1.5 w-1.5 rounded-full bg-current" />}
                    {stage}
                  </button>
                );
              })}
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
            <div className="flex items-center gap-2"><MessageSquare className="h-4 w-4" /><h2 className="font-semibold">AI Employee</h2></div>
            <p className="mt-2 text-sm text-slate-400">One operating layer coordinating customer, engineering and workshop work.</p>
            <div className="mt-6 space-y-3">
              {activity.map((item, index) => (
                <div key={`${item}-${index}`} className="flex gap-3 rounded-xl border border-white/10 bg-slate-900/60 p-3">
                  <div className="mt-0.5 h-2 w-2 rounded-full bg-emerald-300" />
                  <div className="text-sm text-slate-300">{item}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        <section className="grid gap-4 lg:grid-cols-3">
          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6 lg:col-span-2">
            <div className="flex items-center justify-between">
              <div><p className="text-xs uppercase tracking-[0.2em] text-slate-500">Workshop intelligence</p><h2 className="mt-2 text-xl font-semibold">Expected vs observed</h2></div>
              <Wrench className="h-5 w-5 text-slate-500" />
            </div>
            <div className="mt-6 grid gap-4 md:grid-cols-3">
              <Metric label="Expected pieces" value="24" />
              <Metric label="Observed pieces" value={String(observed)} />
              <Metric label="Unobserved" value={String(unobserved)} alert={unobserved > 0} />
            </div>
            <div className="mt-6 rounded-xl border border-white/10 bg-slate-900/70 p-4">
              <div className="flex items-center justify-between text-sm"><span className="text-slate-400">Production observation simulator</span><span>{observed}/24</span></div>
              <input aria-label="Observed pieces" type="range" min="0" max="24" value={observed} onChange={(e) => setObserved(Number(e.target.value))} className="mt-4 w-full" />
            </div>
            <div className="mt-4 flex items-start gap-3 rounded-xl border border-amber-300/20 bg-amber-300/5 p-4">
              <CircleAlert className="mt-0.5 h-4 w-4 text-amber-300" />
              <div><div className="font-medium">Production exception</div><div className="mt-1 text-sm text-slate-400">{unobserved} pieces are not yet observed. Estimated waste: {wasteMeters} m · ₹{wasteValue.toLocaleString("en-IN")}.</div></div>
            </div>
          </div>

          <div className="rounded-2xl border border-white/10 bg-white/[0.04] p-6">
            <div className="flex items-center gap-2"><FileText className="h-4 w-4" /><h2 className="font-semibold">Quote</h2></div>
            <div className="mt-6 space-y-3 text-sm">
              <Row label="Area" value={order.area} />
              <Row label="Profile" value={order.profile} />
              <Row label="Glass" value={order.glass} />
              <Row label="Status" value={approved ? "Approved" : "Awaiting approval"} />
            </div>
            <button onClick={() => setApproved(true)} disabled={approved} className="mt-6 flex w-full items-center justify-center gap-2 rounded-xl bg-white px-4 py-3 text-sm font-semibold text-slate-950 disabled:opacity-50">{approved ? <CheckCircle2 className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />} {approved ? "Approved" : "Approve Quote"}</button>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-4">
          <Kpi icon={<LayoutDashboard />} label="Active projects" value="12" />
          <Kpi icon={<PackageCheck />} label="Quotes pending" value="4" />
          <Kpi icon={<Settings2 />} label="Production jobs" value="3" />
          <Kpi icon={<Truck />} label="Installations" value="2" />
        </section>
      </main>
    </div>
  );
}

function Metric({ label, value, alert = false }: { label: string; value: string; alert?: boolean }) {
  return <div className="rounded-xl border border-white/10 bg-slate-900/70 p-4"><div className="text-xs text-slate-500">{label}</div><div className={`mt-2 text-2xl font-semibold ${alert ? "text-amber-300" : ""}`}>{value}</div></div>;
}

function Row({ label, value }: { label: string; value: string }) { return <div className="flex justify-between gap-4 border-b border-white/5 pb-3"><span className="text-slate-500">{label}</span><span>{value}</span></div>; }

function Kpi({ icon, label, value }: { icon: React.ReactNode; label: string; value: string }) { return <div className="flex items-center gap-3 rounded-2xl border border-white/10 bg-white/[0.04] p-4"><div className="rounded-xl bg-white/5 p-2 text-slate-400">{icon}</div><div><div className="text-xs text-slate-500">{label}</div><div className="mt-1 text-lg font-semibold">{value}</div></div></div>; }
