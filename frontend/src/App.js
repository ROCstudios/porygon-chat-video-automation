import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./components/Login";
import CallbackHandler from "./components/CallbackHandler";
import Dashboard from "./components/Dashboard";
import InstaLogin from "./components/InstaLogin";
function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/instaauth" element={<InstaLogin />} />
        <Route path="/redirect" element={<CallbackHandler />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}

export default App;
