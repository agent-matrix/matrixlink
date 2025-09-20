import React from "react";
import { createRoot } from "react-dom/client";
import AdminApp from "./pages/AdminApp";
const el = document.getElementById("root")!;
createRoot(el).render(<AdminApp />);
