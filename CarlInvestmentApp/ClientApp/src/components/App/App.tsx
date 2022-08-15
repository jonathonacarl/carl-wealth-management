import React from "react";
import { Home } from "../Home/Home";
import { Header } from "../Header/Header";
import { Charts } from "../Charts/Charts";
import { Investments } from "../Investments/Investments";
import { Portfolio } from "../Portfolio/Portfolio";
import { BrowserRouter, Routes, Route, NavLink } from "react-router-dom";

export const App: React.FC = () => {
  return (
    <div>
      <BrowserRouter>
        <Header />
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="Charts" element={<Charts />} />
          <Route path="Investments" element={<Investments />} />
          <Route path="Portfolio" element={<Portfolio />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
};
