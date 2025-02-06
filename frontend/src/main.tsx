import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import App from "./App";
// import App from "./test";
import "./index.css"; // Import Tailwind CSS

createRoot(document.getElementById("root")!).render(
  //<StrictMode>
  <BrowserRouter>
    <App />
  </BrowserRouter>
  //</StrictMode>
);
