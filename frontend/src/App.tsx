import React from "react";
import { Routes, Route } from "react-router-dom";
import About from "./pages/About";
import Commits from "./pages/Commits";
import Contributions from "./pages/Contributions";
import Dashboard from "./pages/Dashboard";
import History from "./pages/History";
import Home from "./pages/Home";
import Login from "./pages/Login";
import NotFound from "./pages/NotFound";
import Repositories from "./pages/Repositories";
import Teams from "./pages/Teams";

const App: React.FC = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/about" element={<About />} />
      <Route path="/login" element={<Login />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/history" element={<History />} />
      <Route path="/contributions" element={<Contributions />} />
      <Route path="/repositories" element={<Repositories />} />
      <Route path="/teams" element={<Teams />} />
      <Route path="/commits" element={<Commits />} />
      <Route path="*" element={<NotFound />} />
    </Routes>
  );
};

export default App;
