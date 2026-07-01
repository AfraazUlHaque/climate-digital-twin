import { Routes, Route, Navigate } from "react-router-dom";
import MainLayout from "./layouts/MainLayout.jsx";

import Dashboard from "./pages/Dashboard.jsx";
import Forecast from "./pages/Forecast.jsx";
import Flood from "./pages/Flood.jsx";
import Drought from "./pages/Drought.jsx";
import GIS from "./pages/GIS.jsx";
import Weather from "./pages/Weather.jsx";
import WhatIf from "./pages/WhatIf.jsx";
import Analytics from "./pages/Analytics.jsx";

function App() {
  return (
    <MainLayout>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/forecast" element={<Forecast />} />
        <Route path="/flood" element={<Flood />} />
        <Route path="/drought" element={<Drought />} />
        <Route path="/gis" element={<GIS />} />
        <Route path="/weather" element={<Weather />} />
        <Route path="/what-if" element={<WhatIf />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </MainLayout>
  );
}

export default App;