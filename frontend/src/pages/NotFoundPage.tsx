import { Link } from "react-router-dom";

export function NotFoundPage(): JSX.Element {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#f6f8f7] px-5">
      <div className="max-w-md text-center">
        <p className="text-sm font-medium uppercase text-brand-700">404</p>
        <h1 className="mt-2 text-3xl font-semibold text-ink-900">Page not found</h1>
        <p className="mt-2 text-sm text-ink-500">The CRM page you requested does not exist.</p>
        <Link
          className="mt-5 inline-flex rounded-md bg-brand-600 px-4 py-2 text-sm font-medium text-white hover:bg-brand-700"
          to="/dashboard"
        >
          Back to dashboard
        </Link>
      </div>
    </main>
  );
}
