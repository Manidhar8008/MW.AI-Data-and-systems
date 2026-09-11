import { createBrowserRouter, Navigate } from "react-router-dom";
import Demo from "../pages/Demo";

export const router = createBrowserRouter([
  { path: "/", element: <Navigate to="/demo" replace /> },
  { path: "/demo", element: <Demo /> },
]);
